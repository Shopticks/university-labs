@echo off

set resultFile="%1result.txt"

echo. > %resultFile%

dir /A:-DR /B >> %resultFile%
dir /A:-R /B >> %resultFile%

exit