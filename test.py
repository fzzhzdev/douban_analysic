import jieba
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from pyecharts.charts import Geo
from pyecharts.charts import Pie
from pyecharts import options as opts
from pyecharts.globals import ChartType, SymbolType
from pyecharts.datasets import COORDINATES

def geo_show() -> Geo:
    c = (
        Geo()
        .add_schema(maptype='china')
        .add("", [list(z) for z in zip(city_name, city_position)])
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(visualmap_opts=opts.VisualMapOpts(), title_opts=opts.TitleOpts(title="《少年的你》评星人位置分布图 by CSDN-虐猫人薛定谔i"))
        .render('result/位置分布图.html')
    )
    return c
