#!/usr/bin/python3

import requests
import argparse
import json
import os

class header:
    _header_path='data/header.json'
    def add(self,header_name,header_str):
        with open(self._header_path,mode='r') as f:
            header=json.load(f)
            header[header_name]=dict(line.split(": ", 1) for line in header_str.split("\n") if line != '')
        with open(self._header_path,mode='w') as f:
            json.dump(header,f)
    def get(self,header_name):
        with open(self._header_path,mode='r') as f:
            header=json.load(f)
            return header[header_name] if header_name in header else None

def rename(path='data/rename_map.txt'):
    with open(path,encoding='utf-8') as list:
        for file in os.listdir('res/'):
            os.rename('res/'+file, 'res/'+list.readline().strip()+'.mp4')

def down_video(url='',headers={},param='',path=''):
    try:
        pre_content_length = 0
        while True:
            res = requests.get(url, headers=headers, params=param, verify=False)
            content_length = int(res.headers['content-length'])
            if content_length < pre_content_length or (os.path.exists(path) and os.path.getsize(path) == content_length) or content_length == 0: 
                break
            pre_content_length = content_length
            with open(path, 'ab') as file:
                file.write(res.content)
                file.flush()
                print('下载成功,file size:%d total size:%d' % (os.path.getsize(path), content_length))
    except Exception as e:
        print(e)

def xinput(end='end', end_char=''):
    data = end
    while True:
        var = input()
        if var == str(end):
            break
        elif end_char != '' and var.find(end_char) != -1:
            var = var[0:var.find(end_char)]
            data = '{}\n{}'.format(data, var)
            break
        else:
            data = '{}\n{}'.format(data, var)
    return data.replace('{}\n'.format(end), '')

def get_param(url):
    url,param=url.split('?')
    param=dict(line.split("=", 1) for line in param.split("&") if line != '')
    return url,param

def del_line(file,line):
    with open(file,'r') as list:
        with open(file,'r+') as list_new:
            current_line,line = 0,0
            while current_line < (line - 1):
                list.readline()
                current_line += 1
            seek_point = list.tell()
            list_new.seek(seek_point, 0)
            list.readline()
            next_line = list.readline()
            while next_line:
                list_new.write(next_line)
                next_line = list.readline()
            list_new.truncate()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A simple Python script to download video from url.',prog='Video fetcher')
    h = header()

    parser.add_argument('--url', type=str, help='url of video', action='extend')
    parser.add_argument('--param', action='store_true', help='if url has param')
    parser.add_argument('--header', type=str, default=None, help='header to be used in downloading')
    parser.add_argument('--rename', action='store_true', help='rename videos after download')
    args = parser.parse_args()
    if args.header==None:
        headers={}
    elif h.get(args.header)==None:
        print('Not an exist header.Add it(input end to finish):',end='')
        h.add(args.header,xinput())
        headers=h.get(args.header)
    else:
        headers=h.get(args.header)
    if args.url==None:
        print('Downloading from list...')
        with open('data/list.txt','r') as list:
            for url in list.readlines():
                video_id=0
                while os.path.isfile('./res/'+str(video_id)+'.mp4'):video_id+=1
                if args.param==False:
                    u,p=get_param(url)
                else:
                    u,p=url,None
                down_video(u,h.get(args.header),p,'./res/'+str(video_id)+'.mp4')
                del_line('data/list.txt',1)
    else:
        print('Downloading from given urls...')
        for url in args.url:
            video_id=0
            while os.path.isfile('./res/'+str(video_id)+'.mp4'):video_id+=1
            if args.param==False:
                u,p=get_param(url)
            else:
                u,p=url,None
            down_video(u,h.get(args.header),p,'./res/'+str(video_id)+'.mp4')
    if args.rename==True:
        rename()