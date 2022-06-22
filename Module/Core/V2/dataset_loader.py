#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Data.dataset import Dataset

class DatasetLoader(object):
    def __init__(self):
        self.dataset = Dataset()
        return

    def reset(self):
        self.dataset.reset()
        return True

    def loadDataset(self, dataset_root_path):
        if not self.dataset.loadRootPath(dataset_root_path):
            print("[ERROR][DatasetLoader::loadDataset]")
            print("\t loadRootPath failed!")
            return False
        return True

    def outputInfo(self, info_level=0, print_cols=10):
        self.dataset.outputInfo(info_level, print_cols)
        return True

def demo():
    dataset_root_path = "/home/chli/scan2cad/shapenet/ShapeNetCore.v2/"

    dataset_loader = DatasetLoader()
    dataset_loader.loadDataset(dataset_root_path)
    dataset_loader.outputInfo()
    return True

if __name__ == "__main__":
    demo()

