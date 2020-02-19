# -*- coding:utf-8 -*-

import requests
from datetime import datetime, timedelta
import os
import time
import sys


class MaoyanFilmReviewSpider:
    """猫眼影评爬虫"""

    def __init__(self, url, end_time, filename):
        # 头部
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        }

        # 目标URL
        self.target_url = url

        # 数据获取时间段，start_time:截止日期，end_time:上映时间
        now = datetime.now()

        # 获取当天的 零点
        self.start_time = now + timedelta(hours=-now.hour, minutes=-now.minute, seconds=-now.second)
        self.start_time = self.start_time.replace(microsecond=0)
        self.end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

        # 打开写入文件, 创建目录
        self.save_path = "files/"
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        self.save_file = open(self.save_path + filename, "a", encoding="utf-8")

    def download(self, url):
        """下载html内容"""

        print("正在下载URL: "+url)
        # 下载html内容
        response = requests.get(url, headers=self.headers)

        # 转成json格式数据
        if response.status_code == 200:
            return response.json()
        else:
            # print(html.status_code)
            print('下载数据为空！')
            return ""

    def parse(self, content):
        """分析数据"""

        comments = []
        try:
            for item in content['cmts']:
                comment = {
                    'nickName': item['nickName'],       # 昵称
                    'cityName': item['cityName'],       # 城市
                    'content': item['content'],         # 评论内容
                    'score': item['score'],             # 评分
                    'startTime': item['startTime'],    # 时间
                }
                comments.append(comment)

        except Exception as e:
            print(e)

        finally:
            return comments

    def save(self, data):
        """写入文件"""

        print("保存数据，写入文件中...")
        self.save_file.write(data)

    def start(self):
        """启动控制方法"""

        print("爬虫开始...\r\n")

        start_time = self.start_time
        end_time = self.end_time

        num = 1
        while start_time > end_time:
            print("执行次数:", num)
            # 1、下载html
            content = self.download(self.target_url + str(start_time))

            # 2、分析获取关键数据
            comments = ''
            if content != "":
                comments = self.parse(content)

            if len(comments) <= 0:
                print("本次数据量为：0，退出爬取！\r\n")
                break

            # 3、写入文件
            res = ''
            for cmt in comments:
                res += "%s###%s###%s###%s###%s\n" % (cmt['nickName'], cmt['cityName'], cmt['content'], cmt['score'], cmt['startTime'])
            self.save(res)

            print("本次数据量：%s\r\n" % len(comments))

            # 获取最后一条数据的时间 ，然后减去一秒
            start_time = datetime.strptime(comments[len(comments) - 1]['startTime'], "%Y-%m-%d %H:%M:%S") + timedelta(seconds=-1)
            # start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")

            # 休眠3s
            num += 1
            time.sleep(0.5)

        self.save_file.close()
        print("爬虫结束...")


if __name__ == "__main__":
    # 确保输入参数
    if len(sys.argv) != 4:
        print("请输入相关参数：[moveid]、[上映日期]和[保存文件名]，如：xxx.py 42962 2018-11-09 text.txt")
        exit()

    # 猫眼电影ID
    mid = sys.argv[1] # "1208282"  # "42964"
    # 电影上映日期
    end_time = sys.argv[2]  # "2018-11-16"  # "2018-11-09"
    # 每次爬取条数
    offset = 15
    # 保存文件名
    filename = sys.argv[3]

    spider = MaoyanFilmReviewSpider(url="http://m.maoyan.com/mmdb/comments/movie/%s.json?v=yes&offset=%d&startTime=" % (mid, offset), end_time="%s 00:00:00" % end_time, filename=filename)
    # spider.start()

    spider.start()
    # t1 = "2018-11-09 23:56:23"
    # t2 = "2018-11-25"
    #
    # res = datetime.strptime(t1, "%Y-%m-%d %H:%M:%S") + timedelta(days=-1)
    # print(type(res))