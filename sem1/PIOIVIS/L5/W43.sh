#!/bin/bash

currentFolder=$2
echo "Test321string" > $2"/File1.txt"

findString="$1"
reverseString="$(echo "$1" | rev)"

for var in $(find $2 -type f -cmin -2 -ctime -30); do

echo $(sed "s/$findString/$reverseString/" $var) > $var

done
