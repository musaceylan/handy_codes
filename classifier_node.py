#!/usr/bin/env python

import rospy
from cv_bridge import CvBridge
from message_filters import TimeSynchronizer, Subscriber
from vision_msgs.msg import Detection2DArray, Detection2D, ObjectHypothesisWithPose
from sensor_msgs.msg import Image
import threading
import atexit
import ctypes
from inspect import isclass
from multiprocessing import Queue
import torch
import torchvision.transforms as transforms
from torch.autograd import Variable
from PIL import Image as PilImage
from vision_classifier.stn_model import STN
import cv2
import numpy as np

node_handle_name = "classification_2d_node"


class ClassifierNode:

    def __init__(self):
        self.cv_bridge = CvBridge()

        self.path_sign_model = rospy.get_param('~traffic_sign_path')
        self.path_light_model = rospy.get_param('~traffic_light_path')

        self.cuda_devices = {0: 'cuda:0',
                             1: 'cuda:1',
                             2: 'cuda:2',
                             3: 'cuda:3'}

        gpu_id = rospy.get_param('~gpu_id')
        self.device = torch.device(self.cuda_devices[gpu_id])

        self.num_traffic_light = rospy.get_param('~num_traffic_light_class')
        self.model_traffic_light = STN(self.num_traffic_light).to(self.device)
        state_dict_light = torch.load(self.path_light_model)
        self.model_traffic_light.load_state_dict(state_dict_light)
        self.model_traffic_light.eval().to(self.device)
        self.model_traffic_light.cuda().to(self.device)

        self.num_traffic_sign = rospy.get_param('~num_traffic_sign_class')
        self.model_traffic_sign = STN(self.num_traffic_sign).to(self.device)
        state_dict_sign = torch.load(self.path_sign_model)
        self.model_traffic_sign.load_state_dict(state_dict_sign)
        self.model_traffic_sign.eval().to(self.device)
        self.model_traffic_sign.cuda().to(self.device)

        self.pub_fm01_new_bbox = rospy.Publisher(node_handle_name + '/cam_fm_01/detection_2d_array/',
                                                 Detection2DArray,
                                                 queue_size=1)
        self.pub_fl01_new_bbox = rospy.Publisher(node_handle_name + '/cam_fl_01/detection_2d_array/',
                                                 Detection2DArray,
                                                 queue_size=1)
        self.pub_fr01_new_bbox = rospy.Publisher(node_handle_name + '/cam_fr_01/detection_2d_array/',
                                                 Detection2DArray,
                                                 queue_size=1)

        self.topic_fm01_img = rospy.get_param('~topic_name_fm01_img')
        self.topic_fm01_bbox = rospy.get_param('~topic_name_fm01_bbox')

        self.sub_image_fm01 = Subscriber(self.topic_fm01_img, Image)
        self.sub_bbox_fm01 = Subscriber(self.topic_fm01_bbox, Detection2DArray)
        self.time_sync_fm01 = TimeSynchronizer([self.sub_image_fm01, self.sub_bbox_fm01], 10)
        self.time_sync_fm01.registerCallback(self.callback_synchronize, "cam_fm_01")

        self.topic_fl01_img = rospy.get_param('~topic_name_fl01_img')
        self.topic_fl01_bbox = rospy.get_param('~topic_name_fl01_bbox')
        self.sub_image_fl01 = Subscriber(self.topic_fl01_img, Image)
        self.sub_bbox_fl01 = Subscriber(self.topic_fl01_bbox, Detection2DArray)
        self.time_sync_fl01 = TimeSynchronizer([self.sub_image_fl01, self.sub_bbox_fl01], 10)
        self.time_sync_fl01.registerCallback(self.callback_synchronize, "cam_fl_01")

        self.topic_fr01_img = rospy.get_param('~topic_name_fr01_img')
        self.topic_fr01_bbox = rospy.get_param('~topic_name_fr01_bbox')
        self.sub_image_fr01 = Subscriber(self.topic_fr01_img, Image)
        self.sub_bbox_fr01 = Subscriber(self.topic_fr01_bbox, Detection2DArray)
        self.time_sync_fr01 = TimeSynchronizer([self.sub_image_fr01, self.sub_bbox_fr01], 10)
        self.time_sync_fr01.registerCallback(self.callback_synchronize, "cam_fr_01")

    def callback_synchronize(self, msg_img, msg_bbox, cam_id):

        cv_img = self.cv_bridge.imgmsg_to_cv2(msg_img)
        new_bbox = Detection2DArray()

        print("aaaaa")

        for detection in msg_bbox.detections:

            box = Detection2D()
            box.bbox = detection.bbox
            pose = ObjectHypothesisWithPose()

            print(detection.results[0].id)

            if detection.results[0].id == 7:  # id:7 Traffic light

                x_min = int(detection.bbox.center.x - (detection.bbox.size_x / 2))
                y_min = int(detection.bbox.center.y - (detection.bbox.size_y / 2))
                x_max = int(detection.bbox.center.x + (detection.bbox.size_x / 2))
                y_max = int(detection.bbox.center.y + (detection.bbox.size_y / 2))

                img_cropped = cv_img[y_min:y_max, x_min:x_max]

                preprocessed_img = self.preprocess_img(img=img_cropped)
                predict_f = self.model_traffic_light(preprocessed_img)
                predict = predict_f.data.max(1, keepdim=True)[1]
                pose.id = int(1000 + int(predict))
                cnn_prob = float(torch.exp(predict_f)[0][int(predict)])
                pose.score = cnn_prob
                box.results.append(pose)

                # pose.id = int(1000 + int(predict))
                # box.results.append(pose)
                if self.validate_light_with_brightness_region(img_cropped, int(predict)):
                    new_bbox.detections.append(box)


            elif detection.results[0].id == 8:  # id:8 Traffic sign

                x_min = int(detection.bbox.center.x - (detection.bbox.size_x / 2))
                y_min = int(detection.bbox.center.y - (detection.bbox.size_y / 2))
                x_max = int(detection.bbox.center.x + (detection.bbox.size_x / 2))
                y_max = int(detection.bbox.center.y + (detection.bbox.size_y / 2))

                img_cropped = cv_img[y_min:y_max, x_min:x_max]

                preprocessed_img = self.preprocess_img(img=img_cropped)
                predict_f = self.model_traffic_sign(preprocessed_img)
                predict = predict_f.data.max(1, keepdim=True)[1]
                cnn_prob = float(torch.exp(predict_f)[0][int(predict)])
                pose.score = cnn_prob
                pose.id = int(2000 + int(predict))
                box.results.append(pose)
                new_bbox.detections.append(box)

            else:
                box = detection
                new_bbox.detections.append(box)

        new_bbox.header = msg_bbox.header
        if cam_id == "cam_fm_01":
            self.pub_fm01_new_bbox.publish(new_bbox)
        elif cam_id == "cam_fr_01":
            self.pub_fr01_new_bbox.publish(new_bbox)
        elif cam_id == "cam_fl_01":
            self.pub_fl01_new_bbox.publish(new_bbox)

    def preprocess_img(self, img):

        loader = transforms.Compose([
            transforms.Resize((32, 32)),
            transforms.ToTensor(),
            transforms.Normalize((0.3337, 0.3064, 0.3171), (0.2672, 0.2564, 0.2629))
        ])

        img = PilImage.fromarray(img)
        img = loader(img).float()
        img = Variable(img)
        img = img.unsqueeze(0)

        return img.cuda(device=self.device)

    def validate_light_with_brightness_region(self, rgb_image, light_id):

        if light_id == 0:
            return True

        hsv = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)

        v = hsv[:, :, 2]
        height, width = v.shape

        height_div3 = int((height - 6) / 3)

        red_region = v[3:3 + height_div3, 3:width - 3]
        yellow_region = v[3 + height_div3:3 + height_div3 * 2, 3:width - 3]
        green_region = v[3 + height_div3 * 2:3 + height_div3 * 3, 3:width - 3]

        sum_brightness_red = np.sum(red_region)
        avg_brightness_red = sum_brightness_red / (height_div3 * width)
        sum_brightness_yellow = np.sum(yellow_region)
        avg_brightness_yellow = sum_brightness_yellow / (height_div3 * width)
        sum_brightness_green = np.sum(green_region)
        avg_brightness_green = sum_brightness_green / (height_div3 * width)

        # print(sum_brightness_red)
        # print(sum_brightness_yellow)
        # print(sum_brightness_green)

        if avg_brightness_red >= avg_brightness_yellow and avg_brightness_red >= avg_brightness_green:
            brightness_predict = 1
        elif avg_brightness_yellow >= avg_brightness_green:
            brightness_predict = 2
        else:
            brightness_predict = 3

        if brightness_predict == light_id:
            return True
        else:
            return False


if __name__ == "__main__":
    rospy.init_node(node_handle_name)
    classifier_node = ClassifierNode()
    rospy.spin()
