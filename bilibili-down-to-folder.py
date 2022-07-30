import glob
import json
import os
import shutil


def get_metadata(folder):
    for file in os.listdir(folder):
        if file.endswith('.dvi') or file.endswith('.info'):
            with open(os.path.join(folder, file), 'r',encoding='utf8') as f:
                return json.loads(f.read())
def filter_name(name):
    '''
    sets = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in name:
        if char in sets:
            name = name.replace(char, '')'''
    return name


def export_video(folder,target):
    def copy_video(folder,target):
        for file in glob.glob(os.path.join(folder,'*.mp4')):
            shutil.copy(file,target)

    for file in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, file)):
            data=get_metadata(os.path.join(folder, file)) 
            title=data['PartName']
            id=data['PartNo']
            copy_video(os.path.join(folder, file),os.path.join(target,'%s.%s.mp4'%(id,filter_name(title))))

def handle_single_video(path):
    data=get_metadata(path)
    vfolder=data['Title']
    target=os.path.join(path, os.pardir,filter_name(vfolder))
    try:
        os.makedirs(target)
    except Exception:
        print('Dir exists')
        return
    export_video(path, target)

if __name__ == '__main__':
    path=input('Path to folder:')
    for file in glob.glob(os.path.join(path, '[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*')):
        vf=os.path.join(path, file)
        if os.path.isdir(vf):
            try:
                handle_single_video(vf)
            except Exception as e:
                print(vf)
    '''fixing video metadata
    for file in os.listdir(target):
        video=os.path.join(target, file)
        print(video)
        os.system('ffmpeg -i "%s" -vcodec copy -acodec copy -movflags faststart "%s"' % (video, '[fix]'+video))
    '''