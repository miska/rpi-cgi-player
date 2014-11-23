#!/bin/bash
cat <<EOF
Content-type: text/html

<!DOCTYPE html>
<html><head>
  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />
  <meta charset=\"UTF-8\">
  <title>File chooser</title>
</head>
<body>
<h1>Choose file</h1>
EOF
stream="`echo "$QUERY_STRING" | sed -n 's|.*stream=||p' | base64 --decode 2> /dev/null`"
[ -n "$stream" ] || stream="`echo "$QUERY_STRING" | sed -n 's|.*stream=||p'`"
name="`echo "$QUERY_STRING" | sed -n 's|name=\(.*\)stream=.*|\1|p'`"
if [ "$stream" ]; then
	killall omxplayer 2> /dev/null
	if [ "$stream" != off ]; then
		SUBS=""
		if [ -f "`echo "$stream" | sed -n 's|\.[^.]*$|.srt|p'`" ]; then
			SUBS=" --align center --subtitles `echo "$stream" | sed -n 's|\.[^.]*$|.srt|p'` "
		fi
		echo screen -md -S player omxplayer $SUBS "$stream"
		screen -md -S player omxplayer $SUBS "$stream"
		echo "<p>File is being played. Turn it  <a href=\"/files.cgi?stream=off\">off</a>?</p>"
	else
		echo "<p>Playing stopped.</p>"
	fi
fi
echo '<ul>'
ls -1 "$HOME/Movies"/* | while read line; do
	NAME="`basename "$line"`"
	echo "<li><a href=\"/files.cgi?stream=`echo "$line" | base64 | tr '\n' ' ' | sed 's|[[:blank:]]*||g'`\">$NAME</a></li>"
done
echo '</ul>'
echo "</body></html>"
