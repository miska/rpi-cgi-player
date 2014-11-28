#!/bin/sh
cat <<EOF
Content-type: text/txt

EOF
[ -n "$QUERY_STRING" ] || read QUERY_STRING
cmd="`echo "$QUERY_STRING" | sed -n 's|.*cmd=\([^&]*\)$|\1|p'`"
[ -n "$cmd" ] || cmd="`echo "$QUERY_STRING" | sed -n 's|.*cmd=\([^&]*\)[&].*|\1|p'`"
case $cmd in
	eject)
		screen -S player -p 0 -X stuff "q"
		killall omxplayer
		;;
	play)
		src="`echo "$QUERY_STRING" |
		      sed -n 's|.*src=\([^&]*\)$|\1|p' |
		      base64 --decode 2> /dev/null`"
		[ -n "$cmd" ] || src="`echo "$QUERY_STRING" |
		      sed -n 's|.*src=\([^&]*\)&.*|\1|p' |
		      base64 --decode 2> /dev/null`"
		sub="`echo "$src" | sed -n 's|^\(/.*\)\.[^.]*$|\1.srt|p'`"
		screen -S player -p 0 -X stuff "q"
		killall omxplayer
		if [ -f "$sub" ]; then
			screen -md -S player omxplayer \
			--align center --subtitles "$sub" -b "$src"
		else
			screen -md -S player omxplayer -b "$src"
		fi
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
echo "$cmd done"