#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Config.sample import \
    SAMPLE_POINT_MATRIX, SAMPLE_Z_ANGLE_LIST, \
    SAMPLE_X_ANGLE_LIST, SAMPLE_Y_ANGLE_LIST

from Method.paths import createFileFolder, getFilePath
from Method.udfs import \
    loadMesh, normalizeMesh, rotateMesh, \
    getRaycastingScene, getPointDistListToMesh, \
    saveUDF

class UDFGenerator(object):
    def __init__(self, mesh_file_path=None):
        self.mesh_file_path = mesh_file_path

        self.mesh = None

        if mesh_file_path is not None:
            self.loadMesh(mesh_file_path)
        return

    def loadMesh(self, mesh_file_path):
        self.mesh = loadMesh(mesh_file_path)

        if self.mesh is None:
            print("[ERROR][UDFGenerator::loadMesh]")
            print("\t loadMesh failed!")
            return False

        normalizeMesh(self.mesh)
        return True

    def getUDF(self, z_angle=0, x_angle=0, y_angle=0):
        if self.mesh is None:
            print("[ERROR][UDFGenerator::getUDF]")
            print("\t mesh is not valid! please call loadMesh first!")
            return None

        if not rotateMesh(self.mesh, z_angle, x_angle, y_angle):
            print("[ERROR][UDFGenerator::getUDF]")
            print("\t rotateMesh failed!")
            return None

        scene = getRaycastingScene(self.mesh)
        udf = getPointDistListToMesh(scene, SAMPLE_POINT_MATRIX)

        if not rotateMesh(self.mesh, -z_angle, -x_angle, -y_angle):
            print("[ERROR][UDFGenerator::getUDF]")
            print("\t rotateMesh for reset failed!")
            return None
        return udf

    def generateUDF(self, udf_save_file_basepath):
        if not createFileFolder(udf_save_file_basepath):
            print("[ERROR][UDFGenerator::generateUDF]")
            print("\t createFileFolder failed!")
            return False

        for z_angle in SAMPLE_Z_ANGLE_LIST:
            for x_angle in SAMPLE_X_ANGLE_LIST:
                for y_angle in SAMPLE_Y_ANGLE_LIST:
                    udf = self.getUDF(z_angle, x_angle, y_angle)

                    if udf is None:
                        print("[ERROR][UDFGenerator::generateUDF]")
                        print("\t getUDF failed!")
                        return False

                    udf_save_file_path = getFilePath(udf_save_file_basepath,
                                                     [["rotz", z_angle],
                                                      ["rotx", x_angle],
                                                      ["roty", y_angle]],
                                                     "npy")
                    if not saveUDF(udf, udf_save_file_path):
                        print("[ERROR][UDFGenerator::generateUDF]")
                        print("\t saveUDF failed!")
                        return False
        return True

def demo():
    mesh_file_path = "/home/chli/scan2cad/im3d/data/pix3d/metadata/model/bed/IKEA_BEDDINGE/model.obj"
    udf_save_file_basepath = "/home/chli/scan2cad/im3d_udf/bed/IKEA_BEDDINGE/udf"

    udf_generator = UDFGenerator(mesh_file_path)
    udf_generator.generateUDF(udf_save_file_basepath)
    return True

