#!/bin/bash

if [ $(($1 % 2)) -eq 0 ]
then
direction="$(pwd)""/Folder"
for (( var1 = 1; var1 <= $1; var1++ ))
do
mkdir -p $direction
echo $(date +%H_%M_%S) > "$direction/Date.txt"
direction=$direction"/Folder"
done
echo $(date +%H_%M_%S) > "$direction/Date.txt"

else
string=""
for (( var1 = 1; var1 <= $1; var1++ ))
do
string="$string $(($RANDOM % 10))"
done

echo $string > Lab1.txt

fi
