"""
🏛️ 박물관 유물 안내 AI 챗봇 (멀티턴 대화 시스템)
===============================================

Figma 디자인 + 멀티턴 대화 플로우 구현
"""

import streamlit as st
from datetime import datetime
import random

# 설정 파일들 import
from config.prompts import WELCOME_MESSAGES, MESSAGES, UI_LABELS
from config.settings import APP_CONFIG, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE

# 데이터 import
from data.artifacts import ARTIFACTS, find_artifact, get_artifact_list

# 서비스 import
from services.llm_service import LLMService

# 컴포넌트 import
from components.chat_bubbles import (
    render_type_a_bot,
    render_type_a_user,
    render_type_b_bot,
    render_type_c_bot
)


# ============================================================
# 📱 페이지 설정
# ============================================================

st.set_page_config(
    page_title="국립중앙박물관 ChatBot",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# 🎨 Figma 디자인 CSS
# ============================================================

st.markdown("""
<style>
    /* Google Fonts - Pretendard */
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 전역 설정 */
    html, body {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Streamlit 기본 스타일 숨기기 */
    #MainMenu, footer, header, 
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    div[data-testid="stStatusWidget"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }
    
    .stApp {
        background: #ffffff !important;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Streamlit 기본 패딩/마진 완전 제거 */
    .main {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    .main .block-container,
    .block-container,
    [data-testid="stAppViewBlockContainer"] {
        padding: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        min-width: 100% !important;
    }
    
    /* Streamlit 1.x 버전 상단 패딩 제거 */
    .css-1d391kg, .css-12oz5g7, .css-1avcm0n, .css-18e3th9,
    .st-emotion-cache-1wrcr25, .st-emotion-cache-z5fcl4,
    .st-emotion-cache-1y4p8pa, .st-emotion-cache-16idsys {
        padding-top: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* 모든 Streamlit 요소 간격 제거 */
    .stMarkdown, .element-container, div[data-testid="stVerticalBlock"] {
        margin: 0 !important;
        padding: 0 !important;
        gap: 0 !important;
    }
    
    div[data-testid="stVerticalBlockBorderWrapper"] {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Streamlit 내부 컨테이너 */
    div[data-testid="stAppViewContainer"] {
        padding-top: 0 !important;
        margin: 0 !important;
    }
    
    div[data-testid="stMain"] {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* 상단 여백 완전 제거 */
    .stApp > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* ===== 헤더 스타일 ===== */
    .figma-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: #07364a;
        height: 103px;
        padding: 56px 15px 0 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        box-sizing: border-box;
        z-index: 1000;
    }
    
    .header-left {
        height: 30px;
        display: flex;
        align-items: center;
    }
    
    .header-title {
        color: #ffffff !important;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif !important;
        font-size: 22px !important;
        font-weight: 700 !important;
        line-height: 30px !important;
        margin: 0 !important;
        padding: 0 !important;
        white-space: nowrap;
        letter-spacing: 0;
    }
    
    .header-icons {
        height: 22px;
        display: flex;
        align-items: center;
        gap: 16px;
    }
    
    .header-icon {
        width: 24px;
        height: 24px;
        color: #ffffff;
        cursor: pointer;
    }
    
    /* ===== 서브헤더 스타일 ===== */
    .figma-subheader {
        position: fixed;
        top: 103px;
        left: 0;
        right: 0;
        background: #e7eef7;
        height: 47px;
        padding: 0 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        box-sizing: border-box;
        z-index: 999;
    }
    
    .subheader-icon {
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        flex-shrink: 0;
    }
    
    .subheader-icon svg {
        width: 20px;
        height: 20px;
    }
    
    .subheader-text-container {
        width: 186.92px;
        height: 21px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    
    .subheader-text {
        color: #000000;
        font-family: 'Pretendard', sans-serif;
        font-size: 15px;
        font-weight: 400;
        line-height: 21px;
        letter-spacing: 0.5px;
        margin: 0;
        white-space: nowrap;
    }
    
    .subheader-icon-right {
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        flex-shrink: 0;
    }
    
    .subheader-icon-right svg {
        width: 24px;
        height: 24px;
    }
    
    /* ===== 채팅 영역 스타일 ===== */
    .figma-chat-container {
        margin-top: 150px;  /* 헤더(103) + 서브헤더(47) */
        margin-bottom: 164px;  /* 입력 필드(60) + 하단 네비(104) */
        background: #ffffff;
        padding: 15px;
        min-height: calc(100vh - 150px - 164px);
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    /* 채팅 턴과 버튼 사이 간격 - Figma gap: 13px */
    .chat-turn {
        margin-bottom: 13px !important;
    }
    
    .chat-content-wrapper {
        width: 100%;
        max-width: 363px;
    }
    
    /* ===== 채팅 턴 스타일 ===== */
    .chat-turn {
        display: flex;
        flex-direction: column;
        gap: 15px;
        margin-bottom: 15px;
    }
    
    .message-group {
        display: flex;
        flex-direction: column;
        gap: 13px;
    }
    
    /* ===== 봇 메시지 스타일 ===== */
    .bot-message-container {
        display: flex;
        flex-direction: column;
        gap: 5px;
        padding-right: 20px;
    }
    
    .bot-header {
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .bot-avatar {
        width: 28px;
        height: 28px;
        border-radius: 1000px;
        background: #f4f4f4;
        border: 0.5px solid #CCCCCC;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        overflow: hidden;
    }
    
    .bot-avatar img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .bot-info {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .bot-name {
        font-family: 'Pretendard', sans-serif;
        font-size: 13px;
        font-weight: 400;
        color: #333333;
        line-height: 1.4;
    }
    
    .bot-timestamp {
        font-family: 'Pretendard', sans-serif;
        font-size: 12px;
        font-weight: 400;
        color: #7a7a7a;
        line-height: 1.4;
    }
    
    .bot-bubble {
        background: #e7eef7;
        padding: 15px;
        border-radius: 0 10px 10px 10px;
        max-width: 343px;
        margin-left: 34px;
    }
    
    .bot-bubble p {
        font-family: 'Pretendard', sans-serif;
        font-size: 16px;
        font-weight: 400;
        color: #333333;
        line-height: 1.4;
        margin: 0;
        white-space: pre-wrap;
    }
    
    /* ===== 사용자 메시지 스타일 ===== */
    .user-message-container {
        display: flex;
        gap: 5px;
        justify-content: flex-end;
        padding-left: 20px;
        align-items: flex-end;
    }
    
    .user-timestamp {
        font-family: 'Pretendard', sans-serif;
        font-size: 12px;
        font-weight: 400;
        color: #7a7a7a;
        line-height: 1.4;
    }
    
    .user-bubble {
        background: #246beb;
        padding: 15px;
        border-radius: 10px 10px 0 10px;
        max-width: 307px;
    }
    
    .user-bubble p {
        font-family: 'Pretendard', sans-serif;
        font-size: 16px;
        font-weight: 400;
        color: #ffffff;
        line-height: 1.4;
        margin: 0;
    }
    
    /* ===== 버튼 그룹 스타일 ===== */
    .button-group {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-left: 34px;
        margin-top: 10px;
    }
    
    /* ===== 하단 네비게이션 스타일 ===== */
    .figma-bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #ffffff;
        border-top: 1px solid #e0e0e0;
        height: 104px;
        display: flex;
        justify-content: space-around;
        align-items: flex-start;
        padding-top: 12px;
        box-sizing: border-box;
        z-index: 1000;
    }
    
    .nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 4px;
        cursor: pointer;
        padding: 4px 8px;
        flex: 1;
        text-decoration: none;
    }
    
    .nav-item:hover {
        background: #f5f5f5;
    }
    
    .nav-icon {
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
    }
    
    .nav-label {
        font-family: 'Pretendard', sans-serif;
        font-size: 11px;
        font-weight: 500;
        color: #666666;
        text-align: center;
    }
    
    /* 하단 여백 */
    .bottom-spacer {
        display: none;
    }
    
    /* Streamlit 버튼 기본 - 아래에서 재정의 */
    
    /* 버튼 - Figma 스타일 */
    .stButton > button {
        background: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #cccccc !important;
        border-radius: 1000px !important;
        padding: 10px 20px !important;
        height: 35px !important;
        font-family: 'Pretendard', sans-serif !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        letter-spacing: -0.16px !important;
        box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.04) !important;
        width: auto !important;
        min-width: fit-content !important;
        line-height: 1.4 !important;
    }
    
    .stButton > button:hover {
        background: #f5f5f5 !important;
        border-color: #999999 !important;
    }
    
    /* 버튼 컨테이너 - Figma gap: 13px */
    div[data-testid="stHorizontalBlock"] {
        gap: 8px !important;
        flex-wrap: wrap !important;
        justify-content: flex-start !important;
        max-width: 363px !important;
        margin: 0 auto !important;
    }
    
    /* 단일 버튼 - 채팅 버블 아래 배치 */
    .stButton {
        max-width: 363px !important;
        margin: 0 auto !important;
        display: block !important;
    }
    
    /* 체크박스 */
    .stCheckbox {
        max-width: 363px !important;
        margin: 0 auto !important;
    }
    
    /* info 메시지 */
    [data-testid="stAlert"] {
        max-width: 363px !important;
        margin: 0 auto !important;
    }
    
    /* 마크다운 텍스트 */
    .element-container:has(.stMarkdown) {
        max-width: 363px !important;
        margin: 0 auto !important;
    }
    
    /* 체크박스 스타일 */
    .stCheckbox {
        margin-left: 34px !important;
    }
    
    .stCheckbox label {
        font-family: 'Pretendard', sans-serif !important;
        font-size: 14px !important;
    }
    
    /* ===== 입력 필드 영역 ===== */
    
    /* wag - 배경 블러 레이어 */
    .stChatInput::before {
        content: '';
        position: fixed;
        bottom: 104px;
        left: 50%;
        transform: translateX(-50%);
        width: 393px;
        height: 65px;
        background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,0.3));
        backdrop-filter: blur(2px);
        -webkit-backdrop-filter: blur(2px);
        z-index: 997;
        pointer-events: none;
    }
    
    /* Input Container */
    .stChatInput {
        position: fixed !important;
        bottom: 104px !important;
        left: 0 !important;
        right: 0 !important;
        background: transparent !important;
        backdrop-filter: blur(2px) !important;
        -webkit-backdrop-filter: blur(2px) !important;
        padding: 10px 15px 15px 15px !important;
        z-index: 998 !important;
        border: none !important;
        margin: 0 !important;
    }
    
    .stChatInput > div {
        max-width: 393px;
        margin: 0 auto;
    }
    
    /* Input Field */
    .stChatInput textarea,
    .stChatInput input,
    .stChatInput [data-testid="stChatInputTextArea"] {
        background: #f1f2f6 !important;
        border: 1px solid #eeeeee !important;
        border-radius: 100px !important;
        padding: 10px 45px 10px 17px !important;
        font-family: 'Pretendard', sans-serif !important;
        font-size: 16px !important;
        line-height: 15px !important;
        color: #333333 !important;
    }
    
    /* Placeholder */
    .stChatInput textarea::placeholder,
    .stChatInput input::placeholder {
        color: #7e7f8a !important;
        font-family: 'Pretendard', sans-serif !important;
        font-size: 16px !important;
    }
    
    /* Input Field - Focus 상태 */
    .stChatInput textarea:focus,
    .stChatInput input:focus,
    .stChatInput [data-testid="stChatInputTextArea"]:focus {
        outline: none !important;
        border: 1px solid #345A6A !important;
    }
    
    /* Send Button 공통 */
    .stChatInput button[kind="primary"],
    .stChatInput [data-testid="stChatInputSubmitButton"] {
        background: transparent !important;
        border: none !important;
        width: 20px !important;
        height: 20px !important;
        padding: 0 !important;
        position: absolute !important;
        right: 26px !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
    }
    
    .stChatInput button[kind="primary"] svg,
    .stChatInput [data-testid="stChatInputSubmitButton"] svg {
        display: none !important;
    }
    
    /* Send Button - 기본/Focus 상태 (비활성화) */
    .stChatInput button[kind="primary"]::after,
    .stChatInput [data-testid="stChatInputSubmitButton"]::after,
    .stChatInput button[kind="primary"]:disabled::after,
    .stChatInput [data-testid="stChatInputSubmitButton"]:disabled::after {
        content: '';
        display: block;
        width: 20px;
        height: 20px;
        background-image: url('app/static/images/icon_send.png');
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
    }
    
    /* Send Button - Active 상태 (활성화, 입력 있음) */
    .stChatInput button[kind="primary"]:not(:disabled)::after,
    .stChatInput [data-testid="stChatInputSubmitButton"]:not(:disabled)::after {
        background-image: url('app/static/images/icon_send_active.png');
    }
    
    /* 퀴즈 선택지 버튼 */
    .quiz-option-btn {
        background: #ffffff !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        text-align: left !important;
        width: 100% !important;
        margin-bottom: 8px !important;
    }
    
    .quiz-option-btn:hover {
        background: #f5f5f5 !important;
        border-color: #246beb !important;
    }
    
    /* 결과 카드 */
    .result-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        margin-left: 34px;
        max-width: 300px;
    }
    
    .result-card h3 {
        font-family: 'Pretendard', sans-serif;
        font-size: 18px;
        font-weight: 700;
        color: #333;
        margin: 0 0 15px 0;
    }
    
    .result-item {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        font-family: 'Pretendard', sans-serif;
        font-size: 14px;
    }
    
    .result-label {
        color: #666;
    }
    
    .result-value {
        color: #333;
        font-weight: 600;
    }
    
    .result-score {
        font-size: 32px;
        font-weight: 700;
        color: #246beb;
        text-align: center;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# 🎯 상수 정의
# ============================================================

# 대화 단계
STEPS = {
    "GREETING": "greeting",
    "USER_TYPE": "user_type",
    "TOUR_CHECK": "tour_check",
    "ARTIFACT_LIST": "artifact_list",
    "ARTIFACT_SELECT": "artifact_select",
    "QUIZ_READY": "quiz_ready",
    "QUIZ_QUESTION": "quiz_question",
    "QUIZ_FEEDBACK": "quiz_feedback",
    "QUIZ_RESULT": "quiz_result",
    "END": "end"
}

# 사용자 유형
USER_TYPES = ["어린이", "초등학생", "중학생", "고등학생", "성인"]

# 사용자 유형별 톤
USER_TYPE_TONE = {
    "어린이": {"style": "반말", "emoji": True, "simple": True},
    "초등학생": {"style": "반말", "emoji": True, "simple": True},
    "중학생": {"style": "존댓말", "emoji": True, "simple": False},
    "고등학생": {"style": "존댓말", "emoji": False, "simple": False},
    "성인": {"style": "존댓말", "emoji": False, "simple": False}
}

# 최소/최대 유물 개수
MIN_ARTIFACTS = 3
MAX_ARTIFACTS = 10


# ============================================================
# 💾 세션 상태 초기화
# ============================================================

def init_session_state():
    """세션 상태 초기화"""
    
    # 대화 메시지
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # 현재 단계
    if "current_step" not in st.session_state:
        st.session_state.current_step = STEPS["GREETING"]
    
    # 사용자 유형
    if "user_type" not in st.session_state:
        st.session_state.user_type = None
    
    # 전시투어 존재 여부 (임시로 True로 설정)
    if "tour_exists" not in st.session_state:
        st.session_state.tour_exists = True
    
    # 사용자의 전시투어 유물 목록 (임시 데이터)
    if "user_artifacts" not in st.session_state:
        st.session_state.user_artifacts = list(ARTIFACTS.keys())
    
    # 선택된 퀴즈 유물
    if "selected_artifacts" not in st.session_state:
        st.session_state.selected_artifacts = []
    
    # 퀴즈 진행 상태
    if "quiz_progress" not in st.session_state:
        st.session_state.quiz_progress = {
            "current_index": 0,
            "total_questions": 0,
            "correct_count": 0,
            "wrong_answers": [],
            "quizzes": []
        }
    
    # 현재 퀴즈
    if "current_quiz" not in st.session_state:
        st.session_state.current_quiz = None
    
    # 언어
    if "language" not in st.session_state:
        st.session_state.language = DEFAULT_LANGUAGE
    
    # LLM 서비스
    if "llm_service" not in st.session_state:
        st.session_state.llm_service = LLMService()

init_session_state()


# ============================================================
# 🛠️ 유틸리티 함수
# ============================================================

def add_bot_message(content: str, sender: str = "철수", msg_type: str = "A", button: dict = None, buttons: list = None):
    """
    봇 메시지 추가
    
    Args:
        content: 메시지 내용
        sender: 발신자
        msg_type: 메시지 타입 (A: 일반, B: 단일버튼, C: 다중버튼)
        button: Type B용 - {"text": "버튼텍스트", "action": "액션명"}
        buttons: Type C용 - [{"text": "버튼1", "action": "액션1"}, ...]
    """
    msg = {
        "role": "assistant",
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M"),
        "sender": sender,
        "type": msg_type
    }
    
    if msg_type == "B" and button:
        msg["button"] = button
    elif msg_type == "C" and buttons:
        msg["buttons"] = buttons
    
    st.session_state.messages.append(msg)

def add_user_message(content: str):
    """사용자 메시지 추가"""
    st.session_state.messages.append({
        "role": "user",
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M"),
        "type": "A"
    })

def get_tone_text(formal: str, casual: str) -> str:
    """사용자 유형에 따른 톤 텍스트 반환"""
    if st.session_state.user_type in ["어린이", "초등학생"]:
        return casual
    return formal

def generate_quiz(artifact_name: str) -> dict:
    """유물에 대한 퀴즈 생성"""
    artifact = ARTIFACTS.get(artifact_name)
    if not artifact:
        return None
    
    # 퀴즈 유형 랜덤 선택
    quiz_types = ["name", "period", "material", "fact"]
    quiz_type = random.choice(quiz_types)
    
    if quiz_type == "name":
        # 이름 맞추기
        question = f"이 유물의 특징이야:\n{artifact['description'][:100]}...\n\n이 유물의 이름은 뭘까?"
        correct = artifact_name
        options = [correct]
        other_artifacts = [k for k in ARTIFACTS.keys() if k != artifact_name]
        options.extend(random.sample(other_artifacts, min(4, len(other_artifacts))))
        random.shuffle(options)
        
    elif quiz_type == "period":
        # 시대 맞추기
        question = f"'{artifact_name}'은(는) 어느 시대에 만들어졌을까?"
        correct = artifact["period"]
        options = [correct, "고조선", "통일신라", "고려", "조선"]
        options = list(set(options))[:5]
        random.shuffle(options)
        
    elif quiz_type == "material":
        # 재료 맞추기
        question = f"'{artifact_name}'은(는) 무엇으로 만들어졌을까?"
        correct = artifact["material"]
        options = [correct, "금", "청동", "옥", "종이", "청자"]
        options = list(set(options))[:5]
        random.shuffle(options)
        
    else:
        # 흥미로운 사실
        fact = random.choice(artifact["fun_facts"])
        question = f"'{artifact_name}'에 대한 설명 중 맞는 것은?"
        correct = fact
        # 다른 유물의 사실들로 오답 생성
        wrong_facts = []
        for name, art in ARTIFACTS.items():
            if name != artifact_name:
                wrong_facts.extend(art["fun_facts"])
        options = [correct] + random.sample(wrong_facts, min(4, len(wrong_facts)))
        random.shuffle(options)
    
    return {
        "artifact_name": artifact_name,
        "question": question,
        "options": options[:5],  # 최대 5개
        "correct_answer": correct,
        "correct_index": options.index(correct),
        "explanation": f"{artifact_name}: {artifact['description'][:150]}..."
    }


# ============================================================
# 🎬 대화 플로우 함수
# ============================================================

def handle_greeting():
    """STEP 1: 그리팅"""
    if len(st.session_state.messages) == 0:
        add_bot_message(
            "안녕! 👋 나는 국립중앙박물관 학습 도우미야!\n"
            "오늘 전시 재밌게 봤어?\n"
            "퀴즈 풀기 전에 먼저 알려줘~",
            msg_type="C",
            buttons=[{"text": t, "action": f"select_{t}"} for t in USER_TYPES]
        )
        st.session_state.current_step = STEPS["USER_TYPE"]

def handle_user_type_selection(selected_type: str):
    """사용자 유형 선택 처리"""
    add_user_message(selected_type)
    st.session_state.user_type = selected_type
    
    # 선택에 따른 응답 - Type C (두 개 버튼)
    if selected_type in ["어린이", "초등학생"]:
        add_bot_message(
            f"{selected_type}이구나! 반가워~ 😊\n혹시 오늘 '나의 전시투어' 만들었어?",
            msg_type="C",
            buttons=[
                {"text": "응, 만들었어!", "action": "tour_yes"},
                {"text": "아니, 아직...", "action": "tour_no"}
            ]
        )
    else:
        add_bot_message(
            f"{selected_type}이시군요! 반갑습니다. 😊\n혹시 오늘 '나의 전시투어'를 만드셨나요?",
            msg_type="C",
            buttons=[
                {"text": "네, 만들었어요!", "action": "tour_yes"},
                {"text": "아니요, 아직이요...", "action": "tour_no"}
            ]
        )
    
    st.session_state.current_step = STEPS["TOUR_CHECK"]

def handle_tour_check(has_tour: bool):
    """전시투어 확인 처리"""
    if has_tour:
        add_user_message("응, 만들었어!" if st.session_state.user_type in ["어린이", "초등학생"] else "네, 만들었어요!")
        
        # 유물 목록 표시
        artifact_list = "\n".join([f"{i+1}. {name}" for i, name in enumerate(st.session_state.user_artifacts)])
        
        msg = get_tone_text(
            f"좋습니다! 전시투어를 불러올게요~ ⏳\n\n와~ 유물 {len(st.session_state.user_artifacts)}개나 담으셨네요! 👏\n\n📜 나의 전시투어\n{artifact_list}",
            f"좋아! 전시투어 불러올게~ ⏳\n\n와~ 유물 {len(st.session_state.user_artifacts)}개나 담았네! 👏\n\n📜 나의 전시투어\n{artifact_list}"
        )
        add_bot_message(msg)
        st.session_state.current_step = STEPS["ARTIFACT_SELECT"]
    else:
        add_user_message("아니, 아직..." if st.session_state.user_type in ["어린이", "초등학생"] else "아니요, 아직이요...")
        
        msg = get_tone_text(
            "앗, 전시투어를 먼저 만들어주세요! 🏛️\n전시투어에 유물을 담아야 퀴즈를 풀 수 있어요.\n\n다음에 다시 만나요! 👋",
            "앗, 전시투어를 먼저 만들어줘! 🏛️\n전시투어에 유물을 담아야 퀴즈를 풀 수 있어.\n\n다음에 다시 만나자! 👋"
        )
        add_bot_message(msg)
        st.session_state.current_step = STEPS["END"]

def handle_artifact_selection(selected: list):
    """유물 선택 처리"""
    st.session_state.selected_artifacts = selected
    selected_names = ", ".join(selected)
    add_user_message(f"{len(selected)}개 선택: {selected_names[:50]}...")
    
    # 퀴즈 생성
    quizzes = []
    for artifact_name in selected:
        quiz = generate_quiz(artifact_name)
        if quiz:
            quizzes.append(quiz)
    
    st.session_state.quiz_progress = {
        "current_index": 0,
        "total_questions": len(quizzes),
        "correct_count": 0,
        "wrong_answers": [],
        "quizzes": quizzes
    }
    
    msg = get_tone_text(
        f"좋습니다! {len(selected)}개 유물로 퀴즈를 시작할게요! 🚀\n준비되셨나요?",
        f"좋아! {len(selected)}개 유물로 퀴즈 시작할게! 🚀\n준비됐어?"
    )
    add_bot_message(msg)
    st.session_state.current_step = STEPS["QUIZ_READY"]

def handle_quiz_start():
    """퀴즈 시작"""
    add_user_message("준비 완료!")
    show_next_question()

def show_next_question():
    """다음 문제 출제"""
    progress = st.session_state.quiz_progress
    
    if progress["current_index"] >= progress["total_questions"]:
        # 퀴즈 종료
        show_quiz_result()
        return
    
    quiz = progress["quizzes"][progress["current_index"]]
    st.session_state.current_quiz = quiz
    
    # 문제 출제
    options_text = "\n".join([f"{'①②③④⑤'[i]} {opt}" for i, opt in enumerate(quiz["options"])])
    
    msg = get_tone_text(
        f"📝 문제 {progress['current_index'] + 1}/{progress['total_questions']}!\n\n{quiz['question']}\n\n{options_text}",
        f"📝 문제 {progress['current_index'] + 1}번!\n\n{quiz['question']}\n\n{options_text}"
    )
    add_bot_message(msg)
    st.session_state.current_step = STEPS["QUIZ_QUESTION"]

def handle_quiz_answer(answer_index: int):
    """퀴즈 답변 처리"""
    quiz = st.session_state.current_quiz
    progress = st.session_state.quiz_progress
    
    selected_option = quiz["options"][answer_index]
    add_user_message(f"{'①②③④⑤'[answer_index]} {selected_option[:20]}...")
    
    is_correct = (answer_index == quiz["correct_index"])
    
    if is_correct:
        progress["correct_count"] += 1
        msg = get_tone_text(
            f"🎉 정답이에요! 대단해요~\n\n{quiz['explanation'][:100]}...",
            f"🎉 정답이야! 대단해~\n\n{quiz['explanation'][:100]}..."
        )
    else:
        progress["wrong_answers"].append({
            "question": quiz["question"],
            "user_answer": selected_option,
            "correct_answer": quiz["correct_answer"],
            "explanation": quiz["explanation"]
        })
        correct_text = quiz["correct_answer"][:30]
        msg = get_tone_text(
            f"앗, 아쉬워요! 😅\n\n정답은 '{correct_text}...'이에요!\n{quiz['explanation'][:80]}...",
            f"앗, 아쉬워! 😅\n\n정답은 '{correct_text}...'야!\n{quiz['explanation'][:80]}..."
        )
    
    add_bot_message(msg)
    
    # 다음 문제로
    progress["current_index"] += 1
    st.session_state.quiz_progress = progress
    st.session_state.current_step = STEPS["QUIZ_FEEDBACK"]

def show_quiz_result():
    """퀴즈 결과 표시"""
    progress = st.session_state.quiz_progress
    total = progress["total_questions"]
    correct = progress["correct_count"]
    score = int((correct / total) * 100) if total > 0 else 0
    
    msg = get_tone_text(
        f"🎊 퀴즈 끝! 수고하셨어요~\n\n"
        f"📊 결과\n"
        f"• 총 문제: {total}개\n"
        f"• 맞은 개수: {correct}개\n"
        f"• 정답률: {score}% {'🌟' if score >= 80 else '💪'}\n\n"
        f"{'와~ 정말 잘하셨어요! 👏👏' if score >= 80 else '다음엔 더 잘할 수 있을 거예요! 💪'}",
        
        f"🎊 퀴즈 끝! 수고했어~\n\n"
        f"📊 결과\n"
        f"• 총 문제: {total}개\n"
        f"• 맞은 개수: {correct}개\n"
        f"• 정답률: {score}% {'🌟' if score >= 80 else '💪'}\n\n"
        f"{'와~ 진짜 잘했어! 👏👏' if score >= 80 else '다음엔 더 잘할 수 있어! 💪'}"
    )
    add_bot_message(msg)
    st.session_state.current_step = STEPS["QUIZ_RESULT"]

def handle_review_wrong():
    """오답 복습"""
    wrong = st.session_state.quiz_progress["wrong_answers"]
    
    if not wrong:
        msg = get_tone_text("틀린 문제가 없어요! 👏", "틀린 문제가 없어! 👏")
    else:
        review_text = "\n\n".join([
            f"❌ {w['question'][:50]}...\n"
            f"네 답: {w['user_answer'][:20]}...\n"
            f"정답: {w['correct_answer'][:20]}..."
            for w in wrong[:3]  # 최대 3개만
        ])
        msg = get_tone_text(
            f"📚 틀린 문제 복습!\n\n{review_text}",
            f"📚 틀린 문제 복습!\n\n{review_text}"
        )
    
    add_bot_message(msg)

def handle_end():
    """대화 종료"""
    msg = get_tone_text(
        "오늘 퀴즈 재밌으셨나요? 😊\n\n다음에 박물관 오시면 또 퀴즈 풀어요!\n오늘 본 유물들 잊지 마세요~ 👋\n\n🏛️ 대화가 종료되었습니다.",
        "오늘 퀴즈 재밌었어? 😊\n\n다음에 박물관 오면 또 퀴즈 풀자!\n오늘 본 유물들 잊지 마~ 👋\n\n🏛️ 대화가 종료되었습니다."
    )
    add_bot_message(msg)
    st.session_state.current_step = STEPS["END"]


# ============================================================
# 🎨 렌더링 함수
# ============================================================

def render_messages():
    """메시지 렌더링 - 타입별 처리"""
    message_parts = []
    
    for msg in st.session_state.messages:
        msg_type = msg.get("type", "A")
        
        if msg["role"] == "assistant":
            sender = msg.get("sender", "철수")
            timestamp = msg.get("timestamp", datetime.now().strftime("%H:%M"))
            content = msg["content"].replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
            
            # 봇 메시지 HTML (모든 타입 공통)
            message_parts.append(
                f'<div class="chat-turn type-{msg_type.lower()}">'
                '<div class="bot-message-container">'
                '<div class="bot-header"><div class="bot-avatar">'
                '<img src="app/static/images/profile.png" alt="profile"></div>'
                f'<div class="bot-info"><span class="bot-name">{sender}</span>'
                f'<span class="bot-timestamp">{timestamp}</span></div></div>'
                f'<div class="bot-bubble"><p>{content}</p></div>'
                '</div></div>'
            )
        else:
            timestamp = msg.get("timestamp", datetime.now().strftime("%H:%M"))
            content = msg["content"].replace("<", "&lt;").replace(">", "&gt;")
            
            message_parts.append(
                '<div class="chat-turn type-a">'
                '<div class="user-message-container">'
                f'<span class="user-timestamp">{timestamp}</span>'
                f'<div class="user-bubble"><p>{content}</p></div>'
                '</div></div>'
            )
    
    return ''.join(message_parts)


def get_last_message_buttons():
    """마지막 메시지의 버튼 정보 반환 (Type B, C용)"""
    if not st.session_state.messages:
        return None
    
    last_msg = st.session_state.messages[-1]
    msg_type = last_msg.get("type", "A")
    
    if msg_type == "B" and "button" in last_msg:
        return {"type": "B", "button": last_msg["button"]}
    elif msg_type == "C" and "buttons" in last_msg:
        return {"type": "C", "buttons": last_msg["buttons"]}
    
    return None


# ============================================================
# 🖥️ 메인 UI
# ============================================================

# 헤더
st.markdown("""
<div class="figma-header">
    <div class="header-left">
        <p class="header-title">ChatBot</p>
    </div>
    <div class="header-icons">
        <svg class="header-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="11" cy="11" r="7" stroke="white" stroke-width="2"/>
            <path d="M20 20L16.5 16.5" stroke="white" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <svg class="header-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 6H21M3 12H21M3 18H21" stroke="white" stroke-width="2" stroke-linecap="round"/>
        </svg>
    </div>
</div>
""", unsafe_allow_html=True)

# 서브헤더
st.markdown("""
<div class="figma-subheader">
    <div class="subheader-icon">
        <img src="app/static/images/icon_refresh.png" alt="refresh" style="width: 20px; height: 20px;">
    </div>
    <div class="subheader-text-container">
        <p class="subheader-text">국립중앙박물관 스마트전시관</p>
    </div>
    <div class="subheader-icon-right" style="opacity: 0;">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M8 5V19L19 12L8 5Z" fill="black"/>
        </svg>
    </div>
</div>
""", unsafe_allow_html=True)

# 그리팅 처리
handle_greeting()

# 채팅 영역
chat_html = f'''
<div class="figma-chat-container" id="chat-container">
    <div class="chat-content-wrapper">
        {render_messages()}
        <div id="chat-bottom"></div>
    </div>
</div>
'''
st.markdown(chat_html, unsafe_allow_html=True)

# 자동 스크롤 JavaScript
st.markdown("""
<script>
    // 페이지 로드 후 맨 아래로 스크롤
    setTimeout(() => {
        window.scrollTo(0, document.body.scrollHeight);
    }, 100);
</script>
""", unsafe_allow_html=True)

# 현재 단계에 따른 버튼/입력 UI
current_step = st.session_state.current_step

if current_step == STEPS["USER_TYPE"]:
    # 사용자 유형 선택 버튼
    cols = st.columns(len(USER_TYPES))
    for i, user_type in enumerate(USER_TYPES):
        with cols[i]:
            if st.button(user_type, key=f"user_type_{i}"):
                handle_user_type_selection(user_type)
                st.rerun()

elif current_step == STEPS["TOUR_CHECK"]:
    # 전시투어 확인 버튼
    col1, col2 = st.columns(2)
    with col1:
        yes_text = "응, 만들었어!" if st.session_state.user_type in ["어린이", "초등학생"] else "네, 만들었어요!"
        if st.button(yes_text, key="tour_yes"):
            handle_tour_check(True)
            st.rerun()
    with col2:
        no_text = "아니, 아직..." if st.session_state.user_type in ["어린이", "초등학생"] else "아니요, 아직이요..."
        if st.button(no_text, key="tour_no"):
            handle_tour_check(False)
            st.rerun()

elif current_step == STEPS["ARTIFACT_SELECT"]:
    # 유물 선택 체크박스
    st.markdown("**퀴즈 풀 유물을 선택하세요 (최소 3개)**")
    
    selected = []
    for artifact_name in st.session_state.user_artifacts:
        if st.checkbox(artifact_name, key=f"artifact_{artifact_name}"):
            selected.append(artifact_name)
    
    if len(selected) >= MIN_ARTIFACTS:
        if st.button(f"선택 완료! ({len(selected)}개)", key="select_done"):
            handle_artifact_selection(selected)
            st.rerun()
    else:
        st.info(f"최소 {MIN_ARTIFACTS}개 이상 선택해주세요. (현재 {len(selected)}개)")

elif current_step == STEPS["QUIZ_READY"]:
    # 퀴즈 시작 버튼
    if st.button("준비 완료! 🚀", key="quiz_start"):
        handle_quiz_start()
        st.rerun()

elif current_step == STEPS["QUIZ_QUESTION"]:
    # 퀴즈 선택지 버튼
    quiz = st.session_state.current_quiz
    if quiz:
        for i, option in enumerate(quiz["options"]):
            if st.button(f"{'①②③④⑤'[i]} {option}", key=f"quiz_opt_{i}"):
                handle_quiz_answer(i)
                st.rerun()

elif current_step == STEPS["QUIZ_FEEDBACK"]:
    # 다음 문제 버튼
    progress = st.session_state.quiz_progress
    if progress["current_index"] < progress["total_questions"]:
        if st.button("다음 문제! ➡️", key="next_question"):
            show_next_question()
            st.rerun()
    else:
        if st.button("결과 보기! 📊", key="show_result"):
            show_quiz_result()
            st.rerun()

elif current_step == STEPS["QUIZ_RESULT"]:
    # 결과 화면 버튼
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("오답 복습 📚", key="review_wrong"):
            handle_review_wrong()
            st.rerun()
    with col2:
        if st.button("다시 풀기 🔄", key="retry_quiz"):
            st.session_state.current_step = STEPS["ARTIFACT_SELECT"]
            st.session_state.quiz_progress = {
                "current_index": 0,
                "total_questions": 0,
                "correct_count": 0,
                "wrong_answers": [],
                "quizzes": []
            }
            add_bot_message(get_tone_text(
                "다시 유물을 선택해주세요!",
                "다시 유물 골라줘!"
            ))
            st.rerun()
    with col3:
        if st.button("끝내기 👋", key="end_chat"):
            handle_end()
            st.rerun()

elif current_step == STEPS["END"]:
    # 대화 종료 - 처음부터 다시 버튼
    if st.button("처음부터 다시 시작 🔄", key="restart"):
        # 세션 초기화
        st.session_state.messages = []
        st.session_state.current_step = STEPS["GREETING"]
        st.session_state.user_type = None
        st.session_state.selected_artifacts = []
        st.session_state.quiz_progress = {
            "current_index": 0,
            "total_questions": 0,
            "correct_count": 0,
            "wrong_answers": [],
            "quizzes": []
        }
        st.rerun()

# 하단 여백
st.markdown('<div class="bottom-spacer"></div>', unsafe_allow_html=True)


# ============================================================
# 📝 자유 입력 처리
# ============================================================

def handle_free_input(user_input: str):
    """자유 입력 처리"""
    add_user_message(user_input)
    
    # 키워드 기반 처리
    input_lower = user_input.lower()
    
    # 종료 키워드
    if any(kw in input_lower for kw in ["종료", "끝", "그만", "bye", "exit"]):
        handle_end()
        return
    
    # 처음부터 키워드
    if any(kw in input_lower for kw in ["처음", "다시", "리셋", "reset"]):
        st.session_state.messages = []
        st.session_state.current_step = STEPS["GREETING"]
        st.session_state.user_type = None
        add_bot_message(get_tone_text(
            "처음부터 다시 시작할게요! 👋",
            "처음부터 다시 시작할게! 👋"
        ))
        return
    
    # 도움말 키워드
    if any(kw in input_lower for kw in ["도움", "도움말", "help", "?"]):
        help_msg = get_tone_text(
            "🆘 도움말\n\n"
            "• '종료' - 대화 종료\n"
            "• '처음' - 처음부터 다시\n"
            "• '도움' - 이 도움말 보기\n\n"
            "버튼을 클릭하거나 자유롭게 입력해주세요!",
            "🆘 도움말\n\n"
            "• '종료' - 대화 끝내기\n"
            "• '처음' - 처음부터 다시\n"
            "• '도움' - 이 도움말 보기\n\n"
            "버튼 누르거나 자유롭게 입력해줘!"
        )
        add_bot_message(help_msg)
        return
    
    # 퀴즈 중 숫자 입력 처리
    if st.session_state.current_step == STEPS["QUIZ_QUESTION"]:
        quiz = st.session_state.current_quiz
        if quiz:
            # 숫자로 답변
            if user_input.strip() in ["1", "2", "3", "4", "5"]:
                answer_index = int(user_input.strip()) - 1
                if answer_index < len(quiz["options"]):
                    handle_quiz_answer(answer_index)
                    return
            # ①②③④⑤로 답변
            for i, symbol in enumerate("①②③④⑤"):
                if symbol in user_input:
                    if i < len(quiz["options"]):
                        handle_quiz_answer(i)
                        return
    
    # 사용자 유형 선택 단계에서 자유 입력
    if st.session_state.current_step == STEPS["USER_TYPE"]:
        for user_type in USER_TYPES:
            if user_type in user_input:
                handle_user_type_selection(user_type)
                return
    
    # 전시투어 확인 단계에서 자유 입력
    if st.session_state.current_step == STEPS["TOUR_CHECK"]:
        if any(kw in input_lower for kw in ["응", "네", "예", "만들었", "yes", "만듬"]):
            handle_tour_check(True)
            return
        if any(kw in input_lower for kw in ["아니", "아직", "no", "없"]):
            handle_tour_check(False)
            return
    
    # 그 외 - 현재 단계에 맞는 안내
    step = st.session_state.current_step
    
    if step == STEPS["USER_TYPE"]:
        add_bot_message(get_tone_text(
            "위 버튼 중에서 선택해주세요! 😊",
            "위에 버튼 중에서 골라줘! 😊"
        ))
    elif step == STEPS["TOUR_CHECK"]:
        add_bot_message(get_tone_text(
            "'응' 또는 '아니'로 대답해주세요!",
            "'응' 아니면 '아니'로 대답해줘!"
        ))
    elif step == STEPS["ARTIFACT_SELECT"]:
        add_bot_message(get_tone_text(
            "유물을 체크박스로 선택한 후 '선택 완료' 버튼을 눌러주세요!",
            "유물 체크하고 '선택 완료' 버튼 눌러줘!"
        ))
    elif step == STEPS["QUIZ_READY"]:
        add_bot_message(get_tone_text(
            "'준비 완료' 버튼을 눌러주세요!",
            "'준비 완료' 버튼 눌러줘!"
        ))
    elif step == STEPS["QUIZ_QUESTION"]:
        add_bot_message(get_tone_text(
            "1~5 중에서 숫자로 대답해주세요!",
            "1~5 중에서 숫자로 대답해줘!"
        ))
    elif step == STEPS["QUIZ_FEEDBACK"]:
        add_bot_message(get_tone_text(
            "'다음 문제' 버튼을 눌러주세요!",
            "'다음 문제' 버튼 눌러줘!"
        ))
    else:
        add_bot_message(get_tone_text(
            "좋은 질문이에요! 하지만 지금은 퀴즈에 집중해볼까요? 😊",
            "좋은 질문이야! 근데 지금은 퀴즈에 집중해볼까? 😊"
        ))


# 텍스트 입력 필드
user_input = st.chat_input("메시지를 입력하세요...")

if user_input:
    handle_free_input(user_input)
    st.rerun()

# 하단 네비게이션
st.markdown("""
<div class="figma-bottom-nav">
    <div class="nav-item">
        <div class="nav-icon">
            <img src="app/static/images/icon_home.png" alt="홈" style="width: 24px; height: 24px;">
        </div>
        <span class="nav-label">홈</span>
    </div>
    <div class="nav-item">
        <div class="nav-icon">
            <img src="app/static/images/icon_exhibition.png" alt="전시" style="width: 24px; height: 24px;">
        </div>
        <span class="nav-label">전시</span>
    </div>
    <div class="nav-item">
        <div class="nav-icon">
            <img src="app/static/images/icon_navigation.png" alt="AR 전시" style="width: 24px; height: 24px;">
        </div>
        <span class="nav-label">AR 전시</span>
    </div>
    <div class="nav-item">
        <div class="nav-icon">
            <img src="app/static/images/icon_website.png" alt="대표 누리집" style="width: 24px; height: 24px;">
        </div>
        <span class="nav-label">대표 누리집</span>
    </div>
    <div class="nav-item active">
        <div class="nav-icon">
            <img src="app/static/images/icon_chatbot_pressed.png" alt="챗봇" style="width: 24px; height: 24px;">
        </div>
        <span class="nav-label" style="color: #345A6A;">챗봇</span>
    </div>
</div>
""", unsafe_allow_html=True)
