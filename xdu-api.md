# 西电一站式API

以下是西电一站式的API：

## 统一身份认证登录

- 详细信息

|标题|内容|
|---|---|
|URL|`https://ids.xidian.edu.cn/authserver/login`|
|method|POST|

>URL好像弄错力（悲

- Response

>???

- 样例代码

```python
import requests

data={
    'username': 'xidian',
    'passwordText': 'passwordText',
}

response = requests.post('https://ids.xidian.edu.cn/authserver/login', data=data)
```

## 课表查询

- 详细信息

|标题|内容|
|---|---|
|URL|`https://ehall.xidian.edu.cn/jwapp/sys/wdkb/modules/xskcb/xsllsykb.do`|
|method|POST|
|负载|XNXQDM=2022-2023-1&SKZC=3|

- Response

```json
{
    "datas": {
        "xsllsykb": {
            "extParams": {
                "code": 1,
                "msg": "查询成功"
            },
            "pageSize": 0,
            "pageNumber": 0,
            "totalSize": -1,
            "rows": [
                {
                    "ZYDM": "0301",
                    "KSSJ": null,
                    "KKDWDM_DISPLAY": "物理学院",
                    "KSJC": 1,
                    "SKZC": "11111011101",
                    "DWDM": "1103",
                    "SKJS": "毕臻",
                    "NJDM_DISPLAY": "2021级",
                    "XNXQDM": "2022-2023-1",
                    "KBID": "E1EB71655DC81DE9E0530D13AC0AA361",
                    "SKBJ": "2103011,2103012,2103013,2103014,2103015",
                    "XMBLX": null,
                    "KKDWDM": "528",
                    "ZYDM_DISPLAY": "计算机科学与技术",
                    "XGXKLBDM": null,
                    "MS": null,
                    "KCM": "大学物理(II)",
                    "JASDM": "A-214",
                    "KBLB": "1",
                    "NJDM": "2021",
                    "KCH": "PY006002",
                    "JXLDM_DISPLAY": "A教学楼",
                    "ISTK_DISPLAY": "否",
                    "XS": 54,
                    "KCXZDM_DISPLAY": "必修",
                    "JASMC": "A-214",
                    "WID": "E1EB71655DC71DE9E0530D13AC0AA361",
                    "JSJC": 2,
                    "XXXQDM": "S",
                    "XGXKLBDM_DISPLAY": "",
                    "XH": "[学号]",
                    "BJDM_DISPLAY": "[班级代码]",
                    "XM": "[姓名]",
                    "ISTK": 0,
                    "YPSJDD": "1-16周 星期四 3-4节 A-214,1-5周,7-9周,11周 星期二 1-2节 A-214",
                    "XF": 3,
                    "SKXQ": 2,
                    "KCXZDM": "001",
                    "JXBID": "202220231PY00600216",
                    "TYXMDM_DISPLAY": "",
                    "KCLBDM_DISPLAY": "通识教育基础课",
                    "XXXQDM_DISPLAY": "南校区",
                    "XNXQDM_DISPLAY": "2022-2023学年第一学期",
                    "KXH": "16",
                    "SYXMMC": null,
                    "BJDM": "[班级代码]",
                    "KCLBDM": "021",
                    "ZCMC": "1-5周,7-9周,11周",
                    "DWDM_DISPLAY": "计算机科学与技术学院",
                    "JSSJ": null,
                    "SKXQ_DISPLAY": "星期二",
                    "JXLDM": "A",
                    "TYXMDM": null
                }
            ]
        }
    },
    "code": "0"
}
```

- 样例代码

```python
import requests

cookies = {
    'EMAP_LANG': 'zh',
    'THEME': 'cherry',
    '_WEU': 'wiIL5xKaLOpG8kgDwr2W6lodt*qlCsQ5Z8VAB1zidH4sWK1eCmlOUImJiRSC*_OwxmaD6xkwc*pZP7HvvSCdS6exT3ZTr7vLMulD3WsXOCegJU3UUd9UWj..',
    'MOD_AUTH_CAS': 'MOD_AUTH_ST-180351-DaWDdA2O0EK0pXbjMBjMbSzkB-Eauthserver1',
    'route': 'efe65af6112e14c9eee4f9e623e0f16d',
    'asessionid': '5733bd10-71fc-4895-9612-661972d587ab',
    'amp.locale': 'undefined',
    'JSESSIONID': 'q-1ANhVopEyXU_J2njSA9lRAryboVURyu7wpG7vfCKhHv-b-c7yf!-849035594',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://ehall.xidian.edu.cn',
    'Referer': 'https://ehall.xidian.edu.cn/jwapp/sys/wdkb/*default/index.do?amp_sec_version_=1&gid_=c1doT3Y4YzFSVVEraUdEQUJSV21Nd1BEUEtNeEsrYTNQL2oxa1U1M2Q5RVE2ckRZMU95VkZWYkI4d1g2elZJWlBEWld6U1lidUNvSkN2c0FTNHphWVE9PQ&EMAP_LANG=zh&THEME=cherry',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'XNXQDM': '2022-2023-1',
    'SKZC': '3',
}

response = requests.post('https://ehall.xidian.edu.cn/jwapp/sys/wdkb/modules/xskcb/xsllsykb.do', cookies=cookies, headers=headers, data=data)
```
