
import io

from mod_color import *

from square_file_system import *

from id_hash_bin import get_game_version_bin
from id_hash_img import get_game_version_img

from tf_index     import *
from tf_hash      import *
from tf_ext_guess import *

def files_transform(in_file_entries, in_version):
    print(f"{CYAN}Transforming files...{RESET}")
    # TRANSFORM 1 - INDEX
    read_index(in_file_entries, in_version)

    # TRANSFORM 2 - HASH
    hashmap_name = f"data/hashmap_{in_version['game']}.csv"
    print(f"{CYAN}[HASHMAP] Retrieving hash map {hashmap_name} for friendly file names...{RESET}")
    hashmgr = HashMapMgr()
    hashmgr.extract_hash_map(hashmap_name)
    read_filetree_hash_supplement(in_file_entries, hashmgr)

    # TRANSFORM 3 - EXT GUESS
    for file_entry in in_file_entries:
        match(in_version['game']):
            case "XENOGEARS":   file_entry.tf_ext.file_ext = xg_guess_file_type(file_entry.data_buffer)
            case "CHRONOCROSS": file_entry.tf_ext.file_ext = cc_guess_file_type(file_entry.data_buffer)
            case "DEWPRISM":    file_entry.tf_ext.file_ext = dp_guess_file_type(file_entry.data_buffer)
            case _:
                print(f"{RED}[FILE ENTRY] ERROR Version not set for guess_file_type!")
                exit(1)

    # TRANSFORM 4 - FINAL
    for file_entry in in_file_entries:
        file_entry.transform()

def files_write(in_file_entries, in_version, output_path):
    print(f"LEGEND: {transformer_index.color}[INDEX] {transformer_hash.color}[HASH] {transformer_ext_guess.color}[EXT GUESS]{RESET}")
    for file_entry in in_file_entries:
        file_entry.print()

    output_path += f"{in_version['game']}_{in_version['version']}_DS{in_version['disc']:02}"

    for file_entry in in_file_entries:
        # Filter out files we won't write
        if file_entry.tf_final.file_name == "dummy" and file_entry.tf_final.file_ext == ".dat": continue # dummy.dat files as learned from Chrono Cross Radical Dreamers Editions.
        if file_entry.dir_entry.nSectorCount == 0 or file_entry.tf_ext.file_ext == ".empty":    continue # Certain entries in the directory are empty
        if file_entry.data_buffer == None:                                                      continue # Nothing to write then we ain't writting.
        if file_entry.tf_ext.file_ext == ".dum" or file_entry.tf_ext.file_ext == ".cdmake":     continue # Dummy files that contain no meaningful gamedata
        if file_entry.tf_ext.file_ext == ".nowab":                                              continue # Useless files that contain only the string nowab.

        file_entry.write(output_path)

    print("DONE!")

def files_debug(in_file_entries):
    print("DEBUG STATISTICS")

    fs_hashes   = {}
    fs_exts     = {}
    empty_files = 0
    named_file_hashes = {}

    for file in in_file_entries:
        # Are there duplicates of this file?
        if file.hash not in fs_hashes.keys():
            fs_hashes[file.hash] = 1
        else:
            fs_hashes[file.hash] += 1

        # How many occurances of this file type?
        if file.fileExtGuess not in fs_exts.keys():
            fs_exts[file.fileExtGuess] = 1
        else:
            fs_exts[file.fileExtGuess] += 1

        # How many entries are empty?
        if file.dir_entry.nSectorCount == 0:
            empty_files += 1

        if file.get_filename() != "":
            # How many occurances of this file type?
            if file.hash not in named_file_hashes.keys():
                named_file_hashes[file.hash] = 1

    print(f"unique entries {len(fs_hashes.keys())} / {len(in_file_entries)}")
    print(fs_exts)
    
    print(f"Named Unique Files {len(named_file_hashes)} / {len(fs_hashes)}")

