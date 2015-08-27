#!/bin/bash
# uses one 14-segment character on LCD BackPack from Adafruit
# to display current system time. accuracy is +-3.75 minutes
#
# time display is implemented as follows:
#  inner segments indicates direction of a longer hand on an analog clock
#  each outer segment lit counts for 2 hours, if a decimal dot is lit it adds another one hour
#  furthermore outer segments are enabled in such a way to resemble the shape of a respective number
#
#  example:
#
# all segments off
# :-------:
# : : : : :
# :  :::  :
#  --- --- 
# :  :::  :
# : : : : :
# :-------: :
#
# 7 hours (am or pm) and around 7.5 minutes
# :ooooooo:
# : : : o o
# :  ::o  o
#  --- ---
# :  :::  o
# : : : : o
# :-------: o
#
# around quarter to 1
# :-------:
# : : : : :
# :  :::  :
#  ooo --- 
# :  :::  :
# : : : : :
# :-------: :
#
# when started without arguments it displays the current time. argument "demo" starts a continous cycle
# where in each iteration additional minute is added to time and shown on both stdout and LCD.
# this can give you an better idea how indication of time works.


#trap 'echo -e "\e0;$BASH_COMMAND\007"' DEBUG
address=0x70
bus=0
# which character to use (counted from 0)
pos=0

digitsmin=(512 1536 1024 1152 128 8320 8192 12288 4096 6144 2048 2112 64 320 256 768 768)
digitshrs=(0 16384 1 16385 36 16417 56 16391 51 16423 59 16443 63)

# set brightness to low
sudo i2cset -y ${bus} "${address}" 0xe0

demo=0
min=1
if [ "$1" = "demo" ]
	then
	echo "demo mode set"
	demo=1
	fi

echo "Clock invoked"
while :
	do
	if [ "${demo}" -eq 1 ]
		then
		DATEARGS="-d now + ${min} minutes"
		read hours minutes seconds < <(date "$DATEARGS" '+%I %M %S' | sed 's/\b0//g')
		echo "displaying $hours:$minutes:$seconds"
		min=$((min+1))
		else
		read hours minutes seconds < <(date '+%I %M %S' | sed 's/\b0//g')
		fi

	if [ ${minutes} -gt 58 ]
		then
		minutes=0
		fi

	# better accuracy now
	minutes=$(perl -e 'print '$minutes'+'$seconds'/60')
	indexm=$(perl -e 'print int((('${minutes}'-1.875)/3.75+1))')

	maskm=${digitsmin[$indexm]}
	maskh=${digitshrs[$hours]}
	mask=$((maskm | maskh))
	if [ "${mask}" != "${lastmask}" ]
		then
		sudo i2cset -y ${bus} "${address}" $((${pos}*2)) ${mask} w
		lastmask=$mask
		fi
		
	if [ "${demo}" -ne 1 ]
		then
		break
		fi
	done
