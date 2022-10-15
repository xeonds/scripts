#!/usr/bin/python3
# run on windows
# env prepare:
# - pip install pyhtml2pdf -i https://pypi.tuna.tsinghua.edu.cn/simple
# - install chrome
import os
from pyhtml2pdf import converter

for root, dirs, files in os.walk('./'):
    for name in files:
        if name[-5:]=='.html':
            path=os.path.abspath(name)
            converter.convert(f'file:///{path}', name[:-5]+'.pdf')
