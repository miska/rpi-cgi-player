#!/bin/sh
cat <<EOF
Content-type: text/txt

EOF
cd "$HOME"
PLAYER="omx"
SUDO=""
[ -n "$QUERY_STRING" ] || read QUERY_STRING
cmd="`echo "$QUERY_STRING" | sed -n 's|.*cmd=\([^&]*\)$|\1|p'`"
[ -n "$cmd" ] || cmd="`echo "$QUERY_STRING" | sed -n 's|.*cmd=\([^&]*\)[&].*|\1|p'`"
case $cmd in
	eject)
		screen -S player -p 0 -X stuff "q" > /dev/null 2> /dev/null
		killall omxplayer > /dev/null 2> /dev/null
		$SUDO killall mpv > /dev/null 2> /dev/null
		;;
	play)
		src="`echo "$QUERY_STRING" | \
		      sed -n 's|.*src=\([^&]*\)$|\1|p' | \
		      base64 --decode 2> /dev/null | tr '\n\r' '\ \ ' | \
		      sed 's|[[:blank:]]*$||'`"
		[ -n "$src" ] || src="`echo "$QUERY_STRING" | \
		      sed -n 's|.*src=\([^&]*\)&.*|\1|p' | \
		      base64 --decode 2> /dev/null | tr '\n\r' '\ \ ' | \
		      sed 's|[[:blank:]]*$||'`"
		[ -n "$src" ] || src="`echo "$QUERY_STRING" | \
		      sed -n 's|.*src=\([^&]*\)&.*|\1|p'`"
		sub="`echo "$src" | sed -n 's|^\(/.*\)\.[^.]*$|\1.srt|p'`"
		if [ "$PLAYER" = omx ]; then
			screen -S player -p 0 -X stuff "q" 2> /dev/null > /dev/null
			killall omxplayer > /dev/null 2> /dev/null
			if [ -f "$sub" ]; then
				screen -md -S player omxplayer --lines 5 \
				--align center --subtitles "$sub" -b "$src"
			else
				screen -md -S player omxplayer -b "$src"
			fi
		else
			screen -S player -p 0 -X stuff "q" 2> /dev/null
			$SUDO killall mpv
			rm -f /tmp/mpv
			mkfifo /tmp/mpv
			screen -md -S player $SUDO /usr/bin/xinit /usr/bin/mpv -fs --input-file=/tmp/mpv "$src"
		fi
		;;
	delete)
		src="`echo "$QUERY_STRING" |
		      sed -n 's|.*src=\([^&]*\)$|\1|p' |
		      base64 --decode 2> /dev/null`"
		[ -n "$src" ] || src="`echo "$QUERY_STRING" |
		      sed -n 's|.*src=\([^&]*\)&.*|\1|p' |
		      base64 --decode 2> /dev/null`"
		rm "$src"
		;;
	download)
		src="`echo "$QUERY_STRING" |
		      sed -n 's|.*src=\([^&]*\)$|\1|p' |
		      base64 --decode 2> /dev/null`"
		[ -n "$src" ] || src="`echo "$QUERY_STRING" |
		      sed -n 's|.*src=\([^&]*\)&.*|\1|p' |
		      base64 --decode 2> /dev/null`"
		cd Movies
		screen -md wget -c "$src"
		;;
	pause)
		if [ "$PLAYER" = omx ]; then
			screen -S player -p 0 -X stuff "p"
		else
			echo cycle pause > /tmp/mpv
		fi
		;;
	info)
		screen -S player -p 0 -X stuff "z"
		;;
	ff)
		if [ "$PLAYER" = omx ]; then
			screen -S player -p 0 -X stuff $'\e'[C
		else
			echo seek +60 > /tmp/mpv
		fi
		;;
	ffff)
		if [ "$PLAYER" = omx ]; then
			screen -S player -p 0 -X stuff $'\e'[A
		else
			echo seek +600 > /tmp/mpv
		fi
		;;
	rr)
		if [ "$PLAYER" = omx ]; then
			screen -S player -p 0 -X stuff $'\e'[D
		else
			echo seek -60 > /tmp/mpv
		fi
		;;
	rrrr)
		if [ "$PLAYER" = omx ]; then
			screen -S player -p 0 -X stuff $'\e'[B
		else
			echo seek -600 > /tmp/mpv
		fi
		;;
	volup)
		if [ "$PLAYER" = omx ]; then
			screen -S player -p 0 -X stuff "+"
		else
			echo add volume 1 > /tmp/mpv
		fi
		;;
	voldown)
		if [ "$PLAYER" = omx ]; then
			screen -S player -p 0 -X stuff "-"
		else
			echo add volume -1 > /tmp/mpv
		fi
		;;
	df)
		df -h --output=avail,size Movies | tail -n 1 | sed -n 's|^[[:blank:]]*\([^[:blank:]]\+\)[[:blank:]]*|\1 free out of |p'
		exit 0
		;;
	show_downloads)
		OUT="`ps -C wget -o args | sed -n 's|wget -c |<br/>|p'`"
		if [ "$OUT" ]; then
			echo "<strong>Currently downloading</strong>"
			echo "$OUT"
		fi
		exit 0
		;;
esac
echo "$cmd command accepted"
