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



if __name__ == '__main__':
  
    
    folder_op = FolderOp("", 'config_output.json')
    folder_op.dfs("Root")


    print(folder_op.extensions)

    #move_folder(config, "Root", "Documents", "Root/Images", "Documents")
    #move_folder(config, "Root", "Documents", "Root/Images", "Doc")
    #move_folder(config, "Root/Documents", "WORD", "Root/Documents", "WORUDO")
    ##move_folder(config, "Root", "Images", "Root/Documents/PDF", "Documento")
    ##remove_folder(config, "Root/Documents/PDF", "Documento")
    #move_folder(config, "Root/Documents", "PDF", "Root/Documents/WORD", "PDFS")

    folder_op.move_folder("Root/Documents/WORD", "PDFS", "Root/Documents", "PDF")

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
    
    #folder_op.move_folder("Root/Documents/WORD/NEWDOCX","YO_THIS_IS_NEW","Root/Documents/WORD/NEWDOCX","YO_THIS_IS_NEW2")

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

    scan = Scan(folder_op.extensions, folder_op.regex)
    scan.scan_directory("test")
    folder_op.save_config('config_output.json')

    print()
    print()
    print(folder_op.config)
    print()
    print(f"THE EXTENSIONS: {folder_op.extensions}")
    print()
    print(folder_op.regex)