def files_read_from_img(in_file_entries, in_img_bytes, in_version):
        print(f"{CYAN}Reading file entry data from image...{RESET}")
        with io.BytesIO(in_img_bytes) as imgFS:
            folderFlag = 0
            folderName = None
            for file_entry in in_file_entries:
                match(in_version['game']):
                    case "XENOGEARS":
                        if file_entry.dir_entry.nFileSize <= 0 or file_entry.dir_entry.nSectorNum <= 0: 
                            folderFlag = -file_entry.dir_entry.nFileSize
                            folderName = str(file_entry.dir_entry.nIndex) + "/"
                            continue

                        if folderFlag:
                            file_entry.tf_index.folder_path = folderName + file_entry.tf_index.folder_path
                            folderFlag -= 1

                dataOffset = file_entry.dir_entry.nSectorNum - in_file_entries[0].dir_entry.nSectorNum
                dataOffset *= DISC_SECTOR_DATA_SIZE

                dataSize = file_entry.dir_entry.nFileSize

                imgFS.seek(dataOffset, 0)
                file_entry.data_buffer = imgFS.read(dataSize)

def files_read_from_dir(in_dir_bytes, in_dir_size, in_version):
    print(f"{CYAN}Extracting Square Directory Entries...{RESET}")
    out_file_entries = []

    with io.BytesIO(in_dir_bytes) as dirFS:

        # Get an estimate of how many entries exist to read
        match(in_version['game']):
            case "XENOGEARS":
                if in_version['version'] == "JP_TAIKEN":
                    dirEntryCount =  int(in_dir_size / DirEntry97_t.get_entry_size()) # 1997 - 8 bytes
                else:
                    dirEntryCount =  int(in_dir_size / DirEntry98_t.get_entry_size()) # 1998 - 7 bytes
            case "CHRONOCROSS" | "DEWPRISM":
                dirEntryCount =  int(in_dir_size / DirEntry99_t.get_entry_size()) # 1999 - 4 bytes
            case _:
                print(f"{RED}[FILE ENTRY] ERROR Version not set for get_dir_entry_count!{RESET}")
                return False

        for entry in range(dirEntryCount):
            match(in_version['game']):
                case "XENOGEARS" if in_version['version'] == "JP_TAIKEN": dirEntry = DirEntry97_t()
                case "XENOGEARS" if in_version['version'] != "JP_TAIKEN": dirEntry = DirEntry98_t()
                case "CHRONOCROSS" | "DEWPRISM":                          dirEntry = DirEntry99_t()
                case _:
                    print(f"{RED}[FILE ENTRY] ERROR Version not set for selecting file version!{RESET}")
                    exit(1)

            dirEntry.read(dirFS)
            out_file_entries.append(dirEntry)

    out_file_entries = out_file_entries[0].get_valid_entries(out_file_entries)
    newFileEntries = []
    for entry in out_file_entries:
        newEntry = SquareFile()
        newEntry.dir_entry = entry
        newFileEntries.append(newEntry)
    out_file_entries = newFileEntries

    return out_file_entries

def extract_fs_bin(input_bin = "", output_path = ""):

    game_version = get_game_version_bin(input_bin)
    if game_version == None:
        print(f"{RED}[ERROR] Unknown Game Version?{RESET}")
        return False

    sfs = SquareFileSystem()
    sfs.version = game_version
    
    with open(input_bin, "rb") as inFileBin:
        if not sfs.read_hed_from_bin(inFileBin):
            print(f"{RED}[ERROR] Unable to read header{RESET}")
            exit()

        if not sfs.read_dir_from_bin(inFileBin):
            print(f"{RED}[ERROR] Unable to read directory{RESET}")
            exit()

        sfs.fileEntries = files_read_from_dir(sfs.dirBytes, sfs.hed.DirSize, sfs.version)

        if not sfs.read_img_from_bin(inFileBin):
            print(f"{RED}[ERROR] Unable to read Image{RESET}")
            exit()

        files_read_from_img(sfs.fileEntries, sfs.imgBytes, sfs.version)

    files_transform(sfs.fileEntries, sfs.version)

    files_write(sfs.fileEntries, sfs.version, output_path)

    write_index(sfs.fileEntries, sfs.version)
    
