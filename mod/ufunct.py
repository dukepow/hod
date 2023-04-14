#!python
# -*- coding: utf8 -*-

import sys, os  #noqa
# sys.path.append(r'../module')
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import pandas as pd
import multipart as mp
from multipart import to_bytes
import UJlib as ulib
from utemple_lib import *
import io
from mod.delphi import *


"""여기서 모든 걸 만들어서 리턴하자"""
class Tuser:

    zRootHtml = TStringList()  #출력할 html
    zReplaceHtml = list()  #임시 잘라놓은 html
    zFormData = dict()  #넘어온 값들
    zSessData = list()  #세션으로 저장된 자료
    zHtmlFileType = list()  #zRootHtml 의 파일 형식
    zHtmlDocumentRoot : str  #html 파일 경로
    zReplaceResult = dict()  #result 정보
    ztdcount : int 
    zRsRow : int # 게시판리스의 줄수

    def __init__(self) -> None:
        """출력할 html"""
        # self.zRootHtml : TStringList()  #출력할 html
        # self.zReplaceHtml : list()  #임시 잘라놓은 html
        # self.zFormData = dict()  #넘어온 값들
        # self.zSessData : list()  #세션으로 저장된 자료
        # self.zHtmlFileType : list()  #zRootHtml 의 파일 형식
        # self.zHtmlDocumentRoot : str  #html 파일 경로
        # self.zReplaceResult : dict()  #result 정보
        # self.ztdcount : int 
        # self.zRsRow : int # 게시판리스의 줄수

    def fcOutHtml(self) -> bytes:
        result = b''.join(self.zRootHtml)
        return result

    def fcFormDataAdd(self, AFieldName, AFieldValue : str):
        self.zFormData[AFieldName.lower()] = AFieldValue
        # zFormData.ContentFields.Values[LowerCase(AFieldName)] = AFieldValue

    def fcReplaceResultAdd(self, AFieldName, AFieldValue : str):
        self.zReplaceResult[AFieldName.lower()] = AFieldValue

    def fcFormDataAddStrings(self, AStrs : list):
        for v in AStrs:
            d = v.split(sep='=', maxsplit=1)
            self.zFormData[d[0].lower()] = d[1]
    
    def fcFormDataAddStrings(self, AStrs : dict):
        self.zFormData.update(AStrs)
        

    def fcFormDataInsert(self, AStr : str):
        AStr = AStr.trim()
        if ulib.explode(AStr, '=', 1) != '':
            self.zFormData[ulib.explode(AStr, '=', 0)] = ulib.explode(AStr, '=', 1)

    def fcFormDataParamInsert(self, AParam : str):
        for v in AParam.split('&'):
            self.fcFormDataInsert(v)

    def DataClear(self):
        self.zReplaceResult = []
        self.fcFormDataAdd('v','')
        self.fcFormDataAdd('src','')
        self.fcFormDataAdd('width','')
        self.fcFormDataAdd('height','')
        self.fcFormDataAdd('img','')
        self.fcFormDataAdd('target','')
        self.fcFormDataAdd('guest','')
        self.fcFormDataAdd('type','')
        self.fcFormDataAdd('frmcheck','')
        self.fcFormDataAdd('temp','')
        self.fcFormDataAdd('href','')
        self.fcFormDataAdd('action','')
        self.fcFormDataAdd('n','')
        self.fcFormDataAdd('step','')
        self.fcFormDataAdd('skin','')
        self.fcFormDataAdd('frmisnan','')
        self.fcFormDataAdd('frmischeck','')
        self.fcFormDataAdd('frmisdate','')
        self.fcFormDataAdd('multiimg','')
        self.fcFormDataAdd('multi','')
        self.fcFormDataAdd('name','')

    def fcf(self, Aname:str) -> str:  # zFormdata 에서 값 찾아줌
        try:
            return self.zFormData[Aname]
        except :
            return ""
        

    def fcr(self, Aname:str) -> str :
        try:
            return self.zReplaceResult[Aname]
        except:
            return ""

    def fcDomain2DirFix(self, AUrl : str) -> str :
        if AUrl.find('/') == 1:
            return ulib.WindowsDirFixup(self.fcf('documentroot') + AUrl)
        else:
            return ulib.WindowsDirFixup(self.zHtmlDocumentRoot + AUrl)


    def fcCuttingTag(self, startline : int, starttag, endtag : str, allcount : int)  -> dict():
        Result = dict()
        k = startline
        ps = self.zRootHtml[k].find(starttag)
        self.zRootHtml[k] = self.zRootHtml[k].replace(starttag, '')
        self.zReplaceHtml = []
        
        while self.zRootHtml[k].find(endtag) == -1 :
            k = k + 1
        
        pe = self.zRootHtml[k].find(endtag)
        self.zRootHtml[k] = self.zRootHtml[k].replace(endtag, '')
        
        if k == startline :
            self.zReplaceHtml.add(self.zRootHtml[k][ps:pe-ps])
            self.zRootHtml[k] = self.zRootHtml[k].replace(self.zRootHtml[k][ps:pe-ps], '')
        elif k > startline :
            for i in {startline:k} :
                if i == startline:
                    self.zReplaceHtml.add(self.zRootHtml[startline][ps:])
                    self.zRootHtml[startline] = self.zRootHtml[startline].replace(self.zRootHtml[startline][ps:],'')
                elif i == k :
                    self.zReplaceHtml.add(self.zRootHtml[startline][:pe])
                    self.zRootHtml[startline+1] = self.zRootHtml[startline+1].replace(self.zRootHtml[startline][:pe],'')
                else :
                    self.zReplaceHtml.add(self.zRootHtml[startline+1])
                    self.zRootHtml.delete(startline+1)
                    allcount = allcount - 1

    def fcArrayInsert(self, insline:int, destList : list, orgList : list):
        for i in range(len(orgList)-1,-1,-1):
            destList.insert(insline, orgList[i])

    def fcArrayReplace(self, insline:int, Replstr : str, destList : list, orgList : list):
        destList.insert(insline+1,'')
        destList[insline+1] = copy(destList[insline], pos(Replstr,destList[insline])+Length(Replstr))
        destList[insline] = copy(destList[insline],1,pos(Replstr,destList[insline])-1)
        for i in range(len(orgList)-1,-1,-1):
            destList.insert(insline+1,orgList[i])
  # publlist,  # construlate:
    # destructor Destroy; override;

if __name__=='__main__':
    l = Tuser()
    l.fcFormDataAdd("tttt","hhhh")
    print(l.zFormData.get("tttt"))

    

    # rs = io.FileIO("J:\dukepow\_SRC\python\HoD\www\imgsubmit1.sod")
    # l.zRootHtml = rs.readlines()
    # temp = []
    # for v in l.zRootHtml:
    #     t = v.decode('UTF-8')
    #     temp.append( t )
    # # print(temp)

    l.zRootHtml.LoadFromFile("J:\dukepow\_SRC\python\HoD\www\imgsubmit1.sod")
    temp = l.zRootHtml

    rootcount = temp.count()
    print(rootcount)
    
    srclist = TStringList(['fdgsgsdgersgrtesfdghser'])

    i = 0
    while i < rootcount:
        ReplaceValue = ParseTag(temp.Strings[i])
        print(ReplaceValue)
        if ParseTag_Name(ReplaceValue) == 'incfile':
            print("=================================")
            ParseStrRep(temp, ReplaceValue, srclist, i, rootcount)
        i = Inc(i)
        #TODO: 문제 있음

    print(temp.Text)

    # l.fcArrayReplace(2,, l.zRootHtml, l.zRootHtml)
    # print(ot)