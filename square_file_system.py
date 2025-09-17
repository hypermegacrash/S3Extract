
import os

from mod_color         import *
from mod_binary_reader import *

from def_square_file import *

from tf_ext_guess import transformer_ext_guess
from tf_hash      import transformer_hash
from tf_index     import transformer_index

class transformed_entry():
    def __init__(self):
        self.file_name   = ""
        self.file_ext    = ""
        self.folder_path = ""

        self.file_name_color_id   = RESET
        self.file_ext_color_id    = RESET
        self.folder_path_color_id = RESET

class SquareFile():
    def __init__(self):
        self.dir_entry   = None
        self.data_buffer = bytearray()

        self.tf_final = transformed_entry() # The transformed file name, file ext and folder path
        # Data Transformers by priority
        self.tf_index = transformer_index()     # ID files by index
        self.tf_hash  = transformer_hash()      # ID files with the same hash
        self.tf_ext   = transformer_ext_guess() # ID files by parsing data buffer and guessing file type

    def transform(self):
        # First, file name
        if self.tf_index.file_name:
            self.tf_final.file_name          = self.tf_index.file_name
            self.tf_final.file_name_color_id = self.tf_index.color
        elif self.tf_hash.file_name:
            self.tf_final.file_name          = self.tf_hash.file_name
            self.tf_final.file_name_color_id = self.tf_hash.color

        # Second, file extension
        if self.tf_index.file_ext:
            self.tf_final.file_ext          = self.tf_index.file_ext
            self.tf_final.file_ext_color_id = self.tf_index.color
        elif self.tf_hash.file_ext:
            self.tf_final.file_ext          = self.tf_hash.file_ext
            self.tf_final.file_ext_color_id = self.tf_hash.color
        elif self.tf_ext.file_ext:
            self.tf_final.file_ext          = self.tf_ext.file_ext
            self.tf_final.file_ext_color_id = self.tf_ext.color

        # Finally, folder path
        if self.tf_index.folder_path:
            self.tf_final.folder_path          = self.tf_index.folder_path
            self.tf_final.folder_path_color_id = self.tf_index.color

    def write(self, output_path = ""):

        # Folder path
        if self.tf_final.folder_path:
            out_file_path = f"{output_path}/{self.tf_final.folder_path}/"
        else:
            out_file_path = f"{output_path}/"

        # Ensure the path exists
        if not os.path.exists(out_file_path):
            os.makedirs(out_file_path)

        # File Index
        out_file_path += f"{self.dir_entry.nIndex}"

        # Hex Offset into .bin file
        #out_file_path += f"{((self.nSectorNum * DISC_SECTOR_SIZE)):08x}_"

        # File Name
        if self.tf_final.file_name != "":
            out_file_path += f"_{self.tf_final.file_name}"

        # File Ext
        out_file_path += f"{self.tf_final.file_ext}"

        # Write it out
        with open(out_file_path, "wb") as outFile:
            outFile.write(self.data_buffer)

    def print(self):
        self.dir_entry.print()
        print(f"name {self.tf_final.file_name_color_id}{self.tf_final.file_name:<20}{RESET} ", end="")
        print(f"ext {self.tf_final.file_ext_color_id}{self.tf_final.file_ext:<6}{RESET} ", end="")
        print(f"extguess {self.tf_ext.file_ext:<6} ", end="")
        print(f"folder {GREEN}{self.tf_final.folder_path:<35}{RESET}")

class SquareFileSystem():
    def __init__(self):
        self.hed = Hed_t()
        self.version = {'game': ""}

        self.hedBytes = bytearray() # Filesystem header bytes
        self.dirBytes = bytearray() # Filesystem directory bytes
        self.imgBytes = bytearray() # Filesystem image bytes
        self.fileEntries = []
          
    def read_hed_from_bin(self, inFile):
        print(f"{CYAN}Grabbing Square Header...{RESET}")

        inFile.seek( HIDDEN_FS_HEADER_OFFSET, 0 )

        self.hedBytes = inFile.read( DISC_SECTOR_DATA_SIZE )
        inFile.seek( -DISC_SECTOR_DATA_SIZE, 1 )

        match self.version['game']:
            case "XENOGEARS":
                self.hed.szTitleID = readString(inFile)

                self.hed.nDiscNum  = int(self.hed.szTitleID[3:4])
                self.hed.nNumDiscs = 2

                self.hed.DirSector = 0x18
                self.hed.UnkSector = 0x28

                self.hed.DirSize = 0x10 * DISC_SECTOR_DATA_SIZE # Guessing 16 sectors worth of directory

                if not self.hed.verify():
                    return False
            case "CHRONOCROSS" | "DEWPRISM":
                if not self.hed.read(inFile):
                    return False
            case _:
                print(f"{RED}[ERROR] Filesystem version not set!")
                exit()

        return True

    def read_dir_from_bin(self, inFile):
        print(f"{CYAN}Grabbing Square Directory...{RESET}")

        dir_offset = (DISC_STARTING_PAD_SIZE + (DISC_SECTOR_SIZE * self.hed.DirSector))

        inFile.seek(dir_offset, 0)

        dir_sector_count = self.hed.UnkSector - self.hed.DirSector
        
        for sector in range(dir_sector_count):
            self.dirBytes.extend(inFile.read(DISC_SECTOR_DATA_SIZE))
            inFile.seek(DISC_SECTOR_DUMMY_SIZE, 1)

        return True

    def read_img_from_bin(self, inFile):
        print(f"{CYAN}Grabbing Square Image...{RESET}")

        # Seek to file data in .bin file
        imgSectorOffset = (DISC_STARTING_PAD_SIZE + (DISC_SECTOR_SIZE * self.fileEntries[0].dir_entry.nSectorNum))
        inFile.seek(imgSectorOffset, 0)

        # Get an estimate of how many sectors are used
        furthestSectorOffset = 0
        furthestSectorOffsetSize = 0
        for entry in self.fileEntries:
            if entry.dir_entry.nSectorNum > furthestSectorOffset and entry.dir_entry.nSectorCount > 0:
                furthestSectorOffset = entry.dir_entry.nSectorNum
                furthestSectorOffsetSize = entry.dir_entry.nSectorCount

        imgSectorCount = furthestSectorOffset + furthestSectorOffsetSize
        imgSectorCount -= self.fileEntries[0].dir_entry.nSectorNum

        # Extract the file data to a bytearray without the sector pad bytes
        for sector in range(imgSectorCount):
            self.imgBytes.extend(inFile.read(DISC_SECTOR_DATA_SIZE))
            inFile.seek(DISC_SECTOR_DUMMY_SIZE, 1)

        return True
