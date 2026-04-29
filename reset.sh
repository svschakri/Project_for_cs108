#!/bin/bash

echo "Game,Draw,Winner,Loser,Date" > history.csv
>users.tsv
make clean
if [[ -f plot.png ]]; then
    rm plot.png
fi