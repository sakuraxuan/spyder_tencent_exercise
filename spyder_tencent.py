# !/usr/bin/env python
# -*- coding:utf-8 -*-

# !/usr/bin/env python
# -*- coding:utf-8 -*-
import json

import requests
from bs4 import BeautifulSoup


class Tencent_Spyder(object):
    """tencent职位爬取----》解析出需要的职位信息元素----->添加是否到最后一页的判断"""

    def __init__(self):
        """准备数据"""
        # # https://hr.tencent.com/position.php?keywords=python&lid=2175&tid=87&start=30
        self.url = 'https://hr.tencent.com/position.php?'
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        self.element_list = []
        self.page = 0

    def send_requests(self, url, params):
        """发送数据"""
        data = requests.get(url, headers=self.headers, params=params).content
        return data



    def analysis_data(self, data):
        """解析数据"""
        # 取元素，一次解析两个循环，发现元素是列表套列表 ，考虑两次循环取完（两次循环都是同一次请求之内页面解析）
        # 一个页面 两次解析 一个循环
        # 1 select出所有行元素 列表
        soup = BeautifulSoup(data, 'lxml')
        # row_element_list = soup.select('#position tr')  # //*[@id="position"]/div[1]/table/tbody/tr
        row_element_list = soup.select('.even, .odd')
        print 'row_element_list %s' % row_element_list
        # 2  循环行元素列表 select出每个行元素的小元素 放进字典
        for row in row_element_list:
            # soup = BeautifulSoup(row, 'lxml') 同一个页面的数据不需要二次转换类型
            element_dict = {}
            element_dict["work_title"] = row.select('td a')[0].get_text()
            element_dict["work_type"] = row.select('td')[1].get_text()
            element_dict["count"] = row.select('td')[2].get_text()
            element_dict["work_address"] = row.select('td')[3].get_text()
            element_dict["create_date"] = row.select('td')[4].get_text()
            self.element_list.append(element_dict)
        # 3  解析是否是最后一页
        result = soup.select('#next')[0].get('class')
        return result

    def writer_file(self):
        """保存数据"""
        data_json = json.dumps(self.element_list)
        with open('05_tencent2.json', 'w')as f:
            f.write(data_json)

    def start_work(self):
        """开始调度"""
        # 参数准备

        while True:

            params = {
                "keywords": "python",
                "lid": "2175",
                "tid": "87",
                "start": self.page
            }
            self.page += 10
            print 'page %s' % self.page
            # 发送请求
            data = self.send_requests(url=self.url, params=params)
            # 检测得到的数据
            #  解析
            result = self.analysis_data(data)

            # 判断是否到最后一页（下一页标签变灰）
            print 'result  %s' % result
            if result:
                break
        # 保存数据
        self.writer_file()


if __name__ == '__main__':
    tool = Tencent_Spyder()
    tool.start_work()
