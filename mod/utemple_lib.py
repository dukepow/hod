#!python
# -*- coding: utf8 -*-

import sys, os  #noqa
# sys.path.append(r'../module')
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from mod import ufunct
from mod import UJlib as ulib

from mod.delphi import *

# def ParseTag_Name(str : String) : String;
# def ParseTag_Text(strt, stro : String) :String;
# def ParseTag(strt : String) : String;
# def ParseTag_List(strt : String) : TStringList;
# def ParseTag_Value(str : String; idx : integer = 0) : String;
# def ParseTag_quot(strt : String) : String;
# def ParseTag_Insert(strt,stro : String) : String;
# def ParseStrRep(dst, src, rep : String) : String; overload;
# def ParseStrRep(var dst : TStringList; ReplaceValue: String; strlist : TStringList;
#   positon : integer; var rootcount : integer) : boolean; overload;
# def  GenKeyForCase(CaseValue : String; const RandomKey : Word = 0) : Cardinal;


#*****************************************************#
#    투명태그에 변수값 insert
#************************************************Jun**#
def ParseTag_Insert(strt : str, stro: str) -> str:
    result = strt
    stro =  trim(stro)

    if pos('>', strt) > 0:
        result = copy(strt,1,pos('>',strt)-1)
    if pos(' ',strt) > 0 :
        result = result + '&' + stro + '>'
    else:
        result = result + ' ' + stro + '>'
    return result

#*****************************************************#
#     parse 투명태그 이름빼내기 없으면 "";
#************************************************Jun**#
def ParseTag_Name(strt : str) -> str:
    result = ''
    if pos('<!@',strt) > 0 :
        strt = copy(strt,pos('<!@',strt)+3,Length(strt))
    if pos(' ',strt) > 0 :
        strt = copy(strt,1,pos(' ',strt)-1)
    else:
        strt = copy(strt,1,pos('>',strt)-1)
    return strt

#*****************************************************#
#     strt에서 stro의 투명태그가 있는지 체크하고
#     해당 투명태그부분을 리턴 없으면 ""
#************************************************Jun**#
def ParseTag_Text(strt : str, stro : str) ->str:
    result = ''
    if not (pos('<!@', stro) > 0) :	
        stro = '<!@'+stro

    if (pos(strt,stro) == 0) :
        result = ''
    else:
        if (pos('>',strt) > 0) :
            result = copy(strt,0,pos('>',strt)+1)
    return result

#*****************************************************#
#     ParseTag_Text결과 투명태그 변수 Text만 빼내기 없으면 ""
#************************************************Jun**#
def ParseTag_Value(str : str, idx : int = 0) -> str:
    result = '';
    str = trim(str);
    if (pos(' ',str) > 0) :
        result = copy(str,pos(' ',str)+1,pos('>',str)-pos(' ',str)-1);
    if idx > 0 :
        result = ulib.explode(result,'&',idx-1)

    return result


#*****************************************************#
#     strt에서 투명태그가 있는지 체크하고
#     해당 투명태그부분을 리턴 없으면 ""
#************************************************Jun**#
def ParseTag(strt : str) -> str:
    if pos('<!@',strt) > 0 :
        strt = copy(strt,pos('<!@',strt),Length(strt))
        strt = copy(strt,1,pos('>',strt))
    return strt

#*****************************************************#
#     strt에서 " 표가 있는지 체크하고
#     해당 "부분을 제거해서 리턴
#************************************************Jun**#
def ParseTag_quot(strt : str) -> str:
    strt = trim(strt)

    if pos('"',strt) == 1 :
        strt = copy(strt,2,Length(strt)-2)
    return strt

#*****************************************************#
#     strt에서 투명태그가 있는지 체크하고
#     해당 투명태그부분을 리턴 없으면 ""
#************************************************Jun**#
def ParseTag_List(strt : str) -> list:
    result = []
    
    temp = strt
    while pos('<!@',temp) > 0 :
        temp = copy(temp,pos('<!@',temp),-1)
        re = copy(temp,1,pos('>',temp));
        result.append(re)
        temp = copy(temp,Length(re),-1)

    return result

#stringreplace
def ParseStrRep(dst : str , src : str, rep : str) -> str:
    return dst.replace(src, ParseTag_quot(rep) )


#stringreplace
# dst 에 position 에 strlist를 삽입
def ParseStrRep(dst : TStringList, ReplaceValue: str, strlist : TStringList, positon : int, rootcount : int) -> bool:

    # dst.Strings[positon] =  dst.Strings[positon].replace(ReplaceValue,'')
    dst.Strings[positon] =  StringReplace(dst.Strings[positon],ReplaceValue,'',[rfIgnoreCase])
    # dst.BeginUpdate;
    print(strlist.count())
    for i in range(strlist.count()-1, -1, -1):
    # for i = strlist.Count-1 downto 0 do
        dst.insert(positon,strlist.Strings[i])
        rootcount = Inc(rootcount)
    
    return True

# def GenKeyForCase(CaseValue : str, RandomKey : Word = 0) : Cardinal;
# var
#  I, Ln : Cardinal;
# begin
#  Result = 0;
#  Ln = Length(CaseValue);
#  if Ln<1 then Exit;
#  for I=1 to Ln
#      do Result = Result + ((Ord(CaseValue[I]) xor (Randomkey * I))) shl ((I and 3) shl 3);
#  Result = Result + 1;
# end;


if __name__ == "__main__":
    print(Length("12345"))
