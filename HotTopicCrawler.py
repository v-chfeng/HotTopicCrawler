#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' Hot topic crawler '

__author__ = 'chenglin(v-chfeng@microsoft.com)'

import os
import requests
from bs4 import BeautifulSoup

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}

class crawler():
    def __init__(self, url, writerPath, htmlencode = 'utf-8'):
        self.url = url
        self.writerPath = writerPath
        self.htmlencode = htmlencode
        

    def run(self, title_cssSelector, url_cssSelector, hotindex_cssSelector, **ValueCssPair):
        """Run Css Selector To Extract Values.
        
        title, url, hotindex must be contained.
        if there are other css selectors, use key value paramters.
        Value is the value name that is extractored by css selector, and css must contain css selector
         and type which property and value should be extractor in Element.
         
         eg. Body = ['.body', 'string'] 
         eg. SourceUrl = ['.someclass', 'href']
        """
        tools = "..\\UploadCosmos\\Microsoft.Label.VCUploadTools.exe"
        use_string = " " + "-u" + " " + self.url
        cmd = tools + use_string
        r = os.popen(cmd)
        use_url = r.read().replace('\n', '')

        url = use_url
        SCRAW_SUCESS = False
        while not SCRAW_SUCESS:
            try:
                print("begin to scraw...")
                r = requests.get(url, headers=headers, timeout=20)
                SCRAW_SUCESS = True
                print("scraw over!")
            except requests.exceptions.ConnectTimeout:
                print("network error!")
                time.sleep(5)
            except requests.exceptions.Timeout:
                print("request Time out!")
                time.sleep(5)
        if r.encoding == 'ISO-8859-1':
            encodings = requests.utils.get_encodings_from_content(r.text)
            if encodings:
                encoding = encodings[0]
        else:
             encoding = r.apparent_encoding
        html = r.content.decode(encoding, 'replace')#.encode('utf-8', 'replace')
        # print(r.text)
        # print(r.text.decode(self.htmlencode))
        # print(html)
        # html = r.text.encode(r.encoding).decode(self.htmlencode)
        soup = BeautifulSoup(html, "lxml")

        othervalue_dic = {}
        title_list = []
        url_list = []
        hotindex_list = []

        title_list = [title_ele.string for title_ele in soup.select(title_cssSelector)]
        url_list_tmp = [title_ele['href'] for title_ele in soup.select(url_cssSelector)]
        hotindex_list = [index_ele.string for index_ele in soup.select(hotindex_cssSelector)]

        for rawurl in url_list_tmp:
            url_list.append(self.url_pathcombine(rawurl))

        othervalue_dic[0] = title_list
        othervalue_dic[1] = url_list
        othervalue_dic[2] = hotindex_list
        value_name_dic = {}
        value_name_dic[0] = 'title'
        value_name_dic[1] = 'url'
        value_name_dic[2] = 'hotindex'

        if len(ValueCssPair) > 0 :
            i = 3
            for value, css in ValueCssPair.items():
                temp_value_list = []
                if len(css) != 2:
                    continue
                value_cssselector = css[0]
                value_property = css[1]
                if value_property.strip(' ') == 'string' :
                    temp_value_list = [value_ele.string for value_ele in soup.select(value_cssselector)]
                else:
                    temp_value_list = [value_ele[value_property] for value_ele in soup.select(value_cssselector)]
                if len(temp_value_list) > 0 and not othervalue_dic.__contains__(value):
                    othervalue_dic[i] = temp_value_list
                    value_name_dic[i] = value
                    i = i + 1
        return self._write_dic(othervalue_dic, value_name_dic)


    def custom_run(self, **value_css_pair):
        """Run Css Selector To Extract Values V2, Allow Input Custom Css Selector Order.

        Use key value paramters.
        Value is the value name that is extractored by css selector, and CSS must contain css selector
         and type which property and value should be extractor in Element.
         
         eg. Body = ['.body', 'string'] 
         eg. SourceUrl = ['.someclass', 'href']
        """
        tools = "..\\UploadCosmos\\Microsoft.Label.VCUploadTools.exe"
        use_string = " " + "-u" + " " + self.url
        cmd = tools + use_string
        r = os.popen(cmd)
        use_url = r.read().replace('\n', '')


        url = use_url
        SCRAW_SUCESS = False
        while not SCRAW_SUCESS:
            try:
                print("begin to scraw...")
                r = requests.get(url, headers=headers, timeout=200)
                SCRAW_SUCESS = True
                print("scraw over!")
            except requests.exceptions.ConnectTimeout:
                print("network error!")
                time.sleep(5)
            except requests.exceptions.Timeout:
                print("request Time out!")
                time.sleep(5)
            except requests.exceptions.ConnectionError:
                print("connection Time out!")
                time.sleep(5)
        if r.encoding.find('ISO-8859') :
            encodings = requests.utils.get_encodings_from_content(r.text)
            if encodings:
                encoding = encodings[0]
        else:
             encoding = r.apparent_encoding
        html = r.content.decode(encoding, 'replace')#.encode('utf-8', 'replace')
        # print(r.text)
        # print(r.text.decode(self.htmlencode))
        # print(html)
        # html = r.text.encode(r.encoding).decode(self.htmlencode)
        soup = BeautifulSoup(html, "lxml")
        (othervalue_dic, value_name_dic) = self._parse_html(soup, **value_css_pair)
        return self._write_dic(othervalue_dic, value_name_dic), othervalue_dic


    def _parse_html(self, soup, **value_css_pair):
        othervalue_dic = {}
        value_name_dic = {}

        if len(value_css_pair) > 0 :
            i = 0
            for value, css in value_css_pair.items():
                temp_value_list = []
                if len(css) != 2:
                    continue
                value_cssselector = css[0]
                value_property = css[1]
                if value_property.strip(' ') == 'string' :
                    temp_value_list = [value_ele.text for value_ele in soup.select(value_cssselector)]
                else:
                    temp_value_list = [value_ele[value_property] for value_ele in soup.select(value_cssselector)]
                if not othervalue_dic.__contains__(value):
                    othervalue_dic[i] = temp_value_list
                    value_name_dic[i] = value
                    i = i + 1
        return othervalue_dic, value_name_dic


    def _write_dic(self, key_list_dic, value_name_dic):
        dest_dir = os.path.dirname(self.writerPath)
        if not os.path.exists(dest_dir):
            os.mkdir(dest_dir)
        if len(key_list_dic) == 0:
            return 
        
        # generate row set
        row_list = []

        max_length = 0
        length_list = []
        for item_list in key_list_dic.values():
            current_length = len(item_list)
            length_list.append(current_length)
            if current_length > max_length:
                max_length = current_length

        for i in range(0, max_length):  # row
            row_item = '\t'
            temp_list = []
            for j in range(0, len(key_list_dic)):      # colum
                if i < length_list[j]:
                    temp_list.append(key_list_dic[j][i])
                else:
                    temp_list.append('')
            row_list.append(row_item.join(temp_list))

        with open(self.writerPath, mode='w', encoding='utf-8') as out_writer:
            out_writer.write('\n'.join(row_list))
        return row_list


    def url_pathcombine(self, href_str):
        """Url Path Combine.
        
        href_str is the 'href' property in the element.
        """
        split_urls = self.url.split('/')        
        if href_str.lower().startswith('http'):
            return href_str
        elif href_str.startswith('#'):
            return ''
        else:
            current_host = ''
            if self.url.lower().__contains__('http'):
                current_host_list = split_urls[0:3]
                current_host = '/'.join(current_host_list)
            else:
                current_host = split_urls[0]
            current_root = split_urls[0:-1]
            (splitchar_num, href_path) = self._parse_href(href_str)
            new_url = self.url + "/" + href_path
            if splitchar_num == 0:
                new_url = "/".join(current_root) + "/" + href_path
            elif splitchar_num == 1:
                new_url = current_host + "/" + href_path
            elif splitchar_num == -1:
                if len(split_urls) > 2:
                    new_url = "/".join(split_urls[0:-2]) + "/" + href_path
                else:
                    return self.url + "/" + href_path
            return new_url


    def _parse_href(self, href_str):
        if href_str.startswith('/'):
            return 1, href_str.lstrip('/')

        split_href = href_str.strip().split('/')
        href_length = len(split_href)
        if href_length == 1:
            return 0, split_href[0]
        elif href_length == 2:
            if not split_href[0]:
                return 1, split_href[1]
            elif split_href[0].startswith('..'):
                return -1, split_href[1]
            elif split_href[1].startswith('.'):
                return 0, split_href[1]
            else:
                return 0, split_href[1]
        else:  # TODO: 完成整个URL解析，目前只支持少部分
            return 0, href_str.lstrip('/')

if __name__ == '__main__':
    testoutpath = './data/realtime.tsv'
    title_css = ['.list-title', 'string']
    url_css = ['.list-title', 'href']
    hotindex_css = ['td[class~="last"] span', 'string']

    realtime_crawler = crawler('http://top.baidu.com/buzz?b=1&c=513&fr=topbuzz_b11_c513', testoutpath)
    # result = realtime_crawler.run(title_css, url_css, hotindex_css)
    # print(result)
    print(realtime_crawler.custom_run(title=title_css, url=url_css, hotindex=hotindex_css))