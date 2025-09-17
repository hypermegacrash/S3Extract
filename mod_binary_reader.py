
import struct

file_endianness = {
    "little": "<",
    "big":    ">"
}

def __readFormat(inFile, format, endianness): 
    format = endianness + format
    buffer = inFile.read(struct.calcsize(format))
    return struct.unpack(format, buffer)[0]

def readS8(inFile):   return __readFormat(inFile, "b", file_endianness["little"])
def readU8(inFile):   return __readFormat(inFile, "B", file_endianness["little"])
def readS16(inFile):  return __readFormat(inFile, "h", file_endianness["little"])
def readU16(inFile):  return __readFormat(inFile, "H", file_endianness["little"])
def readS32(inFile):  return __readFormat(inFile, "i", file_endianness["little"])
def readU32(inFile):  return __readFormat(inFile, "I", file_endianness["little"])
def readS64(inFile):  return __readFormat(inFile, "q", file_endianness["little"])
def readU64(inFile):  return __readFormat(inFile, "Q", file_endianness["little"])
def readF32(inFile):  return __readFormat(inFile, "f", file_endianness["little"])
def readF64(inFile):  return __readFormat(inFile, "d", file_endianness["little"])
def readChar(inFile): return __readFormat(inFile, "c", file_endianness["little"])
def readString(inFile):
        string_bytes = bytearray()
        while True:
            byte = inFile.read(1)
            if not byte:  # End of file
                return string_bytes.decode('utf-8') if string_bytes else None
            if byte == b'\x00':  # Null terminator
                return string_bytes.decode('utf-8')
            string_bytes.extend(byte)