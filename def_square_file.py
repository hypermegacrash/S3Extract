
# File Definitions and parsers for the filesystem structures

from mod_color         import *
from mod_binary_reader import *

DISC_STARTING_PAD_SIZE = 0x18  # There's padding at the start of the ISO before it follows the sector layout
DISC_SECTOR_DATA_SIZE  = 0x800 # The size of actual bytes of data from the start of the sector
DISC_SECTOR_DUMMY_SIZE = 0x130 # The size of dummy bytes appearing after the game data in the sector
DISC_SECTOR_SIZE       = ( DISC_SECTOR_DATA_SIZE + DISC_SECTOR_DUMMY_SIZE )

HIDDEN_FS_HEADER_SECTOR_OFFSET = 0x17 # Only for retail releases, not for demo / taiken builds
HIDDEN_FS_HEADER_OFFSET = ( DISC_STARTING_PAD_SIZE + ( DISC_SECTOR_SIZE * HIDDEN_FS_HEADER_SECTOR_OFFSET ) )

# Flags for Xenogears directory entry structures
class eDirEntryFlag:
    FLAG_DIR_FILE_ENTRY          = 0
    FLAG_DIR_BEGIN_SUB_DIRECTORY = 1
    FLAG_DIR_EMPTY_FILE          = 2
    FLAG_DIR_UNUSED_FILE         = 3
    FLAG_DIR_END                 = 4

# Used exclusively for the Japanese Taikenban / Demo of Xenogears
class DirEntry97_t:
    def __init__(self):
        self.nSectorNum: int = 0 # 0x00 - Sector Offset
        self.nFileSize:  int = 0 # 0x04 - File Size and flags

        # Custom entries not apart of the structure
        self.nIndex:       int = 0
        self.nSectorCount: int = 0
        self.nFolder:      int = -1 # Only used in Xenogears

    def get_entry_size(): return 8

    def get_entry_type(self):
        if self.nSectorNum > 0  and self.nFileSize > 0:  return eDirEntryFlag.FLAG_DIR_FILE_ENTRY
        if self.nSectorNum > 0  and self.nFileSize < 0:  return eDirEntryFlag.FLAG_DIR_BEGIN_SUB_DIRECTORY
        if self.nSectorNum > 0  and self.nFileSize == 0: return eDirEntryFlag.FLAG_DIR_EMPTY_FILE
        if self.nSectorNum == 0 and self.nFileSize == 0: return eDirEntryFlag.FLAG_DIR_UNUSED_FILE
        if self.nSectorNum == -1:                        return eDirEntryFlag.FLAG_DIR_END

    def read(self, in_byte_array):
        self.nSectorNum = int.from_bytes(in_byte_array.read(4), "little", signed=True)
        self.nFileSize  = int.from_bytes(in_byte_array.read(4), "little", signed=True)

    def get_valid_entries(self, in_dir_entry_list: list) -> list:
        out_dir_entry_list = []

        for idx, entry in enumerate(in_dir_entry_list):
            match(entry.get_entry_type()):
                case eDirEntryFlag.FLAG_DIR_END:
                    print(f"{CYAN}{len(out_dir_entry_list)} / {len(in_dir_entry_list)} valid entries.{RESET}")
                    return out_dir_entry_list
                case _:
                    entry.nIndex = idx
                    entry.nSectorCount = in_dir_entry_list[idx + 1].nSectorNum - in_dir_entry_list[idx].nSectorNum
                    out_dir_entry_list.append(entry)

    def print(self):
        match(self.get_entry_type()):
            case eDirEntryFlag.FLAG_DIR_BEGIN_SUB_DIRECTORY: print(f"{GREEN}", end="")
            case eDirEntryFlag.FLAG_DIR_FILE_ENTRY:          print(f"{CYAN}",  end="")
            case eDirEntryFlag.FLAG_DIR_UNUSED_FILE:         print(f"{RED}",   end="")
            case eDirEntryFlag.FLAG_DIR_EMPTY_FILE:          print(f"{RED}",   end="")
            case eDirEntryFlag.FLAG_DIR_END:                 print(f"{RED}",   end="")

        print(f"nIdx {self.nIndex:<4} ", end="")
        print(f"nSectorNum {self.nSectorNum:<6} ", end="")
        print(f"nSectorCount {self.nSectorCount:<6} ", end="")
        print(f"nFileSize {self.nFileSize:<6} ", end="")
        print(f"{RESET}", end="")

