#!/bin/bash

SORT_VAL=$val #val contains the data of metrics to sort some how

GAMES=("Tic_Tac_Toe" "Othello" "Connect_Four")
NAMES= #assume it as defined

for a in "${GAMES[@]}" ; do 
    #logic for individual games
    grep -E "${a}$" history.csv > temp.csv
    awk '
        BEGIN{
                FS=",";
                OFS=",";
            }
        {
            Wins[$1]++;
            Loses[$2]++;
            Players[$1];
            Players[$2];
        }
        END{
            for (i in Players) {
                w_l_ratio = (Loses[i]==0) ? "INFINITE" : sprintf("%.2f", Wins[i]/Loses[i])
                print i,Wins[i],Loses[i],w_l_ratio
            }
        }
        ' temp.csv > table.csv
    if [[ $SORT_VAL == "Wins" ]]; then
        col=2
    elif [[ $SORT_VAL == "Loses" ]]; then
        col=3
    else
        col=4
    fi
    sort -t "," -k $col,$col -nr table.csv 

done