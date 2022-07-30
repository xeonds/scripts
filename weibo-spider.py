import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq
import time
import xlwt
 
#设置代理等（新浪微博的数据是用ajax异步下拉加载的，network->xhr）
host = 'm.weibo.cn'
base_url = 'https://%s/api/container/getIndex?' % host
user_agent = 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Mobile Safari/537.36'
 
#设置请求头
headers = {
    'Host': host,
    'Referer': 'https://m.weibo.cn/search?containerid=231522type%3D1%26q%3D%23%E7%BE%8E%E5%9B%BD%E7%96%AB%E6%83%85%23',
    'User-Agent': user_agent
}
 
# 按页数抓取数据
def get_single_page(page):
    #请求参数
    params = {
        'containerid': '231522type=1&q=#美国疫情#',
        'page_type': 'searchall',
        'page': page
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('抓取错误', e.args)
 
# 解析页面返回的json数据
global count
count = 0
def parse_page(json):
    global count
    items = json.get('data').get('cards')
    for item in items:
        item = item.get('mblog')
        if item:
            data = {
                'id': item.get('id'),
                'created': item.get('created_at'),
                'text': pq(item.get("text")).text(),  # 仅提取内容中的文本
            }
            yield data
            count +=1
 
 
if __name__ == '__main__':
    workbook = xlwt.Workbook(encoding='utf-8')# 创建一个表格
    worksheet = workbook.add_sheet('美国疫情')
    for page in range(1, 200):  # 瀑布流下拉式，加载200次
        json = get_single_page(page)
        results = parse_page(json)
        tmp_list = []
        print(count)
        for result in results: #需要存入的字段
            worksheet.write(count, 0, label=result.get('created').strip('\n'))
            worksheet.write(count, 1, label=result.get('text').strip('\n'))
 
        #time.sleep(0.5) #爬取时间间隔
        workbook.save('conv.xls')