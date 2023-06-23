import streamlit as st  # 网页设计库
import pandas as pd  # 数据分析
import numpy as np  # 数据计算
from streamlit_echarts import st_pyecharts  # 依靠于pyecharts的一个可呈现在streamlit端的制图库
import pyecharts.options as opts  # 图表选项库
from pyecharts.charts import Pie  # 饼图库
from pyecharts.charts import Bar  # 柱状图
from wordcloud import WordCloud  # 词云库
import matplotlib.pyplot as plt  # 制图库
import plotly.express as px  # 制图库
import jieba  # 中文分词库
from PIL import Image  # 读图片用的库
from collections import defaultdict  # 情感分析库


# 饼图函数
def drawpie(ln, ls, name):
    pie = (
        Pie()
        .add("", [list(z) for z in zip(ln, ls)])
        .set_global_opts(title_opts=opts.TitleOpts(title=name),
                         legend_opts=opts.LegendOpts(pos_right="right", pos_bottom="bottom"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"),
                         tooltip_opts=opts.TooltipOpts(formatter="{b}: {c} ({d}%)"))
    )
    st_pyecharts(pie)


# 柱状图函数
def drawbar(ln, ls, name):
    bar = (
        Bar()
        .add_xaxis(ln)
        .add_yaxis("人数", ls)
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=name, subtitle="2023"
            ),
            toolbox_opts=opts.ToolboxOpts(),
        )
    )
    st_pyecharts(bar)


# 散点图函数
def drawscatter(new_data):
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


# 词云函数
def drawcloud(filepath):
    # 读取文本文件
    with open(filepath, 'r', encoding='utf-8') as file:
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


# nlp情感分析
def sentiment_analysis(txt):
    # 生成stopword表，需要去除一些否定词和程度词汇
    stopwords = set()
    fr = open('停用词.txt', 'r', encoding='utf-8')
    for word in fr:
        stopwords.add(word.strip())  # Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。
    # 读取否定词文件
    not_word_file = open('否定词.txt', 'r+', encoding='utf-8')
    not_word_list = not_word_file.readlines()
    not_word_list = [w.strip() for w in not_word_list]
    # 读取程度副词文件
    degree_file = open('程度副词.txt', 'r+', encoding='utf-8')
    degree_list = degree_file.readlines()
    degree_list = [item.split(',')[0] for item in degree_list]
    # 生成新的停用词表
    with open('stopwords.txt', 'w', encoding='utf-8') as f:
        for word in stopwords:
            if (word not in not_word_list) and (word not in degree_list):
                f.write(word + '\n')

    # jieba分词后去除停用词
    def seg_word(sentence):
        seg_list = jieba.cut(sentence)
        seg_result = []
        for i in seg_list:
            seg_result.append(i)
        stopwords = set()
        with open('stopwords.txt', 'r', encoding='utf-8') as fr:
            for i in fr:
                stopwords.add(i.strip())
        return list(filter(lambda x: x not in stopwords, seg_result))

    # 找出文本中的情感词、否定词和程度副词
    def classify_words(word_list):
        # 读取情感词典文件
        sen_file = open('BosonNLP_sentiment_score.txt', 'r+',
                        encoding='utf-8')
        # 获取词典文件内容
        sen_list = sen_file.readlines()
        # 创建情感字典
        sen_dict = defaultdict()
        # 读取词典每一行的内容，将其转换成字典对象，key为情感词，value为其对应的权重
        for i in sen_list:
            if len(i.split(' ')) == 2:
                sen_dict[i.split(' ')[0]] = i.split(' ')[1]

        # 读取否定词文件
        not_word_file = open('否定词.txt', 'r+', encoding='utf-8')
        not_word_list = not_word_file.readlines()
        # 读取程度副词文件
        degree_file = open('程度副词.txt', 'r+', encoding='utf-8')
        degree_list = degree_file.readlines()
        degree_dict = defaultdict()
        for i in degree_list:
            degree_dict[i.split(',')[0]] = i.split(',')[1]

        sen_word = dict()
        not_word = dict()
        degree_word = dict()
        # 分类
        for i in range(len(word_list)):
            word = word_list[i]
            if word in sen_dict.keys() and word not in not_word_list and word not in degree_dict.keys():
                # 找出分词结果中在情感字典中的词
                sen_word[i] = sen_dict[word]
            elif word in not_word_list and word not in degree_dict.keys():
                # 分词结果中在否定词列表中的词
                not_word[i] = -1
            elif word in degree_dict.keys():
                # 分词结果中在程度副词中的词
                degree_word[i] = degree_dict[word]

        # 关闭打开的文件
        sen_file.close()
        not_word_file.close()
        degree_file.close()
        # 返回分类结果
        return sen_word, not_word, degree_word

    # 计算情感词的分数
    def score_sentiment(sen_word, not_word, degree_word, seg_result):
        # 权重初始化为1
        W = 1
        score = 0
        # 情感词下标初始化
        sentiment_index = -1
        # 情感词的位置下标集合
        sentiment_index_list = list(sen_word.keys())
        # 遍历分词结果
        for i in range(0, len(seg_result)):
            # 如果是情感词
            if i in sen_word.keys():
                # 权重*情感词得分
                score += W * float(sen_word[i])
                # 情感词下标加一，获取下一个情感词的位置
                sentiment_index += 1
                if sentiment_index < len(sentiment_index_list) - 1:
                    # 判断当前的情感词与下一个情感词之间是否有程度副词或否定词
                    for j in range(sentiment_index_list[sentiment_index], sentiment_index_list[sentiment_index + 1]):
                        # 更新权重，如果有否定词，权重取反
                        if j in not_word.keys():
                            W *= -1
                        elif j in degree_word.keys():
                            W *= float(degree_word[j])
            # 定位到下一个情感词
            if sentiment_index < len(sentiment_index_list) - 1:
                i = sentiment_index_list[sentiment_index + 1]
        return score

    # 计算得分
    def sentiment_score(sentence):
        # 1.对文档分词
        seg_list = seg_word(sentence)
        # 2.将分词结果转换成字典，找出情感词、否定词和程度副词
        sen_word, not_word, degree_word = classify_words(seg_list)
        # 3.计算得分
        score = score_sentiment(sen_word, not_word, degree_word, seg_list)
        return score

    f = (sentiment_score(txt))
    return f


