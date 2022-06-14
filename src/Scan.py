import os
import re
import shutil

class Scan:
    def __init__(self, extensions, regex):
        self.extensions = extensions
        self.regex = regex
        
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

    #scan a directory and check the extension of each file
    def scan_directory(self,directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                cont_loop = False
                for reg in self.regex:
                    if re.search(reg, file): #TODO: add r in front of string ex. r"" to support \ inside the string 
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
                if "."+file.split('.')[-1] in self.extensions:
                    #move file to the folder
                    new_file_name = self.handle_file_collision(self.extensions['.'+file.split('.')[-1]], file)

                    #This allows to move files between different disk drives
                    shutil.move(os.path.join(root,file), os.path.join(self.extensions['.'+file.split('.')[-1]], new_file_name))
                    ##os.rename(os.path.join(root,file), os.path.join(self.extensions['.'+file.split('.')[-1]],new_file_name))