def extract_fs_hedexeimg(input_hed = "", input_exe = "", input_img = "", output_path = ""):
    
    game_version = get_game_version_img(input_img)
    if game_version == None:
        print(f"{RED}[ERROR] Unknown Game Version?{RESET}")
        return False
    
    sfs = SquareFileSystem()
    sfs.version = game_version

    with open(input_hed, "rb") as inFileHed:
        # Read the hed which is stored in the first sector
        sfs.hed.read(inFileHed)

        # Jump ahead to the next sector which has all the dir bytes
        # TODO: We currently read more than we need to...
        inFileHed.seek(0x800, 0)
        sfs.dirBytes = inFileHed.read()

    sfs.fileEntries = files_read_from_dir(sfs.dirBytes, sfs.hed.DirSize, sfs.version)

    # The hed expects the data buffer to be in this pattern
    #      DATA BUFFER
    # |-------------------|
    # |        EXE        |
    # |-------------------|
    # |        IMG        |
    # |-------------------|
    # Sector offsets are absolute to the start of the disc.
    # We can subtract the sector offset from the first entry to get 
    # offsets relative to the data buffer we create.
    with open(input_exe, "rb") as inFileExe: sfs.imgBytes.extend(inFileExe.read())
    with open(input_img, "rb") as inFileImg: sfs.imgBytes.extend(inFileImg.read())

    files_read_from_img(sfs.fileEntries, sfs.imgBytes, sfs.version)

    files_transform(sfs.fileEntries, sfs.version)

    files_write(sfs.fileEntries, sfs.version, output_path)

    write_index(sfs.fileEntries, sfs.version)

def extract_fs_exeimg(input_exe = "", input_img = "", output_path = ""):
    DIR_OFFSET = 0x804
    DIR_SIZE = DISC_SECTOR_DATA_SIZE * 0x10
    DIR_COUNT = int(DIR_SIZE / DirEntry97_t.get_entry_size())

    game_version = get_game_version_img(input_img)
    if game_version == None:
        print(f"{RED}[ERROR] Unknown Game Version?{RESET}")
        return False

    fileEntries = []

    imgBytes = bytearray()

    # Read in our directory which is contained directly within the Xenogears executable
    with open(input_exe, "rb") as inFileExe:
        inFileExe.seek(DIR_OFFSET, 0)
        
        for entry in range(DIR_COUNT):
            dirEntry = DirEntry97_t()
            dirEntry.read(inFileExe)
            fileEntries.append(dirEntry)

    # Fix up our entries
    fileEntries = fileEntries[0].get_valid_entries(fileEntries)
    newFileEntries = []
    for entry in fileEntries:
        newEntry = SquareFile()
        newEntry.dir_entry = entry
        newFileEntries.append(newEntry)
    fileEntries = newFileEntries

    # The hed expects the data buffer to be in this pattern
    #      DATA BUFFER
    # |-------------------|
    # |        EXE        |
    # |-------------------|
    # |        IMG        |
    # |-------------------|
    # Sector offsets are absolute to the start of the disc.
    # We can subtract the sector offset from the first entry to get 
    # offsets relative to the data buffer we create.
    with open(input_exe, "rb") as inFileExe: imgBytes.extend(inFileExe.read())
    with open(input_img, "rb") as inFileBin: imgBytes.extend(inFileBin.read())

    files_read_from_img(fileEntries, imgBytes, game_version)

    files_transform(fileEntries, game_version)

    files_write(fileEntries, game_version, output_path)

    write_index(fileEntries, game_version)