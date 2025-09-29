@echo off

set line=%1
set num=0

:LOOP
call set tmpa=%%line:~%num%,1%%%
set /a num+=1
if not "%tmpa%" equ "" (
set rline=%tmpa%%rline%
goto LOOP
)

for /F %%f in ('powershell "Get-ChildItem '%2' -recurse | Where-Object { $_.lastwritetime -gt (get-date).addMinutes(-2) } | Where-Object { $_.creationtime -gt (get-date).addDays(-30) } | Foreach-Object { $_.FullName }"') do (
	setlocal enabledelayedexpansion
	echo. > "%2var.txt"
    	for /f "delims=" %%A in ('type "%%f"') do (
        	set line=%%A
        	set newline=!line:%line%=%rline%!
        	echo !newline! >> "%2var.txt"
    	)
	type "%2var.txt" > %%f
	del "%2var.txt"
    	endlocal
)



echo -----------------------------

exit