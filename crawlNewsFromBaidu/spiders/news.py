# -*- coding:utf-8 -*-
__author__ = 'yueg'
import scrapy
import re
from crawlNewsFromBaidu import editDistance
from bs4 import BeautifulSoup as bsp
import HTMLParser
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')
reload(__import__('sys')).setdefaultencoding('utf-8')

class NewsSpider(scrapy.Spider):
    html_parser = HTMLParser.HTMLParser()
    name = "news"
    allowed_domains = [
        "*",
    ]

    def __init__(self, query=None):
        self.start_urls = [
            "http://news.baidu.com/ns?rn=20&word=%s" % query
            # 'http://money.163.com/15/0806/01/B0A4D20S00253B0H.html'
            # 'http://news.pedaily.cn/201509/20150911388164.shtml'
            # 'http://soft.zol.com.cn/540/5404370.html'
            # 'http://finance.sina.com.cn/roll/20150909/050623193451.shtml'
            # 'http://tech.hexun.com/2015-01-09/172220424.html'
            # 'http://mt.sohu.com/20150910/n420821607.shtml'
            # 'http://news.ecust.edu.cn/news/35348?category_id=6'
            # 'http://gold.cnfol.com/qiyedongtai/20150717/21116115.shtml'
            # 'http://stock.sohu.com/20150908/n420597801.shtml'
            # 'http://finance.sina.com.cn/360desktop/money/bank/bank_hydt/20141117/164420840629.shtml'
            # 'http://house.qq.com/a/20150911/052973.htm'
            # 'http://stock.sohu.com/20150417/n411448999.shtml?rdmx=1468395826'
            # 'http://www.southmoney.com/P2P/201509/399987.html'
            # 'http://finance.ifeng.com/a/20150709/13829109_0.shtml'
            # 'http://www.financialnews.com.cn/zq/jj/201508/t20150805_81508.html'
            # 'http://help.3g.163.com/15/0909/17/B33D1G4600964JVP.html'
            # 'http://finance.ifeng.com/a/20150902/13951710_0.shtml'
            # 'http://news.qjwb.com.cn/shehui/2015/0909/172657.shtml'
            # 'http://money.163.com/15/0910/12/B35B68CJ00253B0H.html'
            # 'http://mt.sohu.com/20150907/n420548813.shtml'
            # 'http://money.163.com/15/0817/04/B16MTQLE00253B0H.html'
            # 'http://news.163.com/15/0907/14/B2TRP7G600014Q4P.html'
            # 'https://rong.36kr.com/api/company?fincestatus=1&page=2&type=2'
            # 'http://news.163.com/15/0906/17/B2RLSG4E000146BE.html'
            # 'http://help.3g.163.com/15/0907/17/B2U5DAI100964KEE.html'
            # 'http://it.sohu.com/20150714/n416732309.shtml'
            # 'http://www.nmg.xinhuanet.com/xwzx/2015-08/22/c_1116339680.htm'
            # 'http://gb.cri.cn/44571/2015/06/30/7872s5013933.htm'
            # 'http://cq.people.com.cn/n/2015/0511/c365402-24808401.html?f41095c0'
            # 'http://politics.people.com.cn/BIG5/n/2015/0822/c1001-27500087.html'
            # 'http://sports.qq.com/a/20150909/009089.htm'
            # 'http://sports.qq.com/a/20150908/048538.htm?_t=t'
            # 'http://www.nowscore.com/news/626008.htm',
            # 'http://sports.ynet.com/3.1/1509/11/10371292.html'
            # 'http://sports.gmw.cn/newspaper/2015-09/10/content_109114090.htm'
            # 'http://news.subaonet.com/2015/0911/1547958.shtml'
            # 'http://news.sina.com.cn/o/2015-09-10/doc-ifxhupkn4773974.shtml'
            # 'http://money.163.com/15/0909/14/B331DNRB00253CVK.html'
            # 'http://news.163.com/15/0910/02/B34BU7QF00014AED.html'
            # 'http://info.shoes.hc360.com/2015/09/101902706338.shtml'
            # 'http://sports.eastday.com/s/20150910/u1a9026064.html'
            # 'http://sports.163.com/15/0910/09/B352R7JQ00051CA1.html#p=8Q14QMQE0AI90005'
            # "http://focus.szonline.net/Channel/201509/01/1106802.shtm"
            # 'http://www.cankaoxiaoxi.com/ent/20150910/934719.shtml'
            # "http://www.chinaz.com/manage/2015/0826/438884.shtml?qq-pf-to=pcqq.discussion"
            # "http://www.zjjzx.cn/news/jdrp/40692.html"
            # "http://news.dayoo.com/finance/201508/27/141887_43451353.htm"
            # "http://www.askci.com/news/2015/09/01/93838w3kx.shtml"
            # "http://finance.ifeng.com/a/20150830/13945174_0.shtml"
            # "http://mt.sohu.com/20150901/n420223088.shtml"
            # "http://finance.sina.com.cn/stock/t/20150901/052023133004.shtml"
            # "http://finance.ifeng.com/a/20150830/13945174_1.shtml"
            # "http://www.ebrun.com/20150831/147065.shtml"
            # "http://stock.sohu.com/20150901/n420185055.shtml"
            # "http://news.ifeng.com/a/20150819/44467538_0.shtml"
            # "http://mt.sohu.com/20150825/n419764543.shtml",
            # "http://news.eastday.com/c/20150511/u1a8706292.html"
            # "http://www.cctime.com/html/2014-7-10/2014710111929005.htm"
            # "http://www.cnautonews.com/xwdc/201507/t20150731_418850.htm"
            # "http://auto.sina.com.cn/car/2014-04-05/14471284930.shtml"
            # "http://jnsb.e23.cn/shtml/jnsb/20150613/1448955.shtml"
            # "http://www.shfinancialnews.com/xww/2009jrb/node5019/node5036/node5048/userobject1ai149791.html"
            # "http://www.topnews9.com/article_20150824_45954.html"
            # "http://jjckb.xinhuanet.com/2015-05/26/content_549136.htm"
        ]

    def parse(self, response):
        sel = scrapy.Selector(response)
        url = response.url.encode('utf-8')
        temp = sel.xpath('//html/head/title/text()').extract()
        if len(temp) > 0:
            title = temp[0]
        else:
            temp = sel.xpath('//html/body/title/text()').extract()
            if len(temp) > 0:
                title = temp[0]
            else:
                title = ''
        content = response.body
        urlSplit = url.split('/')
        mainUrl = urlSplit[2]

        if mainUrl == "news.baidu.com":
            for link in sel.xpath('//div/h3/a/@href').extract():
                request = scrapy.Request(link, callback=self.parse, dont_filter=True)
                yield request
        elif mainUrl == 'v.ifeng.com' or mainUrl == 'news.cntv.cn' or mainUrl == 'tv.sohu.com':
            pass
        elif mainUrl.split('.')[0] == 'v':
            pass
        else:
            # content = content.decode('utf-8')
            # print content
            content = self.convCharset2utf8(content)
            # print content
            content = self.dealContent(content)
            # print content
            # soap = bsp(content)
            # h1Finds = soap.find_all(name="h1")

            title = self.getTitle(title, content)
            print '---0---', url
            print '---1---', title
            time = self.getTime(title, content)
            print '---2---', time
            content = self.getContent(title, content)
            print '---------------------------3--------------------------'
            print content




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
        content, number = re.subn('\r', '\n', content)
        content, number = re.subn('<style[\s\S]*?</style>', '', content, flags=re.I)
        content, number = re.subn('<div.*?display:none[\s\S]*?</div.*?>', '', content, flags=re.I)
        content, number = re.subn('<embed[\s\S]*?</embed>', '', content, flags=re.I)
        content, number = re.subn('<script[\s\S]*?</script>', '', content, flags=re.I)
        content, number = re.subn('<noscript[\s\S]*?</noscript>', '', content, flags=re.I)
        # print content
        content, number = re.subn('<iframe[\s\S]*?</iframe>[\n]?', '', content, flags=re.I)
        content, number = re.subn('<img[^<]*?>[\n]', '', content, flags=re.I)
        # print content
        content, number = re.subn('<img[\s\S]*?>', '', content, flags=re.I)
        # print content
        content, number = re.subn('<!--[\s\S]*?-->', '',content)
        content, number = re.subn('<head[\s\S]*?head>', '', content, flags=re.I)
        # content, number = re.subn('<div.*?></div>', '</p>\n<p>', content, flags=re.I)
        find = re.findall('<div.*?>[\s\S]*?</div>', content, re.I)
        for f in find:
            temp, number = re.subn('<[\s\S]*?>', '', f)
            if temp.strip() == '':
                content = content.replace(f, '')
        find = re.findall('<p.*?>[\s\S]*?</p>', content, re.I)
        for f in find:
            temp, number = re.subn('<[\s\S]*?>', '', f)
            if temp.strip() == '':
                content = content.replace(f, '')
        content, number = re.subn('</p>.{0,7}<p.*?>', '</p>\n<p>', content, flags=re.I)
        content, number = re.subn('</tr><tr.*?>', '</tr>\n<tr>', content, flags=re.I)
        content, number = re.subn('<p></p>[\s]*?[\n]', '', content, flags=re.I)
        content, number = re.subn('<div class="gg200x300">[\s\S]*?</div>', '', content, flags=re.I)
        content, number = re.subn('</li>.{0,7}<li.*?>', '</li>\n<li>', content, flags=re.I)
        content = self.html_parser.unescape(content)
        content, number = re.subn('<br[ /]?/?>.?<br[ /]?/?>', '\n', content, flags=re.I)
        content, number = re.subn('<br[ /]?/?>', '\n', content, flags=re.I)
        content, number = re.subn('<br>', '\n', content, flags=re.I)
        content, number = re.subn('\t', '\n', content)
        content, number = re.subn('\n[\s]*?\n', '\n', content)
        content, number = re.subn('\n[\s]*?\n', '\n', content)
        content, number = re.subn('\n[\s]*?\n', '\n', content)
        content, number = re.subn('\n[\s]*?\n', '\n', content)
        return content

    def getTime(self, title, content):
        pattern = []
        timelist = []
        pattern.append(re.compile('(20\d{2}[年]\d{1,2}[月]\d{1,2}日[ ]?\d{0,2}:?\d{0,2}:?\d{0,2})'.decode("utf8")))
        pattern.append(re.compile('(20\d{2}[/]\d{1,2}[/]\d{1,2}[ ]?\d{0,2}:?\d{0,2}:?\d{0,2})'.decode("utf8")))
        pattern.append(re.compile('(20\d{2}[-]\d{1,2}[-]\d{1,2}[ ]?\d{0,2}:?\d{0,2}:?\d{0,2})'.decode("utf8")))
        cutContent = self.cutContent(title, content)
        lines = cutContent.split('\n')
        lineRange = self.getBeginAndEnd(lines)
        lines = cutContent.split('\n')
        end = lineRange['end']
        for i in range(0, end + 1):
            if lines[i] == None or lines[i].strip == '':
                continue
            for patt in pattern:
                temp = re.findall(patt, lines[i].decode('utf8'))
                if len(temp) > 0:
                    return self.getStandardTime(temp[0])
        return self.getTimeFromAllContent(content)

    def getTimeFromAllContent(self, content):
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
        if len(timeList) == 1:
            return self.getStandardTime(timeList[0])
        maxTime = 0
        for time in timeList:
            secsTime = self.getStandardTime(time)
            if secsTime > maxTime:
                maxTime = secsTime
        return maxTime

    def getStandardTime(self, str):
        str, number = re.subn('[/年月]'.decode('utf8'), '-', str)
        str, number = re.subn('[日]'.decode('utf8'), '', str)
        if len(str) > 10 and str[10] != ' ':
            temp = str
            str = temp[:10] + ' ' + temp[10:]
        times = str.split(' ')
        t = ''
        if len(times) > 0:
            temp = times[0].split('-')
            if len(temp) < 3:
                return 0
            if len(temp[0]) != 4:
                return 0
            t += temp[0] + '-'
            if len(temp[1]) == 1:
                t += '0' + temp[1] + '-'
            elif len(temp[1]) == 2:
                t += temp[1] + '-'
            else:
                return 0
            if len(temp[2]) == 1:
                t += '0' + temp[2]
            elif len(temp[2]) == 2:
                t += temp[2]
            else:
                return 0
        elif len(times) > 1:
            t += ' ' + times[2]
        str = t
        # print str
        if len(str) == 10:
            temp = time.strptime(str, "%Y-%m-%d")
        elif len(str) == 13:
            temp = time.strptime(str, "%Y-%m-%d %H")
        elif len(str) == 16:
            temp = time.strptime(str, "%Y-%m-%d %H:%M")
        elif len(str) == 19:
            temp = time.strptime(str, "%Y-%m-%d %H:%M:%S")
        else:
            return 0
        secsTime = time.mktime(temp)
        return secsTime


    def getTitle(self, title, content):
        soup = bsp(content)
        hs = soup.findAll('h1')
        hs += soup.findAll('h2')
        lines = []
        for h in hs:
            lines.append(h.string)
        if len(lines) != 0:
            ret = self.getTitleFromLinesInHTags(title, lines)
            if ret and ret != '':
                return ret
        content, number = re.subn('<[\s\S]*?>', '', content)
        lines = content.split('\n')
        return self.getTitleFromLinesInAllContext(title, lines)

    def getTitleFromLinesInHTags(self, title, lines):
        title = title.strip().encode('utf8')
        count = editDistance.arithmetic().levenshtein(title, u'')
        ret = ''
        for line in lines:
            if line == None:
                continue
            temp = line.strip().encode('utf8')
            if temp == '':
                continue
            editDis = editDistance.arithmetic().levenshtein(title, temp)
            if editDis < count:
                count = editDis
                ret = temp
        if (count + 1.0) / (len(title) + 0.5) > 0.5:
            return ''
        return ret


    def getTitleFromLinesInAllContext(self, title, lines):
        title = title.strip().encode('utf8')
        count = editDistance.arithmetic().levenshtein(title, u'')
        ret = ''
        for line in lines:
            if line == None:
                continue
            temp = line.strip().encode('utf8')
            if temp == '':
                continue
            editDis = editDistance.arithmetic().levenshtein(title, temp)
            if editDis < count:
                count = editDis
                ret = temp
        if (count + 0.5) / (len(title) + 1.0) > 0.5:
            return title
        return ret

    def cutContent(self, title, content):
        content, number = re.subn('<a[\s\S]*?>', '<a>', content, flags=re.I)
        lines = content.split('\n')
        for line in lines:
            find = re.findall('<.*?>', line)
            cnt = len(find)
            find = re.findall('<a.*?>', line, flags=re.I)
            aCnt = len(find)
            find = re.findall('<p.*?>', line, flags=re.I)
            pCnt = len(find)
            # print cnt, aCnt, pCnt
            # print line
            temp, number = re.subn('<.*?>', '', line)
            temp, number = re.subn('\s', '', temp)
            # print temp
            v = (0.0 + aCnt * 7 + cnt + len(temp) * 0.5) / (0.0 + len(temp) + 5 * pCnt + 1)
            # print v
            # if cnt >= 16 and aCnt >= 5 and pCnt <= 2:
            if v >= 1.3:
                # content, number = re.subn(line, '', content)
                content = content.replace(line, '')
        content, number = re.subn('<[\s\S]*?>', '', content)
        content, number = re.subn('.*?\|.*?\|.*?\n', '\n', content)
        content, number = re.subn('.*?┊.*?┊.*?\n', '\n', content)
        content, number = re.subn('\r', '\n', content)
        content, number = re.subn('\t', ' ', content)
        content, number = re.subn(u'分享到.*?\n', '', content)
        content, number = re.subn(u'.*(下[一1]?页).*?\n', '\n', content)
        content, number = re.subn(u'.*相关报道.*?\n', '\n\n', content)
        content, number = re.subn(u'.*相关阅读.*?\n', '\n\n', content)
        content, number = re.subn(u'.*相关链接.*?\n', '\n\n', content)
        content, number = re.subn(u'.*相关新闻.*?\n', '\n\n', content)
        content, number = re.subn(u'.*推荐视频.*?\n', '\n\n', content)
        content, number = re.subn(u'.*扫码关注.*?\n', '\n\n', content)
        content, number = re.subn(u'.*扫描下载.*?\n', '\n\n', content)
        content, number = re.subn(u'.*正文已结束.*?\n', '\n\n', content)
        content, number = re.subn(u'.*发布时间.*?\n', '\n\n', content)
        content, number = re.subn(u'.*往期回顾.*?\n', '\n\n', content)
        content, number = re.subn(u'.*免责声明.*?\n', '\n\n', content)
        content, number = re.subn(u'.*关键[词字].*?\n', '\n\n', content)
        content, number = re.subn(u'.*(支持|反对)作者观点.*?\n\n', '\n', content)
        content, number = re.subn(u'.*扫描下方二维码.*?\n', '\n\n', content)
        content, number = re.subn(u'.*责任编辑[:：].*?\n', '\n\n', content)
        content, number = re.subn(u'.*加关注[:：].*?\n', '\n\n', content)
        content, number = re.subn(u'.*相关热词搜索[:：].*?\n\n', '\n', content)
        content, number = re.subn(u'.*上一条[:：].*?\n', '\n\n', content)
        content, number = re.subn(u'.*下一条[:：].*?\n', '\n\n', content)
        content, number = re.subn(u'.*版权声明[:：].*?\n', '\n\n', content)
        content, number = re.subn(u'.*我要评论.*?\n', '\n\n', content)
        content, number = re.subn(u'.*移动发短信.*?\n', '\n\n', content)
        content, number = re.subn(u'.*作者[:：].*?\n', '\n\n', content)
        content, number = re.subn(u'.*编辑[:：].*?\n', '\n\n', content)
        content, number = re.subn(u'.*声明[:：].*?\n', '\n\n', content)
        content, number = re.subn(u'.*分享到[:：].*?\n', '\n\n', content)
        content, number = re.subn(u'.*字号.*?\n', '\n\n', content)
        content, number = re.subn(u'.*最后修改.*?\n', '\n\n', content)
        content, number = re.subn(u'.*版权作品.*?\n', '\n\n', content)
        content, number = re.subn(u'.*更多精彩.*?\n', '\n\n', content)
        content, number = re.subn(u'.*关注.{0,4}微信.*?\n', '\n\n', content)
        content, number = re.subn(u'.*更多内容.*?\n', '\n\n', content)
        content, number = re.subn(u'.*?CopyRight.*?\n', '\n\n', content, re.I)
        content, number = re.subn(u'.*?Copyright.*?\n', '\n\n', content, re.I)
        content, number = re.subn(u'.*\[打印本稿\].*?\n', '\n\n', content)
        content, number = re.subn(u'.*原标题[:：].*?\n', '\n\n', content)
        content, number = re.subn(u'.*微信[“]?扫一扫[”]?.*?\n', '\n\n', content)
        content, number = re.subn(u'.*扫描.{0,2}二维码?.*?\n', '\n\n', content)
        # content, number = re.subn(u'^【纠错】\n', '\n', content)
        index = content.find(title)
        if index < 0:
            index = 0
        content = content[index:]
        return content

    def getContent(self, title, content):
        # print content
        content = self.cutContent(title, content)
        # print content
        lines = content.split('\n')
        lines = lines[1:]
        cnt = 0
        for i in range(len(lines)):
            if lines[i].strip() != '':
                cnt += 1
                if cnt >=3:
                    continue
            pattern = []
            pattern.append(re.compile('(20\d{2}[年]\d{1,2}[月]\d{1,2}日[ ]?\d{0,2}:?\d{0,2}:?\d{0,2})'.decode("utf8")))
            pattern.append(re.compile('(20\d{2}[/]\d{1,2}[/]\d{1,2}[ ]?\d{0,2}:?\d{0,2}:?\d{0,2})'.decode("utf8")))
            pattern.append(re.compile('(20\d{2}[-]\d{1,2}[-]\d{1,2}[ ]?\d{0,2}:?\d{0,2}:?\d{0,2})'.decode("utf8")))
            mark = ''
            for patt in pattern:
                temp = re.findall(patt, lines[i].decode('utf8'))
                if len(temp) > 0 and i + 2 < len(lines) and (lines[i + 1].strip() == '' or lines[i + 2].strip() == ''):
                    mark = temp[0]
                    break
            if mark != '':
                lines = lines[i + 2:]
                break
        lineRange = self.getBeginAndEnd(lines)
        ret = ''
        for i in range(lineRange['begin'],  lineRange['end'] + 1):
            if lines[i].strip() == '':
                continue
            elif len(lines[i]) <= 5 and i >= 2 and i <= len(lines) -3 and lines[i - 1].strip() == '' and lines[i - 2].strip() == '' and lines[i + 1].strip() == '' and lines[i + 2].strip() == '':
                continue
            ret += lines[i].strip() + '\n'
        return ret

    def getBeginAndEnd(self, lines):
        count = []
        for i in range(len(lines)):
            count.append(0)
            for c in lines[i]:
                if c == ' ' or c == '\t' or c == '  ':
                    count[i] += 1
            if count == 0:
                continue
            if len(lines[i].strip()) <= count[i] and len(lines[i]) <= 10 and lines[i].strip() != '■':
                lines[i] = ''
            elif count[i] > 10 and i > 4 and count[i - 1] > 10 and count[i - 2] > 10 and count[i - 3] > 10 and count[i - 4] > 10:
                lines[i] = ''
                lines[i - 1] = ''
                lines[i - 2] = ''
                lines[i - 3] = ''
                lines[i - 4] = ''

        begin = 0
        maxBegin = 0
        maxEnd = 0
        length = 0
        count = 0
        emptyCount = 0
        degree = 0.0
        i = 0
        while i < len(lines):
            # print lines[i]
            count += len(lines[i].strip())
            if lines[i].strip() == '':
                emptyCount += 1
            else:
                emptyCount = 0
            if emptyCount == 4:
                length = i + 1 - begin
                if (count + 0.0) / (length + 0.0) > degree:
                    degree = (count + 0.0) / (length + 0.0)
                    # print '===================', degree
                    maxBegin = begin
                    maxEnd = i
                i += 1
                while i < len(lines) and lines[i].strip() == '':
                    i += 1
                count = 0
                begin = i
                continue
            i += 1

        begin = maxBegin
        end = maxEnd - 4
        ret = {'begin': begin, 'end': end}
        return ret

