@echo off
chcp 65001 > nul

echo 📥 최신 코드를 불러오는 중...
git pull origin main

if %ERRORLEVEL% NEQ 0 (
    git pull origin master
)

echo.
echo ✅ 코드 업데이트 완료!

REM 가상환경 확인 및 활성화
if exist "venv\Scripts\activate.bat" (
    echo 🔧 가상환경 활성화 중...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  가상환경이 없습니다. 생성 중...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo 📦 패키지 설치 중...
    pip install -r requirements.txt
)

echo.
echo 🚀 Streamlit 앱 실행 중...
echo.

python -m streamlit run app.py
