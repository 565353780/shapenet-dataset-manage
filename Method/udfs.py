#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import open3d as o3d
from math import pi

from Config.sample import SAMPLE_POINT_MATRIX

from Method.paths import createFileFolder

def getRad(angle):
    rad = angle * pi / 180.0
    return rad

def getAngle(rad):
    angle = rad * 180.0 / pi
    return angle

def loadMesh(mesh_file_path):
    if not os.path.exists(mesh_file_path):
        print("[ERROR][udfs::loadMesh]")
        print("\t mesh_file not exist!")
        return None

    mesh = o3d.io.read_triangle_mesh(mesh_file_path)
    return mesh

def getMeshBBox(mesh):
    bbox = mesh.get_axis_aligned_bounding_box()

    max_bound = bbox.get_max_bound()
    min_bound = bbox.get_min_bound()
    return min_bound, max_bound

def getMeshBBoxCenter(mesh):
    min_bound, max_bound = getMeshBBox(mesh)

    center = [(min_bound[0] + max_bound[0]) / 2.0,
              (min_bound[1] + max_bound[1]) / 2.0,
              (min_bound[2] + max_bound[2]) / 2.0]
    return center

def getMeshBBoxDiff(mesh):
    min_bound, max_bound = getMeshBBox(mesh)

    diff = [max_bound[0] - min_bound[0],
              max_bound[1] - min_bound[1],
              max_bound[2] - min_bound[2]]
    return diff

def translateMesh(mesh, z_diff=0, x_diff=0, y_diff=0):
    if z_diff == 0 and x_diff == 0 and y_diff == 0:
        return True

    mesh.translate((z_diff, x_diff, y_diff))
    return True

def rotateMesh(mesh, z_angle=0, x_angle=0, y_angle=0):
    if z_angle == 0 and x_angle == 0 and y_angle == 0:
        return True

    z_rad = getRad(z_angle)
    x_rad = getRad(x_angle)
    y_rad = getRad(y_angle)

    R = mesh.get_rotation_matrix_from_xyz((z_rad, x_rad, y_rad))
    mesh.rotate(R, center=mesh.get_center())
    return True

def scaleMesh(mesh, scale=1):
    if scale == 1:
        return True

    mesh.scale(scale, center=mesh.get_center())
    return True

def normalizeMesh(mesh):
    diff = getMeshBBoxDiff(mesh)
    diff_max = max(diff)
    scaleMesh(mesh, 1.0 / diff_max)

    bbox_center = getMeshBBoxCenter(mesh)
    translateMesh(mesh, -bbox_center[0], -bbox_center[1], -bbox_center[2])
    return True

def getRaycastingScene(mesh):
    mesh = o3d.t.geometry.TriangleMesh.from_legacy(mesh)
    scene = o3d.t.geometry.RaycastingScene()
    _ = scene.add_triangles(mesh)
    return scene

def getPointDistListToMesh(scene, point_list):
    query_point_list = o3d.core.Tensor(point_list, dtype=o3d.core.Dtype.Float32)
    unsigned_distance_list = scene.compute_distance(query_point_list).numpy()
    return unsigned_distance_list

def getSignedPointDistListToMesh(scene, point_list):
    query_point_list = o3d.core.Tensor(point_list, dtype=o3d.core.Dtype.Float32)
    signed_distance_list = scene.compute_signed_distance(query_point_list).numpy()
    return signed_distance_list

def saveUDF(udf, udf_save_file_path):
    if udf is None:
        print("[ERROR][udfs::saveUDF]")
        print("\t udf is None!")
        return False

    if not createFileFolder(udf_save_file_path):
        print("[ERROR][udfs::saveUDF]")
        print("\t createFileFolder failed!")
        return False

    np.save(udf_save_file_path, udf)
    return True

def loadUDF(udf_file_path):
    if not os.path.exists(udf_file_path):
        print("[ERROR][udfs::loadUDF]")
        print("\t udf_file not exist!")
        return None

    udf = np.load(udf_file_path)
    return udf

def visualUDF(udf_file_path):
    dist_max = 10.0

    udf = loadUDF(udf_file_path)

    if udf is None:
        print("[ERROR][udfs::visualUDF]")
        print("\t loadUDF failed!")
        return False

    point_list = []
    dist_list = []

    for z_idx in range(SAMPLE_POINT_MATRIX.shape[0]):
        for x_idx in range(SAMPLE_POINT_MATRIX.shape[1]):
            for y_idx in range(SAMPLE_POINT_MATRIX.shape[2]):
                udf_value = udf[z_idx][x_idx][y_idx]
                if udf_value > dist_max:
                    continue
                point_list.append(SAMPLE_POINT_MATRIX[z_idx][x_idx][y_idx])
                dist_list.append(udf_value)

    max_dist = np.max(dist_list)

    color_list = []
    for dist in dist_list:
        color_weight = 1.0 * dist / max_dist
        color_list.append([color_weight * 255,
                           color_weight * 255,
                           color_weight * 255])

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(point_list)
    pcd.colors = o3d.utility.Vector3dVector(color_list)

    o3d.visualization.draw_geometries([pcd])
    return True

