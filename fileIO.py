# fileio.py

''' This file contains file I/O operations for writing and reading bytes from files.
    This is useful for the storage layer. '''

from struct import pack, unpack

''' Write value to file after converting it to ascii character (1 byte). '''
def write_byte(file, val):
    file.write(chr(val))    

''' Write value to file by packing it into short (2 bytes). '''
def write_short(file, val):
    file.write(pack('h', val)) 

''' Write value to file by packing it into unsigned short (2 bytes). '''
def write_unsigned_short(file, val):
    file.write(pack('H', val)) 
    
''' Write value to file by packing it into int (4 bytes). '''
def write_int(file, val):
    file.write(pack('i', val)) 

''' Write value to file by packing it into unsigned int (4 bytes). '''
def write_unsigned_int(file, val):
    file.write(pack('I', val)) 

''' Gets the value of the ascii character (1 byte). '''
def read_byte(byte_s):
    return ord(byte_s)
    
''' Read value of short (2 bytes). '''
def read_short(short):
    return unpack('h', short)[0] 

''' Read value of unsigned short (2 bytes). '''
def read_unsigned_short(short):
    return unpack('H', short)[0] 
    
''' Read value of int (4 bytes). '''
def read_int(short):
    return unpack('i', short)[0] 

''' Read value of unsigned int (4 bytes). '''
def read_unsigned_int(short):
    return unpack('I', short)[0] 


if __name__ == "__main__":
    file = open('test.bin', 'wb')
    write_byte(file, 10)
    write_int(file, 32768)
    write_unsigned_int(file, 1000000)
    file.close()
    file = open('test.bin', 'rb')
    while 1:
        byte_s = file.read(1)
        int = file.read(4)
        unsigned_int = file.read(4)
        if not byte_s:
            break
        print(read_byte(byte_s))
        print(read_int(int))
        print(read_unsigned_int(unsigned_int))