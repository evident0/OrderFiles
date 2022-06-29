import os
import re
import shutil
# DONE TODO add recursive option to scan folder
# DONE TODO figure out if the tracked folder is the same as destination and if so, DONT COPY/RENAME 
# (what it does now is rename the file incrementally name->name(1)->name(2)... if it already exists)
# TODO add multithreading so that main can have a progress bar

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

    # scan a directory and check the extension of each file
    # this is recursive
    def scan_directory(self,directory):
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
                    continue
                #if no regular expressions matched, move file based on it's extension
                #check if file extension is in the list of extensions
                #check if source and destination are the same and if so, don't move/copy , continue to next file
                if root == self.extensions['.'+file.split('.')[-1]]:
                    print("[EXTENSIONS] Found file with the same source and destination: "+file+" skipping...")
                    continue
                if "."+file.split('.')[-1] in self.extensions:
                    #move file to the folder
                    new_file_name = self.handle_file_collision(self.extensions['.'+file.split('.')[-1]], file)

                    #shutil allows to move files between different disk drives
                    shutil.move(os.path.join(root,file), os.path.join(self.extensions['.'+file.split('.')[-1]], new_file_name))
                    ##os.rename(os.path.join(root,file), os.path.join(self.extensions['.'+file.split('.')[-1]],new_file_name))
    
    # non recursive scan
    def scan_directory_no_recursion(self,directory):
        for file in os.listdir(directory):
            #check if source and destination are the same and if so, don't move/copy , continue to next file
            #check if file is a directory and if so, skip it
            if os.path.isdir(os.path.join(directory,file)):
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
                continue
            #if no regular expressions matched, move file based on it's extension
            #check if file extension is in the list of extensions
            if directory == self.extensions['.'+file.split('.')[-1]]:
                print("[EXTENSIONS] Found file with the same source and destination: "+file+" skipping...")
                continue
            if "."+file.split('.')[-1] in self.extensions:
                #move file to the folder
                new_file_name = self.handle_file_collision(self.extensions['.'+file.split('.')[-1]], file)
                #shutil allows to move files between different disk drives
                shutil.move(os.path.join(directory,file), os.path.join(self.extensions['.'+file.split('.')[-1]], new_file_name))
                
