# 导入所需的库
import requests
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 获取 TIOBE Index 的网页内容
url = "https://www.tiobe.com/tiobe-index/"
response = requests.get(url)
html = response.text

# 从网页内容中提取编程语言的名称和流行度
pattern = r'<tr>.*?<td class="td-top20">.*?<td>(.*?)</td>.*?<td>(.*?)%</td>'
matches = re.findall(pattern, html, re.DOTALL)

# 创建一个字典，存储编程语言的名称和流行度
languages = {}
for match in matches:
    name = match[0].strip()
    popularity = float(match[1])
    languages[name] = popularity

# 创建一个词云对象，设置字体、背景颜色和最大词数
wc = WordCloud(font_path="simhei.ttf", background_color="white", max_words=20)

# 根据编程语言的流行度生成词云
wc.generate_from_frequencies(languages)

# 显示和保存词云图像
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()
wc.to_file("wordcloud.png")
