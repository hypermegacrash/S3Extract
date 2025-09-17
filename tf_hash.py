
# Transformer that identifies copies of the same file using hashing.

import os
import csv
import hashlib

from mod_color import *

class HashMapMgr:
    def __init__(self):
        self.hash_map = {}

    def extract_hash_map(self, in_hashmap_path):
        if not os.path.exists(in_hashmap_path):
            print(f"{YELLOW}[HASHMAP] hashmap file {in_hashmap_path} does not exist, not using hashmap{RESET}")
            return
        else:
            print(f"{GREEN}[HASHMAP] Found {in_hashmap_path}{RESET}")
        
        with open(in_hashmap_path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["hash"] != "None" and row["name"] != "":
                    self.hash_map[int(row["hash"], 16)] = {
                        "name": row["name"],
                        "ext": row["ext"]    
                    }

    def save_blank_hash_map_to_fs(self, out_hashmap_path, in_file_entries):
        with open(out_hashmap_path, "w") as outFile:
            outFile.write(f"hash,name\n")
            for file in in_file_entries:
                outFile.write(f"{file.hash}\n")

    def save_hash_map_to_fs(self, out_hashmap_path):
        with open(out_hashmap_path, "w") as outFile:
            outFile.write(f"hash,name,ext\n")
            for key in self.hash_map.keys():
                outFile.write(f"{key:08x},{self.hash_map[key]['name']},{self.hash_map[key]['ext']}\n")

def read_filetree_hash_supplement(in_file_entries, hashmgr):
    # Then we make hueristic guesses on the unknowns
    for file_entry in in_file_entries:
        file_entry.hash = hashlib.sha256(file_entry.data_buffer).hexdigest()
        intHash = int(file_entry.hash, 16)
        if intHash in hashmgr.hash_map.keys():
            file_entry.tf_hash.file_name = hashmgr.hash_map[intHash]["name"]
            file_entry.tf_hash.file_ext  = hashmgr.hash_map[intHash]["ext"]

class transformer_hash():
    color = MAGENTA

    def __init__(self):
        self.data_buffer_hash = None
        self.file_name        = ""
        self.file_ext         = ""
        self.folder_path      = ""