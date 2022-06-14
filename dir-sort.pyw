#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from cgitb import text
import shutil
import sys
import tkinter
from tkinter.filedialog import askdirectory
from uuid import uuid4
from bs4 import BeautifulSoup
from tkinter import *
import requests
import time
import os
import json

LOG_LINE_NUM = 0



DEFAULT_KEY = 'default'
BACKUP_FILE = '.backup.json' # 防止迁移的时候出现文件重名的情况 
def unique_covert(file_path):
    new_path = '|'.join(file_path.split(os.sep)[:-1])
    if not new_path:
        return file_path
    return os.path.basename(file_path) + ' (' + new_path + ')' 

def coroutine(gen): 
    def wrapper(*arg, **kws):
        coroutine = gen(*arg, **kws)
        next(coroutine)
        return coroutine
    return wrapper

@coroutine 
def save_back_up(target_dir):
    string_len   = len(target_dir)
    back_up_file = os.path.join(target_dir, BACKUP_FILE)
    if os.path.exists(back_up_file):
        go_back(target_dir)
    back_up_tree = {}
    while True:
        tup = yield 
        if not tup:
            break
        (now, prev) = tup
        back_up_tree[now] = prev
    with open(back_up_file, 'w') as buf:
        json.dump(back_up_tree, buf, indent=4)        

# 按扩展名分类 
def classify_by_ext(target_dir, tmp_dir): 
    from collections import defaultdict
    ext_files = defaultdict(list)
    for dir_ in os.walk(target_dir):
        for f in dir_[2]:
            exts = f.split('.')
            key  = exts[-1] if len(exts) != 1 else DEFAULT_KEY
            ext_files[key].append(os.path.join(dir_[0], f))
    for ext, file_list in ext_files.items():
        dest_dir = os.path.join(tmp_dir, ext)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        for file_path in file_list:
            filename      = unique_covert(os.path.relpath(file_path, target_dir))
            dest          = os.path.join(dest_dir, filename).replace('\\','/')
            rel_file_path = os.path.relpath(file_path, target_dir).replace('\\','/')
            os.renames(file_path, dest)
            yield (os.path.join(ext, filename), rel_file_path)
    yield None # 按修改时间分类 

def classify_by_mtime(target_dir, tmp_dir): 
    for dir_ in os.walk(target_dir):
        base_dir = dir_[0]
        for f in dir_[2]:
            abs_file_path = os.path.join(base_dir, f)
            rel_file_path = os.path.relpath(abs_file_path, target_dir)
            if os.path.islink(abs_file_path):
                rel_dest_dir = 'link'
                dest_dir     = os.path.join(tmp_dir, 'link')
            else:
                mtime        = os.stat(abs_file_path)[8]
                (y, m, d)    = map(str, time.localtime(mtime)[:3])
                rel_dest_dir = os.path.join(y, m, d)
                dest_dir     = os.path.join(tmp_dir, rel_dest_dir)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            filename  = unique_covert(rel_file_path)
            dest_file = os.path.join(dest_dir, filename)
            shutil.move(abs_file_path.replace('\\','/'), dest_file.replace('\\','/'))
            yield (os.path.join(rel_dest_dir, filename), rel_file_path)
    yield None # 按字母分类

def classify_by_first_letter(target_dir, tmp_dir): 
    for dir_ in os.walk(target_dir):
        base_dir = dir_[0]
        for f in dir_[2]:
            abs_file_path = os.path.join(base_dir, f)
            rel_file_path = os.path.relpath(abs_file_path, target_dir)
            first_char = f[0]
            if first_char.isalnum():
                dest_dir = os.path.join(tmp_dir, first_char)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                filename  = unique_covert(rel_file_path)
                dest_file = os.path.join(dest_dir, filename)
                shutil.move(abs_file_path.replace('\\','/'), dest_file.replace('\\','/'))
                yield (os.path.join(first_char, filename), rel_file_path)
            else:
                shutil.move(abs_file_path.replace('\\','/'), os.path.join(tmp_dir, f).replace('\\','/'))
                yield (f, rel_file_path)
    yield None 

def go_back(target_dir):
    target_dir = target_dir.decode('utf-8')
    tmp_dir    = os.path.join(os.path.dirname(os.path.dirname(target_dir)), str(uuid4()))
    os.mkdir(tmp_dir)
    back_up_tree = {}
    back_up_file = os.path.join(target_dir, BACKUP_FILE)
    if not os.path.exists(back_up_file):
        raise Exception('已经是初始状态')
    with open(back_up_file, 'rb') as buf:
        back_up_tree = json.load(buf)
    if not back_up_tree:
        raise Exception('备份文件已损坏或不存在')
    for src, old in back_up_tree.items():
        src_file  = os.path.join(target_dir, src)
        dest_file = os.path.join(tmp_dir, old)
        dest_dir  = os.path.dirname(dest_file)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        shutil.move(src_file.replace('\\','/'), dest_file.replace('\\','/'))
    shutil.rmtree(target_dir, ignore_errors=False)
    os.rename(tmp_dir, target_dir)

