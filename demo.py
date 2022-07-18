#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Module.Core.V2.dataset_loader import demo
#  from Module.Core.V2.synset_loader import demo
#  from Module.Core.V2.model_loader import demo

from random import randint

from Method.udfs import *

if __name__ == "__main__":
    #  demo()

    mesh_file_path = "/home/chli/scan2cad/im3d/data/pix3d/metadata/model/bed/IKEA_BEDDINGE/model.obj"
    mesh = loadMesh(mesh_file_path)
    normalizeMesh(mesh)
    rotateMesh(mesh, 0, 0, randint(-179, 180))
    point_list = [
        [0, 0, 0],
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ]
    scene = getRaycastingScene(mesh)
    unsigned_distance_list = getPointDistListToMesh(scene, point_list)
    print("unsigned distance list")
    print(unsigned_distance_list)

