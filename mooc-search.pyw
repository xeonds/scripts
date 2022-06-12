#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from tkinter import *
import requests
import hashlib
import time

LOG_LINE_NUM = 0

class mooc_gui:
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name

    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("mooc_util")
        self.init_window_name.geometry('480x640+10+10')
        #标签
        self.init_data_label = Label(self.init_window_name, text="关键字")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_window_name, text="搜素结果")
        self.result_data_label.grid(row=6, column=0)
        self.log_label = Label(self.init_window_name, text="日志")
        self.log_label.grid(row=12, column=0)
        #文本框
        self.init_data_Text = Text(self.init_window_name, width=48, height=1)  #原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=5)
        self.result_data_Text = Text(self.init_window_name, width=64, height=24)  #处理结果展示
        self.result_data_Text.grid(row=7, column=0, rowspan=5,columnspan=2)
        self.log_data_Text = Text(self.init_window_name, width=64, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=0,columnspan=2)
        #按钮
        self.str_trans_to_md5_button = Button(self.init_window_name, text="搜索", width=10,command=self.search_ans)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=1, column=1)

    #搜索答案
    def search_ans(self):
        word = self.init_data_Text.get(1.0,END).strip().replace("\n","")
        cookies = {
            '__yjs_duid': '1_0bd577a4a992630672a45e2fa3d608391655039108950',
            'Hm_lvt_28b554d945bf3b94a6f5b87c453c73ce': '1655039107',
            'ASPSESSIONIDCCDCSBTS': 'FJHCIMOCPCFJJILFFEADICEE',
            'ASPSESSIONIDACDDSASS': 'OPOJHDPCMJBPEJBKOEHLMODB',
            'Hm_lpvt_28b554d945bf3b94a6f5b87c453c73ce': '1655041620',
        }
        headers = {
            'authority': 'www.jhq8.cn',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            # Requests sorts cookies= alphabetically
            # 'cookie': '__yjs_duid=1_0bd577a4a992630672a45e2fa3d608391655039108950; Hm_lvt_28b554d945bf3b94a6f5b87c453c73ce=1655039107; ASPSESSIONIDCCDCSBTS=FJHCIMOCPCFJJILFFEADICEE; ASPSESSIONIDACDDSASS=OPOJHDPCMJBPEJBKOEHLMODB; Hm_lpvt_28b554d945bf3b94a6f5b87c453c73ce=1655041620',
            'referer': 'https://www.jhq8.cn/s/test/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Microsoft Edge";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.39',
        }
        response = requests.get('https://www.jhq8.cn/s/'+word+'/', cookies=cookies, headers=headers)
        soup=BeautifulSoup(response.text, 'html.parser')
        urls=soup.find_all("div",class_='lift_remen-list')
        for url in urls:
            pass
            
        self.result_data_Text.delete(1.0,END)
        self.result_data_Text.insert(1.0,urls)
        self.write_log_to_Text("INFO: success")

    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time

    #日志动态打印
    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0,2.0)
            self.log_data_Text.insert(END, logmsg_in)


def gui_main():
    init_window = Tk()              #实例化出一个父窗口
    ZMJ_PORTAL = mooc_gui(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


gui_main()