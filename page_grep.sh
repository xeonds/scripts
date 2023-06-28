#!/bin/bash

url="http://v2ex.com"
want="好玩"
wget "$url" -O contents
if result=$(cat contents | ack -i "$want") then
    echo "$result" | mail -s "Notification" youe@mail.com
else
    echo "nothing"
fi
