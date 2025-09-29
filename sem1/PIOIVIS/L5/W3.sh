#!/bin/bash

currentFolder=$3"/Test"

mkdir -p $currentFolder

for (( var1=1 ; var1 <= $4 ; var1++ ))
do
touch $currentFolder"/$var1.txt"
done

while [ $(ls -1q $currentFolder | wc -l) -gt $2 ]
do
for (( var1=1 ; var1 <= $2 ; var1++ ))
do
rm -rf $currentFolder"/$(ls $currentFolder | head -1)"
done
sleep $1
done