# 定义浏览器页面索引标签
st.set_page_config(
    page_title="泸溪河冰红茶最配队",
    page_icon="🍹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 界面设计
if st.sidebar.button('首页'):
    st.markdown('_produced by_ 泸溪河冰红茶最配队')

    # 在这里添加首页的内容
    st.title('欢迎来到我们的课设展示页面！')
    st.title('本次:blue[Python课设]主题：')
    st.title('基于Python的微博文本情绪分析与可视化🌐')
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
                            ['请选择一个你感兴趣的话题', '产品研究中心【apple watch】', '民生热点市集【考试周】', '时政话题速递【c919】'])

# 根据选择的页面显示不同内容
if page == '产品研究中心【apple watch】':
    st.write('走进生活中的产品，以apple watch为例，我们来看看微博用户对apple watch持何看法')

    st.header('当大家谈到Apple Watch🔍：')

    # 是否显示词云
    option0 = st.selectbox('_词云_', ('是否显示关于apple watch的词云', '是', '否'))
    if option0 == '是':
        drawcloud('apple watch.txt')

    # 分析方式设置
    option = st.selectbox('_词典选择_',
                          ('选择一个你感兴趣的词典', '大连理工情感词典', 'BosonNLP情感词典', '知网情感词典'))

    if option == '大连理工情感词典':
        st.markdown('大连理工情感词典它将词类分为两大类七小类')
        st.markdown('两大类：:blue[积极、消极]')
        st.markdown('七小类：:blue[愤怒、厌恶、惊恐、伤心、惊喜、赞成、开心]')

        option = st.selectbox('_呈现方式_', ('选择一个你喜欢的呈现方式', '柱状图', '饼图'))

        # 数据清洗
        ls = pd.read_csv('apple情绪.csv')
        ls = np.array(ls)  # 转换为 ndarray
        ls = ls.reshape(1, len(ls)).tolist()  # 转换成 List [[1, 2, 3]]
        ls = ls[0]  # 取第一个元素得到最终结果 [1, 2, 3]
        del ls[0]
        ls1 = ls[0:2]
        ls2 = ls[2:9]
        ln1 = ['积极', '消极']
        ln2 = ['愤怒', '厌恶', '惊恐', '伤心', '惊喜', '赞成', '开心']

        if option == '柱状图':

            drawbar(ln1, ls1, "两大类的情绪分布柱状图or折线图")
            drawbar(ln2, ls2, "七小类的情绪分布柱状图or折线图")

        elif option == '饼图':

            drawpie(ln1, ls1, "两大类的情绪分布饼图")
            drawpie(ln2, ls2, "七小类的情绪分布饼图")


    elif option == 'BosonNLP情感词典':
        st.markdown('BosonNLP情感词典主要是通过数值展现其情绪的积极性与消极性，'
                    ':blue[数值越高，情绪积极性越强，数值越低，情绪消极性越强]')
        option = st.selectbox('_呈现方式_', ('选择一个你喜欢的呈现方式', '散点图', '柱状图', '饼图'))

        file_path = 'apple nlp情绪分析.txt'  # 文本文件的路径
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

        ls = [a, b, c, d]
        ln = ['很消极', '一般消极', '一般积极', '很积极']

        if option == '散点图':
            st.markdown(
                '由于数据量大，数值集中于0左右，为了更清晰地观察数据分布，我们摘除了大于20和小于-20的数据，得到如下散点分布图')

            drawscatter(new_data)

        elif option == '柱状图':

            drawbar(ln, ls, "情绪分布柱状图")

        elif option == '饼图':

            drawpie(ln, ls, "情绪分布饼图")

    elif option == '知网情感词典':
        st.markdown('知网情感词典主要是通过情感分词展现情绪的积极性与消极性，它将情绪分为三类：')
        st.markdown(':blue[大于零的为积极情绪，等于零的为中性情绪，小于零的为消极情绪]')
        option = st.selectbox('_呈现方式_', ('选择一个你喜欢的呈现方式', '散点图', '柱状图', '饼图'))

        # 知网情感词典情感分析处理后的文本内容
        file_path = 'result_data3.txt'

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
        new_data = []

        # 删除过大或者过小数据
        for element in emotion_scores:
            if element <= 20 and element >= -20:
                new_data.append(element)

        a = 0
        b = 0
        c = 0
        # 给情感数据定界分类
        for i in new_data:
            if i < 0:
                a += 1
            if i == 0:
                b += 1
            if i > 0:
                c += 1

        ls = [a, b, c]
        ln = ['消极', '中性', '积极']

        if option == '散点图':
            st.markdown(
                '由于数据量大，数值集中于0左右，为了更清晰地观察数据分布，我们摘除了大于20和小于-20的数据，得到如下散点分布图')

            drawscatter(new_data)

        elif option == '柱状图':

            drawbar(ln, ls, "情绪分布柱状图")

        elif option == '饼图':

            drawpie(ln, ls, "情绪分布饼图")

