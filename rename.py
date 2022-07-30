#!/usr/bin/python3

# 功能：重命名当前目录下的文件。需要文件名为连续数字编号并给出map.txt。
# TODO：支持map一一映射改名，支持正则匹配改名
# TODO：增加GUI界面/CLI接口

'''
map.txt示例

1-Go语言上手-基础语言.mp4
2-Go语言上手-工程实践.mp4
3-高质量编程与性能调优实战.mp4
4-高性能Go语言发行版优化与落地实践.mp4
5-设计模式之Database-SQL与GORM实践.mp4
6-实战项目-Go语言笔记服务.mp4
7-从需求到上线全流程.mp4
8-打开抖音互联网会发生什么.mp4
9-将我的服务开放给用户.mp4
10-架构初探-谁动了我的蛋糕.mp4
11-Git的正确使用姿势与最佳实践.mp4
12-数据结构与算法.mp4
13-深入浅出RPC框架.mp4
14-HTTP框架修炼之道.mp4
15-微服务架构原理与治理实战.mp4
16-走进消息队列.mp4
17-分布式定时任务那些事.mp4
18-带你认识存储&数据库.mp4
19-深入理解RDBMS.mp4
20-TOS对象存储实战.mp4
21-实操项目-老师手把手教.mp4
'''
import os


def rename(map,ext):
    for index, name in enumerate(map):
        if os.path.exists(str(index+1)+ext):
            os.rename(str(index+1)+ext, str.strip(name))

with open('map.txt') as f:
    map=f.readlines()
rename(map,'.mp4')