#!/usr/bin/env bash

python Parameters.py

filename="lambdas.txt"
while read -r line
do
    para="$line"
    lambdas=(${para})
    echo ${lambdas[0]} ${lambdas[1]} >| boardinput.txt
    counter=1
    while [ ${counter} -le 2 ]
    do
        start=$(date +%s)
        python Main.py --connect 127.0.0.1:14551
        ((counter++))
#        if [ $counter -eq 2 ]
#        then
#            end=$(date +%s)
#            runtime=$(python -c "print(${end} - ${start})")
#            echo "$runtime" >> time.txt
#        fi
    done
    python Avgtime.py
    # Move generated reports in to new folder
    folder="${lambdas[0]}_${lambdas[1]}"
    mkdir ${folder}
    mv Drone_* ${folder}
    mv Board_* ${folder}
done < "$filename"