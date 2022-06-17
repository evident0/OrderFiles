import os
import shutil
import copy
import send2trash
import json
#from Order import extensions, regex, config, EXTENSION, FOLDER, REGULAR_EXPRESSION
#import Order
#TODO: update entensions and regex with only one dfs (ex. dfs_move)
class FolderOp:
    #class initilize with regex, config, EXTENSION, FOLDER, REGULAR_EXPRESSION
    def __init__(self,path_to_root,json_file_to_read,root):# path_to_root, regex, config, extensions, EXTENSION, FOLDER, REGULAR_EXPRESSION):
        
        self.EXTENSION = "EXTENSION"
        self.FOLDER = "FOLDER"
        self.REGULAR_EXPRESSION = "REGULAR_EXPRESSION"

        self.path_to_root = path_to_root
        self.root = root
        self.json_file = json_file_to_read
        
        self.config = self.read_json(json_file_to_read)
        self.regex = {}
        self.extensions = {}

        self.dfs(self.root)

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
        self.dfs_helper(path, path) # path differs from operating system to operating system

    def dfs_helper(self, os_path, json_path): #starts with, path differs from operating system to operating system
    
        for value in self.config[json_path]: #  dict value is a list of lists [value[0]:type, value[1]:name]
            if value[0] == self.FOLDER:
                #create a file if it doesn't exist already
                if not os.path.exists(os.path.join(self.path_to_root,os_path,value[1])):
                    os.makedirs(os.path.join(self.path_to_root, os_path, value[1]))   
                self.dfs_helper(os.path.join(os_path, value[1]), json_path+'/'+value[1])
            elif value[0] == self.EXTENSION: # regex or extension
                self.extensions[value[1]] = os.path.join(self.path_to_root,os_path) # the path to the folder
            elif value[0] == self.REGULAR_EXPRESSION:
                self.regex[value[1]] = os.path.join(self.path_to_root,os_path) # this will be traversed first to match any regex
            else:
                print("Error: unknown type")
    #TODO: deprecated method
    def rename_dfs(self,dictionary, current_name, new_name):
        dictionary[new_name] = dictionary.pop(current_name)

        for value in dictionary[new_name]:
            if value[0] == self.FOLDER:
                self.rename_dfs(dictionary, current_name+'/'+value[1], new_name+'/'+value[1])

    #TODO: deprecated method
    def rename_folder(self,dictionary, parent_dir, current_name, new_name):
    
        if(parent_dir is not None):
            for value in dictionary[parent_dir]:
                if value[0] == self.FOLDER and value[1] == current_name:
                    value[1] = new_name
            self.rename_dfs(dictionary, parent_dir+"/"+current_name, parent_dir+"/"+new_name);
        else: # this is the root
            self.rename_dfs(dictionary, current_name, new_name);
        
        first_pair = next(iter((dictionary.items())))
        
        #first pair is the root
        self.dfs(self.config,first_pair[0])

    def colored(self,r, g, b, text):
        return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

    def move_folder(self, parent_dir, current_folder, new_parent_directory, new_folder):

        #copy the dictionary to a new tempory dictionary
        temp_dictionary = copy.deepcopy(self.config)

        #check if it is a folder
        os_parent_dir = os.path.join(self.path_to_root,*parent_dir.split('/'),current_folder)
        os_new_parent_dir = os.path.join(self.path_to_root,*new_parent_directory.split('/'),new_folder)

        print(os_parent_dir)
        #check if the folders exist
        if os.path.isdir(os_parent_dir) is not True:
            print("ERROR: "+ os_parent_dir+" is not a folder in the os")
            return
        #check if new directory is a subdirectory of the parent directory
        #print("This is the thing1 "+os_parent_dir)
        #print("This is the thing2 "+os_new_parent_dir)
        #print("This is the thing3 "+os.path.commonpath([os_parent_dir, os_new_parent_dir]))
        #changed from os.path.commonprefix that didn't work properly
        if os.path.commonpath([os_parent_dir, os_new_parent_dir]) == os_parent_dir:      
            print("ERROR: "+ os_new_parent_dir + " is a subdirectory of " + os_parent_dir)
            return
        #check if the folder exists in dictionary
        if parent_dir+'/'+current_folder not in self.config:
            print("ERROR: "+ parent_dir+'/'+current_folder +" does not exist in dictionary")
            return
        #check if the new parent directory exists in dictionary
        #if new_parent_directory+'/'+new_folder not in dictionary:
        #    print("ERROR: "+ new_parent_directory+'/'+new_folder +" does not exist in dictionary")
        #    return
        # move a folder in the operating system
        #UNHIDE THIS
        ####os.rename(os_parent_dir,os_new_parent_dir)#os.path.join(parent_dir,current_folder), os.path.join(new_parent_directory,new_folder))
        
        temp_dictionary[parent_dir].remove([self.FOLDER,current_folder])

        temp_dictionary[new_parent_directory].append([self.FOLDER, new_folder]) # add new folder to new parent directory
    
        self.move_dfs(temp_dictionary, parent_dir+"/"+current_folder, new_parent_directory+"/"+new_folder);

        try:
            os.rename(os_parent_dir,os_new_parent_dir)
            self.write_json(self.json_file, temp_dictionary)
            self.config = temp_dictionary
        except:
            print("OS MOVE FAILED REVERTING CHANGES")
            self.dfs(self.root)


    def move_dfs(self,dictionary, current_name, new_name):
        dictionary[new_name]=dictionary.pop(current_name) # append the poped dictionary to the new name

        #compatiblity with the operating system
        os_path = os.path.join(self.path_to_root,*new_name.split('/'))

        for value in dictionary[new_name]:
            if value[0] == self.FOLDER:
                self.move_dfs(dictionary, current_name+'/'+value[1], new_name+'/'+value[1])
                #dictionary[new_name+"/"+value[1]] = dictionary.pop(current_name+"/"+value[1])
            elif value[0] == self.EXTENSION: # regex or extension
                self.extensions[value[1]] = os.path.join(self.path_to_root,os_path) # the path to the folder
            elif value[0] == self.REGULAR_EXPRESSION:
                self.regex[value[1]] = os.path.join(self.path_to_root,os_path) # this will be traversed first to match any regex
            else:
                print("Error: unknown type")

    def remove_folder(self, parent_dir, current_folder):
        #check if folder is in os and return if not
        os_path = os.path.join(self.path_to_root,*parent_dir.split('/'),current_folder)

        if os.path.isdir(os_path) is not True:
            print("ERROR: "+ os_path+" is not a folder in the os")
            return self.config

        #check if it does not exist and return if it does not
        if parent_dir+'/'+current_folder not in self.config:
            print("ERROR: "+ parent_dir+'/'+current_folder +"doesn't exist in dictionary")
            return
        #remove folder from operating system
        ##os.rmdir(os.path.join(parent_dir,current_folder))
        #shutil.rmtree(os_path)
       

        temp_dictionary = copy.deepcopy(self.config)

        temp_dictionary[parent_dir].remove([self.FOLDER,current_folder])
        self.remove_dfs(temp_dictionary, parent_dir+"/"+current_folder)

        try:
            send2trash.send2trash(os_path)
            self.write_json(self.json_file, temp_dictionary)
            self.config = temp_dictionary    
        except:
            print("OS REMOVE FAILED REVERTING CHANGES")
            self.dfs(self.root)

    def remove_dfs(self,dictionary, current_name):
    
        for value in dictionary[current_name]:
            if value[0] == self.FOLDER:
                self.remove_dfs(dictionary, current_name+'/'+value[1])
            elif value[0] == self.EXTENSION: # regex or extension
                self.extensions.pop(value[1]) # remove the entry from the extensions
            elif value[0] == self.REGULAR_EXPRESSION:
                self.regex.pop(value[1]) # remove the entry in regex
        
        dictionary.pop(current_name)

    def add_folder(self, parent_dir, current_folder, list_of_lists):
        #check if parent directory exists in os and return if it does not
        if os.path.isdir(os.path.join(self.path_to_root,*parent_dir.split('/'))) is not True:
            print("ERROR: "+ os.path.join(self.path_to_root,*parent_dir.split('/'))+" is not a folder in the os")
            return

        #check if folder exists in dictionary and return if it does
        if parent_dir+'/'+current_folder in self.config:
            print("ERROR: "+ parent_dir+'/'+current_folder + " already exists")
            return

        temp_dictionary = copy.deepcopy(self.config)

        #create folder in operating system
        os_dir = os.path.join(self.path_to_root,*parent_dir.split('/'),current_folder)

        #add the new folder to the parent directory for reference
        temp_dictionary[parent_dir].append([self.FOLDER, current_folder])

        #create the empty folder in the dictionary
        temp_dictionary[parent_dir+"/"+current_folder] = []

        #for each item in the list of lists, add it to the dictionary
        for value in list_of_lists:
            if value[0] == self.FOLDER:
                #add the folder under the new folder
                temp_dictionary[parent_dir+"/"+current_folder].append([self.FOLDER, value[1]])
                #create the empty folder entry for the dictionary
                temp_dictionary[parent_dir+"/"+current_folder+"/"+value[1]] = []               
            elif value[0] == self.EXTENSION:
                #add the extension to the dictionary list of the new folder
                temp_dictionary[parent_dir+"/"+current_folder].append([self.EXTENSION, value[1]])
                self.extensions[value[1]] = os.path.join(self.path_to_root,os_dir)
            elif value[0] == self.REGULAR_EXPRESSION:
                #add the regex to the dictionary list of the new folder
                temp_dictionary[parent_dir+"/"+current_folder].append([self.REGULAR_EXPRESSION, value[1]])
                self.regex[value[1]] = os.path.join(self.path_to_root,os_dir)
            else:
                print("ERROR: unknown type")
        
        try:
            os.makedirs(os_dir)
            #create the folers if the dictionary updates successfully
            for value in list_of_lists:
                if value[0] == self.FOLDER:
                    os.makedirs(os.path.join(os_dir,value[1]))

            self.write_json(self.json_file, temp_dictionary)
            self.config = temp_dictionary
        except:
            print("ERROR: could not create folder reverting changes...")
            #TODO: add a revert function and use the root the user specified in main
            self.dfs(self.root)

