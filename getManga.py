#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread
import os
import urllib2
import re

mainHost = 'http://www.tuku.cc'
mainCount = 15220
maxCount  = 0
failCount = 0
title = re.compile(r'"current"\s*>\s*<h1\s*>(.*)</h1>')
charpterList = re.compile(r'/comic.*?(/comic/.*?/down.htm).*?title="(.*?)"')
illegal = re.compile(r'[\\\/\:\?\*\<\>\|\"]')
downOriginList = re.compile(r'Tk.jsonp_url\s*?\+\s*?"(.*?)"')
downList = re.compile(r'\\"(http:.*?)\\"')
headersone = {
    'Cookie': 'sess_id=8b57967d54a881c82d6da1fbf3515222; __cfduid=d0c04ad729bbbd673c512749e331ced6b1444051246; JXM702806=1; bdshare_firstime=1444051283274; detail11981=%7B%22model%22%3A%221%22%2C%22id%22%3A%2211981%22%2C%22title%22%3A%22%E4%B9%9D%E6%B3%89%E4%B9%8B%E5%B2%9B%22%2C%22chapter%22%3A%22c_62105%22%2C%22chaptername%22%3A%22%E7%AC%AC3%E8%AF%9D%22%2C%22page%22%3A%221%22%2C%22url%22%3A%22%2Fcomic%2F11981%2Fc_62105%2F%22%2C%22nextpage%22%3A%22%2Fcomic%2F11981%2Fc_62105%2F2%2F%23readcontent%22%2C%22nextchapter%22%3A%22%2Fcomic%2F11981%2Fc_63630%2F%22%2C%22time%22%3A%222015-10-5%2021%3A32%3A51%22%7D; JXD702806=1; imageServerId=0; detail9955=%7B%22model%22%3A%221%22%2C%22id%22%3A%229955%22%2C%22title%22%3A%22GANGSTA%E5%8C%AA%E5%BE%92%22%2C%22chapter%22%3A%22n-1444038481-17474%22%2C%22chaptername%22%3A%22%E7%AC%AC42%E8%AF%9D%22%2C%22page%22%3A%221%22%2C%22url%22%3A%22%2Fcomic%2F9955%2Fn-1444038481-17474%2F%22%2C%22nextpage%22%3A%22%2Fcomic%2F9955%2Fn-1444038481-17474%2F2%2F%23readcontent%22%2C%22nextchapter%22%3A%22%2Fcomic%2F9955%2Frecom%22%2C%22time%22%3A%222015-10-6%2014%3A59%3A16%22%7D; detail15220=%7B%22model%22%3A%221%22%2C%22id%22%3A%2215220%22%2C%22title%22%3A%22%E5%AF%BB%E6%89%BE%E8%BA%AB%E4%BD%93%22%2C%22chapter%22%3A%22n-1411898564-95364%22%2C%22chaptername%22%3A%22%E7%AC%AC1%E8%AF%9D%22%2C%22page%22%3A%224%22%2C%22url%22%3A%22%2Fcomic%2F15220%2Fn-1411898564-95364%2F4%2F%22%2C%22nextpage%22%3A%22%2Fcomic%2F15220%2Fn-1411898564-95364%2F5%2F%23readcontent%22%2C%22nextchapter%22%3A%22%2Fcomic%2F15220%2Fn-1412948595-50697%2F%22%2C%22time%22%3A%222015-10-6%2017%3A54%3A23%22%7D; detail5267=%7B%22model%22%3A%221%22%2C%22id%22%3A%225267%22%2C%22title%22%3A%22%E5%A4%A9%E4%B8%8A%E5%A4%A9%E4%B8%8B%E9%AB%98%E6%B8%85%E6%99%B0%E7%89%88%22%2C%22chapter%22%3A%221%22%2C%22chaptername%22%3A%22%E5%8D%B71%22%2C%22page%22%3A%2212%22%2C%22url%22%3A%22%2Fcomic%2F5267%2F1%2F12%2F%22%2C%22nextpage%22%3A%22%2Fcomic%2F5267%2F1%2F13%2F%23readcontent%22%2C%22nextchapter%22%3A%22%2Fcomic%2F5267%2F2%2F%22%2C%22time%22%3A%222015-10-6%2018%3A24%3A16%22%7D; detail11754=null; readlist=%2211981%2C9955%2C15220%2C5267%2C11437%22; detail11437=%7B%22model%22%3A%221%22%2C%22id%22%3A%2211437%22%2C%22title%22%3A%22%E8%89%B2%E7%B3%BB%E5%86%9B%E5%9B%A2%22%2C%22chapter%22%3A%221%22%2C%22chaptername%22%3A%22%E7%AC%AC1%E8%AF%9D%22%2C%22page%22%3A%222%22%2C%22url%22%3A%22%2Fcomic%2F11437%2F1%2F2%2F%22%2C%22nextpage%22%3A%22%2Fcomic%2F11437%2F1%2F3%2F%23readcontent%22%2C%22nextchapter%22%3A%22%2Fcomic%2F11437%2F2%2F%22%2C%22time%22%3A%222015-10-6%2018%3A54%3A39%22%7D; readnum=25; CNZZDATA5468329=cnzz_eid%3D1038029097-1444048617-null%26ntime%3D1444129633; Hm_lvt_d82238694b9ba2f40c29ec0bec08bc2c=1444051262,1444114659; Hm_lpvt_d82238694b9ba2f40c29ec0bec08bc2c=1444131344',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
}
headerstwo = {
    'Cookie': 'sess_id=dd4527a9195fee7dfc6e5962392def47; CNZZDATA5468329=cnzz_eid%3D655754887-1444124233-http%253A%252F%252Frtk.um5.cc%252F%26ntime%3D1444124233; Hm_lvt_d82238694b9ba2f40c29ec0bec08bc2c=1444128639; Hm_lpvt_d82238694b9ba2f40c29ec0bec08bc2c=1444128639',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
}

