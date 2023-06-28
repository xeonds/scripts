#!/bin/bash

wget -qO- https://www.ithome.com/block/rank.html | grep -oP '<li>\s*<a title="\K[^"]+'
