import os
import re
import shutil
from tqdm import tqdm

# TODO add option to scan only one folder and not all of them ex. order <scanner-name|number|folder_name>

class Scan:
    def __init__(self, folder_op):     
        self.extensions = folder_op.extensions
        self.regex = folder_op.regex

    def handle_file_collision(self,root,file):
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
    def preprocessing(self,directory):
        filescount = 0
        for root, dirs, files in os.walk(directory):
            filescount += len(files)
        return filescount
    # scan a directory and check the extension of each file
    # this is recursive
    def scan_directory(self,directory):
        #get the number of files in the directory
        filescount = self.preprocessing(directory)

        with tqdm(total=filescount) as pbar:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    cont_loop = False
                    for reg in self.regex:
                        if re.search(reg, file):
                            # check if source and destination are the same and if so, don't move/copy , continue to next file
                            if root == self.regex[reg]:
                                print("[Regex] Found file with the same source and destination: "+file+" skipping...")
                                cont_loop = True
                                break
                            #move file to the folder
                            new_file_name = self.handle_file_collision(self.regex[reg],file)

                            #This allows to move files between different disk drives
                            shutil.move(os.path.join(root,file), os.path.join(self.regex[reg],new_file_name))
                            #os.rename(os.path.join(root,file), os.path.join(self.regex[reg],new_file_name))
                        
                            cont_loop = True
                            break
                    if cont_loop:
                        pbar.update(1)
                        continue
                    #if no regular expressions matched, move file based on it's extension
                    #check if file extension is in the list of extensions
                    if "."+file.split('.')[-1] in self.extensions:
                        #check if source and destination are the same and if so, don't move/copy , continue to next file
                        if root == self.extensions['.'+file.split('.')[-1]]:
                            print("[EXTENSIONS] Found file with the same source and destination: "+file+" skipping...")
                            pbar.update(1)
                            continue
                        #move file to the folder
                        new_file_name = self.handle_file_collision(self.extensions['.'+file.split('.')[-1]], file)

                        #shutil allows to move files between different disk drives
                        shutil.move(os.path.join(root,file), os.path.join(self.extensions['.'+file.split('.')[-1]], new_file_name))
                    pbar.update(1)
    
    # non recursive scan
    def scan_directory_no_recursion(self,directory):
        #get the number of files in the directory
        filescount = self.preprocessing(directory)

        with tqdm(total=filescount) as pbar:
            for file in os.listdir(directory):
                #check if source and destination are the same and if so, don't move/copy , continue to next file
                #check if file is a directory and if so, skip it
                if os.path.isdir(os.path.join(directory,file)):
                    pbar.update(1)
                    continue
                root = os.path.join(directory,file)
                cont_loop = False
                for reg in self.regex:
                    if re.search(reg, file):
                        print(root)
                        print(self.regex[reg])
                        if directory == self.regex[reg]:
                            print("[Regex] Found file with the same source and destination: "+file+" skipping...")
                            cont_loop = True
                            break
                        #move file to the folder
                        new_file_name = self.handle_file_collision(self.regex[reg],file)
                        shutil.move(os.path.join(directory,file), os.path.join(self.regex[reg],new_file_name))
                        cont_loop = True
                        break
                if cont_loop:
                    pbar.update(1)
                    continue
                #if no regular expressions matched, move file based on it's extension
                
            
                if "."+file.split('.')[-1] in self.extensions:
                    #check if file extension is in the list of extensions
                    if directory == self.extensions['.'+file.split('.')[-1]]:
                        print("[EXTENSIONS] Found file with the same source and destination: "+file+" skipping...")
                        pbar.update(1)
                        continue
                    #move file to the folder
                    new_file_name = self.handle_file_collision(self.extensions['.'+file.split('.')[-1]], file)
                    #shutil allows to move files between different disk drives
                    shutil.move(os.path.join(directory,file), os.path.join(self.extensions['.'+file.split('.')[-1]], new_file_name))
                pbar.update(1)
                    
