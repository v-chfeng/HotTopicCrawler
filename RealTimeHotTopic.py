#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' baidu real time hot topic crawler '

import HotTopicCrawler

if __name__ == '__main__':
    url = "http://caifuhao.eastmoney.com/topics/hot"
    outputTsv = "./TopFinanceCaifuhao.tsv"
    Is_Crawled_Today = False
    todaytimestamp = str(time.strftime('%Y%m%d', time.localtime()))
    if os.path.exists(outputTsv):
        tsvContent = open(outputTsv, 'r', encoding='utf-8')
        line = tsvContent.readline()
        if todaytimestamp in line:
            Is_Crawled_Today = True

    if not Is_Crawled_Today:
        tsv_writer = open(outputTsv, 'w', encoding='utf-8')
        s1 = sousuo(url, tsv_writer)
        s1.chaxun()
        print(u"complete!")
    else:
        print("Skip this time, because crawled today!")


