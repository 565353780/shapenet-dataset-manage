#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

def getSamplePointMatrix(sample_num):
    if sample_num < 1:
        print("[ERROR][samples::getSamplePointMatrix]")
        print("\t sample_num not valid!")
        return None

    sample_unit_length = 1.0 / sample_num
    sample_start_length = sample_unit_length / 2.0 - 0.5

    sample_point_matrix = np.zeros((sample_num, sample_num, sample_num, 3))
    for z_idx in range(sample_num):
        z_value = sample_start_length + z_idx * sample_unit_length
        for x_idx in range(sample_num):
            x_value = sample_start_length + x_idx * sample_unit_length
            for y_idx in range(sample_num):
                y_value = sample_start_length + y_idx * sample_unit_length
                sample_point_matrix[z_idx][x_idx][y_idx] = [z_value, x_value, y_value]
    return sample_point_matrix

