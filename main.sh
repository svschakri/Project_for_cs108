#!/bin/bash
for i in 1 2; do
	if (( i == 1 )); then
		echo "================================ FIRST PLAYER  ================================"
	else 
		echo "================================ SECOND PLAYER ================================"
	fi
	while true; do	
		echo -n "Username: " 
		read User
		# grep -E "^${User}" users.tsv > line1.txt
		userLine=$(grep -E "^${User}" users.tsv)
		if [[ -z "$userLine" ]]; then
			echo -n "This username doesn't exist! Do you want to register? (y/n) "
			read input
				if [[ ${input} ==  "y" ]]; then
					echo -n "Enter Username: "
					read newUser
					while true; do
						echo -n "Enter Password: "
						read newPass
						echo -n "Confirm Password: "
						read confirmedPass
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
			while true; do
				echo -n "Password: "
				read Pass
				hashPass=$(echo -n $Pass | sha256sum | cut -d " " -f1)
				if [[ $hashPass != $(echo "$userLine" | cut -f2) ]]; then
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