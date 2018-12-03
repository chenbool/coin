#!/usr/bin/python3
# -*- coding:utf-8 -*-
from urllib import request
from bs4 import BeautifulSoup as bs
import json
import re
from time import strftime, time, sleep
from db import Db
__author__ = 'bool'

class App(object):
    soup = ''
    # init
    def __init__(self):
        pass

    # 获取内容
    def setUrl(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        req = request.Request(url, headers=headers)
        resp = request.urlopen(req).read().decode("utf-8")
        self.soup = bs(resp, "html.parser")
        return self.getCont()

    # 获取信息
    def getCont(self):
        res = self.soup.find("div", {"class": "content"})
        # coin - tit
        # head = res.find("div", {"class": "coinHead"}).find("div", {"class": "coin-tit"}).find("h1").getText()

        # 计算 价格、 涨幅金额 、涨幅百分比
        price = res.find("div", {"class": "coinHead"}).find("div", {"class": "price1"}).find("div", {"class": "main"})
        diff = re.findall(r"-?\d{1,}.\d{1,}", str(price))

        # 汇率 、最高、最低、24h成交价、24h成交金额、24h换手率
        lowhigh = res.find("div", {"class": "coinHead"}).find("div", {"class": "lowheight"})
        lowhigh = re.findall(r"-?\d{1,}.\d{1,}", str(lowhigh))
        temp = {
            'price': diff[0],
            'gain': diff[1],
            'rate': diff[2],
            'high': lowhigh[1],
            'low': lowhigh[2],
        }
        return temp
        # print(temp)

    # 获取列表
    def getList(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        req = request.Request(url, headers=headers)
        resp = request.urlopen(req).read().decode("utf-8")
        resp = json.loads(resp)

        # 遍历数据
        for item in resp:
            item = item.split('#')
            # 判断第一个参数大于0则跳出循环
            if int(item[0]) > 0:
                break
            # print(item)
            # 临时保存
            temp = {
                'code': item[1],
                'en_name': item[2],
                'name': item[3],
                'en_code': item[4],
                'logo': 'https://static.feixiaohao.com'+item[5],
                'urls': 'https://m.feixiaohao.com/currencies/'+item[1],
                'upTime': time(),
                'upDate': strftime("%Y-%m-%d %H:%M:%S")
            }

            res = self.setUrl(temp['urls'])
            temp['price'] = res['price']
            temp['gain'] = res['gain']
            temp['rate'] = res['rate']
            temp['high'] = res['high']
            temp['low'] = res['low']
            print(temp)
            self.insertData(temp)
            sleep(1)

        # print(resp[0])
    def insertData(self, temp):
        sqls = "insert into main ('code','en_name','name','en_code','logo','urls','price','gain','rate','high','low','upTime','upDate') values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
            temp['code'], temp['en_name'], temp['name'], temp['en_code'], temp['logo'], temp['urls'], temp['price'], temp['gain'], temp['rate'], temp['high'], temp['low'], temp['upTime'],
            temp['upDate'])
        db = Db()
        if db.ddl(sqls) > 0:
            print(temp['name'] + '----->采集成功')
        pass


if __name__ == '__main__':
    api = App()
    api.getList('https://mapi.feixiaohao.com/api/home/relatedallword')
    # api.setUrl('https://m.feixiaohao.com/')
