# 🏛️ 박물관 AI 가이드 챗봇

## 🚀 빠른 실행 (최신 코드 자동 업데이트)

### 방법 1: 실행할 때마다 자동 업데이트

**Mac/Linux:**
```bash
./run.sh
```

**Windows:**
```bash
run.bat
```

### 방법 2: 백그라운드 자동 감시 (추천! 🌟)

5분마다 자동으로 새 커밋을 확인하고 알림을 줍니다:

**Mac/Linux:**
```bash
./auto_update.sh
```

**Windows:**
```bash
auto_update.bat
```

- ✅ 새 커밋이 있으면 자동으로 pull + 알림음
- 💻 백그라운드에서 계속 감시
- 🛑 종료하려면 `Ctrl + C`

### 방법 3: 수동 실행
```bash
# 최신 코드 가져오기
git pull

# 앱 실행
python -m streamlit run app.py
```

---

## 📢 팀원 Push 알림 받는 방법

### 🌟 GitHub 알림 설정 (제일 쉬움)

1. 레포지토리 페이지 접속
2. 오른쪽 상단 **Watch** → **All Activity** 선택
3. GitHub 설정 → Notifications에서 이메일 알림 켜기
4. GitHub 모바일 앱 설치하면 푸시 알림도 받을 수 있어요!

### 💬 Slack/Discord 연동

레포지토리 Settings → Webhooks에서 Slack/Discord 연결하면
팀원이 push 할 때마다 메시지로 알림 받을 수 있어요.

### 🔄 자동 감시 스크립트 (위 참고)

`auto_update.sh` 또는 `auto_update.bat` 실행하면
5분마다 자동으로 체크하고 알림 줍니다.

---

## 📁 프로젝트 폴더 구조

```
fastcampus-project/
│
├── 📄 app.py                 # 메인 실행 파일 (개발자)
│
├── 🚀 실행 스크립트
│   ├── 📄 run.sh             # 실행 시 자동 업데이트 (Mac/Linux)
│   ├── 📄 run.bat            # 실행 시 자동 업데이트 (Windows)
│   ├── 📄 auto_update.sh     # 🌟 백그라운드 자동 감시 (Mac/Linux)
│   └── 📄 auto_update.bat    # 🌟 백그라운드 자동 감시 (Windows)
│
├── 📁 config/
│   ├── 📄 styles.py          # ⭐ 디자이너 전용 - CSS/색상/폰트
│   ├── 📄 prompts.py         # 기획자 전용 - AI 프롬프트
│   └── 📄 settings.py        # 개발자 전용 - 앱 설정
│
├── 📁 data/
│   └── 📄 artifacts.py       # 콘텐츠 담당 - 유물 데이터
│
├── 📁 services/
│   └── 📄 llm_service.py     # 개발자 전용 - AI 연동 로직
│
└── 📄 requirements.txt       # 패키지 목록
```

## 👥 역할별 담당 파일

| 역할 | 담당 파일 | 수정 내용 |
|------|----------|----------|
| **디자이너** | `config/styles.py` | 색상, 폰트, CSS, 레이아웃 |
| **기획자/PM** | `config/prompts.py` | AI 말투, 언어별 메시지 |
| **콘텐츠** | `data/artifacts.py` | 유물 정보 추가/수정 |
| **개발자** | `app.py`, `services/` | 기능 로직 |

## 🎨 디자이너 작업 방법

1. `config/styles.py` 파일만 열기
2. 색상 코드, CSS 수정
3. 저장 후 git push
4. 끝!

```python
# config/styles.py 예시
COLORS = {
    "primary": "#d4af37",      # ← 이 색상 바꾸면 전체 적용
    "background": "#1a1612",
    "text": "#f5f0e1",
}
```
