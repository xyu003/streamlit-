import streamlit as st  # 网页设计库
import pandas as pd  # 数据分析
import numpy as np  # 数据计算

import streamlit.components.v1 as components
from streamlit_echarts import st_pyecharts  # 依靠于pyecharts的一个可呈现在streamlit端的制图库
import pyecharts.options as opts  # 图表选项库
from pyecharts.charts import Pie  # 饼图库
from pyecharts.charts import Bar  # 柱状图
from wordcloud import WordCloud  # 词云库
import matplotlib.pyplot as plt  # 制图库
import plotly.express as px  # 制图库
import jieba  # 中文分词库
from PIL import Image  # 读图片用的库

# 定义浏览器页面索引标签
st.set_page_config(
    page_title="泸溪河冰红茶最配队",
    page_icon="🍹",
    layout="wide",
    initial_sidebar_state="expanded",
)

if st.sidebar.button('首页'):
    st.markdown('_produced by_ 泸溪河冰红茶最配队')

    # 在这里添加首页的内容
    st.title('欢迎来到我们的课设展示页面！')
    st.title('本次:blue[Python课设]主题：')
    st.title('基于微博用户数据的关键词情感分析🌐')
    # markdown
    st.markdown('课设构想：')
    st.markdown('随着计算机技术的不断进步，人们的生活方式逐渐发生改变，社交网络就是一个非常突出的例子。'
                '越来越多的人参与到社交网络平台中去，与他人互动，分享各种内容。互联网用户不再仅仅是网站内容的浏览者，同时也是网站内容的制造者。'
                '在国内，新浪微博是用户最多、影响最大的社交媒体平台，其凭借平台的开放性、终端扩展性、内容简洁性和低门槛等特性，在网民中快速渗透，发展成为了一个重要的社会化媒体。由此可见，微博活跃用户多，覆盖领域广泛，影响力大，蕴藏着巨大的价值。'
                '无论是从学术意义还是商业价值考虑，微博的数据挖掘都尤为重要。'
                '对政府来说，可以通过情感分析等算法了解大众对社会热点事件的情感倾向，对国家政策的态度等；对广告主来说，需要进行用户分析和调研，以实现定制化服务和精准营销；对普通用户来说，快速获取自己感兴趣的内容是第一诉求，利用推荐算法可以挖掘用户的兴趣偏好，并推荐给用户，提高用户体验。'
                '因此，本次课程设计以微博作为研究对象，围绕微博数据的采集、挖掘、情感分析和可视化进行研究，设计并实现数据挖掘可视化系统。该系统可以实现微博数据的抓取、分析处理和可视化。')

# 在侧边栏中添加下拉菜单
page = st.sidebar.selectbox('分析成果展示',
                            ['请选择一个你感兴趣的话题', '当你看演唱会的时候', '期末周那些事儿~', '待解锁'])

# 根据选择的页面显示不同内容
if page == '当你看演唱会的时候':
    st.write('还在研究噢~')
    # 在这里添加首页的内容
