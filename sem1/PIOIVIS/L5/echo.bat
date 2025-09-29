@echo off


rem powershell "Get-ChildItem 'C:\Mac\Home\Documents\BSUIR\sem1\PIOIVIS\L5\Test\' -recurse | Where-Object { $_.lastwritetime -gt (get-date).addMinutes(-2) } | Where-Object { $_.creationtime -gt (get-date).addDays(-30) } | Foreach-Object { $_.FullName }" > .\output.txt

for /F %%f in ('powershell "Get-ChildItem '%2' -recurse | Where-Object { $_.lastwritetime -gt (get-date).addMinutes(-2) } | Where-Object { $_.creationtime -gt (get-date).addDays(-30) } | Foreach-Object { $_.FullName }"') do (
	echo %%f
)

exit