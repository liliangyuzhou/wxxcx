# coding=utf-8
# @Time    : 2020/6/21 11:27 下午
# @Author  : liliang
# @File    : miniumtest.py
import minium

mini = minium.WXMinium()
print(mini)
system_info = mini.get_system_info()
print(system_info)
