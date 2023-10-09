#!/bin/bash
added=0
deleted=0

while read line; do
    IFS=$'\t' read -r -a array <<<"$line"
    added=$((added + array[0]))
    deleted=$((deleted + array[1]))
done < <(git diff --numstat HEAD)

echo "增加了$added行代码，删除了$deleted行代码"
