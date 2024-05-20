#!/usr/bin/python

import mmap, os

directory = '.'

pngMagicNumberBegin=b"\x89\x50\x4e\x47"
pngMagicNumberEnd=b"\x49\x45\x4e\x44\xae\x42\x60\x82"
    
def exctractPNG(filename):
    with open(filename+".lnb", "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)
        pngIndexBeging=mm.find(pngMagicNumberBegin)
        pngIndexEnd=mm.find(pngMagicNumberEnd)
        pngSize=(pngIndexEnd-pngIndexBeging)
        if(pngIndexEnd>pngIndexBeging>-1):
            with open (filename+".png", "wb") as outFile:
                outFile.write(mm[pngIndexBeging:pngIndexEnd+len(pngMagicNumberEnd)])
                outFile.close()
            mm.close()
            print(f"{pngSize} Bytes written to {filename}.png")


for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        file_name, file_extension = os.path.splitext(f)
        if(file_extension==".lnb"):
            exctractPNG(file_name)