import os
import HotTopicCrawler

url = '  http://caifuhao.eastmoney.com/topic/16/  '

print(url.strip('/ '))
split_urls = url.split('/')
print(split_urls)
print('/'.join(split_urls))

testpath = './data/out.tsv'
print(os.path.exists(testpath))
print(os.path.basename(testpath))
print(os.path.abspath(testpath))
print(os.path.dirname(testpath))
testdir = os.path.dirname(testpath)
os.mkdir(testdir)
print(os.path.exists(testdir))


testoutpath = './data/realtime.tsv'
title_css = '.list-title'
url_css = '.list-title'
hotindex_css = 'td[class~="last"] span'

realtime_crawler = HotTopicCrawler.crawler('http://top.baidu.com/buzz?b=1&c=513&fr=topbuzz_b11_c513', testoutpath)
result = realtime_crawler.run(title_css, url_css, hotindex_css)
print(result)

