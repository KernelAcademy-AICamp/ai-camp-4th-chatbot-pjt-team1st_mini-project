@echo off
chcp 65001
cd /d "%~dp0"
echo ========================================
echo 현재 위치: %CD%
echo ========================================
echo.

if not exist "venv\Scripts\python.exe" (
    echo [오류] 가상환경을 찾을 수 없습니다.
    echo venv\Scripts\python.exe 파일이 없습니다.
    echo.
    pause
    exit /b 1
)

if not exist "app.py" (
    echo [오류] app.py 파일을 찾을 수 없습니다.
    echo 현재 폴더: %CD%
    echo.
    dir /b *.py
    echo.
    pause
    exit /b 1
)

echo [1/3] 가상환경 확인 완료
echo [2/3] 가상환경 활성화 중...
call venv\Scripts\activate.bat
echo.

echo [3/3] Streamlit 앱 실행 중...
echo 브라우저가 자동으로 열립니다...
echo 종료하려면 Ctrl+C를 누르세요
echo ========================================
echo.

python -m streamlit run app.py

echo.
echo 앱이 종료되었습니다.
pause
