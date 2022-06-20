import json
from FolderOp import *
class TreeOp:
    def __init__(self):       
        try:
            self.tree_config = self.read_json("treeConfig.json")
            if self.tree_config:
                print("Tree config file loaded")
                for tree in self.tree_config:
                    print(tree)
        except:
            self.tree_config = {}
            self.write_json("treeConfig.json", self.tree_config) #create new one and initialize with {}

    def create_new_tree(self, tree_path_to_root, root_name):
        if tree_path_to_root + "-" + root_name in self.tree_config:
            print("Tree already exists")
            return
        #create a new json file im the os

        self.tree_config[tree_path_to_root + "-" + root_name] = [] #create new empty dictionary entry

        new_json_file_name = tree_path_to_root + "-" + root_name + ".json"
    
        self.write_json(new_json_file_name, {}) # create new json file and initialize with {}

        folder_op = FolderOp(tree_path_to_root, new_json_file_name, '/Root')

        self.write_json(new_json_file_name, folder_op.config)

    #read from json file
    def read_json(self,file_name):
        with open(file_name, 'r') as f:
            data = json.load(f)
        return data

    #write to json file
    def write_json(self, file_name, data):
        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)