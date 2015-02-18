#!/bin/bash
echo 'Content-type: text/html'
echo
[ "$TMP" ] || TMP="/tmp"
CACHE="$TMP"/rpi_player_streamlist
if [ \! -r "$CACHE" ] || [ Movies -nt "$CACHE" ]; then
echo '<ul>' > "$CACHE"
cat /srv/www/htdocs/streams/* | while read line; do
	NEW_NAME="`echo "$line" | sed -n 's|#EXTINF:,||p'`"
	[ -z "$NEW_NAME" ] || NAME="$NEW_NAME"
	URL="`echo "$line" | grep '^http' | tr '\n' '\ ' | sed 's|[[:blank:]]*$||'`"
	if [ "$URL" ]; then
		echo "<li><a href=\"#\" onClick=\"api_request('play', '`echo "$URL" | \
		base64 | tr '\n' ' ' | sed 's|[[:blank:]]*||g'`')\">$NAME</a></li>"
	fi
	URL=""
done >> "$CACHE"
echo '</ul>' >> "$CACHE"
fi
cat "$CACHE"
