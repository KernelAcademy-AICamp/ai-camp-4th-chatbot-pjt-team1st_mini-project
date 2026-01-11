#!/bin/bash

# 🔄 자동 업데이트 체크 스크립트
# 5분마다 새 커밋이 있는지 확인하고 자동으로 pull

echo "🔍 자동 업데이트 감시 시작..."
echo "5분마다 새 커밋을 확인합니다."
echo "종료하려면 Ctrl+C를 누르세요."
echo ""

while true; do
    # 원격 저장소 최신 정보 가져오기
    git fetch origin > /dev/null 2>&1
    
    # 로컬과 원격의 차이 확인
    LOCAL=$(git rev-parse @)
    REMOTE=$(git rev-parse @{u})
    
    if [ "$LOCAL" != "$REMOTE" ]; then
        echo "🆕 [$(date '+%Y-%m-%d %H:%M:%S')] 새로운 커밋 발견!"
        echo "📥 코드 업데이트 중..."
        
        git pull origin main || git pull origin master
        
        if [ $? -eq 0 ]; then
            echo "✅ 업데이트 완료!"
            echo ""
            
            # 알림음 재생 (Mac만 해당)
            afplay /System/Library/Sounds/Glass.aiff 2>/dev/null
            
            # 데스크탑 알림 (Mac만 해당)
            osascript -e 'display notification "팀원이 새 코드를 push 했습니다!" with title "📥 Git 업데이트"' 2>/dev/null
        fi
    else
        echo "⏳ [$(date '+%Y-%m-%d %H:%M:%S')] 변경사항 없음"
    fi
    
    # 5분 대기
    sleep 300
done
