from genericpath import isdir
import json
import os
from turtle import clear
#import regular expressions
import re
#enum with 3 states
import shutil

from colorama import Fore #for color

from Scan import *
from FolderOp import *

EXTENSION = "EXTENSION"
FOLDER = "FOLDER"
REGULAR_EXPRESSION = "REGULAR_EXPRESSION"


extensions = {}
regex = {}
config = {}



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
  
    config = read_json('config_output.json')
   
    folder_op = FolderOp(regex, config, extensions, EXTENSION, FOLDER, REGULAR_EXPRESSION)
    folder_op.dfs(config,"Root")

    print(extensions)

    #move_folder(config, "Root", "Documents", "Root/Images", "Documents")
    #move_folder(config, "Root", "Documents", "Root/Images", "Doc")
    #move_folder(config, "Root/Documents", "WORD", "Root/Documents", "WORUDO")
    ##move_folder(config, "Root", "Images", "Root/Documents/PDF", "Documento")
    ##remove_folder(config, "Root/Documents/PDF", "Documento")
    #move_folder(config, "Root/Documents", "PDF", "Root/Documents/WORD", "PDFS")
    folder_op.move_folder(config, "Root/Documents", "PDF", "Root/Documents/WORD", "PDFS")
    folder_op.move_folder(config, "Root/Documents/WORD", "PDFS", "Root/Documents", "PDF_NEW")
    folder_op.move_folder(config, "Root/Documents", "PDF_NEW", "Root/Documents", "PDF")
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
    #scan_directory("test")
    scan = Scan(extensions, regex)
    scan.scan_directory("test")
    write_json('config_output.json', config)
    print()
    print()
    print(config)
    print()
    print(extensions)
    print()
    print(regex)