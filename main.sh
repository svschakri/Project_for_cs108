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
			echo "Enter a non-Empty Username"
			continue
		fi
		# grep -E "^${User}" users.tsv > line1.txt
		# userLine=$(grep -E "^${User}" users.tsv)
		userLine=$( cut  -f 1 users.tsv | grep -E "^${User}\b")
		if [[ -z "$userLine" ]]; then
			echo -n "This username doesn't exist! Do you want to register? (y/n) "
			read input
				if [[ ${input} ==  "y" ]]; then
					while true; do
						echo -n "Enter Username: "
						read newUser
						newuserLine=$( cut  -f 1 users.tsv | grep -E "^${newUser}$")
						if [[ -z "$newuserLine" ]]; then
							break;
						else
							echo "This user name is aldready taken. please try another"
							continue;
						fi
					done  
					while true; do
						echo -n "Enter Password: "
						read newPass
						echo -n "Confirm Password: "
						read  confirmedPass
						if [[ "${newPass}" != "${confirmedPass}" ]]; then
							echo "Passwords don't match. Try again."
							continue
						else 
							hashedPass=$(echo -n "$newPass" | sha256sum | cut -d ' ' -f1)
							echo -e "${newUser}\t${hashedPass}" >> users.tsv
							echo "User registered successfully"
							break
						fi
					done
					continue
				else
					echo "Authentication failed."
					exit
				fi
		else
			USER[$i]=$User
			if [[ i -eq 2 ]];then 
				if [[ ${USER[1]} == ${USER[2]} ]];then
					echo "USER1 and USER2 should be"
					continue
				fi
			fi 	
			while true; do
				echo -n "Password: "
				read Pass
				hashPass=$(echo -n $Pass | sha256sum | cut -d " " -f1)
				if [[ $hashPass != $(  grep -E "^${User}\b" users.tsv | cut -f 2 ) ]]; then  
					echo "Password incorrect. Try again."
					continue
				else 
					echo "Authentication Successful"
					break
				fi
			done
		fi
		break
	done
done