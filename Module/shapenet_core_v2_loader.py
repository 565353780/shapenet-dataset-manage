#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

class ShapeNetCoreV2Loader(object):
    def __init__(self):
        self.dataset_root_path = None

        self.synset_id_list = []
        self.model_id_list_dict = {}
        return

    def reset(self):
        self.dataset_root_path = None

        self.synset_id_list = []
        self.model_id_list_dict = {}
        return True

    def setDataPath(self, dataset_root_path):
        if not os.path.exists(dataset_root_path):
            print("[ERROR][ShapeNetCoreV2Loader::setDataPath]")
            print("\t dataset_root_path not exist!")
            return False

        self.dataset_root_path = dataset_root_path
        if self.dataset_root_path[-1] != "/":
            self.dataset_root_path += "/"
        return True

    def loadSynsetId(self):
        root_folder_name_list = os.listdir(self.dataset_root_path)
        for root_folder_name in root_folder_name_list:
            if not os.path.isdir(self.dataset_root_path + root_folder_name):
                continue
            self.synset_id_list.append(root_folder_name)
        return True

    def loadModelId(self):
        if len(self.synset_id_list) == 0:
            return True

        for synset_id in self.synset_id_list:
            synset_folder_path = self.dataset_root_path + synset_id + "/"
            self.model_id_list_dict[synset_id] = os.listdir(synset_folder_path)
        return True

    def loadDataset(self, dataset_root_path):
        self.reset()

        if not self.setDataPath(dataset_root_path):
            print("[ERROR][ShapeNetCoreV2Loader::loadDataset]")
            print("\t setDataPath failed!")
            return False
        if not self.loadSynsetId():
            print("[ERROR][ShapeNetCoreV2Loader::loadDataset]")
            print("\t loadSynsetId failed!")
            return False
        if not self.loadModelId():
            print("[ERROR][ShapeNetCoreV2Loader::loadDataset]")
            print("\t loadModelId failed!")
            return False
        return True

    def outputInfo(self, info_level=0):
        line_start = "\t" * info_level
        print(line_start + "[ShapeNetCoreV2]")
        print(line_start + "\t synsetId size =", len(self.synset_id_list))
        print(line_start + "\t modelId size =", len(self.model_id_list_dict.keys()))
        return True

def demo():
    dataset_root_path = "/home/chli/scan2cad/shapenet/ShapeNetCore.v2/"

    shapenet_core_v2_loader = ShapeNetCoreV2Loader()
    shapenet_core_v2_loader.loadDataset(dataset_root_path)
    shapenet_core_v2_loader.outputInfo()
    return True

if __name__ == "__main__":
    demo()

