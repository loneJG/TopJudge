# coding: UTF-8

import os
import json
import re

#in_path = r"D:\work\law_pre\test\in"
#out_path = r"D:\work\law_pre\test\out"
in_path = r"/disk/mysql/law_data/formed_data"
out_path = r"/disk/mysql/law_data/critical_data"
mid_text = u"  _(:з」∠)_  "
title_list = ["docId", "caseNumber", "caseName", "spcx", "court", "time", "caseType", "bgkly", "yuanwen", "document",
              "cause", "docType", "keyword", "lawyer", "punishment", "result", "judge"]
num_file = 1
num_process = 1

num_list = {
    u"〇": 0,
    u"\uff2f": 0,
    u"\u3007": 0,
    u"\u25cb": 0,
    u"\uff10": 0,
    u"\u039f": 0,
    u'零': 0,
    "O": 0,
    "0": 0,
    u"一": 1,
    u"元": 1,
    u"1": 1,
    u"二": 2,
    u"2": 2,
    u"两": 2,
    u'三': 3,
    u'3': 3,
    u'四': 4,
    u'4': 4,
    u'五': 5,
    u'5': 5,
    u'六': 6,
    u'6': 6,
    u'七': 7,
    u'7': 7,
    u'八': 8,
    u'8': 8,
    u'九': 9,
    u'9': 9,
    u'十': 10,
    u'百': 100,
    u'千': 1000,
    u'万': 10000
}


def parse_term_of_imprisonment(data):
    erf = open("error.log","a")
    if "PJJG" in data["document"]:
        s = data["document"]["PJJG"].replace('b','')
        pattern = re.compile(u"拘役")
        for x in pattern.finditer(s):
            pos = x.start() + len(u"拘役")
            num1 = 0
            while s[pos] in num_list:
                if s[pos] == u"十":
                    if num1 == 0:
                        num1 = 1
                    num1 *= 10
                elif s[pos] == u"百" or s[pos] == u"千" or s[pos] == u"万":
                    print("0 "+s[x.start()-10:pos+20],file=erf)
                    return None
                else:
                    num1 = num1 + num_list[s[pos]]

                pos += 1

            num = 0
            if s[pos] == u"年":
                num2 = 0
                pos += 1
                if s[pos] == u"又":
                    pos += 1
                while s[pos] in num_list:
                    if s[pos] == u"十":
                        if num2 == 0:
                            num2 = 1
                        num2 *= 10
                    elif s[pos] == u"百" or s[pos] == u"千" or s[pos] == u"万":
                        print("1 "+s[x.start()-10:pos+20],file=erf)
                        return None
                    else:
                        num2 = num2 + num_list[s[pos]]

                    pos += 1
                if s[pos] == u"个":
                    pos += 1
                if num2!=0 and s[pos] != u"月":
                    print("2 "+s[x.start()-10:pos+20],file=erf)
                    return None
                num = num1*12 + num2
            else:
                if s[pos] == u"个":
                    pos += 1
                if s[pos] != u"月":
                    print("3 "+s[x.start()-10:pos+20],file=erf)
                    return None
                else:
                    num = num1

            pos += 1
            #print(num,s[x.start():pos])




def parse(data):
    result = {}
    #print(data["document"]["PJJG"])

    result["term_of_imprisonment"] = parse_term_of_imprisonment(data)


def draw_out(in_path, out_path):
    print(in_path)
    inf = open(in_path, "r")
    ouf = open(out_path, "w")

    cnt = 0
    for line in inf:
        #try:
            data = json.loads(line)
            if data["caseType"] == "1" and data["document"] != {} and "Title" in data["document"] and not(re.search(u"判决书",data["document"]["Title"]) is None):
                data["meta_info"] = parse(data)
            cnt += 1
            #if cnt == 50000:
            #    break

        #except Exception as e:
        #    print(e)
        #    gg


def work(from_id, to_id):
    for a in range(int(from_id), int(to_id)):
        print(str(a) + " begin to work")
        draw_out(os.path.join(in_path, str(a)), os.path.join(out_path, str(a)))
        print(str(a) + " work done")


if __name__ == "__main__":
    import multiprocessing

    process_pool = []

    for a in range(0, num_process):
        process_pool.append(
            multiprocessing.Process(target=work, args=(a * num_file / num_process, (a + 1) * num_file / num_process)))

    for a in process_pool:
        a.start()

    for a in process_pool:
        a.join()