# -*- coding: utf-8 -*-
__author__ = 'jaehyek.choi'

"""
purpose : GQIS에 등록된 고객증상을  CSV으로 입력을 받아서, 고객증상 keyword을 뽑고, 
          keyword 간 거리가 10이고  주어 서술의 관계가 있는 pattern을 추출하고 빈도수를 산출하기 위함이다.
          "화면~깨짐" 
"""

"""
from __future__ import division
"""

import argparse
import itertools
import collections
import os
import re
import binascii
import datetime
import glob
import shutil


def main(clsvar):


    listdictfinding = [
                {"head":"업그레이드", "findORitems1":["업그레이드"]},
                {"head":"깜박", "findORitems1":["깜박"]},
                {"head":"삭제제거", "findORitems1":["삭제", "제거"], "findORitems2":["사진", "메세지", "주소록", "번호"]},
                {"head":"부족", "findORitems1":["부족"]},
                {"head":"유심", "findORitems1":["유심", "sim", "usim"]},
                {"head":"진입", "findORitems1":["진입"]},
                {"head":"스토어마켓", "findORitems1":["스토어", "마켓"], "findORitems2":["접속", "진입"]},
                {"head":"메세지", "findORitems1":["메세지", "문자", "mms", "sms"]},
                {"head":"메세지수발신", "findORitems1":["메세지", "문자", "mms", "sms"], "findORitems2":["수신", "수발신", "발신", "전송"]},
                {"head":"화면", "findORitems1":["화면"],"findORitems2":["깨짐", "깨져", "버벅", "떨림"]},
                {"head":"터치", "findORitems1":["터치"], "findORitems2":["불", "안됨", "간헐", "무감","오동작", "오류", "이상", "느림"]},
                {"head":"노크온", "findORitems1":["노크온"]},
                {"head":"배터리", "findORitems1":["배터리","충전"], "findORitems2":["소모", "충전"]},
                {"head":"카메라", "findORitems1":["카메라","camera"], "findORitems2":["전원", "화질","오류", "실행"]},
                {"head":"지문", "findORitems1":["지문"], "findORitems2":["인식"]}

                ]

    # read head
    fincsv = open(clsvar.fileincsv, encoding="utf-8")
    listheads = fincsv.readline().strip().split(",")

    # write head
    foutcsv = open(clsvar.fileoutcsv, "w", encoding="utf-8")
    foutcsv.write(",".join(listheads + [ aa["head"] for aa in listdictfinding]) + "\n" )

    countline = 2
    while(True) :
    # for line in fincsv :
        try :
            line = fincsv.readline()
        except:
            countline += 1
            print("line reading error")
            continue
        # print("line no : %s" % countline)
        if len(line) < 10 :
            break
        listitems = line.strip().split(",")
        dictitems = dict(zip(listheads, listitems))

        # first write the original items.
        foutcsv.write(",".join(listitems) + ",")

        # find items within
        for dictfinding in listdictfinding :
            found = ""
            # check if  findORitems2
            if dictfinding.get("findORitems2", 0 ) == 0 :
                # got only the findORitems1
                for strfind in dictfinding["findORitems1"] :
                    if strfind.lower() in dictitems["CAUSE_DESC"] :  # dictitems["CAUSE_DESC"] :  sentence to search
                        found = dictfinding["head"]


            else:
                # got both the findORitems1 and findORitems2
                for strfind1 in dictfinding["findORitems1"] :
                    if strfind1.lower() in dictitems["CAUSE_DESC"] :  # dictitems["CAUSE_DESC"] :  sentence to search
                        for strfind2 in dictfinding["findORitems2"] :
                            if strfind2.lower() in dictitems["CAUSE_DESC"] :  # dictitems["CAUSE_DESC"] :  sentence to search
                                found += strfind2

            foutcsv.write(found + ",")
        foutcsv.write("\n")

        countline += 1
        print(".", end="")
        if countline %50 == 0 :
            print("\n")

    foutcsv.close()
    fincsv.close()

###  note : ","은  list-up하지 않는다.  --> csv file의 구분자 이므로 .
###       : "-"은 list-up하지 않는다.  단어의 형성에 기여하므로.
listsymbolreplace = [":","/","\(","\)",".","'","?","_", "#", "+", "[", "]", "<", ">", "및"]

