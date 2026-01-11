@echo off
chcp 65001 > nul

echo 🔍 자동 업데이트 감시 시작...
echo 5분마다 새 커밋을 확인합니다.
echo 종료하려면 Ctrl+C를 누르세요.
echo.

:loop
    git fetch origin > nul 2>&1
    
    for /f %%i in ('git rev-parse @') do set LOCAL=%%i
    for /f %%i in ('git rev-parse @{u}') do set REMOTE=%%i
    
    if not "%LOCAL%"=="%REMOTE%" (
        echo 🆕 [%date% %time%] 새로운 커밋 발견!
        echo 📥 코드 업데이트 중...
        
        git pull origin main
        if errorlevel 1 git pull origin master
        
        echo ✅ 업데이트 완료!
        echo.
        
        REM Windows 알림음
        powershell -c (New-Object Media.SoundPlayer "C:\Windows\Media\Windows Notify.wav").PlaySync() 2>nul
    ) else (
        echo ⏳ [%date% %time%] 변경사항 없음
    )
    
    REM 5분(300초) 대기
    timeout /t 300 /nobreak > nul
    
goto loop
