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
from TreeOp import *
EXTENSION = "EXTENSION"
FOLDER = "FOLDER"
REGULAR_EXPRESSION = "REGULAR_EXPRESSION"


if __name__ == '__main__':
  
    #create a file_op object for each tree
    #######folder_op = FolderOp("D:\TreeTest", 'config_output.json', '/Root')#changed this from root to /root

    #DONE: run initial dfs could be done inside folder_op
    #folder_op.dfs("Root")

    treeOp = TreeOp()
    treeOp.create_new_tree("D:\TreeTest", "Root") #also creates root folders
    treeOp.create_new_tree("D:\TreeTest", "Hello") #also creates root folders
    folder_op = treeOp.select_tree("D:\TreeTest", "Hello") #selects the tree
    folder_op.add_folder("/Hello", "Yo", [[FOLDER,"YO2"],[FOLDER,"YO3"],[EXTENSION,".yo"]])
    folder_op.append_rules_to_folder("/Hello", "Yo", [[EXTENSION,".yoyoa"],[REGULAR_EXPRESSION,"*.a*"]])
    folder_op = treeOp.select_tree("D:\TreeTest", "Root") #selects a new tree
    folder_op.add_folder("/Root", "Yo", [[FOLDER,"YO2inRoot"],[FOLDER,"YO3inRoot"],[EXTENSION,".yoinroot"]])
    ###########print(folder_op.extensions)
    #TODO separete program in the windows train that runs this one in a terminal
   
    #do an operation on the config file
    #folder_op.move_folder("Root/Documents", "PDFss", "Root/Documents", "PDF")
    #folder_op.move_folder("Root/Documents", "PDF", "Root/Documents/WORD", "PDFS")
    #folder_op.append_to_folder("Root/Documents/PDF", "PDFssss",[FOLDER, "hello"])
    #folder_op.append_to_folder("Root/Documents/PDF", "PDFssss",[EXTENSION, ".pdfnew"])
    #folder_op.append_to_folder("Root/Documents/PDF", "PDFssss",[REGULAR_EXPRESSION, ".*"])
    #folder_op.remove_folder("Root/Documents/PDF", "PDFssss")
    #folder_op.add_folder("","Root",[FOLDER, "inRoott"])
    #folder_op.remove_folder("","Root")
    #folder_op.add_folder("/Root","Documents",[[FOLDER, "inDocuments"]])
    #folder_op.append_rules_to_folder("/Root","inRoott",[[FOLDER, "hellop"]])
    ##folder_op.move_folder("/Root/Documents/WORD", "PDFS", "/Root/Documents", "PDF")
    ####folder_op.move_folder("", "Root", "", "Root_new") doesnt work
    ###folder_op.append_rules_to_folder("/Root/Documents", "PDF",[[FOLDER, "hello"],[EXTENSION, ".pdfnew"],[REGULAR_EXPRESSION, ".*"]])
    ###folder_op.remove_folder("", "Root")
    ###folder_op.add_folder("", "Root2", [[FOLDER,"helloooo"]])
    ##folder_op.append_to_folder("Root/Documents", "hello2",[FOLDER, "docs"])
    ##folder_op.remove_folder("Root/Documents", "hello2")
    #folder_op.remove_folder("/Root/Documents","hello")
    #initialize a scanner pass folder_op DONE: pass folder_op to scanner
    #########scan = Scan(folder_op)

    #select a directory to scan
    #scan.scan_directory("test")

    #save the config file DONE: do this inside folder_op
    #folder_op.save_config('config_output.json')
    '''
    print()
    print()
    print(folder_op.config)
    print()
    print(f"THE EXTENSIONS: {folder_op.extensions}")
    print()
    print(folder_op.regex)'''

    #move_folder(config, "Root", "Documents", "Root/Images", "Documents")
    #move_folder(config, "Root", "Documents", "Root/Images", "Doc")
    #move_folder(config, "Root/Documents", "WORD", "Root/Documents", "WORUDO")
    ##move_folder(config, "Root", "Images", "Root/Documents/PDF", "Documento")
    ##remove_folder(config, "Root/Documents/PDF", "Documento")
    #move_folder(config, "Root/Documents", "PDF", "Root/Documents/WORD", "PDFS")

    #folder_op.move_folder(config, "Root/Documents", "PDF_NEW", "Root/Documents/WORD", "PDFINWORD")
    #folder_op.move_folder(config, "Root/Documents/WORD", "PDFINWORD", "Root/Documents", "PDF_NEW2")


    #folder_op.move_folder(config, "Root/Documents", "WORD", "Root/Documents/PDF_NEW2", "WORUDO")
    #folder_op.move_folder(config, "Root/Documents/PDF_NEW2", "WORUDO", "Root/Documents/PDF_NEW2", "WORDOINPDF")


    #config = folder_op.move_folder(config, "Root/Documents/WORD", "PDFINWORD", "Root/Documents", "PDFINDOC")


    #config = folder_op.move_folder(config, "Root/Documents", "PDFINDOC", "Root/Documents/DOCX/IMGES", "PDFINIMG")

    #config = folder_op.move_folder(config, "Root/Documents", "DOCX", "Root/Documents/WORD", "NEWDOCX")
    
    #config = folder_op.move_folder("Root/Documents/WORD/NEWDOCX", "IMGES", "Root/Documents", "IMAGESNEWFROMDOCX")
    #folder_op.add_folder("Root","FLDR",[[FOLDER,"NEW_FOLDER_2"],[EXTENSION,".lel"],[EXTENSION, ".hello"]]) #remove and add again
    #folder_op.add_folder("Root/Documents/IMAGESNEWFROMDOCX","FLDRNEW",[[FOLDER,"NEW_FOLDER_200"],[EXTENSION,".leel"],[EXTENSION, ".heello"]])
    #folder_op.remove_folder("Root/Documents/IMAGESNEWFROMDOCX","FLDRNEW")
    #folder_op.remove_folder("Root/Documents/IMAGESNEWFROMDOCX","FLDRNEW")
   ##### folder_op.remove_folder("Root/Documents/WORD","NEWDOCX")
   ##### folder_op.add_folder("Root/Documents/WORD","NEWDOCX",[[FOLDER,"A_FOLDER"],[EXTENSION,".boing"],[EXTENSION, ".sup"]])

    #folder_op.remove_folder("Root/Documents/WORD/NEWDOCX","A_FOLDER")
    #folder_op.add_folder("Root/Documents/WORD/NEWDOCX","A_FOLDER",[[FOLDER,"THIS"],[EXTENSION,".boing2"],[EXTENSION, ".sup2"]])
    
    #folder_op.move_folder("Root/Documents","PDF","Root/Documents/WORD","newpdf")
   # folder_op.move_folder("Root/Documents/WORD","PDFS","Root/Documents","PDF")

    #config = folder_op.move_folder(config, "Root/Documents/DOCX", "IMGES/PDFINIMG", "Root/Documents", "PDFIINIMG")
    
    #config = folder_op.move_folder(config, "Root", "Images", "Root/Documents/DOCX", "IMGES")
    #######folder_op.move_folder(config, "Root/Documents/WORD", "PDFS", "Root/Documents", "PDF_NEW")
    #######folder_op.move_folder(config, "Root/Documents/WORD", "PDFS", "Root/Documents", "PDF_NEW")
    #######folder_op.move_folder(config, "Root/Documents", "PDF_NEW", "Root/Documents", "PDF")
    #move_folder(config, "Root", "Documents", "Root/Documents", "PDF")
    #folder_op.add_folder("Root/Documents","PNGSNEW",[[EXTENSION,".png"],[EXTENSION,".jpg"]])
    #folder_op.add_folder("Root/Documents","YOYO",[[EXTENSION,"YOYO2"],[FOLDER,"YOYO2"],[EXTENSION,".damn"]])
    ###remove_folder(config,"Root","NEW_FOLDER")
    ####folder_op.remove_folder("Root","Documents")
    #scan_directory("test")
    #Unhide this

