# -*- coding:utf-8 -*-
# 批量用例执行--自动加载
import requests
import json
import unittest
import time
import HTMLTestRunner
import os

# 用例路径
case_path = os.path.join(os.getcwd())
# 报告存放路径
report_path = os.path.join(os.getcwd())


def loadJson(file="test.json"):
    f = open(file, encoding='utf-8')
    return json.load(f)


class TestOne(unittest.TestCase):
    def setUp(self):
        # 1、获取当前时间，这样便于下面的使用。
        now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))

        # 2、html报告文件路径
        report_abspath = os.path.join(report_path, "result_" + now + ".html")

        # 3、打开一个文件，将result写入此file中
        self.fp = open(report_abspath, "w+")
        self.fp.write("<h1 style=\"color:blue\">时间:   " + now + "</h1>")
        self.fp.write("<h1 style=\"color:blue\">Title:   " + "自动化测试报告" + "</h1><br><br>")
        self.fp.write("<h1 style=\"color:purple\">描述:</h1>")
        # print(os.path.join(os.getcwd()))
        self.json = loadJson("test.json")
        self.headers = self.json['headers']
        self.length = len(self.json['data'])
        # print(self.headers)
        self.fp.write("<h2>headers:</h2>")
        self.fp.write(json.dumps(self.headers) + "<br><hr>")
        print("开始测试......\n")
        pass

    def test_0(self):
        '''test add method'''
        if self.length == 0:
            return
        for i in range(0, self.length):
            url = self.json['data'][i]['url']
            self.fp.write("<h2 >URL:</h2>" + url)
            self.fp.write("<h2>method:</h2>" + self.json['data'][i]['method'])
            if self.json['data'][i]['method'] == 'GET':
                pass
            if self.json['data'][i]['method'] == 'POST':
                self.fp.write("<h3>发送数据: </h3>" + json.dumps(self.json['data'][i]['req_data']))
                self.fp.write("<h3>测试结果: </h3>")
                r = requests.post(url=url, data=json.dumps(self.json['data'][i]['req_data']), headers=self.headers)
                flag = True
                for j in self.json['data'][i]['res_data']:
                    if j in r.text:
                        flag = True
                    else:
                        flag = False

                try:
                    self.assertTrue(flag, r.text)
                    self.fp.write("<h3 style=\"color:green;\">通过！ </h3><br><br><hr>")
                except Exception as e:
                    self.fp.write("<h3 style=\"color:red;\">错误！ </h3>")
                    self.fp.write("<h3 style=\"color:red\">" + str(e) + " </h3><br><hr>")
                    pass

    def tearDown(self):
        print("end.........\n")
        self.fp.close()
        pass


def all_case():
    discover = unittest.defaultTestLoader.discover(case_path, pattern="test*.py", top_level_dir=None)
    return discover


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    # 4、调用add_case函数返回值
    runner.run(all_case())
