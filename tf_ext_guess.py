
# Transformer that identifies files by using heuristics to guess what file extension this might be

from mod_color import *

class transformer_ext_guess():
    color = YELLOW

    def __init__(self):
        self.file_ext = ".dat" # Everything's a .dat until proven otherwise

def xg_guess_file_type(in_data_buffer):
    return ".dat" # Unknown Binary Data

def cc_guess_file_type(in_data_buffer):
    if len(in_data_buffer) == 0x08: # dummy
        return ".dummy"
    
    if len(in_data_buffer) == 0x18: # It's CDMAKE Dummy !
        # Original filename is dummy.dat
        return ".cdmake"
    
    try:
        if int.from_bytes(in_data_buffer[0:4], "little") == 0x10:
            return ".tim"
    except: pass
    
    try:
        if int.from_bytes(in_data_buffer[0:4], "little") == 1329679169: # AKAO
            return ".akao"
    except: pass

    try:
        if int.from_bytes(in_data_buffer[128:132], "little") == 1329679169: # AKAO
            return ".stv"
    except: pass

    try:
        if int.from_bytes(in_data_buffer[0:4], "little") == 7369316: # drp 
            return ".prd"
    except: pass
    

    return ".dat" # Unknown Binary Data
    try:
        if in_data_buffer[0:7].decode("utf-8") == "BGMPACK":
            return ".bgm" # BackGround Music
    except: pass

def dp_guess_file_type(in_data_buffer):
    try:
        if in_data_buffer[0:7].decode("utf-8") == "BGMPACK":
            return ".bgm" # BackGround Music
    except: pass

    try:
        if in_data_buffer[0:7].decode("utf-8") == "SFXPACK":
            return ".sfx" # Sound Effects
    except: pass

    try:
        test = int.from_bytes(in_data_buffer[0:4], "little")
        testB = int.from_bytes(in_data_buffer[4:8], "little")
        testC = int.from_bytes(in_data_buffer[8:12], "little")
        testD = int.from_bytes(in_data_buffer[12:16], "little")
        testE = int.from_bytes(in_data_buffer[16:20], "little")

        if test == 0 and testB == 0 and testC == 0 and testD == 0 and testE != 0:
            return ".adpcm" # Audio ADPCM Data
    except: pass

    try:
        test = int.from_bytes(in_data_buffer[32:36], "little")

        if test == 305419896:
            return ".chr" # Character Bin (Model, Texture, Animation, etc.)
    except: pass

    # Variant of character bin file, I believe these have no skeletons
    # It is read the same way as .chr so giving it the same extension
    try:
        test = int.from_bytes(in_data_buffer[8:12], "little")

        if test == 0x20:
            return ".chr"
    except: pass

    # I think this is event specific animation data
    # Kept seperate so chrs dont load more animations than they need
    try:
        test = int.from_bytes(in_data_buffer[0:4], "little")
        testB = int.from_bytes(in_data_buffer[8:12], "little")

        if test == 0 and testB == 0x14:
            return ".anm"
    except: pass 

    try:
        testA = int.from_bytes(in_data_buffer[0:4], "little")

        testB = int.from_bytes(in_data_buffer[15:16], "little")
        testC = int.from_bytes(in_data_buffer[16:17], "little")
        testD = int.from_bytes(in_data_buffer[17:18], "little")
        testE = int.from_bytes(in_data_buffer[18:19], "little")
        testF = int.from_bytes(in_data_buffer[19:20], "little")

        if testA == 0x00:
            if testB == 0x01:
                if testC == 0x10:
                    if testD == 0x00:
                        if testE == 0x01:
                            if testF == 0x00:
                                return ".mtd" # Map Texture Data

    except: pass

    try:
        testA = int.from_bytes(in_data_buffer[3:4], "little")
        testB = int.from_bytes(in_data_buffer[5:6], "little")
        testC = int.from_bytes(in_data_buffer[6:7], "little")
        testD = int.from_bytes(in_data_buffer[7:8], "little")
        testE = int.from_bytes(in_data_buffer[9:10], "little")

        if testA == 0x00:
            if testB == 0x00:
                if testC == 0x01:
                    if testD == 0x00:
                        if testE == 0x00:
                            return ".mmd" # Map Model Data

    except: pass

    # Retail
    try:
        if in_data_buffer[0:5].decode("utf-8") == "nowab":
            return ".nowab"
    except: pass

    # Taikenban
    try:
        if in_data_buffer[0:5].decode("utf-8") == "NoWab":
            return ".nowab"
    except: pass

    # I believe these files will have a length field
    try: 
        test = int.from_bytes(in_data_buffer[0:4], "little")

        if test == 0:
            count = int.from_bytes(in_data_buffer[4:8], "little")
            offset = (count * 4) + 8

            testC = int.from_bytes(in_data_buffer[offset:offset+4], "little")

            if testC == len(in_data_buffer) and testC != 0:
                return ".effect"
    except: pass

    try:
        test = int.from_bytes(in_data_buffer[0:4], "little")

        testB = int.from_bytes(in_data_buffer[4:6], "little")
        testC = int.from_bytes(in_data_buffer[6:8], "little")

        testD = int.from_bytes(in_data_buffer[8:10], "little")
        testE = int.from_bytes(in_data_buffer[10:12], "little")

        testF = int.from_bytes(in_data_buffer[12:14], "little")
        testG = int.from_bytes(in_data_buffer[14:16], "little")

        if test == 0 and testB != 0 and testC == 0 and testD != 0 and testE == 0 and testF != 0 and testG == 0:
            return ".ev" # Event scripting
    except: pass

    all_null = all(b == 0 for b in in_data_buffer)
    if all_null:
        return ".empty"

    return ".dat" # Unknown Binary Data