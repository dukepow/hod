import collections
import copy
import datetime
import math
import os
import pickle
import re
from collections import ChainMap
import pandas as pd
import json
import shutil
import progressbar

cnstequal : str = '=='
cnstNotequal : str = '!='
cnstLeftBig : str = '!G'
cnstRightBig : str = '!L'
CRLF : str = '\r\n'
CONSTSL : str = '|_#%#_|'
CONSTSP : str = '|_|%|_|'


def explode(src : str, spli: str,idx = 0):
    v = src.split(spli)
    return v[idx]

def get_dictlist_findidx(dictlist, fkey):
    """idx 를 찾아줌   이런형식 [{'11': 100},,,]"""
    idx = 0
    if len(dictlist) > 0:
        for v in dictlist:
            if fkey in v.keys():
                return idx
            idx += 1

    return -1


def get_dictlist_dict(dictlist, fkey):
    if get_dictlist_findidx(dictlist, fkey) > -1:
        return dictlist[get_dictlist_findidx(dictlist, fkey)]
        # return next((item for item in dictlist if item[fkey] != ''), False)
    else:
        return False


def get_dictlist_value_int(dictlist, fkey, DEBUGMODE=False):
    """딕리스트에서 fkey를 찾아 줌 못찾으면 0   이런형식 [{'11': 100},,,]"""

    rs = get_dictlist_dict(dictlist, fkey)
    if DEBUGMODE:
        print(rs)
    if rs == False:
        return 0
    else:
        return int(rs[fkey])


def get_dictlist_value_str(dictlist, fkey, DEBUGMODE=False):
    """딕리스트에서 fkey를 찾아 줌 못찾으면 ''  이런형식 [{'11': 100},,,]"""
    rs = get_dictlist_dict(dictlist, fkey)
    if DEBUGMODE:
        print(rs)
    if rs == False:
        return ''
    else:
        return str(rs[fkey])


def get_dictlist_sorted(dictlist):  # TODO: 아 몰라 안되
    """중복 제거 및 정렬   이런형식 [{'11':100},,,]"""
    # return dict(ChainMap(*dictlist))

    # rt = [item for item in dictlist]
    rt = sorted(dictlist, key=lambda item: [item for item in dictlist])
    print("*" * 8, [v for v in [item for item in dictlist]])

    return rt


def get_dictlist_org_findidx(dictlist, fkey, val):
    idx = 0
    for v in dictlist:
        if v[fkey] == val:
            return idx
        idx += 1
    return -1


def get_dictlist_org_only_sorted(dictlist, fkey):
    """fkey 로 정렬만 하기   이런형식 [{'code': '11', 'money': 100},,,]"""
    # return sorted(dictlist, key=lambda sss: sss[0])
    from operator import itemgetter
    # return sorted(dictlist, key=itemgetter('11'))
    return sorted(dictlist, key=lambda x: x[fkey])


def get_work_end(hms):
    """시간보다 지나갔으면 true"""
    cuttime = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d {}".format(hms)),
                                         "%Y-%m-%d %H:%M:%S")
    return (datetime.datetime.now() > cuttime)  # 시간 끝났으면 true


def get_work_end_day(day, aftday=0):
    """날짜 str 을 넣고 aftday 를 지났으면 true"""
    cuttime = datetime.datetime.strptime(day + " 23:59:59", "%Y-%m-%d %H:%M:%S")
    cuttime = cuttime + datetime.timedelta(days=aftday)
    if cuttime > datetime.datetime.now():
        return False
    else:
        return True


def list_SaveToFile(slist, file_name="sample"):
    file_name = "{}.pkl".format(file_name)
    open_file = open(file_name, "wb")
    pickle.dump(slist, open_file)
    open_file.close()


def list_LoadFromFile(file_name="sample"):
    file_name = "{}.pkl".format(file_name)
    if os.path.isfile(file_name):
        open_file = open(file_name, "rb")
        slist = pickle.load(open_file)
        open_file.close()
        return slist
    else:
        return []