def replacesymbolwithspace(strline) :
    """
    keyword을 찾기전에 먼저 문장의 symbol들을 space chararcter으로 치환하고 리턴한다.
    :param strline: 
    :return: 
    """
    global  listsymbolreplace
    for symbol in listsymbolreplace :
        strline = strline.replace(symbol, " ")

    return strline

def getSymptomSegmentation(clsvar):
    # read head
    fincsv = open(clsvar.fileincsv, encoding="utf-8")
    listheads = fincsv.readline().strip().split(",")

    setSegment = set()
    countline = 0
    while (True):
        # for line in fincsv :
        countline += 1
        if  countline % 100 == 0 :
            print(".\n")
        try:
            line = fincsv.readline()
        except:
            countline += 1
            print("line reading error")
            continue

        if (len(line)) < 5 :
            break

        listitems = line.strip().split(",")
        dictitems = dict(zip(listheads, listitems))

        setSegment.update( replacesymbolwithspace(dictitems["CAUSE_DESC"]).split() )

    # pprint.pprint(setkeyword)
    foutcsv = open(clsvar.fileseqment, "w", encoding="utf-8")
    for aa in setSegment :
        foutcsv.write(aa + "\n")
    fincsv.close()
    foutcsv.close()

    print("countline : %s" % countline)

def sortKeyword(clsvar):
    listkeyword = []
    for keyword in open(clsvar.keywordprev, encoding="utf-8") :
        listkeyword.append(keyword.strip())

    listkeyword = sorted(listkeyword)
    fkeyword = open(clsvar.keywords, "w", encoding="utf-8")
    for keyword in listkeyword :
        fkeyword.write(keyword+"\n")

        fkeyword.close()

listSentenceWords = [
        "upgrade~멈춤",
        "데이터~멈춤",
        "인터넷~멈춤",
        "app~멈춤",
        "sms~멈춤",
        "설정~멈춤",

        "upgrade~꺼짐",
        "데이터~꺼짐",
        "인터넷~꺼짐",
        "app~꺼짐",
        "sms~꺼짐",
        "설정~꺼짐",

        "파일~깨짐",
        "인터넷~깨짐",

        "app~느림",
        "upgrade~느림",
        "인터넷~느림",
        "데이터~느림",

        "upgrade~reset",
        "인터넷~reset",
        "데이터~reset",
        "부팅~reset",
        "app~reset",
        "동기화~reset",

        "유투브~오류",
        "유투브~안됨",

        "카카오~오류",
        "카카오~안됨",
        "카카오~멈춤",
        "카카오~느림",

        "playstore~오류",
        "playstore~안됨",
        "playstore~멈춤",

        "갤러리~멈춤",
        "갤러리~깨짐",
        "갤러리~안됨",
        "갤러리~오류",
        "갤러리~없음",

        "비디오~깨짐",
        "비디오~끈김",
        "비디오~느림",
        "비디오~멈춤",
        "비디오~안됨",
        "비디오~없음",
        "비디오~오류",

        "카메라~꺼짐",
        "카메라~느림",
        "카메라~멈춤",
        "카메라~오류",
        "카메라~안됨",

        "usim~reset",
        "usim~안됨",
        "usim~오류",

        "터치~멈춤",
        "터치~느림",
        "터치~오류",
        "터치~안됨",

        "지문~안됨",

        "자판~오류",
        "자판~안됨",
        "자판~안뜸",
        "자판~멈춤",
        "자판~안나",
        "자판~느림",

        "tmap~안됨",
        "tmap~멈춤",
        "tmap~오류",


        "화면~검정",
        "화면~멈춤",
        "화면~안됨",
        "화면~꺼짐",
        "화면~오류",
        "화면~느림",
        "화면~깨짐",
        "화면~줄감",
        "화면~안나",
        "화면~안켜",
        "화면~안뜸",
        "화면~겹침",
        "화면~깜박",

        "hotspot~안됨",

        "메모리~인식",
        "메모리~오류",
        "메모리~멈춤",

        "이어잭~안됨",
        "이어잭~오류",
        "이어잭~안들림",

        "백업~안됨",
        "백업~오류",
        "백업~멈춤",
        "백업~느림",

        "sd~오류",
        "sd~안됨",

        "batt~소모",
        "batt~교체",
        "batt~급방",
        "batt~안됨",
        "batt~느림",
        "batt~reset",
        "batt~오류"


    ]
