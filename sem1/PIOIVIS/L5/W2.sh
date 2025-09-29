#!/bin/bash

currentFolder=$(pwd)"/Test"

mkdir -p $currentFolder

for (( var1 = 0 ; var1 < $1; ++var1 ))
do

    case $(( $var1 % 3 )) in
        2) touch $currentFolder"/$(($var1 + 1)).docx" ;;
        *) echo "$(date +%H_%M_%S)" > $currentFolder"/$(($var1 + 1)).txt" ;;
    esac

done


for name in $(ls $currentFolder); do
    line=$(cat $currentFolder"/$name")
    if [[ "$line" == *"$2"* ]]; then
        echo "$name" >> $currentFolder"/Equal07.txt"
        continue
    fi
done
