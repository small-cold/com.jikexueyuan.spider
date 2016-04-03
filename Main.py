#!/usr/bin/python3

from PathSpider import PathSpider
import platform
import os
import re


def int_input(info="请选择：", list=()):
    while True:
        input_str = input(info)
        input_int = -1
        try:
            input_int = int(input_str)
        except ValueError:
            print("请输入数字！")
            continue
        else:
            if list.count(input_int) == 0:
                print("请根据提示输入！")
                continue
            else:
                return input_int


def path_input():

    ''' 检查输入的路径是否存在，存在则返回
        如果不存在，创建该文件夹，
            创建失败，重新输入
            创建成功，返回路径
     '''

    default = default_path()
    input_path = ""
    while input_path == "":
        input_path = input('请输入存储路径【默认"' + default + '"】:')

        if input_path == "":
            input_path = default
        elif re.match("[A-Z]|[a-z]://", input_path) is None:
            input_path = default + "/" + input_path
        elif re.match("/|~", input_path) is None:
            input_path = default + "/" + input_path
        else:
            pass
        if check_path(input_path) or make_file_path(input_path):
            return input_path
        else:
            print("地址【", input_path, "】无效，情重新输入", flush=True)
            continue


def check_path(file_path):
    if os.path.exists(file_path):
        return True
    else:
        return False


def make_file_path(file_path):
    try:
        os.makedirs(file_path)
    except IOError as ioe:
        print("创建文件夹失败")
        return False
    else:
        return True


def default_path():
    sys_name = platform.system()
    path_list = []
    if sys_name == "Windows":
        path_list = ["F://", "E://", "D://", "C://"]
    elif sys_name == "Linux":
        path_list = ["",]
    else:
        return ''

    for dpath in path_list:
        if os.path.exists(dpath):
            return dpath + '极客学院视频'
    return ""


if __name__ == '__main__':

    try:
        path_spider = PathSpider()
        path_spider.parse_html()
        path_spider.show()
        _path_list = path_spider.path_info_list
        course_spider = None
        index = 0
        if len(_path_list) > 0:
            print("[1~", len(_path_list), "]选择课程路线/ 0 退出")
            index = int_input(list=range(0, len(_path_list) + 1))
        if index == 0:
            exit()
        else:
            _path_list[index - 1].show()
            course_spider = _path_list[index - 1].sub_spider()

            course_spider.parse_html()
            print("全部下载[0]，按章下载请输入[1~", len(course_spider.chapter_list), "]")
            index = int_input(list=range(0, len(_path_list)))

        path = path_input()
        print("视频将下载到下载到：", path)
        if index == 0:
            course_spider.download(path)
        else:
            course_spider.download(path, index)
    except ConnectionError as ce:
        print("连接超时，请检查网络！")
    else:
        print("下载结束！")