listoutputhead = ["MODEL","모델","WARRANTY_FLAG", "DEFECT_DESC","CRC32","CAUSE_DESC", "RCPT_DT_ORD_DT"]


def combinatekeyword(clsvar):
    global  listSentenceWords


    print("reading keywordsort keywordreplace txt")
    listkeywords = [ aa.strip().lower() for aa in open(clsvar.keywords, encoding="utf-8").readlines()]
    listlistkeywordreplace = [aa.strip().lower().split() for aa in open(clsvar.filekeyreplace, encoding="utf-8").readlines()]

    listkeywords = [ aa[0] for aa in listlistkeywordreplace] + listkeywords

    # won't find the below word
    listnotallow = [  "문의", "정상", "프로그램", "사용", "설명", "안내", "내용", "발생"]
    listkeywords = list(set(listkeywords) - set(listnotallow))
    
    # add some type keyword like as sentence which is composed as keyword~keyword
    # note :  결과에서 해당 keyword을 찾을 때, 소문자로 찾아야 한다.   TMAP --> tmap

    listSentenceWords = [aa.lower() for aa in listSentenceWords ]
    listkeywords += listSentenceWords

    print("reading input file")
    # read head
    listfincsv = open(clsvar.fileincsv,encoding="utf-8").readlines()
    listheads = listfincsv[0].strip().split(",")

    # make string lower
    print("making the input file lower()")
    listfincsv = [aa.lower() for aa in listfincsv]

    ddictlistlinenos = collections.defaultdict(list)
    countline = 0

    print("before loop of replacing keyword and finding")

    # 초기화 문구 찾을 때,
    listinitializewords = ["초기", "emergency", "이머전시", "이머젼시" ]

    for line in listfincsv[1:] :
        countline += 1
        if countline % 50 == 0 :
            print(".", end="")

        if countline % 500 == 0 :
            print("\n")

        listitems = line.strip().split(",")
        dictitems = dict(zip(listheads, listitems))

        # 초기 혹은 emergency word가 있는 경우만 처리할 경우 아래의 line을 활성화한다.
        # 즉, emergency word가 전혀 발견되지 않으면 처리하지 않는다.
        listinitword = [ (dictitems["PROC_DETAIL"].find(aa) == -1) for aa in listinitializewords ]
        if all(listinitword) == True :
            continue


        # replace the symbols with space
        strtemp = replacesymbolwithspace(dictitems["CAUSE_DESC"])

        # replace the smiliar word with listkeywordreplace[][0]
        for listkeywordreplace in listlistkeywordreplace :
            # keywordreplacehead = " " + listkeywordreplace[0] + " "
            keywordreplacehead = listkeywordreplace[0]
            for keywordreplace in listkeywordreplace :
                strtemp =  strtemp.replace(keywordreplace, keywordreplacehead)

        # find the keyword in strtemp
        listfoundkeywords = []
        for keywordsort in listkeywords :
            if "~" in keywordsort :         # find a sentence
                listsent = keywordsort.split("~")
                foundff = [aa.start() for aa in re.finditer(listsent[0], strtemp)]
                founddd = [ strtemp.find(listsent[1], aa) - aa for aa in foundff ]
                if any([(0 + len(listsent[0])) <= aa <= (10 + len(listsent[0]) ) for aa in founddd]) == True :
                    listfoundkeywords.append(keywordsort)
            else:
                if strtemp.find(keywordsort) >= 0 :
                    listfoundkeywords.append(keywordsort)

        # make the combination the found word, add the line number to ddictcount
        maxcombi = len(listfoundkeywords)
        if len(listfoundkeywords) > 2 :
            maxcombi = 2
        for combino in range(1, maxcombi+ 1 ) :
            for tuplekeyword in itertools.combinations( listfoundkeywords, combino) :
                ddictlistlinenos[tuple(sorted(tuplekeyword))].append(countline)




    # count the number of countline of combi and  ordering-down that .
    print("count the number of combi lines")
    listlistsetcount = []
    for  setlist in ddictlistlinenos.items() :
        listlistsetcount.append([setlist[0], len(setlist[1])])

    # sort the listlistsetcount
    listlistsetcount.sort(key=lambda item: item[1], reverse=True)

    # write out the content of listlistsetcount
    # keyword별  빈도수를 구한다. 이는 중요 keyword을 선택하기 위해서.
    print("writing to listlistsetcount.csv")
    fsetcount = open("listlistsetcount.csv", "w", encoding="utf-8")
    for listsetcount in listlistsetcount :
        if listsetcount[1] <  100 :
            break
        fsetcount.write(str(listsetcount[1]) + "," + str(len(listsetcount[0]))+ "," + ",".join(listsetcount[0]) + "\n")
    fsetcount.close()

    try:
        os.mkdir(clsvar.tempdir)
    except:
        pass

    countcsvout = len(listlistsetcount)
    print("the number of combination : %s"% countcsvout)
    # write the tuple  in csv file

    print("make a file for listlistsetcount")
    for listsetcount in listlistsetcount :
        countcsvout -= 1

        if listsetcount[1] < 100 :
            break
        # if len(listsetcount[0]) == 1 :
        #     continue

        print("remaind items : %s" % countcsvout)
        # print("listsetcount[0] : %s , listsetcount[1]: %s"%(listsetcount[0], listsetcount[1]))

        fcombicsv = "-".join(["%0.6d"% listsetcount[1], "_".join(listsetcount[0])]) + ".csv"
        fcombicsv =  os.path.join(clsvar.tempdir, fcombicsv)

        foutcsv = open( fcombicsv, "w", encoding="utf-8")
        foutcsv.write(",".join(listoutputhead) + "\n")
        for lineno in ddictlistlinenos[listsetcount[0]] :
            dictitems = dict(zip(listheads, listfincsv[lineno].strip().split(",")))
            crc32 = binascii.crc32(bytes(dictitems["MODEL"] + dictitems["CAUSE_DESC"] + dictitems.get("RCPT_DT_ORD_DT", "00000000")[0:8], encoding="utf-8"))
            foutcsv.write( ",".join([dictitems["MODEL"],dictitems["모델"],dictitems["WARRANTY_FLAG"],dictitems["DEFECT_DESC"], str(crc32), dictitems["CAUSE_DESC"], dictitems.get("RCPT_DT_ORD_DT", "000000")[0:6]]) +"\n")
        foutcsv.close()


