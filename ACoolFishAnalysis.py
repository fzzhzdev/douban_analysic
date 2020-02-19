# -*- coding:utf-8 -*-
from pyecharts.charts import Geo, Bar, Bar3D, Pie
import jieba
from pyecharts.globals import ChartType
from wordcloud import STOPWORDS, WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from pyecharts import options as opts
plt.switch_backend('agg')

class ACoolFishAnalysis:
    """无名之辈 --- 数据分析"""
    def __init__(self):
        pass

    def readCityNum(self):
        """读取观众城市分布数量"""
        d = {}

        with open("files/myCmts2.txt", "r", encoding="utf-8") as f:
            row = f.readline()

            while row != "":
                arr = row.split('###')

                # 确保每条记录长度为 5
                while len(arr) < 5:
                    row += f.readline()
                    arr = row.split('###')

                # 记录每个城市的人数
                if arr[1] in d:
                    d[arr[1]] += 1
                else:
                    d[arr[1]] = 1   # 首次加入字典，为 1

                row = f.readline()


            # print(len(comments))
            # print(d)

        # 字典 转 元组数组
        res = []
        for ks in d.keys():
            if ks == "":
                continue
            tmp = (ks, d[ks])
            res.append(tmp)

        # 按地点人数降序
        res = sorted(res, key=lambda x: (x[1]),reverse=True)
        return res

    def readAllComments(self):
        """读取所有评论"""
        comments = []

        # 打开文件读取数据
        with open("files/myCmts2.txt", "r", encoding="utf-8") as f:
            row = f.readline()

            while row != "":
                arr = row.split('###')

                # 每天记录长度为 5
                while len(arr) < 5:
                    row += f.readline()
                    arr = row.split('###')

                if len(arr) == 5:
                    comments.append(arr[2])

                # if len(comments) > 20:
                #     break
                row = f.readline()

        return comments

    def createCharts(self):
        """生成图表"""

        # 读取数据,格式：[{"北京", 10}, {"上海",10}]
        data = self.readCityNum()

        # 1 热点图

        geo1 = Geo("《无名之辈》观众位置分布热点图", "数据来源：猫眼，Fly采集",page_title="#FFF", title_pos="center", width="100%", height=600, bg_color="#404A59")

        attr1, value1 = geo1.cast(data)

        geo1.add("", attr1, value1, type="heatmap", visual_range=[0, 1000], visual_text_color="#FFF", symbol_size=15, is_visualmap=True, is_piecewise=False, visual_split_number=10)
        geo1.render("files/无名之辈-观众位置热点图.html")

        # 2 位置图
        geo2 = Geo("《无名之辈》观众位置分布", "数据来源：猫眼，Fly采集", title_color="#FFF", title_pos="center", width="100%", height=600,
                   background_color="#404A59")

        attr2, value2 = geo1.cast(data)
        geo2.add("", attr2, value2, visual_range=[0, 1000], visual_text_color="#FFF", symbol_size=15,
                is_visualmap=True, is_piecewise=False, visual_split_number=10)
        geo2.render("files/无名之辈-观众位置图.html")

        # 3、top20 柱状图
        data_top20 = data[:20]
        bar = Bar("《无名之辈》观众来源排行 TOP20", "数据来源：猫眼，Fly采集", title_pos="center", width="100%", height=600)
        attr, value = bar.cast(data_top20)
        bar.add('', attr, value, is_visualmap=True, visual_range=[0, 3500], visual_text_color="#FFF", is_more_utils=True, is_label_show=True)
        bar.render("files/无名之辈-观众来源top20.html")

        print("图表生成完成")

    def createWordCloud(self):
        """生成评论词云"""
        comments = self.readAllComments()  # 19185

        # 使用 jieba 分词
        commens_split = jieba.cut(str(comments), cut_all=False)
        words = ''.join(commens_split)

        # 给词库添加停止词
        stopwords = STOPWORDS.copy()
        stopwords.add("电影")
        stopwords.add("一部")
        stopwords.add("无名之辈")
        stopwords.add("一部")
        stopwords.add("一个")
        stopwords.add("有点")
        stopwords.add("觉得")

        # 加载背景图片
        bg_image = plt.imread("files/2048.jpg")

        # 初始化 WordCloud
        wc = WordCloud(width=1200, height=800, background_color='#FFF', mask=bg_image, font_path='C:/Windows/Fonts/STFANGSO.ttf', stopwords=stopwords, max_font_size=400, random_state=50)
        # 生成，显示图片
        wc.generate_from_text(words)

        # 改变字体颜色
        img_colors = ImageColorGenerator(bg_image)
        # 字体颜色为背景图片的颜色
        wc.recolor(color_func=img_colors)
        plt.imshow(wc)
        plt.axis('off')
        plt.show()

    def geo_show(self) -> Geo:
        data = self.readCityNum()

        c = (
            # 读取数据,格式：[{"北京", 10}, {"上海",10}]
            Geo()
                .add_schema(maptype='china')
                .add("", data)
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(visualmap_opts=opts.VisualMapOpts(),
                                 title_opts=opts.TitleOpts(title="《少年的你》评星人位置分布图 by CSDN-虐猫人薛定谔i"))
                .render('files/位置分布图.html')
        )
        return c

    def pie_show(self) -> Pie:
        data = self.readCityNum()
        c = (
            Pie()
                #.add("", [list(z) for z in zip(star, values)])
                .add("", data)
                .set_global_opts(title_opts=opts.TitleOpts(title="《少年的你》评星"))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}%"))
                .render('files/饼状分布图.html')
        )
        return c

    def geo_heatmap(self) -> Geo:
        data = self.readCityNum()
        c = (
            Geo()
                .add_schema(maptype="china")
                .add(
                "geo",
                data,
                type_=ChartType.HEATMAP,
            )
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(max_ = 5),
                title_opts=opts.TitleOpts(title="Geo-HeatMap"),
            )
                .render('files/热点分布图.html')
        )
        return c

if __name__ == "__main__":
    demo = ACoolFishAnalysis()
    demo.geo_heatmap()
    demo.pie_show()
    demo.geo_show()
    demo.createWordCloud()
    #0.5X版本，不能用
    #demo.createCharts()