def run(target_dir, classify_func):
    tmp_dir = os.path.join(os.path.dirname(os.path.dirname(target_dir)), str(uuid4()))
    os.mkdir(tmp_dir)
    target_dir=target_dir.replace('\\','/').replace(r'\\','/')
    tmp_dir=tmp_dir.replace('\\','/').replace(r'\\','/')

    save_backup_gen = save_back_up(target_dir)
    classify_gen    = classify_func(target_dir, tmp_dir)
    finished        = 0
    begin           = time.time()
    while True:
        tup      = classify_gen.send(None)
        finished += 1
        sys.stdout.write(u'已完成%s个文件\r' % finished)
        sys.stdout.flush()
        if not tup:
            break
        save_backup_gen.send(tup)
    print(u'已完成%s个文件，耗时%s秒' % (finished, time.time() - begin))

    shutil.rmtree(target_dir, ignore_errors=False)
    os.renames(tmp_dir, target_dir)
    try:
        save_backup_gen.send(None)
    except StopIteration:
        pass 

def main_sort(target_dir,op):
    if op == 'ext':
        run(target_dir, classify_by_ext)
    elif op == 'mtime':
        run(target_dir, classify_by_mtime)
    elif op == 'word':
        run(target_dir, classify_by_first_letter)
    elif op == 'back':
        go_back(target_dir)

class gui:
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name
        self.path=None
        self.type=1

    #设置窗口
    def set_init_window(self):
        self.form = Canvas(self.init_window_name,width = 700,height = 440)
        self.form.place(x = 0,y = 0,width = 700,height = 440)
        self.init_window_name.title("Dir-Sort")
        self.init_window_name.geometry('700x440+10+10')
        self.form.configure(bg = "#efefef")
        self.form.configure(highlightthickness = 0)

        LabelFrame_17 = LabelFrame(self.form,text="整理方式",takefocus = True,width = 10,height = 4)
        LabelFrame_17.place(x = 24,y = 144,width = 144,height = 144)
        LabelFrame_17.configure(relief = "groove")
        RadioButton_13 = Radiobutton(LabelFrame_17,value=1,text="按后缀",variable=self.type)
        RadioButton_13.place(x = 22,y = 29,width = 72,height = 24)
        RadioButton_14 = Radiobutton(LabelFrame_17,value=2,text="按时间",variable=self.type)
        RadioButton_14.place(x = 22,y = 53,width = 72,height = 24)
        RadioButton_15 = Radiobutton(LabelFrame_17,value=3,text="按名称",variable=self.type)
        RadioButton_15.place(x = 22,y = 77,width = 72,height = 24)
        self.type=1
        LabelFrame_18 = LabelFrame(self.form,text="待整理目录路径",takefocus = True,width = 10,height = 4)
        LabelFrame_18.place(x = 24,y = 24,width = 144,height = 96)
        LabelFrame_18.configure(relief = "groove")
        Button_12 = Button(LabelFrame_18,text="选择",width = 10,height = 4)
        Button_12.place(x = 22,y = 29,width = 96,height = 24)
        Button_12.configure(command=self.selectPath)
        self.dir_text = Text(self.form)
        self.dir_text.place(x = 192,y = 24,width = 480,height = 384)
        LabelFrame_20 = LabelFrame(self.form,text="整理",takefocus = True,width = 10,height = 4)
        LabelFrame_20.place(x = 24,y = 312,width = 144,height = 96)
        LabelFrame_20.configure(relief = "groove")
        bt_do = Button(LabelFrame_20,text="整理",width = 10,height = 4,command=self.do)
        bt_do.place(x = 22,y = 8,width = 96,height = 28)
        bt_undo = Button(LabelFrame_20,text="撤销",width = 10,height = 4,command=self.undo)
        bt_undo.place(x = 22,y = 38,width = 96,height = 28)

    def selectPath(self):
        self.path=StringVar()
        self.path.set(os.path.abspath("."))
        self.path_ = askdirectory()
        if self.path_ == "":
            self.path.get()
        else:
            self.path_ = self.path_.replace("/", "\\")
            self.path.set(self.path_)
        r=os.popen('tree /f '+self.path.get())
        self.dir_text.insert('insert',r.read())
        r.close()

    def do(self):
        if self.path==None:
            return
        main_sort(self.path.get(),['ext', 'mtime', 'word'][self.type-1])
        r=os.popen('tree /f '+self.path_)
        self.dir_text.insert('insert',r.read())
        r.close()

    def undo(self):
        if self.path==None:
            return
        main_sort(self.path.get(),'back')
        r=os.popen('tree /f '+self.path.get())
        self.dir_text.insert('insert',r.read())
        r.close()

init_window = Tk()
ZMJ_PORTAL = gui(init_window)
ZMJ_PORTAL.set_init_window()
init_window.mainloop()