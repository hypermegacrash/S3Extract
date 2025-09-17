
import os
import io

def get_eof(file_object):
    current_pos = file_object.tell()
    file_object.seek(0, os.SEEK_END)
    end_pos = file_object.tell()
    file_object.seek(current_pos, os.SEEK_SET) # Restore original position
    return current_pos == end_pos

def readString(inFile):
    string_bytes = bytearray()
    while True:
        byte = inFile.read(1)
        if not byte:  # End of file
            return string_bytes.decode('utf-8') if string_bytes else None
        if byte == b'\x00':  # Null terminator
            return string_bytes.decode('utf-8')
        string_bytes.extend(byte)

with open("cdrom.fnd", "rb") as inFile:
    inFile.seek(0, os.SEEK_END)
    end_pos = inFile.tell()
    inFile.seek(0, os.SEEK_SET)

    fs_strs = []

    while inFile.tell() < end_pos:
        inData = inFile.read(0x40)

        with io.BytesIO(inData) as inBuffer:
            testStr = readString(inBuffer)
            testStr = testStr.strip("C:\\")
            testStr = testStr.strip("c:\\")
            
            fs_strs.append(testStr)

    with open("fnd.csv", "w") as outcsv:
        outcsv.write("path,name\n")

        for entry in fs_strs:
            head, tail = os.path.split(entry)
            outcsv.write(f"{tail},{head}\n")
            #print(f"PATH {head} FILE {tail}\n")