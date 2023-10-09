#!/bin/bash

while true
do
	res=($(nvidia-smi |grep 180W |awk -F ' ' '{print $5" "$7}' |sed 's/W//g'))
	if ((res[0] > res[1])); then
		echo -e "GPU overloaded. ${res[0]}W/${res[1]}W"
	fi
	sleep 1
done

