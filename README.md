# 📁 프로젝트 폴더 구조

```
museum-chatbot/
│
├── 📄 app.py                 # 메인 실행 파일 (개발자)
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
