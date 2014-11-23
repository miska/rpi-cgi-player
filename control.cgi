#!/bin/bash
cat <<EOF
Content-type: text/html

<!DOCTYPE html>
<html><head>
  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />
  <meta charset=\"UTF-8\">
  <title>Player control</title>
  <style>
    body {
      background: black;
      color: white;
      text-align: center;
    }
    a:link, a:visited {
      color: white;
      background: black;
      text-decoration: none;
    }
    a:hover, a:active {
      color: black;
      background: white;
      text-decoration: none;
    }
  </style>
</head>
<body>
<h1>Player control</h1>
EOF
cmd="`echo "$QUERY_STRING" | sed -n 's|.*cmd=||p'`"
case $cmd in
	eject)
		screen -S player -p 0 -X stuff "q"
		killall omxplayer
		;;
	pause)
		screen -S player -p 0 -X stuff "p"
		;;
	ff)
		screen -S player -p 0 -X stuff $'\e'[C
		;;
	ffff)
		screen -S player -p 0 -X stuff $'\e'[A
		;;
	rr)
		screen -S player -p 0 -X stuff $'\e'[D
		;;
	rrrr)
		screen -S player -p 0 -X stuff $'\e'[B
		;;
	volup)
		screen -S player -p 0 -X stuff "+"
		;;
	voldown)
		screen -S player -p 0 -X stuff "-"
		;;
esac
cat <<EOF
<h2>
<a href=\"/control.cgi?cmd=eject\">&#x23cf;</a>
<a href=\"/control.cgi?cmd=rrrr\">&#x23ea;</a>
<a href=\"/control.cgi?cmd=rr\">&#x23f4;</a>
<a href=\"/control.cgi?cmd=pause\">&#x23ef;</a>
<a href=\"/control.cgi?cmd=ff\">&#x23f5;</a>
<a href=\"/control.cgi?cmd=ffff\">&#x23e9;</a>
<a href=\"/control.cgi?cmd=voldown\">&#x1f509;</a>
<a href=\"/control.cgi?cmd=volup\">&#x1f50a;</a>
</h2>
</body></html>
EOF
