import os
import shutil
import copy
import send2trash
import json
from pathlib import Path
from defines import *
from Error import *
#NOTE An idea: merge directories and rules
class FolderOp:
    #class initilize with regex, config, EXTENSION, FOLDER, REGULAR_EXPRESSION
    def __init__(self,path_to_root,json_file_to_read,root):# path_to_root, regex, config, extensions, EXTENSION, FOLDER, REGULAR_EXPRESSION):
    
        self.path_to_root = path_to_root
        self.root = root
        self.json_file = json_file_to_read

        try:
            self.config = self.read_json(json_file_to_read)
        except ValueError:
            print("json is empty, creating new empty config")
            self.config = {}
        except FileNotFoundError:
            print_err("json File not found error")
        except PermissionError:
            print_err("json File permission denied")
        
        self.regex = {}
        self.extensions = {}

        # get the first entry of the dictionary config
        if self.config:
            first_key_is_root = next(iter(self.config))
            self.dfs(str(first_key_is_root))
        else:
            print("Note: config is empty")
            print("creating a new root")
            self.config[root] = []
            first_key_is_root = next(iter(self.config))
            self.dfs(str(first_key_is_root))
            try:
                self.write_json(json_file_to_read, self.config)
            except:
                print_err("Error: could not write to json file")
    

    def save_config(self):
        self.write_json(self.json_file, self.config)
      
    #read from json file
    def read_json(self,file_name):
        with open(file_name, 'r') as f:
            data = json.load(f)
        return data

    #write to json file
    def write_json(self, file_name, data):
        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)



    def dfs(self, path):
        self.extensions.clear()
        self.regex.clear()

        os_path = path.split("/") # this is for the root TODO: should not be here TODO: exists_ok=True
        if not os.path.exists(os.path.join(self.path_to_root,*os_path)):
                os.makedirs(os.path.join(self.path_to_root, *os_path))
        
        self.dfs_helper(path) # path differs from operating system to operating system

    def dfs_helper(self, path): #starts with, path differs from operating system to operating system
    
        for value in self.config[path]: #  dict value is a list of lists [value[0]:type, value[1]:name]
            os_path = path.split("/") # we need to split because for windows: \\, for linux: / we will join them later based on the os
            if value[0] == FOLDER:
                #create a file if it doesn't exist already
                # the * ensures to pass the list as arguments
                if not os.path.exists(os.path.join(self.path_to_root,*os_path, value[1])):
                    os.makedirs(os.path.join(self.path_to_root, *os_path, value[1]))   
                self.dfs_helper(path+'/'+value[1]) # this is for the dictionary, notice no os.path.join
            elif value[0] == EXTENSION: # regex or extension
                self.extensions[value[1]] = os.path.join(self.path_to_root,*os_path) # the path to the folder
            elif value[0] == REGULAR_EXPRESSION:
                self.regex[value[1]] = os.path.join(self.path_to_root,*os_path) # this will be traversed first to match any regex
            else:
                print_err("Error: unknown type " + value[0])

    def move_folder(self, parent_dir, current_folder, new_parent_directory, new_folder):
        
        #copy the dictionary to a new tempory dictionary
        temp_dictionary = copy.deepcopy(self.config) # the idea is to apply changes only if I/O operations succeed

        os_path = os.path.join(self.path_to_root,*parent_dir.split('/'),current_folder)
        os_new_path = os.path.join(self.path_to_root,*new_parent_directory.split('/'),new_folder)
        
        os_new_parent_dir = os.path.join(self.path_to_root,*new_parent_directory.split('/'))

        #check if the folders exist
        if os.path.isdir(os_path) is not True:
            print_err("ERROR: "+ os_path+" is not a folder in the os")
            return
        #check for max recursion error
        if os.path.commonpath([os_path, os_new_path]) == os_path:      
            print_err("ERROR: "+ os_new_path + " is a subdirectory of " + os_path)
            return
        #check if the folder exists in dictionary
        if parent_dir+'/'+current_folder not in self.config:
            print_err("ERROR: "+ parent_dir+'/'+current_folder +" does not exist in dictionary")
            return  
        #TODO create the folders on the way down
        if os.path.isdir(os_new_parent_dir) is not True:
            print_err("ERROR: "+ os_new_path+" is not a folder in the os, this method doesn't create the path")
            return
        #TODO create the folders on the way down
        if new_parent_directory not in self.config:
            print_err("ERROR: "+ new_parent_directory +" does not exist in dictionary, this method doesn't create the path")
            return #TODO new_parent_directory can be the empty string
        
        temp_dictionary[parent_dir].remove([FOLDER,current_folder])

        temp_dictionary[new_parent_directory].append([FOLDER, new_folder]) # add new folder to new parent directory
    
        self.move_dfs(temp_dictionary, parent_dir+"/"+current_folder, new_parent_directory+"/"+new_folder);

        try:
            os.rename(os_path,os_new_path)
            self.write_json(self.json_file, temp_dictionary)
            self.config = temp_dictionary
        except Exception as e:
            print_err("OS MOVE FAILED REVERTING CHANGES "+ str(e))
            self.dfs(self.root)


    def move_dfs(self,dictionary, current_name, new_name):
        dictionary[new_name]=dictionary.pop(current_name) # append the poped dictionary to the new name

        #compatiblity with the operating system
        os_path = os.path.join(self.path_to_root,*new_name.split('/'))

        for value in dictionary[new_name]:
            if value[0] == FOLDER:
                self.move_dfs(dictionary, current_name+'/'+value[1], new_name+'/'+value[1])
                #dictionary[new_name+"/"+value[1]] = dictionary.pop(current_name+"/"+value[1])
            elif value[0] == EXTENSION: # regex or extension
                self.extensions[value[1]] = os.path.join(self.path_to_root,os_path) # the path to the folder
            elif value[0] == REGULAR_EXPRESSION:
                self.regex[value[1]] = os.path.join(self.path_to_root,os_path) # this will be traversed first to match any regex
            else:
                print_err("Error: unknown type " + value[0])

    def remove_folder(self, parent_dir, current_folder):
        #check if folder is in os and return if not
        os_path = os.path.join(self.path_to_root,*parent_dir.split('/'),current_folder)

        if os.path.isdir(os_path) is not True:
            print_err("ERROR: "+ os_path + " is not a folder in the os")
            return self.config

        #check if it does not exist and return if it does not
        if parent_dir+'/'+current_folder not in self.config:
            print_err("ERROR: "+ parent_dir+'/'+current_folder +"doesn't exist in dictionary")
            return
        #remove folder from operating system
        ##os.rmdir(os.path.join(parent_dir,current_folder))
        #shutil.rmtree(os_path)
       

        temp_dictionary = copy.deepcopy(self.config)
        if parent_dir != "": # fast fix for root directory
            temp_dictionary[parent_dir].remove([FOLDER,current_folder])

        self.remove_dfs(temp_dictionary, parent_dir+"/"+current_folder)

        try:
            send2trash.send2trash(os_path)
            self.write_json(self.json_file, temp_dictionary)
            self.config = temp_dictionary    
        except Exception as e:
            print_err("OS REMOVE FAILED REVERTING CHANGES "+ str(e))
            self.dfs(self.root)

    def remove_dfs(self,dictionary, current_name):
    
        for value in dictionary[current_name]:
            if value[0] == FOLDER:
                self.remove_dfs(dictionary, current_name+'/'+value[1])
            elif value[0] == EXTENSION: # regex or extension
                self.extensions.pop(value[1]) # remove the entry from the extensions
            elif value[0] == REGULAR_EXPRESSION:
                self.regex.pop(value[1]) # remove the entry in regex
        
        dictionary.pop(current_name)

    def add_folder(self, parent_dir, current_folder, list_of_lists):
        #check if parent directory exists in os and return if it does not
        if os.path.isdir(os.path.join(self.path_to_root,*parent_dir.split('/'))) is not True:
            print_err("ERROR: "+ os.path.join(self.path_to_root,*parent_dir.split('/'))+" is not a folder in the os")
            return

        #check if folder exists in dictionary and return if it does
        if parent_dir+'/'+current_folder in self.config:#TODO call append_rules if it exists instead of throwing an error
            print_err("ERROR: "+ parent_dir+'/'+current_folder + " already exists")
            return

        temp_dictionary = copy.deepcopy(self.config)

        #create folder in operating system
        os_dir = os.path.join(self.path_to_root,*parent_dir.split('/'),current_folder)

        #add the new folder to the parent directory for reference
        temp_dictionary[parent_dir].append([FOLDER, current_folder])

        #create the empty folder in the dictionary
        temp_dictionary[parent_dir+"/"+current_folder] = []

        #for each item in the list of lists, add it to the dictionary
        for value in list_of_lists:
            if value[0] == FOLDER:
                if [FOLDER,value[0]] in temp_dictionary[parent_dir+"/"+current_folder]:
                    print_err("ERROR: folder "+ value[1]+" already exists in "+parent_dir+'/'+current_folder)
                    return
                #add the folder under the new folder
                temp_dictionary[parent_dir+"/"+current_folder].append([FOLDER, value[1]])
                #create the empty folder entry for the dictionary
                temp_dictionary[parent_dir+"/"+current_folder+"/"+value[1]] = []               
            elif value[0] == EXTENSION:
                if value[1] in self.extensions:
                    print_err("ERROR: extension "+ value[1]+" already exists in folder: "+self.extensions[list[1]])
                    return
                #add the extension to the dictionary list of the new folder
                temp_dictionary[parent_dir+"/"+current_folder].append([EXTENSION, value[1]])
                self.extensions[value[1]] = os.path.join(self.path_to_root,os_dir)
            elif value[0] == REGULAR_EXPRESSION:
                if value[1] in self.regex:
                    print_err("ERROR: regex "+ value[1]+" already exists in folder: "+self.regex[list[1]])
                    return
                #add the regex to the dictionary list of the new folder
                temp_dictionary[parent_dir+"/"+current_folder].append([REGULAR_EXPRESSION, value[1]])
                self.regex[value[1]] = os.path.join(self.path_to_root,os_dir)
            else:
                print_err("ERROR: unknown type "+ value[0])
        
        try:
            os.makedirs(os_dir, exist_ok=True)
            #create the folers if the dictionary updates successfully
            for value in list_of_lists:
                if value[0] == FOLDER:
                    os.makedirs(os.path.join(os_dir,value[1]), exist_ok=True)

            self.write_json(self.json_file, temp_dictionary)
            self.config = temp_dictionary
        except Exception as e:
            print_err("ERROR: could not create folder reverting changes..." + str(e))
            self.dfs(self.root)
    def append_to_folder(self, parent_dir, current_folder, list):

        os_dir = os.path.join(self.path_to_root,*parent_dir.split('/'),current_folder)
        print(os_dir)
        #check if folder exists in os and return if it does not
        if os.path.isdir(os.path.join(self.path_to_root,*parent_dir.split('/'), current_folder)) is not True:
            print_err("ERROR: "+ os.path.join(self.path_to_root,*parent_dir.split('/'), current_folder)+" is not a folder in the os")
            return

        #check if folder exists in dictionary and return if it does not
        if parent_dir+'/'+current_folder not in self.config:
            print_err("ERROR: "+ parent_dir+'/'+current_folder + " doesn't exist in dictionary")
            return

        temp_dictionary = copy.deepcopy(self.config)
        
        if list[0] == FOLDER:
            #search the list in the dictionary entry if it didn't find a folder with the same name then append it
            if [FOLDER, list[1]] not in temp_dictionary[parent_dir+'/'+current_folder]:
                temp_dictionary[parent_dir+'/'+current_folder].append([FOLDER, list[1]])
                temp_dictionary[parent_dir+"/"+current_folder+"/"+list[1]] = []
            else:#TODO: check this condition first
                print_err("ERROR: folder "+ list[1]+" already exists in "+parent_dir+'/'+current_folder)
                return
        elif list[0] == EXTENSION:
            if list[1] in self.extensions:
                print_err("ERROR: extension "+ list[1]+" already exists in folder: "+self.extensions[list[1]])
                return
            else:#TODO: else not necessary
                temp_dictionary[parent_dir+"/"+current_folder].append([EXTENSION, list[1]])
                self.extensions[list[1]] = os.path.join(self.path_to_root,os_dir)
        elif list[0] == REGULAR_EXPRESSION:
            if list[1] in self.regex:
                print_err("ERROR: regex "+ list[1]+" already exists in folder: "+self.regex[list[1]])
                return
            else:
                temp_dictionary[parent_dir+"/"+current_folder].append([REGULAR_EXPRESSION, list[1]])
                self.regex[list[1]] = os.path.join(self.path_to_root,os_dir)
        else:
            print_err("ERROR: unknown type"+ list[0])
            return
        try:
            if list[0] == FOLDER:
                os.makedirs(os.path.join(os_dir,list[1]))
            self.write_json(self.json_file, temp_dictionary)
            self.config = temp_dictionary
        except Exception as e:
            print_err("ERROR: could not append changes reverting..." + str(e))
    
    def append_rules_to_folder(self, parent_dir, current_folder, list_of_lists):
        for list in list_of_lists:
            self.append_to_folder(parent_dir, current_folder, list)
    def touch_folder(self, parent_dir, current_folder, list_of_lists):
        #check if folder exists in the dictionary
        if parent_dir+'/'+current_folder not in self.config:
            self.add_folder(parent_dir, current_folder, list_of_lists)
        else:
            self.append_rules_to_folder(parent_dir, current_folder, list_of_lists)
    def remove_folder_rules(self, parent_dir, current_folder, list_of_lists):
        #this doesn't remove folders from the dictionary
        #check if folder exists in the dictionary
        os_dir = os.path.join(self.path_to_root,*parent_dir.split('/'),current_folder)

        if os.path.isdir(os.path.join(self.path_to_root,*parent_dir.split('/'), current_folder)) is not True:
            print_err("ERROR: "+ os.path.join(self.path_to_root,*parent_dir.split('/'), current_folder)+" is not a folder in the os")
            return

        if parent_dir+'/'+current_folder not in self.config:
            print_err("ERROR: "+ parent_dir+'/'+current_folder + " doesn't exist in dictionary")
            return
        
        temp_dictionary = copy.deepcopy(self.config)

        for value in list_of_lists:
            if value[0] == FOLDER:
                print("FOLDER rule detected if you want to remove a folder (send it to trash) use remove_folder")
                print("skipping...")
                continue
            elif value[0] == EXTENSION:
                if value[1] not in self.extensions:
                    print_err(f"ERROR: extension {value[1]} doesnt exist in extension list")
                    return
                else:
                    try:
                        temp_dictionary[parent_dir+"/"+current_folder].remove([EXTENSION, value[1]])
                    except ValueError:
                        print_err(f"ERROR: could not remove extension {value[1]} (doesn't exist in folder)")
                        return
                    del self.extensions[value[1]]
            elif value[0] == REGULAR_EXPRESSION:
                if value[1] not in self.regex:
                    print_err(f"ERROR: regex {value[1]} doesnt exist in regex list")
                    return
                else:
                    try:
                        temp_dictionary[parent_dir+"/"+current_folder].remove([REGULAR_EXPRESSION, value[1]])
                    except ValueError:
                        print_err(f"ERROR: could not remove regex {value[1]} (doesn't exist in folder)")
                        return
                    del self.regex[value[1]]
        try:
            self.write_json(self.json_file, temp_dictionary)
            self.config = temp_dictionary
        except Exception as e:
            print_err("ERROR write to json failed: could not remove changes, reverting..." + str(e))
            self.dfs(self.root) # entensions and regex dictionaries might have changed but write failed (regenerate the dictionaries)





