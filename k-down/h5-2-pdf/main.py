#!/usr/bin/python3
import os
import re
import time
import logging
import requests
from bs4 import BeautifulSoup
from dashtable import html2md
from PyPDF2 import PdfFileMerger

header={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cookie": "lv=1; _uid=191344375; UID=191344375; vc=BC20AF6DEF74049C35A98A497ED918D7; xxtenc=5252e1ddb0233b8a1e4b76bba8b3104c; fid=16820; uname=21009201021; k8s=5a6705e44f28d254efb85a514c6693738fd018bc; jrose=EC185B96BDF518B4430CB640E85F6277.mooc-1766992143-mgkx9; route=440ceb57420433374ff0504da9778fc7; uf=b2d2c93beefa90dc86c5249277b5a0515fb3a392dc603cb5be8a7647aacbbe70c39710ba77c436d0554274954c4a6ce9748a002894d7f44e88b83130e7eb470482d49b6a3665adad3ca8199aea40b85fc992d031135b2ab78900094d3416108b067291c37c2271c4aa2ebad65cd196bb; _d=1653992295796; vc2=CEAE1411149EA3FBE34D0645BADB15ED; vc3=VzCmbRNnrlS4oXRBQRHk1C%2BZahZReehhZwOGYnvdRgpZJvaTfFGbU5kZl5vI5U42d7l5kWurK4NBXfrIu1qp4hwcXG8DOy3fPYrYDYF6pKGTWoxNa1txr8pLT7uLIGN4RI7tTqyRSHNuuEhkWJHukbp%2Bxb4qdeRglPjJlTCaTcg%3D750ddfc2f4e40856d6e2bcda7a431586; DSSTASH_LOG=C_38-UN_1065-US_191344375-T_1653992295797; thirdRegist=0; videojs_id=1167958",
    "Host": "mooc1.chaoxing.com",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://mooc1.chaoxing.com/ztnodedetailcontroller/visitnodedetail?courseId=200024577&knowledgeId=103220228&_from_=223058809_51685828_191344375_f63fc299bf04e0baa2a6737eb0e611cd&rtag=&nohead=1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53",
}
base_url = "http://www.chaoxing.com"

def parse_url_to_html(url, name):
  """
  解析URL,返回HTML内容
  :param url:解析的url
  :param name: 保存的html文件名
  :return: html
  """
  try:
    response = requests.get(url,headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    # 正文
    body = soup.find_all(class_="ans-cc")[-1]
    # 标题
    title = soup.find_all(class_="fix")[0].get_text()
    # 标题加入到正文的最前面，居中显示
    html = str(body)
    # # body中的img标签的src相对路径的改成绝对路径
    pattern = "(<img .*?src=\")(.*?)(\")"
    def func(m):
      if not m.group(3).startswith("http"):
        rtn = m.group(1) + base_url + m.group(2) + m.group(3)
        return rtn
      else:
        return m.group(1)+m.group(2)+m.group(3)
    html = re.compile(pattern).sub(func, html)
    html = html.encode("utf-8")
    with open(name,'wb') as f:f.write(html)
    return html
  except Exception as e:
    logging.error("解析错误", exc_info=True)

def get_url_list():
  """
  获取所有URL目录列表
  :return:
  """
  url="http://mooc1.chaoxing.com/ztnodedetailcontroller/visitnodedetail?courseId=200024577&knowledgeId=103220216&_from_=223058809_51685828_191344375_f63fc299bf04e0baa2a6737eb0e611cd&rtag=&nohead=1"
  response = requests.get(url,headers=header)
  soup = BeautifulSoup(response.content, "html.parser")
  menu_tag = soup.find_all(class_="mt10")[0]
  urls = []
  for li in menu_tag.find_all("li"):
    url = "http://mooc1.chaoxing.com" + li.a.get('href')
    urls.append(url)
  return urls

def save_md(htmls,md_name):
    with open(md_name,'w') as f:f.write(html2md(htmls))
  
def main():
    start = time.time()
    file_name = "western_music"
    urls = get_url_list()
    for index, url in enumerate(urls):
        html=parse_url_to_html(url, str(index) + ".html")
        save_md(html, str(index)+'.md')
        print("Saved "+str(index)+' page.')
    total_time = time.time() - start
    print(u"总共耗时：%f 秒" % total_time)


if __name__ == '__main__':
    #down htmls
    main()
    #convert pdf using html2pdf in windows
    #merge pdfs
    fm=PdfFileMerger()
    for pdf in [str(i)+'.pdf' for i in range(19)]:
        fm.append(pdf,import_bookmarks=True)
    fm.write(r'merged.pdf')