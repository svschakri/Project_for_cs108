#!/bin/bash
# USER1=""
# USER2=""
for i in 1 2; do
	if (( i == 1 )); then
		echo "================================ FIRST PLAYER  ================================"
	else 
		echo "================================ SECOND PLAYER ================================"
	fi
	while true; do	
		echo -n "Username: " 
		read User
		if [[ $User == "" ]];then
			echo -e "\e[31mEnter a non-Empty Username\e[0m"
			continue
		fi
		# grep -E "^${User}" users.tsv > line1.txt
		# userLine=$(grep -E "^${User}" users.tsv)
		userLine=$( cut  -f 1 users.tsv | grep -E "^${User}\b")
		if [[ -z "$userLine" ]]; then
			echo -n -e "\e[31mThis username doesn't exist! Do you want to register? (y/n) \e[0m"
			read input
				if [[ ${input} ==  "y" ]]; then
					while true; do
						echo -n "Enter Username: "
						read newUser
						if [[ $newUser == "" ]];then
							echo -e "\e[31mEnter a non-Empty Username\e[0m"
							continue
						fi
						newuserLine=$( cut  -f 1 users.tsv | grep -E "^${newUser}$")
						if [[ -z "$newuserLine" ]]; then
							break;
						else
							echo -e "\e[31mThis user name is aldready taken. please try another\e[0m"
							continue;
						fi
					done  
					while true; do
						echo -n "Enter Password: "
						read newPass
						echo -n "Confirm Password: "
						read  confirmedPass
						if [[ "${newPass}" != "${confirmedPass}" ]]; then
							echo -e "\e[31mPasswords don't match. Try again.\e[0m"
							continue
						else 
							hashedPass=$(echo -n "$newPass" | sha256sum | cut -d ' ' -f1)
							echo -e "${newUser}\t${hashedPass}" >> users.tsv
							echo -e "\e[32mUser registered successfully\e[0m"
							break
						fi
					done
					continue
				else
					echo -e "\e[31mAuthentication failed.\e[0m"
					exit
				fi
		else
			USER[$i]=$User
			if [[ i -eq 2 ]];then 
				if [[ ${USER[1]} == ${USER[2]} ]];then
					echo -e "\e[31mUSER1 and USER2 should be different\e[0m"
					continue
				fi
			fi 	
			while true; do
				echo -n "Password: "
				read Pass
				hashPass=$(echo -n $Pass | sha256sum | cut -d " " -f1)
				if [[ $hashPass != $(  grep -E "^${User}\b" users.tsv | cut -f 2 ) ]]; then  
					echo -e "\e[31mPassword incorrect. Try again.\e[0m"
					continue
				else 
					echo -e "\e[32mAuthentication Successful\e[0m"
					break
				fi
			done
		fi
		break
	done
done