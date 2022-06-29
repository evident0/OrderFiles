
     ██████╗ ██████╗ ██████╗ ███████╗██████╗ 
    ██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
    ██║   ██║██████╔╝██║  ██║█████╗  ██████╔╝
    ██║   ██║██╔══██╗██║  ██║██╔══╝  ██╔══██╗
    ╚██████╔╝██║  ██║██████╔╝███████╗██║  ██║
     ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
     
    --------------------------General Commands:--------------------------

    create </folder_name> create a tree structure with root </folder_name>
    select - select a tree
    exit, exit the program

    -----------------------Tree specific commands:-----------------------
    tree - display the tree
    scanner <os_path> - create a scanner for this folder. It will be used for ordering the files in the currently selected tree
    scanrm <os_path> - remove a scanner from the currently selected tree
    scaninf - display all the folders to be scanned when ordering
    order <N/A|-r> - order the files from the scanner folders, use -r for recursive scan
    mk <folder_name> <[...,[FOLDER|EXTENSION|REGULAR_EXPRESSION,<name>],...]>, create folder with list of rules
    rr <folder_name> <[...,[EXTENSION|REGULAR_EXPRESSION,<name>],...]>, remove rules from folder (use rm for FOLDER rules)
    rm <folder_name>, recursively send directory to trash
    mv <folder_name> <new_folder_name>, move folder to new location
   
## Installing

Clone this project and name it accordingly:

``git clone https://github.com/BillyA15/OrderFiles/tree/alpha`` 

Create a virtual enviroment 

Windows: ``python -m venv .venv`` 

Linux: ``python3 -m venv .venv`` 

Activate virtual enviroment 

Windows CMD: ``path\to\venv\Scripts\activate.bat`` 

Windows PowerShell: ``path\to\venv\Scripts\Activate.ps1`` 

Linux: ``source /path/to/venv/bin/activate`` 

Install Dependencies:

``pip install -r requirements.txt``

# Getting Started

(Please note that the script has not been thoroughly tested on Linux)

1. Run the ``CommandLineInterface.py`` using python 3.10 and above is recommended
2. ``help`` for a list of commands
3. ``create <directory-path>`` to create a new tree Structure
4. ``select`` a tree 
5.  edit the tree


