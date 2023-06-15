#!/usr/bin/python
# -*- coding:utf-8 -*-
import jieba
txt = open("微博.txt", "r", encoding="utf-8").read()


def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':  # 判断一个uchar是否是汉字
        return True
    else:
        return False


def allcontents(contents):
    content = ''
    for i in contents:
        if is_chinese(i):
            content = content + i
    print('\n处理后的句子为:\n' + content)
    return content

txt1 = allcontents(txt)
words = jieba.lcut(txt1)
counts = {}
for word in words:
    if len(word) == 1:
        continue
    else:
        counts[word] = counts.get(word,0) + 1
items = list(counts.items())
items.sort(key=lambda x:x[1], reverse=True)
for i in range(100):
    word, count = items[i]
    print("{0:<10}{1:>5}".format(word, count))