elif page == '民生热点市集【考试周】':
    st.write('我们来看看期末周的人们在想什么')

    # 展示一级标题
    st.header('考试周大家be like：')

    # 是否显示词云
    option0 = st.selectbox('_词云_', ('是否显示关于考试周的词云', '是', '否'))
    if option0 == '是':
        drawcloud('weibowenben.txt')

    # 分析方式设置
    option = st.selectbox('_词典选择_',
                          ('选择一个你感兴趣的词典', '大连理工情感词典', 'BosonNLP情感词典', '知网情感词典'))

    if option == '大连理工情感词典':
        st.markdown('大连理工情感词典它将词类分为两大类七小类')
        st.markdown('两大类：:blue[积极、消极]')
        st.markdown('七小类：:blue[愤怒、厌恶、惊恐、伤心、惊喜、赞成、开心]')

        option = st.selectbox('_呈现方式_', ('选择一个你喜欢的呈现方式', '柱状图', '饼图'))

        # 数据清洗
        ls = pd.read_csv('情绪总分析.csv')
        ls = np.array(ls)  # 转换为 ndarray
        ls = ls.reshape(1, len(ls)).tolist()  # 转换成 List [[1, 2, 3]]
        ls = ls[0]  # 取第一个元素得到最终结果 [1, 2, 3]
        del ls[0]
        ls1 = ls[0:2]
        ls2 = ls[2:9]
        ln1 = ['积极', '消极']
        ln2 = ['愤怒', '厌恶', '惊恐', '伤心', '惊喜', '赞成', '开心']

        if option == '柱状图':

            drawbar(ln1, ls1, "两大类的情绪分布柱状图or折线图")
            drawbar(ln2, ls2, "七小类的情绪分布柱状图or折线图")

        elif option == '饼图':

            drawpie(ln1, ls1, "两大类的情绪分布饼图")
            drawpie(ln2, ls2, "七小类的情绪分布饼图")


    elif option == 'BosonNLP情感词典':
        st.markdown('BosonNLP情感词典主要是通过数值展现其情绪的积极性与消极性，'
                    ':blue[数值越高，情绪积极性越强，数值越低，情绪消极性越强]')
        option = st.selectbox('_呈现方式_', ('选择一个你喜欢的呈现方式', '散点图', '柱状图', '饼图'))

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

        ls = [a, b, c, d]
        ln = ['很消极', '一般消极', '一般积极', '很积极']

        if option == '散点图':
            st.markdown(
                '由于数据量大，数值集中于0左右，为了更清晰地观察数据分布，我们摘除了大于20和小于-20的数据，得到如下散点分布图')

            drawscatter(new_data)

        elif option == '柱状图':

            drawbar(ln, ls, "情绪分布柱状图")

        elif option == '饼图':

            drawpie(ln, ls, "情绪分布饼图")

    elif option == '知网情感词典':
        st.markdown('知网情感词典主要是通过情感分词展现情绪的积极性与消极性，它将情绪分为三类：')
        st.markdown(':blue[大于零的为积极情绪，等于零的为中性情绪，小于零的为消极情绪]')
        option = st.selectbox('_呈现方式_', ('选择一个你喜欢的呈现方式', '散点图', '柱状图', '饼图'))

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
        new_data = []

        # 删除过大或者过小数据
        for element in emotion_scores:
            if element <= 20 and element >= -20:
                new_data.append(element)

        a = 0
        b = 0
        c = 0
        # 给情感数据定界分类
        for i in new_data:
            if i < 0:
                a += 1
            if i == 0:
                b += 1
            if i > 0:
                c += 1

        ls = [a, b, c]
        ln = ['消极', '中性', '积极']

        if option == '散点图':
            st.markdown(
                '由于数据量大，数值集中于0左右，为了更清晰地观察数据分布，我们摘除了大于20和小于-20的数据，得到如下散点分布图')

            drawscatter(new_data)

        elif option == '柱状图':

            drawbar(ln, ls, "情绪分布柱状图")

        elif option == '饼图':

            drawpie(ln, ls, "情绪分布饼图")

    # 在这里添加关于页面的内容
