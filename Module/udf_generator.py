#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Config.sample import SAMPLE_NUM

from Method.samples import getSamplePointMatrix
from Method.udfs import \
    loadMesh, normalizeMesh, rotateMesh, \
    getRaycastingScene, getPointDistListToMesh

class UDFGenerator(object):
    def __init__(self):
        self.sample_point_matrix = getSamplePointMatrix(SAMPLE_NUM)

        self.mesh = None
        return

    def loadMesh(self, mesh_file_path):
        self.mesh = loadMesh(mesh_file_path)
        normalizeMesh(self.mesh)
        point_list = getSamplePointMatrix(2)
        print(point_list)
        scene = getRaycastingScene(mesh)
        unsigned_distance_list = getPointDistListToMesh(scene, point_list)
        print("unsigned distance list")
        print(unsigned_distance_list)
        return True

    def getUDF(self, z_angle=0, x_angle=0, y_angle=0):
        if not rotateMesh(self.mesh, z_angle, x_angle, y_angle):
            print("[ERROR][UDFGenerator::getUDF]")
            print("\t rotateMesh failed!")
            return None

        scene = getRaycastingScene(self.mesh)
        udf = getPointDistListToMesh(scene, self.sample_point_matrix)

        if not rotateMesh(self.mesh, -z_angle, -x_angle, -y_angle):
            print("[ERROR][UDFGenerator::getUDF]")
            print("\t rotateMesh for reset failed!")
            return None
        return udf

def demo():
    mesh_file_path = "/home/chli/scan2cad/im3d/data/pix3d/metadata/model/bed/IKEA_BEDDINGE/model.obj"

    udf_generator = UDFGenerator()
    udf_generator.loadMesh(mesh_file_path)
    return True

