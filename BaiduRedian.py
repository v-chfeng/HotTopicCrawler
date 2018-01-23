#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' baidu real time hot topic crawler '

import os
import time
import subprocess
import HotTopicCrawler


# def _custom_format_out(results_list):
#     for one_line in results_list:
#         columns_list = one_line.split('\t')
#         source = 'baidu'
#         category1 = '热点'
#         category2 = '实时'
#         title = columns_list[0]
#         body = columns_list[3]
#         url = columns_list[1]
#         hotindex = columns_list[2]
#         frequency = 'daily'


def _crawl_article(article_url):
    print('scraw', ' ', article_url)
    # 有卡片(图片)的百度页面
    article_outpath = './data/redian_article_temp.tsv'
    first_title_css = ['.OP_LOG_LINK','string']
    body_css = ['.op_sp_realtime_bigpic5_first_abs','string']
    first_url_css = ['.op_sp_realtime_bigpic5_first_abs a','href']
    first_source_css = ['.op_sp_realtime_bigpic5_first_abs+.g', 'string']
    others_title_css = ['.op_sp_realtime_bigpic5_list_info div a', 'string']
    others_url_css = ['.op_sp_realtime_bigpic5_list_info div a', 'href']
    others_sourece_css = ['.op_sp_realtime_bigpic5_list_info div .g', 'string']

    # 没有卡片的百度页面
    body2_css = ['.c-offset .c-row', 'string']   # soup 不支持 伪css 选择器
    url2_css = ['.c-offset .c-row a', 'href']

    art_crawler = HotTopicCrawler.crawler(article_url, article_outpath)
    (art_results_list, art_results_dic) = art_crawler.custom_run(body=body_css, firsturl=first_url_css, otherurls = others_url_css, body2=body2_css, url2=url2_css)
    bodystr = ''
    body2str = ''
    url_list = []
    if len(art_results_dic) > 0:
        i = 0
        for eachvalue in art_results_dic.values():
            if len(eachvalue) > 0:
                if i == 0:  # body1
                    bodystr = eachvalue[0]
                elif i == 1:  # first url
                    if eachvalue[0]:
                        url_list.append(eachvalue[0])
                elif i == 2:  # other urls
                    for urlitem in eachvalue:
                        if urlitem:
                            url_list.append(urlitem)
                elif i==3:  # body2
                    body2str = eachvalue[0]  # 只有第一个有简介
                elif i==4:
                    for url2item in eachvalue:
                        if url2item:
                            url_list.append(url2item)
                i = i + 1
    if len(url_list) > 3:
        url_list = url_list[0:3]

    finalbody = ''
    if bodystr:
        finalbody = bodystr.replace(u'详情>>', '').replace('\n','').replace(' ','')
    elif body2str:
        bodyindex = 0
        split_body = body2str.split('\n')
        for i in range(0, len(split_body)):
            one_line = split_body[i]
            if one_line.replace('"','').replace(' ',''):
                bodyindex = i
        finalbody = split_body[bodyindex].replace('"','').replace(' ','')  # 取最后一段文本。  文本样式eg. 4小时前\n title\n 来源\n 简介\n 
    return finalbody, ';'.join(url_list)


if __name__ == '__main__':

    temp_outpath = './data/redian_temp.tsv'
    final_outpath = './data/baiduRedian_' + str(time.strftime('%Y%m%d', time.localtime())) + ".tsv"
    title_css = ['.list-title', 'string']
    url_css = ['.list-title', 'href']
    hotindex_css = ['td[class~="last"] span', 'string']
    websource = 'baidu'
    webcategory1 = '热点'
    webcategory2 = ''
    frequency = 'daily'

    redian_url_dic = {}

    redian_url_dic['今日热点'] = 'http://top.baidu.com/buzz?b=341&fr=topboards'
    redian_url_dic['七日热点'] = 'http://top.baidu.com/buzz?b=42&c=513&fr=topbuzz_b341'
    redian_url_dic['民生热点'] = 'http://top.baidu.com/buzz?b=342&c=513&fr=topbuzz_b42_c513'
    redian_url_dic['娱乐热点'] = 'http://top.baidu.com/buzz?b=344&c=513&fr=topbuzz_b342_c513'
    redian_url_dic['体育热点'] = 'http://top.baidu.com/buzz?b=11&c=513&fr=topbuzz_b344_c513'

    Is_Crawled_Today = False
    todaytimestamp = str(time.strftime('%Y%m%d', time.localtime()))
    if os.path.exists(final_outpath):
        file_modify_time = time.localtime(os.path.getmtime(final_outpath))
        modify_time_str = str(time.strftime('%Y%m%d', file_modify_time))
        file_size = os.path.getsize(final_outpath)
        if modify_time_str == todaytimestamp and file_size > 0:
            Is_Crawled_Today = True
    if not Is_Crawled_Today:        
        for redian_key, redian_value in redian_url_dic.items():
            webcategory2 = redian_key
            realtime_crawler = HotTopicCrawler.crawler(redian_value, temp_outpath)
            (results_list, results_dic) = realtime_crawler.custom_run(title=title_css, url=url_css, hotindex=hotindex_css)
            new_results_list = []
            for resultitem in results_list:
                split_items = resultitem.split('\t')
                split_title = split_items[0]
                split_url = split_items[1]
                split_hotindex = split_items[2]
                bodystr = ''
                urls = ''
                try:
                    if split_url:
                        bodystr, urls = _crawl_article(split_url)
                except:
                    print('crawl article failed.')
                newline_list = []
                newline_list.append(todaytimestamp)
                newline_list.append(websource)
                newline_list.append(webcategory1)
                newline_list.append(webcategory2)
                newline_list.append(split_title)
                newline_list.append(bodystr)
                newline_list.append(split_hotindex)
                newline_list.append(split_url+";"+urls)
                newline_list.append(frequency)
                new_results_list.append('\t'.join(newline_list))

            with open(final_outpath, mode='a', encoding='utf-8') as writer:
                writer.write('\n'.join(new_results_list))
                writer.write('\n')

            UploadTools = "..\\UploadCosmos\\Microsoft.Label.VCUploadTools.exe"
            filedir, filename = os.path.split(final_outpath)
            CosmosPath = "https://cosmos09.osdinfra.net/cosmos/searchSTC-A/shares/XiaoIce/ToB/SAI/Analytics/Prod/TopQuery/Baidu/Delta/" + str(time.strftime('%Y/%m', time.localtime())) + "/" + filename
            comm = UploadTools + " " + "-o" + " " + final_outpath + " " + CosmosPath
            CosmosFile = "https://cosmos09.osdinfra.net/cosmos/searchSTC-A/shares/XiaoIce/ToB/SAI/Analytics/Prod/TopQuery/Baidu/baiduRedian.tsv"
            commFile = UploadTools + " " + "-o" +" "+ final_outpath + " " + CosmosFile
            os.system(comm )
            os.system(commFile)
            print('complete!')
    else:
        print('skip today!')
