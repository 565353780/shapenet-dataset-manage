#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def renameFile(source_file_path, target_file_path):
    assert os.path.exists(source_file_path)

    while os.path.exists(source_file_path):
        try:
            os.rename(source_file_path, target_file_path)
        except:
            continue
    return True


def removeFile(file_path):
    while os.path.exists(file_path):
        try:
            os.remove(file_path)
        except:
            continue
    return True
