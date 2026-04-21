#!/bin/bash

SORT_VAL=$1 #val contains the data of metrics to sort some how
game_arr=()

for line in $(cut -d "," -f1 games.csv) ; do
    games_arr+=($line)
done

Largest_game_len

NAMES= #assume it as defined

for a in "${games_arr[@]}" ; do 
    #logic for individual games
    echo ========${a}=========
    grep -E "^${a}" history.csv > temp.csv
    awk '
        BEGIN{
                FS=",";
                OFS=",";
            }
        ($2 !~ /Draw/){
            Wins[$3]++;
            Loses[$4]++;
            Players[$3];
            Players[$4];
        }
        END{
            for (i in Players) {
                w_l_ratio = (Loses[i]==0) ? "INFINITE" : sprintf("%.2f", Wins[i]/Loses[i])
                print i,Wins[i],Loses[i],w_l_ratio
            }
        }
        ' temp.csv > table_${a}.csv
    if [[ $SORT_VAL == "Wins" ]]; then
        col=2
    elif [[ $SORT_VAL == "Loses" ]]; then
        col=3
    else
        col=4
    fi
    sort -t "," -k $col,$col -nr table_${a}.csv 
    echo =============END==========

done