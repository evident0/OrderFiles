from genericpath import isdir
import json
import os
from turtle import clear
#import regular expressions
import re
#enum with 3 states
import shutil

from colorama import Fore #for color

EXTENSION = "EXTENSION"
FOLDER = "FOLDER"
REGULAR_EXPRESSION = "REGULAR_EXPRESSION"

#could be a dataclass
class Rule():
    def __init__(self, rule_type, rule_name):
        self.rule_type = rule_type
        self.rule_name = rule_name

extensions = {}
regex = {}

def dfs(dictionary, path):
    extensions.clear()
    dfs_helper(dictionary, path, path) # path differs from operating system to operating system

def dfs_helper(dictionary, os_path, json_path): #starts with, path differs from operating system to operating system

    short_path = ""
    short_path = os.path.split(os_path)[-1]
  
    for value in dictionary[json_path]: # dict value is a list of lists [value[0]:type, value[1]:name]
        if value[0] == FOLDER:
            #create a file if it doesn't exist already
            if not os.path.exists(os_path+"/"+value[1]):
                os.makedirs(os.path.join(os_path, value[1]))
            #print ("This"+short_path + '/' + value[1])            
            dfs_helper(dictionary, os.path.join(os_path, value[1]), json_path+'/'+value[1])
        elif value[0] == EXTENSION: # regex or extension
            extensions[value[1]] = os_path # the path to the folder
        elif value[0] == REGULAR_EXPRESSION:
            regex[value[1]] = os_path # this will be traversed first to match any regex
        else:
            print("Error: unknown type")

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

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

def move_folder(dictionary, parent_dir, current_folder, new_parent_directory, new_folder):
    #check if it is a folder
    os_parent_dir = os.path.join(*parent_dir.split('/'),current_folder)
    os_new_parent_dir = os.path.join(*new_parent_directory.split('/'),new_folder)

    print(os_parent_dir)
    if os.path.isdir(os_parent_dir) is not True or os.path.isdir(os_new_parent_dir) is not True:

        print("ERROR: "+ os.path.join(parent_dir,current_folder)+" is not a folder")

        return
    #check if new directory is a subdirectory of the parent directory
    if os.path.commonprefix([os_parent_dir, os_new_parent_dir]) == os_parent_dir:
        
        print("ERROR: "+ os_new_parent_dir + " is a subdirectory of " + os_parent_dir)

        return

    # move a folder in the operating system
    os.rename(os.path.join(parent_dir,current_folder), os.path.join(new_parent_directory,new_folder))
     
    dictionary[parent_dir].remove([FOLDER,current_folder])

    dictionary[new_parent_directory].append([FOLDER, new_folder]) # add new folder to new parent directory
  
    move_dfs(dictionary, parent_dir+"/"+current_folder, new_parent_directory+"/"+new_folder);

    first_pair = next(iter((dictionary.items())))
    #update extensions
    #first pair is the root
    dfs(config,first_pair[0])

def move_dfs(dictionary, current_name,new_name):
    dictionary[new_name]=dictionary.pop(current_name) # append the poped dictionary to the new name

    for value in dictionary[new_name]:
        if value[0] == FOLDER:
            rename_dfs(dictionary, current_name+'/'+value[1], new_name+'/'+value[1])
            #dictionary[new_name+"/"+value[1]] = dictionary.pop(current_name+"/"+value[1])

def remove_folder(dictionary, parent_dir, current_folder):
    #check if it does not exist and return if it does not
    if parent_dir+'/'+current_folder not in dictionary:
        print("ERROR: "+ os.path.join(parent_dir,current_folder)+" does not exist")
        return
    #remove folder from operating system
    ##os.rmdir(os.path.join(parent_dir,current_folder))
    shutil.rmtree(os.path.join(parent_dir,current_folder))

    dictionary[parent_dir].remove([FOLDER,current_folder])
    remove_dfs(dictionary, parent_dir+"/"+current_folder)

    first_pair = next(iter((dictionary.items())))
    #update extensions
    #first pair is the root
    dfs(config,first_pair[0])

def remove_dfs(dictionary, current_name):
   
    for value in dictionary[current_name]:
        if value[0] == FOLDER:
            remove_dfs(dictionary, current_name+'/'+value[1])
    
    dictionary.pop(current_name)

