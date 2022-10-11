#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tqdm import tqdm

from shapenet_dataset_manage.Method.path import renameFile, removeFile
from shapenet_dataset_manage.Method.image_format import isImageFormatValid

from shapenet_dataset_manage.Module.Core.V2.dataset_loader import DatasetLoader


class ImageFormatFixer(object):

    def __init__(self, dataset_folder_path):
        self.dataset_folder_path = dataset_folder_path
        self.dataset_loader = DatasetLoader()
        self.dataset_loader.loadDataset(dataset_folder_path)
        return

    def isImageFormatValid(self, model):
        image_folder_path = model.root_path + "images/"
        if not os.path.exists(image_folder_path):
            return True

        image_file_name_list = os.listdir(image_folder_path)

        for image_file_name in image_file_name_list:
            if image_file_name.split(".")[-1] not in ["png", "jpg", "jpeg"]:
                continue

            image_file_path = image_folder_path + image_file_name
            is_valid, image_format = isImageFormatValid(image_file_path)
            assert image_format is not None, image_file_path

            if not is_valid:
                return False
        return True

    def fixImageFormat(self, model):
        image_folder_path = model.root_path + "images/"
        assert os.path.exists(image_folder_path)

        image_file_name_list = os.listdir(image_folder_path)

        image_rename_dict = {}
        for image_file_name in image_file_name_list:
            if image_file_name.split(".")[-1] not in ["png", "jpg", "jpeg"]:
                continue

            image_file_path = image_folder_path + image_file_name
            is_valid, image_format = isImageFormatValid(image_file_path)
            if is_valid:
                continue
            image_rename_dict[image_file_name] = image_file_name.split(
                ".")[0] + "." + image_format

        assert len(list(image_rename_dict.keys())) > 0

        for source_image_name, target_image_name in image_rename_dict.items():
            source_image_file_path = image_folder_path + source_image_name
            target_image_file_path = image_folder_path + target_image_name
            renameFile(source_image_file_path, target_image_file_path)

        mtl_file_path = model.normalized_mtl_file_path
        assert os.path.exists(mtl_file_path)

        new_mtl_file_path = mtl_file_path[:-4] + "_new.mtl"

        with open(mtl_file_path, "r") as fr:
            lines = fr.readlines()
            with open(new_mtl_file_path, "w") as fw:
                for line in lines:
                    new_line = line
                    for source_image_name, target_image_name in image_rename_dict.items(
                    ):
                        if source_image_name not in line:
                            continue
                        new_line = line.replace(source_image_name,
                                                target_image_name)
                        break
                    fw.write(new_line)

        removeFile(mtl_file_path)
        renameFile(new_mtl_file_path, mtl_file_path)
        return True

    def fixAllImageFormat(self, print_progress=False):
        if print_progress:
            print("[INFO][ImageFormatFixer::fixAllImageFormat]")
            print("\t start fix all image format...")
        synset_idx = 0
        synset_num = len(list(self.dataset_loader.dataset.synset_dict.keys()))
        for synset_id, synset in self.dataset_loader.dataset.synset_dict.items(
        ):
            synset_idx += 1
            for_data = synset.model_dict.items()
            if print_progress:
                print("[INFO][ImageFormatFixer::fixAllImageFormat]")
                print("\t start fix image format for synset [" + synset_id +
                      "], " + str(synset_idx) + "/" + str(synset_num) + "...")
                for_data = tqdm(for_data)
            for _, model in for_data:
                if self.isImageFormatValid(model):
                    continue

                self.fixImageFormat(model)
                print("[INFO][ImageFormatFixer::fixAllImageFormat]")
                print("\t found error models :")
                print(model.root_path)
        return True
