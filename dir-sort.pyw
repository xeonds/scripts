#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import shutil
import sys
from tkinter.filedialog import askdirectory
from uuid import uuid4
from tkinter import *
import time
import os
import json

def unique_covert(file_path):
    new_path = '|'.join(file_path.split(os.sep)[:-1])
    if not new_path: return file_path
    return os.path.basename(file_path) + ' (' + new_path + ')' 

class Sort:
    def __init__(self, folder, method):
        if not os.path.isdir(folder): 
            raise Exception("Folder '{}' not found.".format(folder))  
        if method not in ['name','extension','time']:
            raise Exception("Method '{}' not supported.".format(method))  
        self._method=method
        self._dir=folder
        self._tmp_dir = os.path.join(os.path.dirname(os.path.dirname(self._dir)), str(uuid4()))

    def execution(self):
        # create temporary directory
        os.mkdir(self._tmp_dir)
        # choose the classify function to use
        if self._method == 'name':
            classify_func=self.by_name
        elif self._method == 'extension':
            classify_func=self.by_ext
        elif self._method == 'time':
            classify_func=self.by_time
        # 
        save_backup_gen = self.save_back_up()
        classify_gen    = classify_func()
        # begin           = time.time()
        while True:
            tup      = classify_gen.send(None)
            if not tup:
                break
            save_backup_gen.send(tup)
        shutil.rmtree(self._dir, ignore_errors=False)
        os.renames(self._tmp_dir, self._dir)
        try:
            save_backup_gen.send(None)
        except StopIteration:
            pass 
        # time spend: time.time() - begin

    def save_back_up(self):
        back_up_file = os.path.join(self._dir, '.backup.json')
        if os.path.exists(back_up_file):
            self.go_back(self._dir)
        back_up_tree = {}
        while True:
            tup = yield 
            if not tup:
                break
            (now, prev) = tup
            back_up_tree[now] = prev
        with open(back_up_file, 'w') as buf:
            json.dump(back_up_tree, buf, indent=4)

    def go_back(self):
        self._dir = self._dir.decode('utf-8')
        self._tmp_dir    = os.path.join(os.path.dirname(os.path.dirname(self._dir)), str(uuid4()))
        os.mkdir(self._tmp_dir)
        back_up_tree = {}
        back_up_file = os.path.join(self._dir, '.backup.json')
        if not os.path.exists(back_up_file):
            raise Exception('已经是初始状态')
        with open(back_up_file, 'rb') as buf:
            back_up_tree = json.load(buf)
        if not back_up_tree:
            raise Exception('备份文件已损坏或不存在')
        for src, old in back_up_tree.items():
            src_file  = os.path.join(self._dir, src)
            dest_file = os.path.join(self._tmp_dir, old)
            dest_dir  = os.path.dirname(dest_file)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            shutil.move(src_file, dest_file)
        shutil.rmtree(self._dir, ignore_errors=False)
        os.rename(self._tmp_dir, self._dir)

    def by_name(self):
        for dir_ in os.walk(self._dir):
            base_dir = dir_[0]
            for f in dir_[2]:
                abs_file_path = os.path.join(base_dir, f)
                rel_file_path = os.path.relpath(abs_file_path, self._dir)
                first_char = f[0]
                if first_char.isalnum():
                    dest_dir = os.path.join(self._tmp_dir, first_char)
                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)
                    filename  = unique_covert(rel_file_path)
                    dest_file = os.path.join(dest_dir, filename)
                    shutil.move(abs_file_path, dest_file)
                    yield (os.path.join(first_char, filename), rel_file_path)
                else:
                    shutil.move(abs_file_path, os.path.join(self._tmp_dir, f))
                    yield (f, rel_file_path)
        yield None 

    def by_ext(self): 
        from collections import defaultdict
        ext_files = defaultdict(list)
        for dir_ in os.walk(self._dir):
            for f in dir_[2]:
                exts = f.split('.')
                key  = exts[-1] if len(exts) != 1 else 'default'
                ext_files[key].append(os.path.join(dir_[0], f))
        for ext, file_list in ext_files.items():
            dest_dir = os.path.join(self._tmp_dir, ext)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            for file_path in file_list:
                filename      = unique_covert(os.path.relpath(file_path, self._dir))
                dest          = os.path.join(dest_dir, filename)
                rel_file_path = os.path.relpath(file_path, self._dir)
                os.renames(file_path, dest)
                yield (os.path.join(ext, filename), rel_file_path)
        yield None # 按修改时间分类 

    def by_time(self):
        for dir_ in os.walk(self._dir):
            base_dir = dir_[0]
            for f in dir_[2]:
                abs_file_path = os.path.join(base_dir, f)
                rel_file_path = os.path.relpath(abs_file_path, self._dir)
                if os.path.islink(abs_file_path):
                    rel_dest_dir = 'link'
                    dest_dir     = os.path.join(self._tmp_dir, 'link')
                else:
                    mtime        = os.stat(abs_file_path)[8]
                    (y, m, d)    = map(str, time.localtime(mtime)[:3])
                    rel_dest_dir = os.path.join(y, m, d)
                    dest_dir     = os.path.join(self._tmp_dir, rel_dest_dir)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                filename  = unique_covert(rel_file_path)
                dest_file = os.path.join(dest_dir, filename)
                shutil.move(abs_file_path, dest_file)
                yield (os.path.join(rel_dest_dir, filename), rel_file_path)
        yield None # 按字母分类

