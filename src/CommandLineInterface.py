from pathlib import Path
from posixpath import basename
import ast #literal_eval of input argument for touching folders
from colorama import *
from FolderOp import *
from TreeOp import *
EXTENSION = "EXTENSION"
FOLDER = "FOLDER"
REGULAR_EXPRESSION = "REGULAR_EXPRESSION"

from pathlib import Path
# prefix components:
space =  '    '
branch = '│   '
# pointers:
tee =    '├── '
last =   '└── '
class CommandLineInterface:
    def __init__(self) -> None:
        self.folder_op = None #TODO multiple of these somewhere else not in this class
        self.tree_op = TreeOp() #initialize tree_op
        self.tree_selected = ""
        self.dict = {
            "/Root": [
                [
                    "FOLDER",
                    "Images"
                ],
                [
                    "FOLDER",
                    "Documents"
                ],
                [
                    "FOLDER",
                    "inRoot"
                ]
            ],
            "/Root/Images": [
                [
                    "EXTENSION",
                    ".png"
                ],
                [
                    "EXTENSION",
                    ".tiff"
                ],
                [
                    "EXTENSION",
                    ".jpg"
                ],
                [
                    "REGULAR_EXPRESSION",
                    "^The.*Spain"
                ]
            ],
            "/Root/Documents": [
                [
                    "FOLDER",
                    "DOCX"
                ],
                [
                    "FOLDER",
                    "WORD"
                ],
                [
                    "FOLDER",
                    "PDF"
                ]
            ],
            "/Root/Documents/DOCX": [
                [
                    "EXTENSION",
                    ".docx"
                ]
            ],
            "/Root/Documents/WORD": [
                [
                    "EXTENSION",
                    ".doc"
                ]
            ],
            "/Root/inRoot": [],
            "/Root/Documents/PDF": [
                [
                    "EXTENSION",
                    ".pdf"
                ],
                [
                    "EXTENSION",
                    ".adobe"
                ],
                [
                    "REGULAR_EXPRESSION",
                    "([a-z]*) are ([a-z]*?) .*"
                ],
                [
                    "FOLDER",
                    "hello"
                ],
                [
                    "EXTENSION",
                    ".pdfnew"
                ],
                [
                    "REGULAR_EXPRESSION",
                    ".*"
                ]
            ],
            "/Root/Documents/PDF/hello": []
        }
    def select_tree(self):

        a_list = self.tree_op.get_tree_list() #DONE
        # a selection screen for the a_list
        
        number = 0
        for item in a_list:
            print(f"{number}. {item}")
            number += 1
        print("select one tree of the above [1,2,3,...]")
        sel = input("> ")
        #check the bounds of the selection
        if int(sel) > len(a_list):
            print("invalid selection")
            return
        self.folder_op = self.tree_op.select_tree(os.path.dirname(a_list[int(sel)]),os.path.basename(a_list[int(sel)]))
        print(f"the root: {self.folder_op.root}")
        return a_list[int(sel)]


    def tree_dict(self,dictionary, path, prefix: str=''):
        """A recursive generator, given a directory Path object
        will yield a visual tree structure line by line
        with each line prefixed by the same characters
        """
        contents = dictionary[path]

        pointers = [tee] * (len(contents) - 1) + [last]
        for pointer, value in zip(pointers, contents):
            if value[0] == EXTENSION:
                yield  prefix + pointer + Fore.RED + value[1] + Style.RESET_ALL
            elif value[0] == REGULAR_EXPRESSION:
                yield  prefix + pointer + Fore.GREEN + value[1] + Style.RESET_ALL 
            elif value[0] == FOLDER:
                yield  prefix + pointer + Fore.YELLOW + value[1] + Style.RESET_ALL
            if value[0] == FOLDER:
                extension = branch if pointer == tee else space
                yield from self.tree_dict(dictionary, path + '/' + value[1], prefix=prefix+extension)

    def dispay_help(self):
        print(Fore.RED + 'Help Menu' + Style.RESET_ALL)
        print('--------------------------General Commands:--------------------------')
        print('create </folder_name> create a tree structure with root </folder_name>')
        print('select - select a tree')
        print('-----------------------Tree specific commands:-----------------------')
        print('--------------------(need to select a tree first)--------------------')
        print('tree - display the tree')
        print('scanner <os_path> - create a scanner for this folder. It will be used for ordering the files in the currently selected tree')
        print('order - order the files from the scanner folders')
        print('mk <folder_name> <[...,[FOLDER|EXTENSION|REGULAR_EXPRESSION,<name>],...]>, create folder with list of rules')
        print('rm <folder_name>, recursively send directory to trash')
        print('mv <folder_name> <new_folder_name>, move folder to new location')
        print('up <folder_name> <[...,[FOLDER|EXTENSION|REGULAR_EXPRESSION,<name>],...]>, append new rules for a folder')
        print('scan <folder_name>, add a folder to scan and move the files')
        
    def print_tree(self):
        if self.folder_op is None:
            print("IN_RED tree selection failed")
            return
        for line in command_line.tree_dict(self.folder_op.config, self.folder_op.root):#TODO self.folder_op
            print(line)
    
    def tree_operations(self, command, arguments_size , arguments):
       
        if command == 'mk':
            if arguments_size < 2:
                print('mk <folder_name> <[...,[FOLDER|EXTENSION|REGULAR_EXPRESSION,<name>],...]>, create folder with list of rules')
                return False
            else:
                #do the mk command
                try:
                    parent_path = arguments[0].rsplit('/',1)[0]
                    folder_name = arguments[0].rsplit('/',1)[1]
                except IndexError:
                    print('<folder_name> is a relative path ex. /Root/Documents/PDF')
                    return False
                
                try:
                    rule_list = ast.literal_eval(arguments[1])
                    #check if rule_list is a list of lists
                    if not isinstance(rule_list, list) or not (isinstance(el, list) for el in rule_list):
                        print('<ruless> is not a valid list ex. [[FOLDER,<name>],[EXTENSION,<name>],[REGULAR_EXPRESSION,<name>]]')
                        return False
                except SyntaxError:
                    print('<rules> is not a valid list ex. [[FOLDER,<name>],[EXTENSION,<name>],[REGULAR_EXPRESSION,<name>]]')
                    return False
                

                #self.folder_op.make_folder(arguments[0],arguments[1:])
                print("making...")
                self.folder_op.touch_folder(parent_path, folder_name, rule_list)
                self.print_tree()
                return True
        if command == 'rr':
            if arguments_size < 2:
                print('rr <folder_name> <[...,[EXTENSION|REGULAR_EXPRESSION,<name>],...]>, remove rules from folder (use rm for FOLDERS)')
                return False
            else:
                #do the rl command
                try:
                    parent_path = arguments[0].rsplit('/',1)[0]
                    folder_name = arguments[0].rsplit('/',1)[1]
                except IndexError:
                    print('<folder_name> is a relative path ex. /Root/Documents/PDF')
                    return False
                
                try:
                    rule_list = ast.literal_eval(arguments[1])
                    #check if rule_list is a list of lists
                    if not isinstance(rule_list, list) or not (isinstance(el, list) for el in rule_list):
                        print('<ruless> is not a valid list ex. [[FOLDER,<name>],[EXTENSION,<name>],[REGULAR_EXPRESSION,<name>]]')
                        return False
                except SyntaxError:
                    print('<rules> is not a valid list ex. [[FOLDER,<name>],[EXTENSION,<name>],[REGULAR_EXPRESSION,<name>]]')
                    return False
                
                #self.folder_op.make_folder(arguments[0],arguments[1:])
                print("making...")
                self.folder_op.remove_folder_rules(parent_path, folder_name, rule_list)
                self.print_tree()
                return True
        elif command == 'rm':
            if arguments_size < 1:
                print('rm <folder_name>, recursively send directory to trash')
                return False
            else:
                try:
                    parent_path = arguments[0].rsplit('/',1)[0]
                    folder_name = arguments[0].rsplit('/',1)[1]
                except IndexError:
                    print('<folder_name> is a relative path ex. /Root/Documents/PDF')
                    return False
                #do the rm command
                self.folder_op.remove_folder(parent_path,folder_name)
                ##self.folder_op.remove_folder(parent_path, folder_name)
                print("removing...")
                self.print_tree()
                return True
        elif command == 'mv':
            if arguments_size < 2:
                print('mv <folder_name> <new_folder_name>, move folder to new location')
                return False
            else:
                try:
                    parent_path = arguments[0].rsplit('/',1)[0]
                    folder_name = arguments[0].rsplit('/',1)[1]
                    new_parent_path = arguments[1].rsplit('/',1)[0]
                    new_folder_name = arguments[1].rsplit('/',1)[1]
                except IndexError:
                    print('<folder_name> is a relative path ex. /Root/Documents/PDF')
                    return False
                #do the mv command

                print (f"ppath {parent_path},pname {folder_name}, nppath{new_parent_path}, npname{new_folder_name}")
                self.folder_op.move_folder(parent_path, folder_name, new_parent_path, new_folder_name)
                #self.folder_op.move_folder(parent_path, folder_name, new_parent_path, new_folder_name)
                print("moving...")
                self.print_tree()
                return True
        elif command == 'scanner':
            if arguments_size < 1:
                print('scanner <folder_path> | add a folder to scan and move the files')
                return False
            else:
                #do the up command
                self.tree_op.add_scanable_folder(self.folder_op, arguments[0])
                #self.folder_op.append_rules_to_folder(parent_path,folder_name,[["FOLDER","ininRoot"],["EXTENSION",".inroot"]])
                print("appending...")
                self.print_tree()
                return True
        elif command == 'order':
          
            #do the order command
            self.tree_op.order_files(self.folder_op)
            print("ordering...")

            return True
        elif command == 'tree':
            self.print_tree()
        else:
            print(f'Invalid command: {command} type help')
            return False

    def match_input(self,input):
        #split input into command and arguments
        command = input.split(' ')[0]
        arguments = input.split(' ')[1:]
        #check if command is valid
        parent_path = ""
        folder_name = ""
        new_parent_path = ""
        new_folder_name = ""
        '''if len(arguments) >= 1:
            try:
                parent_path = arguments[0].rsplit('/',1)[0]
                folder_name = arguments[0].rsplit('/',1)[1]
            except IndexError:
                print('<folder_name> is a relative path ex. /Root/Documents/PDF')
                return False

        if len(arguments) >= 2:
            try:
                new_parent_path = arguments[1].rsplit('/',1)[0]
                new_folder_name = arguments[1].rsplit('/',1)[1]
            except IndexError:
                print('<new_folder_name> is a relative path ex. /Root/Documents/PDF')
                return False'''

        
        if command == 'scan':#TODO change to add scan
            if len(arguments) < 1:
                print('scan <folder_name>, add a folder to scan and move the files')
                return False
            else:
                #do the scan command
                
                return True
        elif command == 'create':#TODO create the files in os for now just reads them
            if len(arguments) < 1:
                print('create <folder_path> create a tree structure with root </folder_name>')
                return False
            else:
                try:
                    dir_name = os.path.dirname(arguments[0])
                    base_name = os.path.basename(arguments[0])
                except IndexError:
                    print('<folder_name> is a relative path ex. /Root/Documents/PDF')
                    return False
                #IMPORTANT TODO: it doesn't need slash ("Root" not "/Root")
                self.tree_op.create_new_tree(dir_name, base_name) 
                #do the create command
                #self.folder_op = FolderOp("D:\TreeTest", 'config_output.json', arguments[0])#TODO ROOT has been selected from a previous menu
                print("creating...")
                self.print_tree()
                return True
        elif command == 'select':
            self.tree_selected = self.select_tree()
        elif self.tree_selected != "":#TODO change this
            is_ok = self.tree_operations(command, len(arguments), arguments)
            if not is_ok:
                return False
            return True
        else:
            print(f'Invalid command: {command} or no tree selected to perform operation type help')
            return False


if __name__ == '__main__':
   
    command_line = CommandLineInterface()
    while True:
       
        #print()
        #print('-h: Display help menu')
        #print(Fore.YELLOW+'C:/TreeTest'+Style.RESET_ALL+'> ', end='')#TODO get path_to_root
        usr_input = input(f"{Fore.YELLOW}{command_line.tree_selected}{Style.RESET_ALL}>")

        if usr_input == 'help':
            command_line.dispay_help()
        command_line.match_input(usr_input)
        #print('Invalid command type "help" for help')

        #command_line.tree_selected = command_line.select_tree()
        #print('C:/TreeTest> ', end='')
        
        #dispay_help()
        #for line in tree(Path('Root')):
        #    print(line)
        #print("\033[31mThis is red font.\033[0m")
    
