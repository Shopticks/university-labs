#!/bin/bash

if [ ! -d "$1" ]; then
  echo "$1 does not exist."
  exit
fi

(find $1 ! -perm -u+w -execdir echo {} ';' ) > "$1/result.txt"
(find $1 ! -perm -u+r -execdir echo {} ';' ) >> "$1/result.txt"
(find $1  -perm -u+r,u+w -execdir echo {} ';' ) >> "$1/result.txt"

exit