def copySentenceWordsCSV(fromdir , todir, listcsv):
    """
    keysentence 의 item 이름을 포함하는 파일을 fromdir에서 todir으로 copy한다.
    이런 파일들은  두 item 이름간에는 거리가 10이내 이므로 중요한 의미를 포함한다. 
    :param fromdir: 
    :param todir: 
    :param listcsv: 
    :return: 
    """
    global listSentenceWords
    try:
        os.mkdir(todir)
    except:
        pass

    for csvitem in listcsv :
        filetemp =  os.path.join(fromdir, "*[0-9]-" + csvitem + ".csv" )
        for fname in glob.glob( filetemp) :
            shutil.copy2(fname, todir)


def groupSentensceByCoreWord(clsvar) :
    """
    listSentenceWords은 dir dest에서의 csv file 이름들의 list이다. 여기서  같은 key에 해당하는 file들은  하나의 file으로 통합한다.
    :param clsvar: 
    :return: 
    """
    global  listSentenceWords

    listcoreword = ["멈춤", "꺼짐", "깨짐", "느림", "reset", "유투브", "카카오", "playstore",
                    "갤러리", "비디오", "카메라", "usim", "터치", "지문", "자판", "tmap", "화면",
                    "hotspot", "데이터", "스미싱", "메모리", "이어잭", "백업", "sd", "batt" ]
    try:
        os.mkdir(clsvar.fileoutdir)
    except:
        pass

    for coreword in listcoreword :
        listSentenceCore = [ aa for aa in listSentenceWords if coreword in aa ]

        # first,create output file
        foutcsv = open( os.path.join(clsvar.fileoutdir, coreword+".csv"), "wb")



        # write the CSV head + "feature"  for core kinds
        foutcsv.write((",".join(listoutputhead) + ",feature \n").encode("cp949"))

        # create the defaultdict and count the unique crc .
        dictmodelset = collections.defaultdict(set)
        for SentenceCore in listSentenceCore :
            feature = (set(SentenceCore.split("~")) - set([coreword])).pop()
            # get list of sentence file filtered by coreword
            filetemp = os.path.join(clsvar.sentencedir, "*" + SentenceCore + "*.csv")
            for fname in glob.glob(filetemp):
                fsentence = open(fname, encoding="utf-8")

                # read-out the first head
                fsentence.readline()
                for line in fsentence:
                    dictline = dict(zip(listoutputhead, line.strip().split(",")))
                    dictmodelset[dictline["모델"]].add(dictline["CRC32"])

                    line = line.strip() + "," + feature + "\n"
                    try:
                        foutcsv.write(line.encode("cp949"))
                    except:
                        continue

                fsentence.close()

        foutcsv.close()
        print("core csv file finished: %s"%(coreword+".csv"))

        # second,create a csv file containing count of crc  not to duplicate
        foutcsvcount = open(os.path.join(clsvar.fileoutdir, coreword + "_count.csv"), "wb")
        liststrmodelcount = [   ",".join( (aa[0], str(len(aa[1])) ))for aa in dictmodelset.items()   ]
        foutcsvcount.write( "\n".join(liststrmodelcount).encode("cp949") )
        foutcsvcount.close()


