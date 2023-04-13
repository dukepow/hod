#!python
# -*- coding: utf8 -*-

import pandas as pd
import multipart as mp
from multipart import to_bytes
import UJlib as ulib

class Tuser:

    def __init__(self) -> None:
        self.zRootHtml : list()  #출력할 html
        self.zReplaceHtml : list()  #임시 잘라놓은 html
        self.zFormData = dict()  #넘어온 값들
        self.zSessData : list()  #세션으로 저장된 자료
        self.zHtmlFileType : list()  #zRootHtml 의 파일 형식
        self.zHtmlDocumentRoot : str  #html 파일 경로
        self.zReplaceResult : dict()  #result 정보
        self.ztdcount : int 
        self.zRsRow : int # 게시판리스의 줄수

    def fcFormDataAdd(self, AFieldName, AFieldValue : str):
        self.zFormData[AFieldName.lower()] = AFieldValue
        # zFormData.ContentFields.Values[LowerCase(AFieldName)] = AFieldValue

    def fcReplaceResultAdd(self, AFieldName, AFieldValue : str):
        self.zReplaceResult[AFieldName.lower()] = AFieldValue

    def fcFormDataAddStrings(self, AStrs : list):
        for v in AStrs:
            d = v.split(sep='=', maxsplit=1)
            self.zFormData[d[0].lower()] = d[1]
        

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
        return self.zFormData[Aname]

    def fcr(self, Aname:str) -> str :
        return self.zReplaceResult[Aname]

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
    # public
    # constructor Create;
    # destructor Destroy; override;

if __name__=='__main__':
    l = Tuser()
    l.fcFormDataAdd("tttt","hhhh")
    print(l.zFormData.get("tttt"))