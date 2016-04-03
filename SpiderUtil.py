#!/usr/bin/python3
import re

STATUS_SUCCEED = '成功'
STATUS_FAILED = '失败'
STATUS_JUMPED = '跳过'

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
           'Connection': 'keep-alive',
           'DNT': '1',
           'Host': 'www.jikexueyuan.com',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'}
cookies = {'stat_uuid': '1449798718230117830638',
           'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%221531e3f6ba8116-0bfac12aa-424b0021-100200-1531e3f6ba91b4%22%7D',
           'r_user_id': '79c5192f-2246-4318-a613-f917403dd813',  # stat_fromWebUrl': '',
           'stat_ssid': '1459654434692',
           'looyu_id': '827d4cd057d8999f16a9eaa28f61229fc7_20001269%3A8',
           '_gat': '1',
           'uname': '%E7%A8%8B%E5%BA%8F%E8%89%BA%E6%9C%AF%E5%AE%B6',
           'uid': '4523395',
           'code': '0H25MS',
           'authcode': 'fda4wDDS34qNVBgnIgQVyon0OZJ4CvDZAY0OlP%2FL5UprasyQUJoMi2RkV1uxXuTX5Tb3KHz26BG03oBCv0GZ8Se252uNEQkqe8pQiC%2Brg%2BNE3CoLuVib9uWN%2FMBIz%2BgjwgVymcD%2B%2B9uFRAWxIS%2FuH6IjvxSDeg1%2FutKoqCzWUoSc',
               # '9d446luIOAeMNY8dZMO8gWWesyJsPwVDoLhRiQGyW6sf74aBQG8FZCa0zrQQFFcGBn6KBjKWD0bWdYk3YAmlaJXQHUFsfwhKeZh1ZV7ZQ%2Bq5x8nxbGLQdh2JcwnQGiPopXqwAcIctgalKMN4IVTW31vGhe%2FIM%2BBGJGPnNNbC1LHD',
           'level_id': '2',
           'is_expire': '0',
           'domain': 'code_art',
           '_99_mon': '%5B0%2C0%2C0%5D',
           'Hm_lvt_f3c68d41bda15331608595c98e9c3915': '1459231126,1459393493,1459394410,1459492438',
           'Hm_lpvt_f3c68d41bda15331608595c98e9c3915': '1459493170',
           # 'undefined': '',
           'stat_isNew': '0',
           'looyu_20001269': 'v%3A58100ca24d3c28fb6ecc018b58cbef41bd%2Cref%3A%2Cr%3A%2Cmon%3Ahttp%3A//m9104.talk99.cn/monitor%2Cp0%3Ahttp%253A//www.jikexueyuan.com/course/201.html',
           '_ga': 'GA1.2.850847531.1459188866', }

def is_ok(str1):
    if isinstance(str1, str):
        return str1.lower() == "ok" or str1.lower() == "y" or str == ''
    else:
        return False


def is_all(str1):
    if isinstance(str1, str):
        return str1.lower() == "a" or str == ''
    else:
        return False


def is_valid_index(index, length):
    if isinstance(index, int):
        if (index >= 1) and (index <= length):
            return index - 1
    elif isinstance(index, str):
        try:
            index2 = int(index)
        except Exception as e:
            print(e)
            return 0
        else:
            if (index2 >= 1) and (index2 <= length):
                return index2 - 1
    else:
        return 0


def replace_special(source_str):
    # special = ('/', '\\', ':', '<', '>', '|', '*', '?', '"', ' ', '[\\x00-\\x08]|[\\x0b-\\x0c]|[\\x0e-\\x1f]')
    # for s in special:
    #     source_str = source_str.replace(s, "")
    source_str = re.sub('[/|\\\\|:|<|>|*|?|"| |\']|[\x00-\x08]|[\x0b-\x0c]|[\x0e-\x1f]', "", source_str, count=0)
    return source_str

if __name__ == '__main__':
    jieguo = is_valid_index("3", 10)
    print(jieguo)
    print(is_ok("Ok"))
    print(is_ok("oo"))
    special_str = 'AA/ \\F\\F\\F\\F\\ " ? * | < > : \x08 \x00\x0b\x0c\x0e \x1a BBB'
    print(special_str)
    print("特殊字符替换", replace_special(special_str))

    # print("----------------------------")
    # with closing(requests.get("http://www.baidu.com", stream=True)) as response:
    #     for line in response.iter_lines():
    #         print(line)


class ProgressBar(object):

    def __init__(self, title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "    < %s >%s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.statue)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status,
                             self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)