elif page == '期末周那些事儿~':
    st.write('我们来看看期末周的人们在想什么')

    # 展示一级标题
    st.header('考试周大家be like：')

    # 是否显示词云
    option0 = st.selectbox('_词云_',('是否显示关于考试周的词云','是','否'))
    if option0 == '是':
        # 读取文本文件
        with open('weibowenben.txt', 'r', encoding='utf-8') as file:
            text = file.read()

        # 使用jieba进行中文分词
        seg_list = jieba.cut(text)

        # 过滤长度小于2的词语
        filtered_seg_list = [word for word in seg_list if len(word) >= 2]

        # 将过滤后的词语拼接成字符串
        filtered_seg_text = ' '.join(filtered_seg_list)

        # 读取自定义形状图像
        mask = np.array(Image.open('logo.png'))

        # 生成词云
        wordcloud = WordCloud(width=800, height=800, background_color='white', mask=mask,
                              font_path='msyh.ttc').generate(
            filtered_seg_text)

        # 显示词云
        plt.figure(figsize=(10, 10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)

    # 分析方式设置
    option = st.selectbox('_词典选择_', ('选择一个你感兴趣的词典','大连理工情感词典', 'BosonNLP情感词典','知网情感词典'))

    if option == '大连理工情感词典':
        st.markdown('大连理工情感词典它将词类分为两大类七小类')
        st.markdown('两大类：:blue[积极、消极]')
        st.markdown('七小类：:blue[愤怒、厌恶、惊恐、伤心、惊喜、赞成、开心]')

        option = st.selectbox('_呈现方式_', ('选择一个你喜欢的呈现方式','柱状图','饼图'))

        # 处理情绪分析文本
        ls = pd.read_csv('情绪总分析.csv')
        ls = np.array(ls)  # 转换为 ndarray
        ls = ls.reshape(1, len(ls)).tolist()  # 转换成 List [[1, 2, 3]]
        ls = ls[0]  # 取第一个元素得到最终结果 [1, 2, 3]
        del ls[0]
        ls1 = ls[0:2]
        ls2 = ls[2:9]

        if option == '柱状图':
            bar1 = (
                Bar()
                .add_xaxis(['积极', '消极'])
                .add_yaxis("人数", ls1)
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="两大类的情绪分布柱状图or折线图", subtitle="2023"
                    ),
                    toolbox_opts=opts.ToolboxOpts(),
                )
            )
            st_pyecharts(bar1)

            bar2 = (
                Bar()
                .add_xaxis(['愤怒', '厌恶', '惊恐', '伤心', '惊喜', '赞成', '开心'])
                .add_yaxis("人数", ls2)
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="七小类的情绪分布柱状图or折线图", subtitle="2023"
                    ),
                    toolbox_opts=opts.ToolboxOpts(),
                )
            )
            st_pyecharts(bar2)

        elif option == '饼图':
            ln1 = ['积极', '消极']
            ln2 = ['愤怒', '厌恶', '惊恐', '伤心', '惊喜', '赞成', '开心']

            pie1 = (
                Pie()
                .add("", [list(z) for z in zip(ln1, ls1)])
                .set_global_opts(title_opts=opts.TitleOpts(title="情绪分布（简略版）"),
                                 legend_opts=opts.LegendOpts(pos_right="right", pos_bottom="bottom"))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"),
                                 tooltip_opts=opts.TooltipOpts(formatter="{b}: {c} ({d}%)"))
            )
            st_pyecharts(pie1)

            pie2 = (
                Pie()
                .add("", [list(z) for z in zip(ln2, ls2)])
                .set_global_opts(title_opts=opts.TitleOpts(title="情绪分布（详细版）"),
                                 legend_opts=opts.LegendOpts(pos_right="right", pos_bottom="bottom"))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"),
                                 tooltip_opts=opts.TooltipOpts(formatter="{b}: {c} ({d}%)"))
            )
            st_pyecharts(pie2)

    elif option == 'BosonNLP情感词典':
        st.markdown('BosonNLP情感词典主要是通过数值展现其情绪的积极性与消极性，'
                    ':blue[数值越高，情绪积极性越强，数值越低，情绪消极性越强]')
        option = st.selectbox('_呈现方式_', ('选择一个你喜欢的呈现方式','散点图', '柱状图', '饼图'))

        file_path = 'nlp情绪分析.txt'  # 文本文件的路径
        data = []  # 存储读取到的数据

        with open(file_path, 'r') as file:
            for line in file:
                # 移除行末的换行符，并将数据转换为浮点数
                value = float(line.strip())
                data.append(value)

        # 转换为 NumPy 数组
        data = np.array(data)
        new_data = []

        # 删除过大或者过小数据
        for element in data:
            if element <= 20 and element >= -20:
                new_data.append(element)

        a = 0
        b = 0
        c = 0
        d = 0
        # 给情感数据定界分类
        for i in new_data:
            if i >= -20 and i <= -10:
                a += 1
            if i >= -10 and i <= 0:
                b += 1
            if i >= 0 and i <= 10:
                c += 1
            if i >= 10 and i <= 20:
                d += 1

        data1 = [a, b, c, d]

        if option == '散点图':
            st.markdown(
                '由于数据量大，数值集中于0左右，为了更清晰地观察数据分布，我们摘除了大于20和小于-20的数据，得到如下散点分布图')

            # 创建 DataFrame
            df = pd.DataFrame({'new_data': new_data})

            # 绘制散点分布图
            fig = px.scatter(df, x=df.index, y='new_data')

            # 设置图表标题和坐标轴标签
            fig.update_layout(
                title='一维散点分布图',
                xaxis_title='数据点索引',
                yaxis_title='情绪分布'
            )

            # 在 Streamlit 中显示图表
            st.plotly_chart(fig)

        elif option == '柱状图':

            b = (
                Bar()
                .add_xaxis(['很消极', '一般消极', '一般积极', '很积极'])
                .add_yaxis("人数", data1)
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="数据清洗后的情绪分布柱状图or折线图", subtitle="2023"
                    ),
                    toolbox_opts=opts.ToolboxOpts(),
                )
            )
            st_pyecharts(
                b, key="echarts"
            )

        elif option == '饼图':
            l = ['很消极', '一般消极', '一般积极', '很积极']
            pie3 = (
                Pie()
                .add("", [list(z) for z in zip(l, data1)])
                .set_global_opts(title_opts=opts.TitleOpts(title="数据清洗后的情绪分布饼图"),
                                 legend_opts=opts.LegendOpts(pos_right="right", pos_bottom="bottom"))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"),
                                 tooltip_opts=opts.TooltipOpts(formatter="{b}: {c} ({d}%)"))
            )
            st_pyecharts(pie3)

    elif option == '知网情感词典':
        st.markdown('知网情感词典主要是通过情感分词展现情绪的积极性与消极性，它将情绪分为三类：')
        st.markdown(':blue[大于零的为积极情绪，等于零的为中性情绪，小于零的为消极情绪]')
        option = st.selectbox('_呈现方式_', ('选择一个你喜欢的呈现方式','散点图', '柱状图', '饼图'))

        # 知网情感词典情感分析处理后的文本内容
        file_path = 'result_data2.txt'

        # 提取数据
        emotion_scores = []  # 存储情感分值的列表
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()  # 去除换行符和空格
                parts = line.split('：')  # 使用冒号进行分割，获取情感分值
                if len(parts) == 2:
                    try:
                        emotion_score = float(parts[1])  # 尝试将情感分值转换为浮点数
                        emotion_scores.append(emotion_score)  # 将情感分值添加到列表中
                    except ValueError:
                        continue  # 如果转换失败，跳过当前行
        new_data=[]

        # 删除过大或者过小数据
        for element in emotion_scores:
            if element <= 20 and element >= -20:
                new_data.append(element)

        a = 0
        b = 0
        c = 0
        # 给情感数据定界分类
        for i in new_data:
            if i<0:
                a += 1
            if i==0:
                b += 1
            if i>0:
                c += 1

        data1 = [a, b, c]

        if option == '散点图':
            st.markdown(
                '由于数据量大，数值集中于0左右，为了更清晰地观察数据分布，我们摘除了大于20和小于-20的数据，得到如下散点分布图')

            # 创建 DataFrame
            df = pd.DataFrame({'new_data': new_data})

            # 绘制散点分布图
            fig = px.scatter(df, x=df.index, y='new_data')

            # 设置图表标题和坐标轴标签
            fig.update_layout(
                title='一维散点分布图',
                xaxis_title='数据点索引',
                yaxis_title='情绪分布'
            )

            # 在 Streamlit 中显示图表
            st.plotly_chart(fig)

        elif option == '柱状图':
            b = (
                Bar()
                .add_xaxis(['消极', '中性', '积极'])
                .add_yaxis("人数", data1)
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="数据清洗后的情绪分布柱状图or折线图", subtitle="2023"
                    ),
                    toolbox_opts=opts.ToolboxOpts(),
                )
            )
            st_pyecharts(
                b, key="echarts"
            )

        elif option == '饼图':
            l = ['消极', '中性',  '积极']
            pie3 = (
                Pie()
                .add("", [list(z) for z in zip(l, data1)])
                .set_global_opts(title_opts=opts.TitleOpts(title="数据清洗后的情绪分布饼图"),
                                 legend_opts=opts.LegendOpts(pos_right="right", pos_bottom="bottom"))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"),
                                 tooltip_opts=opts.TooltipOpts(formatter="{b}: {c} ({d}%)"))
            )
            st_pyecharts(pie3)

    # 在这里添加关于页面的内容
elif page == '待解锁':
    st.write('什么也没有')
    # 在这里添加联系页面的内容
