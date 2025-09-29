@echo off
setlocal enabledelayedexpansion

REM Проверка наличия двух аргументов
if "%~1"=="" (
    echo Использование: %~nx0 "строка" "относительный_путь_к_папке"
    exit /b 1
)

REM Присвоение аргументов переменным
set "search_string=%~1"
set "relative_path=%~2"

REM Получение текущего месяца и года
for /f "tokens=2 delims==" %%i in ('wmic os get localdatetime /value') do set datetime=%%i
set "current_year=!datetime:~0,4!"
set "current_month=!datetime:~4,2!"

REM Преобразование относительного пути в абсолютный
pushd "%relative_path%" || (echo Невозможно перейти в директорию "%relative_path%" & exit /b 1)
set "absolute_path=%cd%"
popd

REM Поиск файлов, созданных в текущем месяце и не изменявшихся последние 2 минуты
forfiles /p "%absolute_path%" /s /m *.* /d +%current_month% /c "cmd /c if @isdir==FALSE (
    for %%F in (@path) do (
        set file=%%~fF
        set mod_time=%%~tF
        set mod_time=!mod_time:~11,5!
        call :CheckTime !mod_time!
        if !time_diff! geq 2 (
            findstr /m /c:\"%search_string%\" \"!file!\" >nul && (
                powershell -Command \"(Get-Content -Path '!file!') -replace '%search_string%', '321' | Set-Content -Path '!file!'\"
                echo Обработан файл: !file!
            )
        )
    )
)"

REM Функция для вычисления разницы во времени
:CheckTime
setlocal
set "file_time=%1"
set "current_time=%time:~0,5%"
set /a file_minutes=1%file_time:~0,2%*60 + 1%file_time:~3,2%
set /a current_minutes=1%current_time:~0,2%*60 + 1%current_time:~3,2%
set /a time_diff=(%current_minutes% - %file_minutes% + 1440) %% 1440
endlocal & set "time_diff=%time_diff%"
exit /b
