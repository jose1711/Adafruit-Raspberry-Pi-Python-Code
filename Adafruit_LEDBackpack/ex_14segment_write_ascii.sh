#!/bin/bash
# displays ascii string (either entered on input or specified as an argument) on a 14-segment LCD BackPack display from Adafruit
#
# optional flags:
#  -c    clears screen when finished
#  -d    prints some extra info to stdout for debugging
#  -m    deMo mode (ignores input and instead output characters codes 32--127 of ascii table
#  -q    be quiet (no output to stdout)
#
# characters 1..127 of ascii table
chars=(0 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192 16384 32768 0 0 0 0 0 0 0 0 4809 5568 4857 227 1328 4808 14848 5888 8 6 544 4814 4845 3108 9053 1024 9216 2304 16320 4800 2048 192 0 3072 3135 6 219 143 230 8297 253 7 255 239 4608 2560 9216 200 2304 4227 699 247 4751 57 4623 249 113 189 246 4608 30 9328 56 1334 8502 63 243 8255 8435 237 4609 62 3120 10294 11520 5376 3081 57 8448 15 3075 8 256 4184 8312 216 2190 2136 113 1166 4208 4096 14 13824 48 4308 4176 220 368 1158 80 8328 120 28 8196 10260 10432 8204 2120 2377 4608 9353 1312 16383)
# uncomment the line below if you want to make use of the decimal dot in characters: !.? and _ (_ without a dot denotes a space)
chars=(0 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192 16384 32768 0 0 0 0 0 0 0 0 4809 5568 4857 227 1328 4808 14848 5888 8 16390 544 4814 4845 3108 9053 1024 9216 2304 16320 4800 2048 192 16384 3072 3135 6 219 143 230 8297 253 7 255 239 4608 2560 9216 200 2304 20611 699 247 4751 57 4623 249 113 189 246 4608 30 9328 56 1334 8502 63 243 8255 8435 237 4609 62 3120 10294 11520 5376 3081 57 8448 15 3075 16392 256 4184 8312 216 2190 2136 113 1166 4208 4096 14 13824 48 4308 4176 220 368 1158 80 8328 120 28 8196 10260 10432 8204 2120 2377 4608 9353 1312 16383)
address=0x70

# how many digit-display you have (or want to use)
digits=2

# which digit to start for display (starting with zero)
startdigit=2

# delay in seconds before redraw (may be specified as fractions of seconds)
delay=1

# ic2 bus number (you may need to change this for banana pi for instance)
bus=0

which i2cset &>/dev/null || {
	echo 'i2cset not found in current path!'
	exit 1
}

while getopts ":dmcq" opt; do
    case $opt in
    q)
      QUIET=1
    ;;
    d)
      DEBUG=1
    ;;
	c)
	  CLEAR=1
	;;
	m)
	  DEMO=1
	;;
	\?)
	  echo "Invalid option: -$OPTARG" >&2
	  exit 1
	;;
	esac
done

shift $((OPTIND-1))

if [[ ${DEMO} < 1 ]]
	then
		if [ -z "${1}" ]
			then
				echo "input string"
				read text
			else
				text=$1
			fi
	else
		text=$(
		for chr in $(seq 32 127)
			do
			printf "\x`printf "%x" $chr`"
			done
)
	fi

echo "${text}" | perl -pe 's/(.{'${digits}'})/$1\n/g' | grep -Ev '^$' | while IFS='' read -r line
	do
		[[ ${QUIET} ]] || echo "${line}"
		printf "%-"${digits}"s" "${line}" | sed -e 's/./&\n/g' | head -${digits} | cat -n | while IFS=`echo -e "\t"` read -r pos char 
			do
				if [[ ${DEBUG} ]]
					then
					echo "showing character '${char}' on position ${position}"
					fi
				charcode=$(printf "%d" "'${char}")
				if [ ${charcode} -gt 127 ]
					then
					if [[ ${DEBUG} ]]
						then
						echo "Charcode ${charcode} > 127, changing it to 127"
						fi
					charcode=127
					else
					if [[ ${DEBUG} ]]
						then
						echo "Charcode: ${charcode}"
						fi
					fi
				if [[ ${DEBUG} ]]
					then
					echo "Running: i2cset -y ${bus} "${address}" $(((pos-1+startdigit)*2)) ${chars[$charcode]} w"
					fi
				sudo i2cset -y ${bus} "${address}" $(((pos-1+startdigit)*2)) ${chars[$charcode]} w
			done
		sleep "${delay}"
	done

if [[ ${CLEAR} ]]
	then
		for pos in $(seq ${startdigit} $((startdigit+digits-1)))
			do
			if [[ ${DEBUG} ]]
				then
				echo "Running: i2cset -y ${bus} ${address} $((pos*2)) 0 w clearing the screen"
				fi
			sudo i2cset -y ${bus} "${address}" "$((pos*2))" 0 w
			done
	fi
