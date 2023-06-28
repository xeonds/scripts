#!/bin/bash

ENGINE=google 	# 定义要使用的翻译引擎，可以是google, bing, yandex等
TEXT=$1 		# 定义要翻译的文本，可以是任意语言
TARGET=$2 		# 定义要翻译成的目标语言，可以是任意语言代码，如zh-CN, en, fr等

# 使用translate-shell的api接口
CURL="curl -s https://translate.shell/api/translate" 
JSON=$($CURL -G --data-urlencode "engine=$ENGINE" --data-urlencode "text=$TEXT" --data-urlencode "target=$TARGET")
echo $JSON | jq -r '.translation'