def add_folder(dictionary, parent_dir, current_folder, list_of_lists):
    #check if folder exists in dictionary and return if it does
    if parent_dir+'/'+current_folder in dictionary:
        print("ERROR: "+ parent_dir+'/'+current_folder + " already exists")
        return

    #create folder in operating system
    os_dir = os.path.join(*parent_dir.split('/'),current_folder)
    os.makedirs(os.path.join(os_dir))

    #add the new folder to the parent directory for reference
    dictionary[parent_dir].append([FOLDER, current_folder])

    #create the empty folder in the dictionary
    dictionary[parent_dir+"/"+current_folder] = []

    #for each item in the list of lists, add it to the dictionary
    for value in list_of_lists:
        if value[0] == FOLDER:
            #add the folder under the new folder
            dictionary[parent_dir+"/"+current_folder].append([FOLDER, value[1]])
            #create the empty folder entry for the dictionary
            dictionary[parent_dir+"/"+current_folder+"/"+value[1]] = []
        elif value[0] == EXTENSION:
            #add the extension to the dictionary list of the new folder
            dictionary[parent_dir+"/"+current_folder].append([EXTENSION, value[1]])
        elif value[0] == REGULAR_EXPRESSION:
            #add the regex to the dictionary list of the new folder
            dictionary[parent_dir+"/"+current_folder].append([REGULAR_EXPRESSION, value[1]])
        else:
            print("ERROR: unknown type") # ERROR all CAPS
    
    first_pair = next(iter((dictionary.items())))

    #update extensions
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

def handle_file_collision(root,file):
    while os.path.isfile(os.path.join(root,file)):
                        #get the file name and extension
        file_name = os.path.splitext(file)[0]
        file_extension = os.path.splitext(file)[1]
        #get the number in parenthesis
        number = re.search(r'\((\d+)\)', file_name)
        if number:
            #get the number
            number = number.group(1)
            #remove the number in parenthesis
            file_name = file_name.replace('('+number+')','')
            #increase the number by 1
            number = int(number) + 1
            #add the number in parenthesis
            file_name = file_name + '(' + str(number) + ')' + file_extension
        else:
            #add the number in parenthesis
            file_name = file_name + '(1)' + file_extension
        file = file_name
    return file

#scan a directory and check the extension of each file
def scan_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            cont_loop = False
            for reg in regex:
                if re.search(reg, file):
                    #move file to the folder
                    
                    new_file_name = handle_file_collision(regex[reg],file)
                   
                    os.rename(os.path.join(root,file), os.path.join(regex[reg],new_file_name))
                  
                    cont_loop = True
                    break
            if cont_loop:
                continue
            #if no regular expressions matched, move file based on it's extension
            #check if file extension is in the list of extensions
            if "."+file.split('.')[-1] in extensions:
                #move file to the folder
                new_file_name = handle_file_collision(extensions['.'+file.split('.')[-1]],file)

                os.rename(os.path.join(root,file), os.path.join(extensions['.'+file.split('.')[-1]],new_file_name))

if __name__ == '__main__':
  
    config = read_json('config_output.json')
    dfs(config,"Root")
    print(extensions)

    #move_folder(config, "Root", "Documents", "Root/Images", "Documents")
    #move_folder(config, "Root", "Documents", "Root/Images", "Doc")
    #move_folder(config, "Root/Documents", "WORD", "Root/Documents", "WORUDO")
    ##move_folder(config, "Root", "Images", "Root/Documents/PDF", "Documento")
    ##remove_folder(config, "Root/Documents/PDF", "Documento")
    #move_folder(config, "Root/Documents", "PDF", "Root/Documents/WORD", "PDFS")
    ##move_folder(config, "Root/Documents", "PDF", "Root/Documents/WORD", "PDFS")
    #move_folder(config, "Root", "Documents", "Root/Documents", "PDF")
    ###add_folder(config,"Root","NEW_FOLDER",[[FOLDER,"NEW_FOLDER_2"],[EXTENSION,".txt"]])
    ###remove_folder(config,"Root","NEW_FOLDER")
    '''
    rename_folder(config, None , "Root", "New Root")
    rename_folder(config, "New Root" ,"Documents", "Doc")
    
    print(config)
    rename_folder(config, "New Root/Doc" ,"PDF", "pf")
    rename_folder(config, "New Root" ,"Images", "Img")
    print(config)
    '''
    scan_directory("test")
    write_json('config_output.json', config)
    print()
    print()
    print(config)
    print()
    print(extensions)
    print()
    print(regex)