# Used for every Xenogears release post Japanese Taikenban demo
class DirEntry98_t:
    def __init__(self):
        self.nSectorNum: int = 0 # 0x00 - Sector Offset
        self.nFileSize:  int = 0 # 0x03 - File Size and flags

        # Custom entries not apart of the structure
        self.nIndex:       int = 0
        self.nSectorCount: int = 0
        self.nFolder:      int = -1

    def get_entry_size(): return 7

    def get_entry_type(self):
        if self.nSectorNum > 0  and self.nFileSize > 0:  return eDirEntryFlag.FLAG_DIR_FILE_ENTRY
        if self.nSectorNum > 0  and self.nFileSize < 0:  return eDirEntryFlag.FLAG_DIR_BEGIN_SUB_DIRECTORY
        if self.nSectorNum > 0  and self.nFileSize == 0: return eDirEntryFlag.FLAG_DIR_EMPTY_FILE
        if self.nSectorNum == 0 and self.nFileSize == 0: return eDirEntryFlag.FLAG_DIR_UNUSED_FILE
        if self.nSectorNum == -1:                        return eDirEntryFlag.FLAG_DIR_END

    def read(self, in_byte_array):
        self.nSectorNum = int.from_bytes(in_byte_array.read(3), "little", signed=True)
        self.nFileSize  = int.from_bytes(in_byte_array.read(4), "little", signed=True)

    def get_valid_entries(self, in_dir_entry_list: list) -> list:
        out_dir_entry_list = []

        for idx, entry in enumerate(in_dir_entry_list):
            match(entry.get_entry_type()):
                case eDirEntryFlag.FLAG_DIR_END:
                    print(f"{CYAN}{len(out_dir_entry_list)} / {len(in_dir_entry_list)} valid entries.{RESET}")
                    return out_dir_entry_list
                case _:
                    entry.nIndex = idx
                    entry.nSectorCount = in_dir_entry_list[idx + 1].nSectorNum - in_dir_entry_list[idx].nSectorNum
                    out_dir_entry_list.append(entry)

    def print(self):
        match(self.get_entry_type()):
            case eDirEntryFlag.FLAG_DIR_BEGIN_SUB_DIRECTORY: print(f"{GREEN}", end="")
            case eDirEntryFlag.FLAG_DIR_FILE_ENTRY:          print(f"{CYAN}",  end="")
            case eDirEntryFlag.FLAG_DIR_UNUSED_FILE:         print(f"{RED}",   end="")
            case eDirEntryFlag.FLAG_DIR_EMPTY_FILE:          print(f"{RED}",   end="")
            case eDirEntryFlag.FLAG_DIR_END:                 print(f"{RED}",   end="")

        print(f"nIdx {self.nIndex:<4} ", end="")
        print(f"nSectorNum {self.nSectorNum:<6} ", end="")
        print(f"nSectorCount {self.nSectorCount:<8} ", end="")
        print(f"nFileSize {self.nFileSize:<10} ", end="")
        print(f"{RESET}", end="")

