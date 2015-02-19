#!/bin/bash
echo 'Content-type: text/html'
echo
cd /home/michal
[ "$TMP" ] || TMP="/tmp"
CACHE="$TMP"/rpi_player_filelist
if [ \! -r "$CACHE" ] || [ Movies -nt "$CACHE" ]; then 
rm -f /tmp/tmp.*
NEWCACHE="$TMP"/rpi_player_filelist.new
if [ -r "$NEWCACHE" ]; then
	echo "Loading ..."
	exit 0
fi
touch "$TMP"/rpi_player_filelist.new.ts
echo '<ul>' > "$NEWCACHE"
ls -1 "Movies"/* | while read line; do
	NAME="`basename "$line"`"
	if [ -n "`file --mime-type "$line" | grep "video/[^[:blank:]]*"`" ] || expr match "$line" '^.*\.[Mm]\?[Tt][Ss]$' > /dev/null; then
		echo "<li><a href=\"#\" onClick=\"api_request('delete', '`echo "$(pwd)/$line" | \
		      base64 | tr '\n' ' ' | sed 's|[[:blank:]]*||g'`'); load_files();\"><img src=\"font/delete.svg\" style=\"height: 1em; vertical-align: bottom;\"/></a>"
		echo "<a href=\"#\" onClick=\"api_request('play', '`echo "$(pwd)/$line" | \
		      base64 | tr '\n' ' ' | sed 's|[[:blank:]]*||g'`')\">$NAME</a></li>"
	fi
done >> "$NEWCACHE"
echo '</ul>' >> "$NEWCACHE"
cat "$NEWCACHE" > "$CACHE"
touch -r "$TMP"/rpi_player_filelist.new.ts "$CACHE"
rm -f "$NEWCACHE" "$TMP"/rpi_player_filelist.new.ts
fi
cat "$CACHE"
