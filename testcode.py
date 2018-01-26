import os
import subprocess
import HotTopicCrawler

# DebugPath = ".\\UploadCosmos\\Microsoft.Label.VCUploadTools.exe"
# FilePath = ".\\data\\article_temp.tsv"
# CosmosPath = "https://cosmos09.osdinfra.net/cosmos/searchSTC-A/local/users/v-shluo/test1.tsv"
#
# ll = "cd c: ";
# lll = "dir"
#
# os.system(ll)
# os.system(lll)

# comm = DebugPath +" "+"-o"+" "+FilePath+" "+CosmosPath

# os.system(comm)
# body_url = "http://s.weibo.com/weibo/%25E9%2599%2588%25E7%25BF%2594%25E5%259B%259E%25E5%25BA%2594&Refer=top"
# tools = ".\\Tools\\Microsoft.Label.VCUploadTools.exe"
# use_string = " " + "-u" + " " + body_url
# cmd = tools + use_string
# r = os.popen(cmd)
# use_url = r.read().replace('\n','')
#
# body_css = ['.comment_txt', 'string']
# body_output = '.\\data\\body_weiboreal.tsv'
# body_crawl = HotTopicCrawler.crawler(use_url, body_output)
# (body_results_list, body_results_dic) = body_crawl.custom_run(body=body_css)
#
# use_body = body_results_dic[0][0].replace('\t', '').replace('\n', '')
#
# print(use_body)
uploadtools = ".\\UploadCosmos\\Microsoft.Label.VCUploadTools.exe"
uploadfile =".\\data\\baiduRedian_20180125.tsv"
cosmospath = "https://cosmos09.osdinfra.net/cosmos/searchSTC-A/local/users/v-shluo/test/baiduRedian.tsv"

cmd = uploadtools + " " + "-o" + " " + uploadfile + " " + cosmospath

r = os.popen(cmd)

readinfo = r.read()

if (not readinfo == ''):
    if os.path.exists(uploadfile):
        os.remove(uploadfile)
else:
    print("failed!")