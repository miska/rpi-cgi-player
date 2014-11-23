#!/bin/bash
cat <<EOF
Content-type: text/html

<!DOCTYPE html>
<html><head>
  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />
  <meta charset=\"UTF-8\">
  <title>Stream chooser</title>
</head>
<body>
<h1>Choose stream</h1>
EOF
stream="`echo "$QUERY_STRING" | sed -n 's|.*stream=||p'`"
name="`echo "$QUERY_STRING" | sed -n 's|name=\(.*\)stream=.*|\1|p'`"
if [ "$stream" ]; then
	killall omxplayer 2> /dev/null
	if [ "$stream" != off ]; then
		screen -md -S player omxplayer "$stream"
		echo "<p>Stream running. Turn it <a href=\"/streams.cgi?stream=off\">off</a>?</p>"
	else
		echo "<p>Stream off.</p>"
	fi
fi
echo '<ul>'
cat /srv/www/htdocs/streams/* | while read line; do
	NEW_NAME="`echo "$line" | sed -n 's|#EXTINF:,||p'`"
	[ -z "$NEW_NAME" ] || NAME="$NEW_NAME"
	URL="`echo "$line" | grep '^http'`"
	if [ "$URL" ]; then
		echo "<li><a href=\"/streams.cgi?stream=$URL\">$NAME</a></li>"
	fi
done
echo '</ul>'
echo "</body></html>"
