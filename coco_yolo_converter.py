from pycocotools.coco import COCO
import shutil
import os

print("hello world!")

coco_dataset_folder = "/home/otonom2/Downloads/DFG/JPEGImages"
label_folder = '/home/otonom2/Downloads/DFG/DFG-tsd-annot-json/train.json'
darknet_folder = "/home/otonom2/Downloads/DFG_dataset"

coco = COCO(label_folder)

category_names = ["traffic sign"]



if __name__ == "__main__":

    cat_ids = coco.getCatIds(catNms=category_names)
    train_file = open("/home/otonom2/Downloads/DFG_dataset/train.txt", "a+")
    
    for cat_id in cat_ids:

        ann_ids = coco.getAnnIds(catIds=cat_id)
        anns = coco.loadAnns(ann_ids)

        print("Category id :" + str(cat_id))
        print("BDD-100K label : " + str(coco_id_to_bddk[int(cat_id)]))
        print("Annotation len : " + str(len(anns)))

        for ann in anns:
            x_top_left = ann['bbox'][0]
            y_top_left = ann['bbox'][1]
            bbox_width = ann['bbox'][2]
            bbox_height = ann['bbox'][3]


            img_id = ann['image_id']
            img = coco.loadImgs(ids=img_id)
            img_name = img[0]['file_name']
            image_width = img[0]['width']
            image_height = img[0]['height']

            x_center = x_top_left + bbox_width / 2
            y_center = y_top_left + bbox_height / 2

            # darknet annotation format
            a = format(x_center / image_width, '.6f')
            b = format(y_center / image_height, '.6f')
            c = format(bbox_width / image_width, '.6f')
            d = format(bbox_height / image_height, '.6f')

            # print("{} {} {} {} {}".format(1, a, b, c, d))

            shutil.copy(coco_dataset_folder + img_name, darknet_folder + "train/" + img_name)
            with open(os.path.splitext(darknet_folder + "train/" + img_name)[0] + ".txt", "a+") as fp:
                fp.write("{} {} {} {} {}\n".format(str(coco_id_to_bddk[int(cat_id)]), a, b, c, d))

        print("Category id :" + str(cat_id) + " COMPLETED...")

    train_file.close()