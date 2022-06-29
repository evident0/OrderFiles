from pathlib import Path
from posixpath import basename
import ast #literal_eval of input argument for touching folders
from colorama import *
from FolderOp import *
from TreeOp import *
from defines import * # defines for extensions, folders, regex_expression

from pathlib import Path
# prefix components:
space =  '    '
branch = '│   '
# pointers:
tee =    '├── '
last =   '└── '
class CommandLineInterface:
    def __init__(self) -> None:
        self.folder_op = None # the instance of FolderOp, for simplicity only one folder_op is used at a time
        self.tree_op = TreeOp() # initialize tree_op see the class for more details
        self.tree_selected = "" # used in the cli to keep track of the selected tree
    def select_tree(self):

        a_list = self.tree_op.get_tree_list()
        
        # a selection screen for the a_list
        number = 0
        for item in a_list:
            print(f"{number}. {item}")
            number += 1
        print("select one tree of the above [0,1,2,3,...]")
        sel = input("> ")
        #check the bounds of the selection
        if int(sel) > len(a_list):
            print("invalid selection")
            return ""
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
        #print(Back.LIGHTWHITE_EX + Fore.BLACK + '------------------------------HELP MENU------------------------------' + Style.RESET_ALL)
        #print()
        print(Back.LIGHTWHITE_EX + Fore.BLACK +'--------------------------General Commands:--------------------------' + Style.RESET_ALL)
        print()
        print('create </folder_name> create a tree structure with root </folder_name>')
        print('select - select a tree')
        print('exit, exit the program')
        print()
        print(Back.LIGHTWHITE_EX + Fore.BLACK +'-----------------------Tree specific commands:-----------------------' + Style.RESET_ALL)
        print('--------------------(need to select a tree first)--------------------')
        print('tree - display the tree')
        print('scanner <os_path> - create a scanner for this folder. It will be used for ordering the files in the currently selected tree')
        print('scanrm <os_path> - remove a scanner from the currently selected tree')
        print('scaninf - display all the folders to be scanned when ordering')
        print('order <N/A|-r> - order the files from the scanner folders, use -r for recursive scan')
        print('mk <folder_name> <[...,[FOLDER|EXTENSION|REGULAR_EXPRESSION,<name>],...]>, create folder with list of rules')
        print('rr <folder_name> <[...,[EXTENSION|REGULAR_EXPRESSION,<name>],...]>, remove rules from folder (use rm for FOLDER rules)')
        print('rm <folder_name>, recursively send directory to trash')
        print('mv <folder_name> <new_folder_name>, move folder to new location')
        print()
        print(Back.LIGHTWHITE_EX + Fore.BLACK + "page (1/1)" + Style.RESET_ALL) 
        
    def print_tree(self):
        if self.folder_op is None:
            print(Back.RED+Fore.WHITE+"Tree selection failed"+Style.RESET_ALL)
            return
        tree_empty = True
        for line in command_line.tree_dict(self.folder_op.config, self.folder_op.root):
            print(line)
            tree_empty = False
        if tree_empty:
            print(Back.RED+Fore.WHITE+"Tree is empty"+Style.RESET_ALL)
       
    
    def tree_operations(self, command, arguments_size , arguments):
       
        if command == 'mk':
            if arguments_size != 2:
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
                
                #print("making...")
                #TODO return something if it succeeds
                self.folder_op.touch_folder(parent_path, folder_name, rule_list)
                #self.print_tree()
                return True
        if command == 'rr':
            if arguments_size != 2:
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
                        print('<rules> is not a valid list ex. [[FOLDER,<name>],[EXTENSION,<name>],[REGULAR_EXPRESSION,<name>]]')
                        return False
                except SyntaxError:
                    print('<rules> is not a valid list ex. [[FOLDER,<name>],[EXTENSION,<name>],[REGULAR_EXPRESSION,<name>]]')
                    return False
                
                #print("making...")
                #TODO return something if it succeeds
                self.folder_op.remove_folder_rules(parent_path, folder_name, rule_list)
                #self.print_tree()
                return True
        elif command == 'rm':
            if arguments_size != 1:
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
                #TODO return something if it succeeds
                self.folder_op.remove_folder(parent_path,folder_name)
                #print("removing...")
                #self.print_tree()
                return True
        elif command == 'mv':
            if arguments_size != 2:
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
                #print (f"ppath {parent_path},pname {folder_name}, nppath{new_parent_path}, npname{new_folder_name}")
                #TODO return something if it succeeds
                self.folder_op.move_folder(parent_path, folder_name, new_parent_path, new_folder_name)
                #print("moving...")
                #self.print_tree()
                return True
        elif command == 'scanner':
            if arguments_size != 1:
                print('scanner <folder_path> | add a folder to scan and move the files')
                return False
            else:
                #do the scanner command
                self.tree_op.add_scanable_folder(self.folder_op, arguments[0])
                return True
        elif command == 'scanrm':
            if arguments_size != 1:
                print('scanrm <folder_path> | remove a scanner from the currently selected tree')
                return False
            else:
                #do the scanrm command
                self.tree_op.remove_scanable_folder(self.folder_op, arguments[0])
                return True
        elif command == 'scaninf':
            #display all the folders scanned when ordering
            scan_list = self.tree_op.get_scanable_folders(self.folder_op)
            if len(scan_list) == 0:
                print(Back.LIGHTWHITE_EX + Fore.BLACK  + 'No folders to scan (add one with the scanner command, type help for info)' + Style.RESET_ALL)
            else:
                print(Back.LIGHTWHITE_EX + Fore.BLACK +'Folders to scan' + Style.RESET_ALL)
                for folder in scan_list:
                    print(folder)
            return True

        elif command == 'order':
            if len(arguments) > 1:
                print('order <N/A|-r> | order the files in a folder, use -r for recursive scan')
                return False
            #do the order command
            if len(arguments) == 0:
                print("ordering...")
                #TODO return something if it succeeds
                self.tree_op.order_files_no_recursion(self.folder_op)
                print(Fore.GREEN+"Done"+Style.RESET_ALL)
            elif arguments[0] == '-r':
                print("ordering...")
                #TODO return something if it succeeds
                self.tree_op.order_files(self.folder_op)
                print(Fore.GREEN+"Done"+Style.RESET_ALL)
            else:
                print('none valid argument for order, use use -r for recursive scan')
                return False
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
      
        if command == 'exit':
            #exit the program
            exit()
        if command == 'create':
            if len(arguments) != 1:
                print('create <folder_path> create a tree structure with root </folder_name>')
                return False
            else:
                try:
                    dir_name = os.path.dirname(arguments[0])
                    base_name = os.path.basename(arguments[0])
                except IndexError:
                    print('<folder_name> is a relative path ex. /Root/Documents/PDF')
                    return False
                #IMPORTANT NOTE: it doesn't need slash ("Root" not "/Root")
                #TODO return something if it succeeds
                self.tree_op.create_new_tree(dir_name, base_name) 
                #print("creating...")
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
    title = """
    
 ██████╗ ██████╗ ██████╗ ███████╗██████╗ 
██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██║   ██║██████╔╝██║  ██║█████╗  ██████╔╝
██║   ██║██╔══██╗██║  ██║██╔══╝  ██╔══██╗
╚██████╔╝██║  ██║██████╔╝███████╗██║  ██║
 ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝

    """
    print(title)
    print(Back.LIGHTWHITE_EX + Fore.BLACK + "Welcome to order type help to begin" + Style.RESET_ALL)
    command_line = CommandLineInterface()
    while True:
       
        usr_input = input(f"{Fore.YELLOW}{command_line.tree_selected}{Style.RESET_ALL}> ")

        if usr_input == 'help':
            command_line.dispay_help()
        else:
            command_line.match_input(usr_input)
    
