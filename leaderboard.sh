#!/bin/bash

SORT_VAL=$1 #val contains the data of metrics to sort some how
game_arr=()

max_len=0
while read -r line; do
    games_arr+=("$line")
    len=${#line}
    if (( max_len <= len )); then
        max_len=$len
    fi
done < <(cut -d "," -f1 games.csv)

for game in "${games_arr[@]}" ; do 
    #logic for individual games
    awk -v max_len=$max_len -v game="$game" '
        function max(x, y, z) {
            mx = x
            if (mx < y) mx = y
            if (mx < z) mx = z
            return mx
        }

        function format(str, mx_len) {
            spaces = mx_len - length(str)
            res = str ""
            for (i = 0; i < spaces; i++) {
                res = res " "
            }
            return res
        }

        function format_header(str, mx_len, pad_char) {
            head_len = 36 + mx_len
            padding = int((head_len - length(str) - 2)/2)
            pad_str = ""
            for (i = 0; i < padding; i++) {
                pad_str = pad_str pad_char
            }
            res = sprintf("%s %s %s", pad_str, str, pad_str)
            if ((head_len - length(str))%2 == 1) {
                res = res pad_char
            }
            return res "\n"
        }

        BEGIN{
                FS=",";
                OFS="| ";
                ORS = "";
                max_name_len = 0
                printf "%s\n", format_header(game, max_len, "=")
                found = 0
            }
        {
            if ($0 ~ "^" game) {
                if ($2 !~ /Draw/) {
                    Wins[$3]++
                    Losses[$4]++
                }
                Players[$3]
                Players[$4]
                max_name_len = max(max_name_len, length($3), length($4))
                found = 1
            }
        }
        END{
            mx_width["name"] = max(max_name_len, 8, 0) + 3
            mx_width["wins"] = 7
            mx_width["losses"] = 7
            mx_width["w_l_ratio"] = 10
            
            if (found == 1) {
                printf "|| "
                print format("Username", mx_width["name"]), format("Wins", mx_width["wins"]), format("Losses", mx_width["losses"]), format("W/L Ratio", mx_width["w_l_ratio"])
                printf " ||\n"
            }
            for (i in Players) {
                w = Wins[i] + 0
                l = Losses[i] + 0
                w_l_ratio = (l==0) ? "INF" : sprintf("%.2f", w/l)
                printf "|| "
                print format(i, mx_width["name"]), format(w, mx_width["wins"]) , format(l, mx_width["losses"]), format(w_l_ratio, mx_width["w_l_ratio"])
                printf " ||\n"
            }
            printf "\n%s\n", format_header("END", max_len, "=")
        }
        ' "history.csv"

    # if [[ $SORT_VAL == "Wins" ]]; then
    #     col=2
    # elif [[ $SORT_VAL == "Losses" ]]; then
    #     col=3
    # else
    #     col=4
    # fi
    # sort -t "," -k $col,$col -nr "table_${game}.csv"
    # rm "table_${game}.csv"
    # echo -e "\n========== END ==========\n"

done