class gui:
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name
        self.init_window_name.title("Dir-Sort")
        self.init_window_name.geometry('700x440+10+10')
        self._type=1
        self._path=None
        self._sort=None

    #设置窗口
    def set_init_window(self):
        self.form = Canvas(self.init_window_name,width = 700,height = 440)
        self.form.place(x = 0,y = 0,width = 700,height = 440)

        self.lf_sort_method = LabelFrame(self.form,text="整理方式",takefocus = True,width = 10,height = 4)
        self.lf_sort_method.place(x = 24,y = 144,width = 144,height = 144)
        self.rb_by_type = Radiobutton(self.lf_sort_method,value=1,text="按后缀",variable=self._type)
        self.rb_by_type.place(x = 22,y = 29,width = 72,height = 24)
        self.rb_by_time = Radiobutton(self.lf_sort_method,value=2,text="按时间",variable=self._type)
        self.rb_by_time.place(x = 22,y = 53,width = 72,height = 24)
        self.rb_by_name = Radiobutton(self.lf_sort_method,value=3,text="按名称",variable=self._type)
        self.rb_by_name.place(x = 22,y = 77,width = 72,height = 24)

        self.lf_path_to_sort = LabelFrame(self.form,text="待整理目录路径",takefocus = True,width = 10,height = 4)
        self.lf_path_to_sort.place(x = 24,y = 24,width = 144,height = 96)
        self.btn_choose_path = Button(self.lf_path_to_sort,text="选择",command=self.selectPath)
        self.btn_choose_path.place(x = 22,y = 29,width = 96,height = 24)
        
        self.lf_action = LabelFrame(self.form,text="整理",takefocus = True,width = 10,height = 4)
        self.lf_action.place(x = 24,y = 312,width = 144,height = 96)
        self.btn_do = Button(self.lf_action,text="整理",width = 10,height = 4,command=self.do)
        self.btn_do.place(x = 22,y = 8,width = 96,height = 28)
        self.btn_undo = Button(self.lf_action,text="撤销",width = 10,height = 4,command=self.undo)
        self.btn_undo.place(x = 22,y = 38,width = 96,height = 28)
        
        self.text_dir_struct = Text(self.form)
        self.text_dir_struct.place(x = 192,y = 24,width = 480,height = 384)

    def selectPath(self):
        self._path=StringVar()
        self._path.set(os.path.abspath("."))
        path = askdirectory()
        if path == "": self._path.get()
        else: self._path.set(path.replace("/", "\\"))
        r=os.popen('tree /f '+self._path.get())
        self.text_dir_struct.insert('insert',r.read())
        r.close()

    def do(self):
        if self._path==None:
            return
        self._sort=Sort(self._path.get(),['ext', 'mtime', 'word'][self._type-1])
        self._sort.execution()
        r=os.popen('tree /f '+self._path)
        self.text_dir_struct.insert('insert',r.read())
        r.close()

    def undo(self):
        if self._path==None:
            return
        self._sort.go_back()
        r=os.popen('tree /f '+self._path.get())
        self.text_dir_struct.insert('insert',r.read())
        r.close()

init_window = Tk()
sorts = gui(init_window)
sorts.set_init_window()
init_window.mainloop()