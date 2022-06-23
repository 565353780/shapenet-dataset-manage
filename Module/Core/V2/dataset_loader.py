#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv

from Data.dataset import Dataset

from Module.command_runner import CommandRunner

class DatasetLoader(object):
    def __init__(self):
        self.dataset = Dataset()
        # self.csv_dict[SynsetId] = {key:ModelId}
        # self.csv_dict[SynsetId][ModelId] = {key:Id, Split}
        # self.csv_dict[SynsetId]["SubSynsetIdList"] = [SubSynsetId]
        self.csv_dict = {}

        self.command_runner = CommandRunner()
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

    def loadCSVDict(self, csv_file_path):
        if not os.path.exists(csv_file_path):
            print("[ERROR][DatasetLoader::loadCSVDict]")
            print("\t csv file not exist!")
            return False

        csv_reader = csv.reader(open(csv_file_path))
        for line in csv_reader:
            Id, SynsetId, SubSynsetId, ModelId, Split = line
            if Id == "id":
                continue
            if SynsetId not in self.csv_dict.keys():
                self.csv_dict[SynsetId] = {}
                self.csv_dict[SynsetId]["SubSynsetIdList"] = []
            if SubSynsetId not in self.csv_dict[SynsetId]["SubSynsetIdList"]:
                self.csv_dict[SynsetId]["SubSynsetIdList"].append(SubSynsetId)
            if ModelId not in self.csv_dict[SynsetId].keys():
                self.csv_dict[SynsetId][ModelId] = {"Id": Id, "Split": Split}
        return True

    def getSplit(self, synset_id, model_id):
        if synset_id not in self.csv_dict.keys():
            print("[ERROR][DatasetLoader::getSplit]")
            print("\t synset_id not found in csv_dict!")
            return None
        if model_id not in self.csv_dict[synset_id].keys():
            print("[ERROR][DatasetLoader::getSplit]")
            print("\t model_id not found in csv_dict!")
            return None

        return self.csv_dict[synset_id][model_id]["Split"]

    def transObjToGrd(self, msh2df_path, grd_save_folder_path):
        total_trans_num = 10

        if grd_save_folder_path[-1] != "/":
            grd_save_folder_path += "/"
        os.makedirs(grd_save_folder_path, exist_ok=True)

        self.command_runner.reset()

        for synset_id in self.dataset.synset_id_list:
            synset = self.dataset.synset_dict[synset_id]

            synset_save_folder_path = grd_save_folder_path + synset_id + "/"
            os.makedirs(synset_save_folder_path, exist_ok=True)

            synset_trans_num = 0
            for model_id in synset.model_id_list:
                model = synset.model_dict[model_id]
                if model.normalized_obj_file_path is None:
                    continue

                model_grd_file_path = synset_save_folder_path + model_id + ".grd"
                if os.path.exists(model_grd_file_path):
                    synset_trans_num += 1
                    if synset_trans_num >= total_trans_num:
                        break
                    continue

                command = msh2df_path + " " + model.normalized_obj_file_path + " " + model_grd_file_path + \
                    " -estimate_sign -spacing 0.002 -v"
                self.command_runner.addCommand(command)

                synset_trans_num += 1
                if synset_trans_num >= total_trans_num:
                    break

        print("[INFO][DatasetLoader::transObjToGrd]")
        print("\t start trans files from obj to grd...")
        self.command_runner.start()
        return True

    def transGrdToPly(self, grd2msh_path, grd_save_folder_path, ply_save_folder_path):
        if not os.path.exists(grd_save_folder_path):
            print("[ERROR][DatasetLoader::transGrdToPly]")
            print("\t grd_save_folder_path not exist!")
            return False

        if grd_save_folder_path[-1] != "/":
            grd_save_folder_path += "/"

        if ply_save_folder_path[-1] != "/":
            ply_save_folder_path += "/"
        os.makedirs(ply_save_folder_path, exist_ok=True)

        self.command_runner.reset()

        grd_synset_id_list = os.listdir(grd_save_folder_path)
        for synset_id in grd_synset_id_list:
            synset_grd_folder_path = grd_save_folder_path + synset_id + "/"
            model_grd_file_name_list = os.listdir(synset_grd_folder_path)

            synset_save_folder_path = ply_save_folder_path + synset_id + "/"
            os.makedirs(synset_save_folder_path, exist_ok=True)

            for model_grd_file_name in model_grd_file_name_list:
                model_grd_file_path = synset_grd_folder_path + model_grd_file_name

                model_id = model_grd_file_name.split(".")[0]
                model_ply_file_path = synset_save_folder_path + model_id + ".ply"
                if os.path.exists(model_ply_file_path):
                    continue

                command = grd2msh_path + " " + model_grd_file_path + " " + model_ply_file_path
                self.command_runner.addCommand(command)

        print("[INFO][DatasetLoader::transGrdToPly]")
        print("\t start trans files from grd to ply...")
        self.command_runner.start()
        return True

    def transObjToPly(self, msh2df_path, grd2msh_path, grd_save_folder_path, ply_save_folder_path):
        if not self.transObjToGrd(msh2df_path, grd_save_folder_path):
            print("[ERROR][DatasetLoader::transObjToPly]")
            print("\t transObjToGrd failed!")
            return False
        if not self.transGrdToPly(grd2msh_path, grd_save_folder_path, ply_save_folder_path):
            print("[ERROR][DatasetLoader::transObjToPly]")
            print("\t transGrdToPly failed!")
            return False
        return True

    def splitPly(self, ply_save_folder_path, split_save_folder_path):
        return True

    def outputInfo(self, info_level=0, print_cols=10):
        self.dataset.outputInfo(info_level, print_cols)
        return True

def demo():
    dataset_root_path = "/home/chli/scan2cad/shapenet/ShapeNetCore.v2/"
    csv_file_path = "/home/chli/scan2cad/shapenet/all.csv"
    msh2df_path = "/home/chli/github/local-deep-implicit-functions/ldif/gaps/bin/x86_64/msh2df"
    grd2msh_path = "/home/chli/github/local-deep-implicit-functions/ldif/gaps/bin/x86_64/grd2msh"
    grd_save_folder_path = "/home/chli/scan2cad/shapenet/v2_grd/"
    ply_save_folder_path = "/home/chli/scan2cad/shapenet/v2_ply/"
    split_save_folder_path = "/home/chli/scan2cad/shapenet/v2_split/"

    dataset_loader = DatasetLoader()
    dataset_loader.loadDataset(dataset_root_path)
    dataset_loader.loadCSVDict(csv_file_path)
    dataset_loader.transObjToPly(msh2df_path, grd2msh_path, grd_save_folder_path, ply_save_folder_path)
    dataset_loader.splitPly(ply_save_folder_path, split_save_folder_path)

    dataset_loader.outputInfo()
    return True

if __name__ == "__main__":
    demo()

