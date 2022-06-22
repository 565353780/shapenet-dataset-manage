#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Data.model import Model

class ModelLoader(object):
    def __init__(self):
        self.model = Model()
        return

    def reset(self):
        self.model.reset()
        return True

    def loadModel(self, model_root_path):
        if not self.model.loadRootPath(model_root_path):
            print("[ERROR][ModelLoader::loadModel]")
            print("\t loadRootPath failed!")
            return False
        return True

    def outputInfo(self, info_level=0):
        self.model.outputInfo(info_level)
        return True

def demo():
    model_root_path = "/home/chli/scan2cad/shapenet/ShapeNetCore.v2/02691156/10155655850468db78d106ce0a280f87/"

    model_loader = ModelLoader()
    model_loader.loadModel(model_root_path)
    model_loader.outputInfo()
    return True

if __name__ == "__main__":
    demo()

