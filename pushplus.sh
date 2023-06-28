#!/bin/bash

token=""
url=http://www.pushplus.plus/send

json="{\"token\": \"$token\", \"title\": \"$1\", \"content\": \"$2\"}"
curl -H "Content-Type: application/json" -X POST -d "$json" $url
