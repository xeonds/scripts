#!/bin/bash

wget -qO- --header='Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  --header='Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6' \
  --header='Cache-Control: max-age=0' \
  --header='Connection: keep-alive' \
  --header='Content-Type: application/x-www-form-urlencoded' \
  --header='Cookie: browser=103.90.138.37.1686589330171428; arxiv-search-parameters="{\"order\": \"-announced_date_first\"\054 \"size\": \"50\"\054 \"abstracts\": \"show\"}"' \
  --header='Origin: https://arxiv.org' \
  --header='Referer: https://arxiv.org/multi?group=grp_cs&%2Fcatchup=Catchup' \
  --header='Sec-Fetch-Dest: document' \
  --header='Sec-Fetch-Mode: navigate' \
  --header='Sec-Fetch-Site: same-origin' \
  --header='Sec-Fetch-User: ?1' \
  --header='Upgrade-Insecure-Requests: 1' \
  --header='User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.41' \
  --header='sec-ch-ua: "Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"' \
  --header='sec-ch-ua-mobile: ?0' \
  --header='sec-ch-ua-platform: "Windows"' \
  --post-data 'archive=cs&sday=05&smonth=06&syear=2023&method=without' \
  https://arxiv.org/catchup | grep -E 'Title:|Subjects:' | awk -F '>' '{print $NF}' | sed -e 's/^ \([^;].*\)/\n## \1/g' -e 's/^;/-/g'