def getIndex():
    global mainCount
    try:
        mainOriginSite = urllib2.urlopen(mainHost + '/comic/' + str(mainCount)).read()
    except:
        mainCount -= 1
        return 0;
    temp = title.search(mainOriginSite)
    if temp:
        titleText = illegal.sub('-', temp.group(1))
    else:
        return 0
    temp = charpterList.findall(mainOriginSite)
    if temp:
        threads = []
        results = []
        for item in temp[::-1]:
            if not len(results) == 3:
                results.append(ChapterDown(item[0], item[1], titleText))
            else:
                threads.append(results)
                results = []
                results.append(ChapterDown(item[0], item[1], titleText))
        for oneThread in threads:
            for one in oneThread:
                one.start()
            for one in oneThread:
                one.join()

def getDown(downPage, downName, mangaName):
    req = urllib2.Request(mainHost + downPage, headers=headersone)
    try:
        downOriginSite = urllib2.urlopen(req).read()
    except:
        global failCount
        failCount += 1
        print 'download', downName, 'fail'
        return 0
    dl = downOriginList.search(downOriginSite)
    if dl:
        url = 'http://rtk.um5.cc' + dl.group(1)
        req = urllib2.Request(url = url + '&sess_id=8b57967d54a881c82d6da1fbf3515222&callback=getData', headers=headerstwo)
        lists = urllib2.urlopen(req).read()
        lists = downList.findall(lists)
        if lists:
            while True:
                print 'downloading', downName.decode('utf-8')
                if getFile(lists[0].replace('\\', ''), downName.decode('utf-8'), mangaName.decode('utf-8')):
                    break


def getFile(url, name, dirName):
    if not os.path.exists(dirName):
        os.mkdir(dirName)
    name = './' + dirName + '/' + name + '.zip'
    if not os.path.exists(name):
        req = urllib2.Request(url=url, headers=headerstwo)
        try:
            data = urllib2.urlopen(req).read()
        except:
            return False
        f = open(name, 'wb')
        f.write(data)
        f.close()
    return True

class ChapterDown(Thread):
    def __init__(self, downPage, downName, mangaName):
        super(ChapterDown, self).__init__()
        self.downPage = downPage
        self.downName = downName
        self.mangaName = mangaName
    def run(self):
        req = urllib2.Request(mainHost + self.downPage, headers=headersone)
        try:
            downOriginSite = urllib2.urlopen(req).read()
        except:
            global failCount
            failCount += 1
            print 'download', self.downName, 'fail'
            return 0
        dl = downOriginList.search(downOriginSite)
        if dl:
            url = 'http://rtk.um5.cc' + dl.group(1)
            req = urllib2.Request(url = url + '&sess_id=8b57967d54a881c82d6da1fbf3515222&callback=getData', headers=headerstwo)
            lists = urllib2.urlopen(req).read()
            lists = downList.findall(lists)
            if lists:
                while True:
                    print 'downloading', self.downName.decode('utf-8')
                    if getFile(lists[0].replace('\\', ''), self.downName.decode('utf-8'), self.mangaName.decode('utf-8')):
                        break


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        mainCount = int(sys.argv[1])
        if len(sys.argv) > 2:
            maxCount = int(sys.argv[2])
        else:
            maxCount = mainCount
        while mainCount <= maxCount:
            getIndex()
            mainCount += 1
        print 'download fail num', failCount