elif page == '时政话题速递【c919】':
    st.write('5.28 C919的商业首航成功，昭示了中国高端制造业的崛起以及未来国内民航市场的巨大潜力')
    st.write('接下来我们走进微博来看看大家对此持何看法')

    # 展示一级标题
    st.header('当谈到C919,我们第一时间在想：')

    # 是否显示词云
    option0 = st.selectbox('_词云_', ('是否显示关于C919的词云', '是', '否'))
    if option0 == '是':
        drawcloud('c919.txt')

    # 分析方式设置
    option = st.selectbox('_词典选择_',
                          ('选择一个你感兴趣的词典', '大连理工情感词典', 'BosonNLP情感词典', '知网情感词典'))

    if option == '大连理工情感词典':
        st.markdown('大连理工情感词典它将词类分为两大类七小类')
        st.markdown('两大类：:blue[积极、消极]')
        st.markdown('七小类：:blue[愤怒、厌恶、惊恐、伤心、惊喜、赞成、开心]')

        option = st.selectbox('_呈现方式_', ('选择一个你喜欢的呈现方式', '柱状图', '饼图'))

        # 数据清洗
        ls = pd.read_csv('c919大连情绪.csv')
        ls = np.array(ls)  # 转换为 ndarray
        ls = ls.reshape(1, len(ls)).tolist()  # 转换成 List [[1, 2, 3]]
        ls = ls[0]  # 取第一个元素得到最终结果 [1, 2, 3]
        del ls[0]
        ls1 = ls[0:2]
        ls2 = ls[2:9]
        ln1 = ['积极', '消极']
        ln2 = ['愤怒', '厌恶', '惊恐', '伤心', '惊喜', '赞成', '开心']

        if option == '柱状图':

            drawbar(ln1, ls1, "两大类的情绪分布柱状图or折线图")
            drawbar(ln2, ls2, "七小类的情绪分布柱状图or折线图")

        elif option == '饼图':

            drawpie(ln1, ls1, "两大类的情绪分布饼图")
            drawpie(ln2, ls2, "七小类的情绪分布饼图")


    elif option == 'BosonNLP情感词典':
        st.markdown('BosonNLP情感词典主要是通过数值展现其情绪的积极性与消极性，'
                    ':blue[数值越高，情绪积极性越强，数值越低，情绪消极性越强]')
        option = st.selectbox('_呈现方式_', ('选择一个你喜欢的呈现方式', '散点图', '柱状图', '饼图'))

        file_path = 'c919 nlp情绪分析.txt'  # 文本文件的路径
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

        ls = [a, b, c, d]
        ln = ['很消极', '一般消极', '一般积极', '很积极']

        if option == '散点图':
            st.markdown(
                '由于数据量大，数值集中于0左右，为了更清晰地观察数据分布，我们摘除了大于20和小于-20的数据，得到如下散点分布图')

            drawscatter(new_data)

        elif option == '柱状图':

            drawbar(ln, ls, "情绪分布柱状图")

        elif option == '饼图':

            drawpie(ln, ls, "情绪分布饼图")

    elif option == '知网情感词典':
        st.markdown('知网情感词典主要是通过情感分词展现情绪的积极性与消极性，它将情绪分为三类：')
        st.markdown(':blue[大于零的为积极情绪，等于零的为中性情绪，小于零的为消极情绪]')
        option = st.selectbox('_呈现方式_', ('选择一个你喜欢的呈现方式', '散点图', '柱状图', '饼图'))

        # 知网情感词典情感分析处理后的文本内容
        file_path = 'result_data4.txt'

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
        new_data = []

        # 删除过大或者过小数据
        for element in emotion_scores:
            if element <= 20 and element >= -20:
                new_data.append(element)

        a = 0
        b = 0
        c = 0
        # 给情感数据定界分类
        for i in new_data:
            if i < 0:
                a += 1
            if i == 0:
                b += 1
            if i > 0:
                c += 1

        ls = [a, b, c]
        ln = ['消极', '中性', '积极']

        if option == '散点图':
            st.markdown(
                '由于数据量大，数值集中于0左右，为了更清晰地观察数据分布，我们摘除了大于20和小于-20的数据，得到如下散点分布图')

            drawscatter(new_data)

        elif option == '柱状图':

            drawbar(ln, ls, "情绪分布柱状图")

        elif option == '饼图':

            drawpie(ln, ls, "情绪分布饼图")

txt = st.sidebar.text_input('一个小彩蛋🎈')

if txt:
    score = sentiment_analysis(txt)
    st.sidebar.write('情感分数:', score)
    if score > 0:
        st.sidebar.markdown('[人间六月天，开心每一天✨]')
    if score == 0:
        st.sidebar.markdown('[生活就是这样慢慢亦满满]')
    if score < 0:
        st.sidebar.markdown('[别沮丧，生活就像心电图，一帆风顺就说明你挂了]')
