import json
import os

#enum with 3 states

EXTENSION = "EXTENSION"
FOLDER = "FOLDER"
REGULAR_EXPRESSION = "REGULAR_EXPRESSION"

#could be a dataclass
class Rule():
    def __init__(self, rule_type, rule_name):
        self.rule_type = rule_type
        self.rule_name = rule_name

extensions = {}
def dfs(dictionary, path):
    dfs_helper(dictionary, path, path) # path differs from operating system to operating system

def dfs_helper(dictionary, os_path, json_path): #starts with, path differs from operating system to operating system

    short_path = ""
    short_path = os.path.split(os_path)[-1]
  
    for value in dictionary[json_path]: # dict value is a list of lists [value[0]:type, value[1]:name]
        if value[0] == FOLDER:
            #print ("This"+short_path + '/' + value[1])            
            dfs_helper(dictionary, os.path.join(os_path, value[1]), json_path+'/'+value[1])
        else: # regex or extension
            extensions[value[1]] = os_path # the path to the folder

def rename_dfs(dictionary, current_name, new_name):
    dictionary[new_name] = dictionary.pop(current_name)

    for value in dictionary[new_name]:
        if value[0] == FOLDER:
            rename_dfs(dictionary, current_name+'/'+value[1], new_name+'/'+value[1])
            #dictionary[new_name+"/"+value[1]] = dictionary.pop(current_name+"/"+value[1])

def rename_folder(dictionary, parent_dir, current_name, new_name):

    
    if(parent_dir is not None):
        for value in dictionary[parent_dir]:
            if value[0] == FOLDER and value[1] == current_name:
                value[1] = new_name
        rename_dfs(dictionary, parent_dir+"/"+current_name, parent_dir+"/"+new_name);
    else: # this is the root
        rename_dfs(dictionary, current_name, new_name);
    
    first_pair = next(iter((dictionary.items())))
    
    #first pair is the root
    dfs(config,first_pair[0])

#read from json file
def read_json(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data

#write to json file
def write_json(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
  
    config = read_json('config.json')
    dfs(config,"Root")
    print(extensions)

    rename_folder(config, None , "Root", "New Root")
    rename_folder(config, "New Root" ,"Documents", "Doc")
    
    print(config)
    rename_folder(config, "New Root/Doc" ,"PDF", "pf")
    rename_folder(config, "New Root" ,"Images", "Img")
    print(config)
    
    write_json('config.json', config)

    print(extensions)