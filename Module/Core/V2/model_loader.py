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

