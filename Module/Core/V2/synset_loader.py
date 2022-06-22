#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Data.synset import Synset

class SynsetLoader(object):
    def __init__(self):
        self.synset = Synset()
        return

    def reset(self):
        self.synset.reset()
        return True

    def loadSynset(self, synset_root_path):
        if not self.synset.loadRootPath(synset_root_path):
            print("[ERROR][SynsetLoader::loadSynset]")
            print("\t loadRootPath failed!")
            return False
        return True

    def outputInfo(self, info_level=0, print_cols=5):
        self.synset.outputInfo(info_level, print_cols)
        return True

def demo():
    synset_root_path = "/home/chli/scan2cad/shapenet/ShapeNetCore.v2/02691156/"

    synset_loader = SynsetLoader()
    synset_loader.loadSynset(synset_root_path)
    synset_loader.outputInfo()
    return True

if __name__ == "__main__":
    demo()

