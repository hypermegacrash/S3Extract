
# Transformer that identifies files by a matching index and game version

import csv

from mod_color import *

def get_folder_name(version): return f"{version['game']}_{version['version']}_DS{version['disc']:02}"

class transformer_index():
    color = GREEN
    
    def __init__(self):
        self.file_name   = ""
        self.file_ext    = ""
        self.folder_path = ""

def read_index(in_file_entries, in_version):
    in_filetree_path = f"data/index_{get_folder_name(in_version)}.csv"
    print(f"{CYAN}[INDEX] Looking for filetree {in_filetree_path} for file names...{RESET}")
    if not os.path.exists(in_filetree_path):
        print(f"{RED}[INDEX] filetree file {in_filetree_path} does not exist{RESET}")
        return
    else:
        print(f"{GREEN}[INDEX] Using filetree {in_filetree_path}{RESET}")
    
    with open(in_filetree_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for index, row in enumerate(reader):
            if in_version['game'] == "CHRONOCROSS":
                root, extension = os.path.splitext(row["rde_name"])
                in_file_entries[index].tf_index.file_name   = root
                in_file_entries[index].tf_index.file_ext    = extension
                in_file_entries[index].tf_index.folder_path = row["rde_folder"]
            else:
                in_file_entries[index].tf_index.file_name   = row["name"]
                in_file_entries[index].tf_index.file_ext    = row["ext"]
                in_file_entries[index].tf_index.folder_path = row['folder']

def write_index(in_file_entries, in_version):
    file_path = f"data/index_{get_folder_name(in_version)}.csv"
    print(f"{CYAN}[INDEX] Checking if index file {file_path} exists...{RESET}")
    if os.path.exists(file_path):
        print(f"{RED}[INDEX] index file {file_path} already exists? Not overriding.{RESET}")
        return
    with open(file_path, "w") as outFile:
        print(f"{GREEN}[INDEX] Writting index file {file_path}...{RESET}")
        outFile.write(f"index,name,ext,folder\n")
        for entry in in_file_entries:
            outFile.write(f"{entry.dir_entry.nIndex},,,\n")