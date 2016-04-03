#!/usr/bin/python3
import os
import re

import requests
from lxml import etree
from contextlib import closing

import SpiderUtil

STATUE_SUCCEED = SpiderUtil.STATUS_SUCCEED
STATUE_FAILED = SpiderUtil.STATUS_FAILED
STATUE_JUMPED = SpiderUtil.STATUS_JUMPED

url_download = 'http://www.jikexueyuan.com/course/video_download'
video_ex_name = ".mp4"
xpath_lesson_bg = '//div[@class="infor-content"]/text()'
xpath_video_list = '//div[@class="lesson-box"]/ul/li'

xpath_video_index = 'i[@class="lessonmbers"]/em/text()'
xpath_video_name = 'div[@class="text-box"]/h2/a/text()'
xpath_video_href = 'div[@class="text-box"]/h2/a/@href'


class VideoSpider(object):

    """ VideoSpider 课程详情页，即视频播放页面  """

    def __init__(self, name=None):
        super(VideoSpider, self).__init__()
        self.url = ""
        self.name = name or "name"
        self.course_id = ""
        self.video_list = []
        self.bg_txt = ""
        self.response = None
        self.selector = None

    def parse_html(self, url):
        if re.match("http://", url) is None:
            raise ValueError("Invalid URL "+url)
        self.url = url
        print("正在获取下载地址：" + self.url, end='\r')
        course_id_list = re.findall('/(\d*?).html', url)
        self.course_id = ""
        if len(course_id_list) == 1:
            self.course_id = course_id_list[0]

        self.response = requests.get(self.url, headers=SpiderUtil.headers, cookies=SpiderUtil.cookies)
        self.selector = etree.HTML(self.response.text)
        self.bg_txt = self.selector.xpath(xpath_lesson_bg)
        for video_ele in self.selector.xpath(xpath_video_list):
            video = Video()
            video.parse_html(video_ele, self.course_id)
            self.add_video(video)
        print("下载地址分析完成：" + self.url, end='\r')

    def add_video(self, video):
        if isinstance(video, Video):
            self.video_list.append(video)

    def download(self, path, url):
        self.parse_html(url)
        print("【", self.name, "】共有", len(self.video_list), '个视频', " " * len(self.url))
        if not os.path.exists(path):
            os.makedirs(path)
        result = {STATUE_SUCCEED: 0, STATUE_FAILED: 0, STATUE_JUMPED: 0}
        for video in self.video_list:
            data = video.download(path)
            result[data] += 1
        file = open(path + "/readme.txt", "a+")
        file.write("\n下载日志：总计" + str(len(self.video_list)) + str(result))
        file.close()
        print("    -->>总计", len(self.video_list), result)
        return result

    def save_info(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        file = open(path + "/readme.txt", "a+")
        for text in self.bg_txt:
            file.write(text)
        for video in self.video_list:
            video.save_info(file)
        file.close()


class Video(object):

    """docstring for VideoInfo"""

    def __init__(self, seq="1", index="1", name="name", href=""):
        super(Video, self).__init__()
        self.seq = seq
        self.index = index
        self.name = name
        self.href = href
        self.response = None
        self.result_dic = {}
        self.download_flag = False

    def parse_html(self, selector, course_id):
        self.index = selector.xpath(xpath_video_index)[0]
        self.name = selector.xpath(xpath_video_name)[0]
        self.href = selector.xpath(xpath_video_href)[0]
        temp = re.findall('_(\d).html', self.href)
        if len(temp) == 1:
            self.seq = temp[0]
        params = {'seq': self.seq, 'course_id': course_id}
        self.response = requests.get(url_download, params=params,
                                     headers=SpiderUtil.headers, cookies=SpiderUtil.cookies)
        self.result_dic = eval(self.response.text)

        # print("下载请求返回结果：", self.response.text)
        if len(self.result_dic["data"]) == 0:
            raise ValueError("cookies is not a valid")
        else:
            self.download_flag = True
            return "OK"

    def url(self):
        if self.result_dic["code"] == 200:
            return self.result_dic["data"]["urls"]
        else:
            return ""

    def file_name(self):
        try:
            self.result_dic["filename"]
        except KeyError:
            file_name = SpiderUtil.replace_special(self.result_dic["data"]["title"])
            self.result_dic["filename"] = self.index + "." + file_name + video_ex_name
        else:
            pass
        finally:
            return self.result_dic["filename"]

    def download(self, path):
        if not self.download_flag:
            raise ValueError("cookies is not a valid")
        file_name = path + "/" + self.file_name()
        if not os.path.exists(file_name):
            with closing(requests.get(self.url(), stream=True)) as response:
                chunk_size = 1024
                content_size = int(response.headers['content-length'])
                progress = SpiderUtil.ProgressBar(self.file_name(), total=content_size,
                                                  unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
                # chunk_size = chunk_size < content_size and chunk_size or content_size
                try:
                    with open(file_name, "wb") as file:
                        for data in response.iter_content(chunk_size=chunk_size):
                            file.write(data)
                            progress.refresh(count=len(data))

                except Exception as e:
                    progress.refresh(progress.total, status="下载失败")
                    print(e)
                    return STATUE_FAILED
                else:
                    return STATUE_SUCCEED
        else:
            print("    <", self.file_name(), ">已被", STATUE_JUMPED, flush=True)
            return STATUE_JUMPED

    def save_info(self, file):
        file.write("\n"+self.seq + self.name)
        file.write("\n请求结果：" + str(self.result_dic))

if __name__ == '__main__':
    videoSpider = VideoSpider()
    videoSpider.download("pythontest", 'http://www.jikexueyuan.com/course/636.html')