train_path = "/home/otonom2/Documents/Projects/stn_traffic_sign_classification-master/GTSRB/Train"

import torch
from torchvision import datasets, transforms
import numpy as np
from torch.utils import data

train_dataset_data_transform = datasets.ImageFolder(
    root=train_path,
    transform=transforms.Compose([
        transforms.Resize((32, 32)),
        transforms.ToTensor()
    ])
)

train_loader = data.DataLoader(
    train_dataset_data_transform,
    batch_size=64,
    num_workers=8,
    shuffle=True)

def online_mean_and_sd(loader):
    cnt = 0
    fst_moment = torch.empty(3)
    snd_moment = torch.empty(3)

    for data in loader:

        b, c, h, w = data[0].shape
        nb_pixels = b * h * w
        sum_ = torch.sum(data[0], dim=[0, 2, 3])
        sum_of_square = torch.sum(data[0] ** 2, dim=[0, 2, 3])
        fst_moment = (cnt * fst_moment + sum_) / (cnt + nb_pixels)
        snd_moment = (cnt * snd_moment + sum_of_square) / (cnt + nb_pixels)

        cnt += nb_pixels
    return fst_moment, torch.sqrt(snd_moment - fst_moment ** 2)


mean, std = online_mean_and_sd(train_loader)

print("Mean : " + str(mean))
print("Std : " + str(std))