from importlib.resources import path
import json
import os
from FolderOp import *
from defines import *
class TreeOp:
    def __init__(self): 
        self.folder_op_list = []     
        try:
            self.tree_config = self.read_json("treeConfig.json")
            if self.tree_config:
                print("Tree config file loaded")
                for tree in self.tree_config:
                    path_to_root = os.path.dirname(tree)
                    root = os.path.basename(tree)
                    json_file_name = self.json_file_string(path_to_root, root)
                    self.folder_op_list.append(FolderOp(path_to_root, json_file_name , root))
                    print(tree)
        except:
            self.tree_config = {}
            self.write_json("treeConfig.json", self.tree_config) #create new one and initialize with {}

    def create_new_tree(self, tree_path_to_root, root_name):
        os_path = os.path.join(tree_path_to_root , root_name)

        if os_path in self.tree_config:
            print("Tree already exists")
            return
        #create a new json file im the os

        self.tree_config[os_path] = [] #create new empty dictionary entry
        #TODO replace / with - and \\ with -
        new_json_file_name = self.json_file_string(tree_path_to_root, root_name)
    
        self.write_json(new_json_file_name, {}) # create new json file and initialize with {}

        folder_op = FolderOp(tree_path_to_root, new_json_file_name, '/'+root_name)

        self.write_json(new_json_file_name, folder_op.config)

        self.write_json("treeConfig.json", self.tree_config)

    def remove_tree(self, tree_path_to_root, root_name):
        os_path = os.path.join(tree_path_to_root , root_name)
        if os_path not in self.tree_config:
            print("Tree does not exist")
            return
        del self.tree_config[tree_path_to_root + "-" + root_name]
        self.write_json("treeConfig.json", self.tree_config)#we don't have to remove folderop config
    
    def select_tree(self, tree_path_to_root, root_name):
        folder_op = self.find_folder_op(tree_path_to_root, root_name)
        if folder_op == None:
            print("Tree does not exist")
            return None
        return folder_op
       

    #find the folderop object that corresponds to the tree
    def find_folder_op(self, tree_path_to_root, root_name):
        for folder_op in self.folder_op_list:
            if folder_op.path_to_root == tree_path_to_root and folder_op.root == root_name:
                return folder_op
        return None
        



    #read from json file
    def read_json(self,file_name):
        with open(file_name, 'r') as f:
            data = json.load(f)
        return data

    #write to json file
    def write_json(self, file_name, data):
        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)

    def json_file_string(self, path_to_root, root):
        return (path_to_root + root + ".json").replace("\\", "").replace("/",
        "").replace(":", "").replace("*", "").replace("?", "").replace("\"", "").replace("<",
        "").replace(">", "").replace("|", "")