if __name__ == "__main__":

    fileincsv = ""
    now = datetime.datetime.now()

    cmdlineopt = argparse.ArgumentParser(description='find some text within csv file and print the result into csv file')
    cmdlineopt.add_argument('-i', action="store", dest="fileincsv", default='', help='input csv file .')
    cmdlineopt.add_argument('-o', action="store", dest="fileoutdir", default='output', help='output dir .')
    cmdlineopt.add_argument('-s', action="store", dest="sentencedir", default='sentence', help='sentence csv file dir.')
    cmdlineopt.add_argument('-t', action="store", dest="tempdir", default='tempdir', help='temporary dir.')
    cmdlineopt.add_argument('-p', action="store", dest="keywordprev", default='keywordprev.txt', help='keyword file .')
    cmdlineopt.add_argument('-k', action="store", dest="keywords", default='keywords.txt', help='keyword sorted file .')
    cmdlineopt.add_argument('-r', action="store", dest="filekeyreplace", default='keyreplace.txt', help='keyword replace file .')

    clsvar = cmdlineopt.parse_args()
    if len(clsvar.fileincsv) == 0 :
       print(" Must have the value of fileincsv as parameter")
       exit()

    ### note : fileincsv 은  ",", "\\" 을 포함하는 cell이 있어서는 안된다.  --> 미리 제거해야 한다.

    # 증상 문장을 space단위로 분활 및 저장
    clsvar.fileseqment = "symseg.txt"

    # 1. 증상에 해당하는 문장을  분해해서 저장한다.
    # getSymptomSegmentation(clsvar)

    # 2. symseg.txt 에서 원하는 keyword을 추출하고  "keywordprev.txt"에 저장한다.
    # 3. "keywordprev.txt"을 읽어서 sort하고, 다시 "keywordwords.txt"에 저장한다.
    # sortKeyword(clsvar)

    # 4. "keywordprev.txt" 와 replace.txt을 읽어들어,  keyword 기준으로 문장 combination을 한다.
    combinatekeyword(clsvar)
    
    # 5. keysentence에 해당하는 파일을 temp dir에서 sentence dir에 copy한다.
    copySentenceWordsCSV(clsvar.tempdir, clsvar.sentencedir, listSentenceWords)

    # 6. groupSentensceByCoreWord(clsvar)은  listSentenceWords CSV file list을 core 이름 군으로  grouping하고,
    # 이를  "core이름".csv 이름의 파일에 출력한다.
    groupSentensceByCoreWord(clsvar)



    timediff = datetime.datetime.now() - now
    print("total wasted time : %s" % (str(timediff)))