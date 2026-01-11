@echo off
chcp 65001 > nul

echo 🚀 Streamlit 앱 실행 중...
echo.

REM 가상환경 활성화 및 앱 실행
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    python -m streamlit run app_figma.py --server.headless true
) else (
    echo ⚠️  가상환경이 없습니다. 'venv' 폴더를 확인하거나 생성해주세요.
    echo (예: python -m venv venv)
    pause
)

echo.
echo 앱이 종료되었습니다.
pause
