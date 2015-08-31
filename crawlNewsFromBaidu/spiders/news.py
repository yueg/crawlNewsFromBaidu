# -*- coding:utf-8 -*-
__author__ = 'yueg'
import scrapy
import re
from crawlNewsFromBaidu import editDistance
from bs4 import BeautifulSoup as bsp

class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = [
        "*",
    ]

    def __init__(self, query=None):
        self.start_urls = [
            "http://news.baidu.com/ns?rn=20&word=%s" % query,
            # "http://mt.sohu.com/20150825/n419764543.shtml",
            # "http://www.shfinancialnews.com/xww/2009jrb/node5019/node5036/node5048/userobject1ai149791.html"
            # "http://www.topnews9.com/article_20150824_45954.html"
            # "http://jjckb.xinhuanet.com/2015-05/26/content_549136.htm"
        ]

    def parse(self, response):
        sel = scrapy.Selector(response)
        url = response.url.encode('utf-8')
        title = sel.xpath('//html/head/title/text()').extract()[0]
        content = response.body
        urlSplit = url.split('/')
        mainUrl = urlSplit[2]

        if mainUrl == "news.baidu.com":
            for link in sel.xpath('//div/h3/a/@href').extract():
                request = scrapy.Request(link, callback=self.parse, dont_filter=True)
                yield request
        else:
            # content = content.decode('utf-8')
            content = self.convCharset2utf8(content)
            content = self.dealContent(content)
            # soap = bsp(content)
            # h1Finds = soap.find_all(name="h1")
            time = self.getNewsTime(content)
            title = self.getTitle(title, content)
            print title


    def convCharset2utf8(self, content):
        patt = re.compile('<meta.*?charset=["]?(.*?)"');
        code = re.findall(patt, content)
        if len(code) > 0:
            type = code[0].lower()
            if type == 'gb2312':
                content = content.decode('gbk').encode('utf-8')
            else:
                content = content.decode(type).encode('utf-8')
        return content

    def dealContent(self, content):
        content, number = re.subn('(?i)<style[\s\S]*?</style>', '', content)
        content, number = re.subn('(?i)<script[\s\S]*?</script>', '', content)
        content, number = re.subn('(?i)<noscript[\s\S]*?</noscript>', '', content)
        content, number = re.subn('(?i)<iframe[\s\S]*?</iframe>', '', content)
        content, number = re.subn('<!--[\s\S]*?-->', '',content)
        content, number = re.subn('(i?)<head[\s\S]*?head>', '', content)
        # content, number = re.subn('(i?)<a[\s\S]*?a>', '', content)
        content, number = re.subn('(i?)(&nbsp;)+', '', content)
        content, number = re.subn('(i?)(&copy;)+', '', content)
        content, number = re.subn('(i?)(&quot;)+', '', content)
        content, number = re.subn('<br[ /]?/?>', '\n', content)
        return content

    def getNewsTime(self, content):
        pattern = []
        pattern.append(re.compile('(20\d{2}[年]\d{1,2}[月]\d{1,2}日[ ]?\d{0,2}:?\d{0,2}:?\d{0,2})'.decode("utf8")))
        pattern.append(re.compile('(20\d{2}[/]\d{1,2}[/]\d{1,2}[ ]?\d{0,2}:?\d{0,2}:?\d{0,2})'.decode("utf8")))
        pattern.append(re.compile('(20\d{2}[-]\d{1,2}[-]\d{1,2}[ ]?\d{0,2}:?\d{0,2}:?\d{0,2})'.decode("utf8")))
        timelist = []
        for patt in pattern:
            temp = re.findall(patt, content.decode('utf8'))
            timelist.extend(temp)
        return self.getRealTimeFromList(timelist)

    def getRealTimeFromList(self, timeList):
        if len(timeList) == 0:
            return ""
        maxLen = 0
        for i in range(len(timeList)):
            timeList[i], number = re.subn('[/年月]'.decode('utf8'), '-', timeList[i])
            timeList[i], number = re.subn('[日]'.decode('utf8'), '', timeList[i])
            if len(timeList[i]) > maxLen:
                maxLen = len(timeList[i])
        maxLenTimeList = []
        for time in timeList:
            if len(time) == maxLen:
                maxLenTimeList.append(time)
        if len(maxLenTimeList) == 1:
            return maxLenTimeList[0]
        for time in maxLenTimeList:
            elements = time.split('-')
            year = elements[0]
            month = elements[1]
            day = elements[2]
            # print year, month, day

    def getTitle(self, title, content):
        # content, number = re.subn('<br>', '\n', content)
        title = title.strip().encode('utf8')
        content, number = re.subn('<[\s\S]*?>', '', content)
        content, number = re.subn(u'[\n]{2}', u'\n', content.decode('utf8'))
        lines = content.split('\n')
        count = editDistance.arithmetic().levenshtein(title, u'')
        ret = ''
        for line in lines:
            temp = line.strip()
            if temp == '':
                continue
            editDis = editDistance.arithmetic().levenshtein(title, temp.encode('utf8'))
            if editDis < count:
                count = editDis
                ret = temp
        return ret