def dictlist_update(source, dict, fname=""):
    """source 에서 dict 의 키가 있는지 검사하고 추가 또는 수정 한다 [{'11': 100},,,]"""
    idx = get_dictlist_findidx(source, "".join(dict.keys()))
    if idx == -1:  # 없으니가 추가
        dictlist_append(source, dict, fname)
    else:
        source[idx] = dict
        if fname != "":
            list_SaveToFile(source, fname)

    return source


def dictlist_append(source, appenddict, fname=""):
    """dictlist 에 추가 해주고 저장한다 [{'11': 100},,,]"""
    source.append(appenddict)
    if fname != "":
        list_SaveToFile(source, fname)
    return source


def dictlist_delete(source, idx=-1, key="", fname=""):
    """dictlist 에서 해당 idx 나 key 값을 찾아 지워주고 저장한다 [{'11': 100},,,]"""
    if idx == -1 and key != "":
        idx = get_dictlist_findidx(source, key)

    if idx > -1:
        del source[idx]

    if fname != "":
        list_SaveToFile(source, fname)

    return source


def get_stock_diff(oldstocks, stocks):
    # return 사라진것, 생긴것
    if len(oldstocks) == 0:
        if len(stocks) == 0:
            return "0", []
        else:
            return "+", stocks
    else:
        if len(stocks) == 0:
            return "-", oldstocks
        else:
            cl_sara = [v for v in oldstocks if v not in stocks]
            cl_innun = [v for v in stocks if v not in oldstocks]

            return cl_sara, cl_innun


def get_trading_val(money, basemoney, trading, start_time="09:00:00", timegugan=6):
    """거래량 기준 뽑기 starttime=09:00:00"""
    if money > 0:
        tr = trading / (money * 1) * basemoney * 1.6
    else:
        tr = trading

    td = datetime.datetime.now() - datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d ") + start_time, "%Y-%m-%d %H:%M:%S")
    if td < datetime.timedelta(minutes=1):
        return tr
    tds = math.trunc(td.total_seconds() / 60)
    # tds = tds + 1
    print(tds)
    if tds > (timegugan * 60):
        return int(tr)
    else:
        return int(tr * (tds / (timegugan * 60)))


def get_now(type="ymd"):
    if type == "ymd":
        return datetime.datetime.now().strftime('%Y-%m-%d')
    elif type == "hms":
        return datetime.datetime.now().strftime('%H:%M:%S')
    elif type == "all":
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def RemoveChar(sSrc, CharList='~`!@#$%^&*()-+|\/<>{} '):
    """ 해당 특수문자 제거 공백도 특수문자로 취급됨"""
    # import re
    #
    # string = "Hey! What's up bro?"
    # new_string = re.sub(r"[^a-zA-Z0-9]", "", string)
    # print(new_string)
    Result = ''
    for I in range(len(sSrc)):
        if not (sSrc[I] in CharList):
            Result = Result + sSrc[I]
    return Result


def fileMove(ifile, tDir, enc=False):
    """패스가 포함된 ifile, tDir로 무브 하는데 enc=true면 새이름으로 만들고 카피"""
    # os.path.dirname  디렉토리 구하기
    # os.path.basename
    if enc:     # 일련번호먹이기
        tfile = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + os.path.basename(ifile)
        shutil.copy(ifile, tDir + tfile)
    else:
        tfile = os.path.basename(ifile)
        shutil.move(ifile, tDir + tfile)

    return tDir,  tfile


def ToDictlist(dfs):
    # dataframe 을 dictlist 로 바꾸어 준다  쓸때는 for v in dictlist    v["code"]
    if issubclass(type(dfs), pd.DataFrame):
        return dfs.to_dict('records')
    return dfs


pbar = None


def show_progress(block_num, block_size, total_size):
    """progress bar를 위한 handler"""
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None


def ExtractFileExt(filename):
    return os.path.splitext(filename)[1]


def FileExists(filename):
    return os.path.isfile(filename)

"""------------------------ 윈도우디렉토리를 정확히한다  -----------------------------"""
def WindowsDirFixup(APath:str)->str:
    APath = APath.replace('/','\\')
    APath = APath.replace('\\\\','\\')
    return APath