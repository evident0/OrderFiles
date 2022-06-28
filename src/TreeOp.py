from importlib.resources import path
import json
import os
from FolderOp import *
from defines import *
from Scan import *
from Error import *
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
                    self.folder_op_list.append(FolderOp(path_to_root, json_file_name , '/'+root)) # slash needed because not given by user
                    print(f"Loaded tree {tree} /{root} from json file {json_file_name}")
        except:
            self.tree_config = {}
            self.write_json("treeConfig.json", self.tree_config) #create new one and initialize with {}

    def create_new_tree(self, tree_path_to_root, root_name):
        os_path = os.path.join(tree_path_to_root , root_name)
        if not os.path.isdir(tree_path_to_root):
            print_err("Parent directory of tree must be a valid os directory")
            return
        if os_path in self.tree_config:
            print_err("Tree already exists")
            return
        #create a new json file im the os

        self.tree_config[os_path] = [] #create new empty dictionary entry

        new_json_file_name = self.json_file_string(tree_path_to_root, root_name)
    
        self.write_json(new_json_file_name, {}) # create new json file and initialize with {}

        folder_op = FolderOp(tree_path_to_root, new_json_file_name, '/'+root_name) # TODO slash fix this

        self.write_json(new_json_file_name, folder_op.config)

        self.write_json("treeConfig.json", self.tree_config)

        self.folder_op_list.append(folder_op)

    def remove_tree(self, tree_path_to_root, root_name):
        os_path = os.path.join(tree_path_to_root , root_name)
        if os_path not in self.tree_config:
            print_err("Tree does not exist")
            return
        del self.tree_config[tree_path_to_root + "-" + root_name]
        self.write_json("treeConfig.json", self.tree_config)#we don't have to remove folderop config
    
    def select_tree(self, tree_path_to_root, root_name):
        folder_op = self.find_folder_op(tree_path_to_root, root_name)
        if folder_op == None:
            print_err("Tree does not exist")
            return None
        return folder_op
       

    #find the folderop object that corresponds to the tree
    def find_folder_op(self, tree_path_to_root, root_name):
        for folder_op in self.folder_op_list:
            if folder_op.path_to_root == tree_path_to_root and folder_op.root == '/'+root_name:# / hiden from user
                return folder_op
        return None
        
    def add_scanable_folder(self, folder_op, folder_to_scan):
        #check folder_to_scan is a valid folder
        if not os.path.isdir(folder_to_scan):
            print("Folder does not exist in the os returning...")
            return 
        path_to_root = folder_op.path_to_root
        root = folder_op.root
        tree_config_entry_name = os.path.join(path_to_root, root.replace("/", ""))#one / at the start must be removed
        #check folder_to_scan is not already in the tree config
        if folder_to_scan in self.tree_config[tree_config_entry_name]:
            print(f"Folder already in the tree config for entry {tree_config_entry_name} returning...")
            return
    
        self.tree_config[tree_config_entry_name].append(folder_to_scan)
        try:
            self.write_json("treeConfig.json", self.tree_config)
        except Exception as e:
            print_err("Failed to write to tree config file" + str(e))
            self.tree_config[tree_config_entry_name].remove(folder_to_scan) # revert change
            return

    def remove_scanable_folder(self, folder_op, folder_to_remove):
        if not os.path.isdir(folder_to_remove):
            print("NOTE that folder does not exist in the os")
            #don't return because we want to remove it from the tree config
        path_to_root = folder_op.path_to_root
        root = folder_op.root
        tree_config_entry_name = os.path.join(path_to_root, root.replace("/", ""))
        if folder_to_remove not in self.tree_config[tree_config_entry_name]:
            print_err(f"Folder {folder_to_remove} not in the tree config for entry {tree_config_entry_name}, type scaninf, returning...")
            return
        self.tree_config[tree_config_entry_name].remove(folder_to_remove)
        try:
            self.write_json("treeConfig.json", self.tree_config)
        except Exception as e:
            print_err("Failed to write to tree config file" + str(e))
            self.tree_config[tree_config_entry_name].append(folder_to_remove) # revert change

    def order_files(self, folder_op):
        #TODO DO NOT CREATE AND DELETE A SCANNER
        scan = Scan(folder_op)
        path_to_root = folder_op.path_to_root
        root = folder_op.root
        tree_config_entry_name = os.path.join(path_to_root, root.replace("/", ""))
        for folder_to_scan in self.tree_config[tree_config_entry_name]:
            scan.scan_directory(folder_to_scan)
        del scan

    #return a list with all the keys in the tree config
    def get_tree_list(self):
        return list(self.tree_config.keys())

    #return the list of scannable folders for a given tree
    def get_scanable_folders(self, folder_op):
        path_to_root = folder_op.path_to_root
        root = folder_op.root
        tree_config_entry_name = os.path.join(path_to_root, root.replace("/", ""))
        if tree_config_entry_name not in self.tree_config:
            print_err("ERROR Tree does not exist")
            return None
        return self.tree_config[tree_config_entry_name]
        
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
        return (path_to_root +"\\"+ root + ".json").replace("\\", "-").replace("/",
        "-").replace(":", "").replace("*", "").replace("?", "").replace("\"", "-").replace("<",
        "").replace(">", "").replace("|", "")