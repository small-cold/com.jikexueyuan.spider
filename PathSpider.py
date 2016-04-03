#!/usr/bin/python3
import requests
import SpiderUtil
from lxml import etree
from CoursePathSpider import CoursePathSpider


class PathSpider(object):

    """ 课程路径图爬虫 """

    URL_PATH = 'http://www.jikexueyuan.com/path/'
    XPATH_PATH_LINK = '//a[@class="pathlist-one cf"]'
    XPATH_PATH_NAME = 'div[@class="pathlist-txt"]/h2/text()'
    XPATH_PATH_INTRO = 'div[@class="pathlist-txt"]/p/text()'

    def __init__(self):
        super(PathSpider, self).__init__()
        self.path_info_list = []
        self.response = None
        self.selector = None

    def parse_html(self):
        print("正在获取课程路线列表...")
        # try:
        self.response = requests.get(PathSpider.URL_PATH)
        # print(self.response.text)
        self.selector = etree.HTML(self.response.text)
        for link_ele in self.selector.xpath(PathSpider.XPATH_PATH_LINK):
            self.path_info_list.append(_PathInfo(link_ele))
        # except Exception:
        #     print("连接异常")
        #     # exit()
        # else:
        #     pass

    def show(self):
        n = 0
        print("共有学习路线图：", len(self.path_info_list), "个，分别是：")
        for info in self.path_info_list:
            n += 1
            print(str(n)+".", info.name)

    def show_detail(self, index):
        if SpiderUtil.is_valid_index(index, len(self.path_info_list)):
            self.path_info_list[index].show()
            return "OK"
        else:
            return "error"

    def download(self, index):
        if SpiderUtil.is_valid_index(index, len(self.path_info_list)):
            print("开始下载", self.path_info_list[index].name)
            self.path_info_list[index].download()
            return "OK"
        else:
            return "error"


class _PathInfo(object):

    def __init__(self, selector):
        super(_PathInfo, self).__init__()
        # print("正在获取课程路线列表...")
        self.selector = selector
        self.name = selector.xpath(PathSpider.XPATH_PATH_NAME)[0]
        self.inrto = selector.xpath(PathSpider.XPATH_PATH_INTRO)
        self.url = selector.xpath('@href')[0]

    def show(self):
        print("课程：", self.name)
        print("简介：", self.inrto)
        print("链接：", self.url)
        return

    def sub_spider(self):
        spider = CoursePathSpider(self.url, self.name)
        return spider

    def download(self):
        self.sub_spider().download()
