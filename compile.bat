
setlocal enabledelayedexpansion
set "ANDROID_HOME=D:\HobbyProjects\AndroidDevelopment\cmdline-tools\latest"
set "GRADLE_HOME=D:\HobbyProjects\AndroidDevelopment\gradle-9.2.1"
set "PATH=%GRADLE_HOME%\bin;%ANDROID_HOME%\cmdline-tools\latest\bin;%ANDROID_HOME%\platform-tools;%PATH%"
set "PROJECT=Camera"
set "WORK_SPACE=D:\HobbyProjects\AndroidDevelopment\"
@REM :: Verify it works
@REM sdkmanager --sdk_root=%ANDROID_HOME%\cmdline-tools\bin --version
@REM sdkmanager --sdk_root=%ANDROID_HOME%\cmdline-tools\latest "build-tools;35.0.0" "platforms;android-34" "platform-tools" "platforms;android-34" "build-tools;34.0.0"

@echo off

set DIR=%WORK_SPACE%\%PROJECT%App

if exist %DIR% (
    echo INFO, already Directory exists: %DIR%
    echo Proceeding with compilation
    python android_compile.py
    IF ERRORLEVEL 1 (
        echo Compilation failed
    ) ELSE (
        echo Compilation succeeded!!
        move %WORK_SPACE%\%PROJECT%App\app\build\outputs\apk\debug\app-debug.apk %WORK_SPACE%\%PROJECT%App\app\build\outputs\apk\debug\%PROJECT%.apk
        set "PAY_LOAD=%WORK_SPACE%\%PROJECT%App\app\build\outputs\apk\debug\%PROJECT%.apk"
        echo Copying it to Google Drive...
        @REM python uploadWithTokens.py
        call :GetTimeStamp
        @echo on
        echo !PAY_LOAD!
        adb devices
        adb install -r "!PAY_LOAD!"
        adb shell ip addr show wlan0
        adb tcpip 5555
    )
) else (
    echo Directory does not exist: %DIR%
    python mkDroidTemplate.py
    cd /d %WORK_SPACE%\%PROJECT%App
    call gradle wrapper
    cd /d %WORK_SPACE%\
)

@echo off
setlocal enabledelayedexpansion

REM Example usage

echo Current time is %TIMESTAMP%

endlocal
exit /b

:GetTimeStamp
REM Grab %TIME% and format as HHMMSS
set "t=%TIME%"
set "hh=%t:~0,2%"
set "mm=%t:~3,2%"
set "ss=%t:~6,2%"

REM Fix leading space in hour
if "%hh:~0,1%"==" " set "hh=0%hh:~1,1%"

set "TIMESTAMP=%hh%%mm%%ss%"
goto :eof
