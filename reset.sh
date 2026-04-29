#!/bin/bash

>history.csv
>users.tsv
make clean
if [[ -f plot.png ]]; then
    rm plot.png
fi