from pathlib import Path
from colorama import *
from FolderOp import *
EXTENSION = "EXTENSION"
FOLDER = "FOLDER"
REGULAR_EXPRESSION = "REGULAR_EXPRESSION"
'''class DisplayablePath(object):
    display_filename_prefix_middle = '├──'
    display_filename_prefix_last = '└──'
    display_parent_prefix_middle = '    '
    display_parent_prefix_last = '│   '

    def __init__(self, path, parent_path, is_last):
        self.path = Path(str(path))
        self.parent = parent_path
        self.is_last = is_last
        if self.parent:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0

    @property
    def displayname(self):
        if self.path.is_dir():
            return self.path.name + '/'
        return self.path.name

    @classmethod
    def make_tree(cls, root, parent=None, is_last=False, criteria=None):
        root = Path(str(root))
        criteria = criteria or cls._default_criteria

        displayable_root = cls(root, parent, is_last)
        yield displayable_root

        children = sorted(list(path
                               for path in root.iterdir()
                               if criteria(path)),
                          key=lambda s: str(s).lower())
        count = 1
        for path in children:
            is_last = count == len(children)
            if path.is_dir():
                yield from cls.make_tree(path,
                                         parent=displayable_root,
                                         is_last=is_last,
                                         criteria=criteria)
            else:
                yield cls(path, displayable_root, is_last)
            count += 1

    @classmethod
    def _default_criteria(cls, path):
        return True

    @property
    def displayname(self):
        if self.path.is_dir():
            return self.path.name + '/'
        return self.path.name

    def displayable(self):
        if self.parent is None:
            return self.displayname

        _filename_prefix = (self.display_filename_prefix_last
                            if self.is_last
                            else self.display_filename_prefix_middle)

        parts = ['{!s} {!s}'.format(_filename_prefix,
                                    self.displayname)]

        parent = self.parent
        while parent and parent.parent is not None:
            parts.append(self.display_parent_prefix_middle
                         if parent.is_last
                         else self.display_parent_prefix_last)
            parent = parent.parent

        return ''.join(reversed(parts))



if __name__ == '__main__':

    paths = DisplayablePath.make_tree(Path('Root'))
    for path in paths:
        print(path.displayable())
'''

from pathlib import Path
# prefix components:
space =  '    '
branch = '│   '
# pointers:
tee =    '├── '
last =   '└── '
class CommandLineInterface:
    def __init__(self) -> None:
        folder_op = None #TODO multiple of these somewhere else not in this class
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


    '''def tree(dir_path: Path, prefix: str=''):
        """A recursive generator, given a directory Path object
        will yield a visual tree structure line by line
        with each line prefixed by the same characters
        """    
        contents = list(dir_path.iterdir()) # for loop for dir
        # contents each get pointers that are ├── with a final └── :
        pointers = [tee] * (len(contents) - 1) + [last] # how many |- in addition with one -
        for pointer, path in zip(pointers, contents):
            yield prefix + pointer + path.name
            if path.is_dir(): # extend the prefix and recurse:
                extension = branch if pointer == tee else space 
                # i.e. space because last, └── , above so no more |
                yield from tree(path, prefix=prefix+extension)'''


    def dispay_help(self):
        print(Fore.RED + 'Help Menu' + Style.RESET_ALL)
        print('mk <folder_name> <[...,[FOLDER|EXTENSION|REGULAR_EXPRESSION,<name>],...]>, create folder with list of rules')
        print('rm <folder_name>, recursively send directory to trash')
        print('mv <folder_name> <new_folder_name>, move folder to new location')
        print('up <folder_name> <[...,[FOLDER|EXTENSION|REGULAR_EXPRESSION,<name>],...]>, append new rules for a folder')
        print('scan <folder_name>, add a folder to scan and move the files')
        print('create </folder_name> create a tree structure with root </folder_name>')
    def print_tree(self):
        for line in command_line.tree_dict(self.folder_op.config, "/Root"):
            print(line)
    def match_input(self,input):
        #split input into command and arguments
        command = input.split(' ')[0]
        arguments = input.split(' ')[1:]
        #check if command is valid
        if command == 'mk':
            if len(arguments) < 2:
                print('mk <folder_name> <[...,[FOLDER|EXTENSION|REGULAR_EXPRESSION,<name>],...]>, create folder with list of rules')
                return False
            else:
                #do the mk command
                parent_path = arguments[0].rsplit('/',1)[0]
                folder_name = arguments[0].rsplit('/',1)[1]
                self.folder_op.make_folder(arguments[0],arguments[1:])
                self.print_tree()
                return True
        elif command == 'rm':
            if len(arguments) < 1:
                print('rm <folder_name>, recursively send directory to trash')
                return False
            else:
                #do the rm command
                parent_path = arguments[0].rsplit('/',1)[0]
                folder_name = arguments[0].rsplit('/',1)[1]
                self.folder_op.remove_folder(parent_path, folder_name)
                self.print_tree()
                return True
        elif command == 'mv':
            if len(arguments) < 2:
                print('mv <folder_name> <new_folder_name>, move folder to new location')
                return False
            else:
                #do the mv command
                parent_path = arguments[0].rsplit('/',1)[0]
                folder_name = arguments[0].rsplit('/',1)[1]
                new_parent_path = arguments[1].rsplit('/',1)[0]
                new_folder_name = arguments[1].rsplit('/',1)[1]
                self.folder_op.move_folder(parent_path, folder_name, new_parent_path, new_folder_name)
                self.print_tree()
                return True
        elif command == 'up':
            if len(arguments) < 2:
                print('up <folder_name> <[...,[FOLDER|EXTENSION|REGULAR_EXPRESSION,<name>],...]>, append new rules for a folder')
                return False
            else:
                #do the up command
                parent_path = arguments[0].rsplit('/',1)[0]
                folder_name = arguments[0].rsplit('/',1)[1]
                print(parent_path+'/'+folder_name)
                self.folder_op.append_rules_to_folder(parent_path,folder_name,[["FOLDER","ininRoot"],["EXTENSION",".inroot"]])
                self.print_tree()
                return True
        elif command == 'scan':#TODO scans the second you input the command but should be saved in a file
            if len(arguments) < 1:
                print('scan <folder_name>, add a folder to scan and move the files')
                return False
            else:
                #do the scan command
                
                return True
        elif command == 'create':#TODO create the files in os for now just reads them
            if len(arguments) < 1:
                print('create </folder_name> create a tree structure with root </folder_name>')
                return False
            else:
                #do the create command
                self.folder_op = FolderOp("D:\TreeTest", 'config_output.json', arguments[0])#TODO ROOT has been selected from a previous menu
                print()
                print()
                print(self.folder_op.config)
                print()
                print(f"THE EXTENSIONS: {self.folder_op.extensions}")
                print()
                print(self.folder_op.regex)
                self.print_tree()
                return True
        else:
            print('Invalid command')
            return False


if __name__ == '__main__':
    dict = {
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
    command_line = CommandLineInterface()
    while True:
       
        print()
        print('-h: Display help menu')
        print(Fore.YELLOW+'C:/TreeTest'+Style.RESET_ALL+'> ', end='')#TODO get path_to_root
        usr_input = input()
        if usr_input == '-h':
            command_line.dispay_help()
        print(command_line.match_input(usr_input))
        
        print('C:/TreeTest> ', end='')
        
        #dispay_help()
        #for line in tree(Path('Root')):
        #    print(line)
        #print("\033[31mThis is red font.\033[0m")
    