# Used for every release of Chrono Cross and Dewprism / Threads of Fate
class DirEntry99_t:
    def __init__(self):
        self.nSectorNum:   int  = 0 # 0x00 : 23 - Sector Offset
        self.bEmpty:       bool = 0 # 0x00 :  1 - TRUE if this entry is empty and contains no data
        self.nUnusedBytes: int  = 0 # 0x03 - Number of unused bytes within last sector ( nUnusedBytes * 8 )

        # Custom entries not apart of the structure
        self.nIndex:       int = 0
        self.nSectorCount: int = 0
        self.nFileSize:    int = 0

    def get_entry_size(): return 4

    def read(self, in_byte_array):
        inData = int.from_bytes(in_byte_array.read(3), "little", signed=False)

        self.nSectorNum = inData & 0x7FFFFF # Extract sector number ( 23 bits )
        self.bEmpty     = inData >> 23      # Extract flag ( Remaining bit )

        self.nUnusedBytes = int.from_bytes(in_byte_array.read(1), "little", signed=False)

    def print(self):
        if self.bEmpty:
            print(f"{RED}", end="")
        print(f"nIdx {self.nIndex:<4} ", end="")
        print(f"nSectorNum {self.nSectorNum:<6} ", end="")
        print(f"bEmpty {self.bEmpty:<2} ", end="")
        print(f"nUnusedBytes {self.nUnusedBytes:<6} ", end="")
        print(f"nSectorCount {self.nSectorCount:<8} ", end="")
        print(f"nFileSize {self.nFileSize:<10} ", end="")
        print(f"{RESET}", end="")

    def get_valid_entries(self, in_dir_entry_list: list) -> list:
        out_dir_entry_list = []

        for idx, entry in enumerate(in_dir_entry_list):
            entry.nSectorCount = in_dir_entry_list[idx + 1].nSectorNum - in_dir_entry_list[idx].nSectorNum

            if entry.nSectorCount < 0:
                print(f"{CYAN}{len(out_dir_entry_list)} / {len(in_dir_entry_list)} valid entries.{RESET}")
                return out_dir_entry_list
            
            entry.nIndex = idx
            entry.nFileSize = entry.nSectorCount * DISC_SECTOR_DATA_SIZE
            entry.nFileSize -= ( entry.nUnusedBytes * 8 )

            out_dir_entry_list.append(entry)

# Used for every release of Chrono Cross and Dewprism / Threads of Fate
# Xenogears used an earlier version of this that only had a string field ( DS01_XENOGEARS or DS02_XENOGEARS )
class Hed_t:
    def __init__(self):
        self.nDiscNum:   int = 0  # 0x00 - Disc number ( 1 or 2 )
        self.nNumDiscs:  int = 0  # 0x02 - Total number of discs ( Expected to be 2 )
        self.IDSector:   int = 0  # 0x04 -
        self.IDSize:     int = 0  # 0x06 -
        self.DirSector:  int = 0  # 0x08 - Sector Offset to directory
        self.DirSize:    int = 0  # 0x0A - Size in bytes of the directory
        self.UnkSector:  int = 0  # 0x0C - Sector Offset of unknown data used as reference for where data is
        self.UnkSize:    int = 0  # 0x0E -
        self.pad:        int = 0  # 0x10 - Padding
        self.szTitleID:  str = "" # 0x20 - Title ID ( Null-terminated string )

    def verify(self):
        if self.nDiscNum != 1 and self.nDiscNum != 2:
            print(f"{RED}[HED_T] - Disc Number not 1 or 2, not valid header, found {self.nDiscNum}{RESET}")
            return False

        if self.nNumDiscs != 2:
            print(f"{RED}[HED_T] - Number of discs not 2, not valid header, found {self.nNumDiscs}{RESET}")
            return False
        
        if self.DirSize < 0:
            print(f"{RED}[HED_T] - Dir Size less than 0?, found {self.DirSize}{RESET}")
            return False

        if self.szTitleID == "":
            print(f"{RED}[HED_T] - Disc Name not valid, did not find a string at expected offset.{RESET}")
            return False
        
        return True

    def read(self, in_byte_array):
        self.nDiscNum  = readU16(in_byte_array)
        self.nNumDiscs = readU16(in_byte_array)
        self.IDSector  = readU16(in_byte_array)
        self.IDSize    = readU16(in_byte_array)
        self.DirSector = readU16(in_byte_array)
        self.DirSize   = readU16(in_byte_array)
        self.UnkSector = readU16(in_byte_array)
        self.UnkSize   = readU16(in_byte_array)
        self.pad       = in_byte_array.read(16)
        self.szTitleID = readString(in_byte_array)  

        if self.verify():
            return True
        else:
            return False

    def print(self):
        print("HED_T")
        print(f"nDiscNum:  {self.nDiscNum}"  )
        print(f"nNumDiscs: {self.nNumDiscs}" )
        print(f"IDSector:  {self.IDSector}"  )
        print(f"IDSize:    {self.IDSize}"    )
        print(f"DirSector: {self.DirSector}" )
        print(f"DirSize:   {self.DirSize}"   )
        print(f"UnkSector: {self.UnkSector}" )
        print(f"UnkSize:   {self.UnkSize}"   )
        print(f"pad:       {self.pad}"       )
        print(f"szTitleID: {self.szTitleID}" )
