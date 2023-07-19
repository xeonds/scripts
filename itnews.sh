#!/bin/bash

echo -e "# IT news Today\n\n$(wget -qO- https://www.ithome.com/block/rank.html | grep -oP '<li>\s*<a\K[^>]+' | awk -F '"' '{print "["$2"]("$6")"}' | sed 's/^/- /g')"
