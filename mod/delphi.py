#!python3

# delphi to python

import os, io, re

rfIgnoreCase = 1
rfReplaceAll = 2

def trim(strt:str) -> str:
    return strt.strip()

def copy(strt:str, spos : int, count: int = -1) -> str:
    spos = spos - 1
    if count == -1 :
        return strt[spos:]
    else:
        return strt[spos:count]

def pos(sub, strt : str) -> int:
    return (strt.find(sub) + 1)

def Length(strt:str) -> int:
    return len(strt)

""" inc 함수 이나 꼭 리턴값을 이용하여야 함"""
def Inc(val : int) -> int:
    return val + 1


# TODO: 더 추가 필요
class TStringList:
    Strings = []
    
    def __init__(self, intarray:list = None) -> None:
        if intarray != None:
            self.Strings = intarray
        else:
            self.Strings = []

    def LoadFromFile(self, filename:str, enc :str = 'utf-8'):
        handle = io.FileIO(filename, 'rb')
        temp = handle.readlines()
        for v in temp:
            t = v.decode(enc)
            t = t.replace('\n', '')
            t = t.replace('\r', '')
            self.Strings.append(t)
    
    def count(self) -> int:
        return len(self.Strings)

    def _get_Text(self) -> str:
        result = ""
        for v in self.Strings:
            result = result + v + '\r\n'
        return result

    def _set_Text(self, intext:str):
        self.Strings.clear()
        self.Strings.append(intext)

    Text = property(_get_Text, _set_Text)

    # 이렇게 도 할 수 있음
    # @property
    # def Text(self) ....
    # @Text.setter
    # def Text(self, intext)  ....

    def insert(self, position:int, intext:str):
        self.Strings.insert(position, intext)

# StringReplace(dst.Strings[positon],ReplaceValue,'',[rfIgnoreCase])
def StringReplace(dststr : str, findval:str, changeval:str, opt:list) -> str:
    if rfReplaceAll in opt:
        repcount = 0
    else:
        repcount = 1
    if rfIgnoreCase in opt:
        hh = re.compile(re.escape(findval), re.IGNORECASE)
        result = hh.sub(changeval, dststr, count=repcount)
    else :
        hh = re.compile(re.escape(findval))
        result = hh.sub(changeval, dststr, count=repcount)

    return result
