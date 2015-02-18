#!/bin/sh
cat <<EOF
Content-type: text/txt

EOF
cd "$HOME"
[ -n "$QUERY_STRING" ] || read QUERY_STRING
cmd="`echo "$QUERY_STRING" | sed -n 's|.*cmd=\([^&]*\)$|\1|p'`"
[ -n "$cmd" ] || cmd="`echo "$QUERY_STRING" | sed -n 's|.*cmd=\([^&]*\)[&].*|\1|p'`"
case $cmd in
	eject)
		screen -S player -p 0 -X stuff "q" > /dev/null 2> /dev/null
		killall omxplayer > /dev/null 2> /dev/null
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
		screen -S player -p 0 -X stuff "q" 2> /dev/null > /dev/null
		killall omxplayer > /dev/null 2> /dev/null
		if [ -f "$sub" ]; then
			screen -md -S player omxplayer --lines 5 \
			--align center --subtitles "$sub" -b "$src"
		else
			screen -md -S player omxplayer -b "$src"
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
		screen -S player -p 0 -X stuff "p"
		;;
	info)
		screen -S player -p 0 -X stuff "z"
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
