#!/bin/bash
echo Username1 : 
read User1
grep -E "^\${User1}$" users.tsv > line1.txt
if [[ $(cat line1.txt) == "" ]];then
	echo "This Username name doesn't exist do you wanna register"
	rm line1.txt
else 	
	echo Password1 :
	read Pass1
	Hash1=$(echo $Pass1 | sha256sum | cut -d " " -f 1)
	if [[ $Hash1 != $(cut -f 2 line1.txt ) ]];then
	       echo "This Password doesn't match Try again"
	       rm line1.txt
        else	
	 	rm line1.txt	
		echo Username2 :
		read User2
		grep -E "^\${User2}$" users.tsv > line2.txt
		if [[ $(cat line2.txt) == "" ]];then
		       	echo "This Username name doesn't exist do you wanna register"
			rm line2.txt 
	       	else		
			echo Pass2 :
			read Pass2
			Hash2=$(echo $Pass2 | sha256sum | cut -d " " -f 1)
        		if [[ $Hash2 != $(cut -f 2 line2.txt ) ]];then
               			echo "This Password doesn't match Try again"
				rm line2.txt
			else
				rm line2.txt
				python3 game.py $User1 $User2
			fi
		fi
	fi
fi
