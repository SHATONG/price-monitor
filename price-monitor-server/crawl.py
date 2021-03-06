# -*- coding: utf-8 -*-
import requests
import json
from lxml import etree


class Crawl(object):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'}

    def get_price(self, item_id_inner):
        url = 'https://p.3.cn/prices/mgets?callback=&skuIds=J_' + item_id_inner
        print '该商品价格URL：', url
        r = requests.get(url, headers=self.headers)
        price = r.text
        price = price[2:-4]
        js = json.loads(str(price))
        return js['p']

    def get_name(self, item_id_inner):
        url = 'https://item.jd.com/' + item_id_inner + '.html'
        r = requests.get(url, headers=self.headers)
        selector = etree.HTML(r.text)
        name = selector.xpath("//*[@class='sku-name']/text()")  # list
        try:
            name = name[0].strip()
        except IndexError as e:
            print('尝试第二种名称捕获方式')
            try:
                name = selector.xpath("//*[@id='name']/h1/text()")
                name = name[0].strip()
            except IndexError as e:
                print('名称捕获失败')
        return name
