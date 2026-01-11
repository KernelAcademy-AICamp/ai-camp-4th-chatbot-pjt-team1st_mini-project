#!/bin/bash

# 🔄 최신 코드 가져오기
echo "📥 최신 코드를 불러오는 중..."
git pull origin main

# 실패 시 다른 브랜치 시도
if [ $? -ne 0 ]; then
    git pull origin master
fi

echo ""
echo "✅ 코드 업데이트 완료!"

# 가상환경 활성화
if [ -d "venv" ]; then
    echo "🔧 가상환경 활성화 중..."
    source venv/bin/activate
else
    echo "⚠️  가상환경이 없습니다. 생성 중..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📦 패키지 설치 중..."
    pip install -r requirements.txt
fi

echo "🚀 Streamlit 앱 실행 중..."
echo ""

# 🏃 앱 실행
python -m streamlit run app.py
