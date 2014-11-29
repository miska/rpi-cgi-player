#!/bin/bash
echo 'Content-type: text/html'
echo 
echo '<ul>'
ls -1 "Movies"/* | while read line; do
	NAME="`basename "$line"`"
	if [ -n "`file --mime-type "$line" | grep "video/[^[:blank:]]*"`" ]; then
		echo "<li><a href=\"#\" onClick=\"api_request('delete', '`echo "$line" | \
		      base64 | tr '\n' ' ' | sed 's|[[:blank:]]*||g'`')\">&#x267B;</a>"
		echo "<a href=\"#\" onClick=\"api_request('play', '`echo "$line" | \
		      base64 | tr '\n' ' ' | sed 's|[[:blank:]]*||g'`')\">$NAME</a></li>"
	fi
done
echo '</ul>'
