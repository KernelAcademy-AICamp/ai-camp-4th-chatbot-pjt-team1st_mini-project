"""
🏛️ 박물관 유물 안내 AI 챗봇
============================

실행: python -m streamlit run app.py
"""

import streamlit as st

# 설정 파일들 import
from config.styles import generate_css, get_header_html
from config.prompts import WELCOME_MESSAGE, MESSAGES, UI_LABELS
from config.settings import APP_CONFIG

# 데이터 import
from data.artifacts import ARTIFACTS, find_artifact, get_artifact_list

# 서비스 import
from services.llm_service import LLMService


# ============================================================
# 📱 페이지 설정
# ============================================================

st.set_page_config(
    page_title=f"{APP_CONFIG['icon']} {APP_CONFIG['title']}",
    page_icon=APP_CONFIG["icon"],
    layout=APP_CONFIG["layout"]
)


# ============================================================
# 🎨 스타일 적용 (styles.py에서 가져옴)
# ============================================================

st.markdown(generate_css(), unsafe_allow_html=True)


# ============================================================
# 💾 세션 상태 초기화
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_artifact" not in st.session_state:
    st.session_state.current_artifact = None

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "llm_service" not in st.session_state:
    st.session_state.llm_service = LLMService()

if "current_quiz" not in st.session_state:
    st.session_state.current_quiz = None


# ============================================================
# 🖥️ 헤더
# ============================================================

st.markdown(
    get_header_html(
        APP_CONFIG["title"], 
        APP_CONFIG["title_en"]
    ), 
    unsafe_allow_html=True
)


# ============================================================
# ⚙️ 사이드바: 설정
# ============================================================

with st.sidebar:
    st.markdown(f"## ⚙️ {UI_LABELS['settings']}")

    # API 키 설정
    st.markdown(f"### 🔑 {UI_LABELS['api_key_label']}")
    api_key = st.text_input(
        "API Key",
        type="password",
        value=st.session_state.api_key,
        placeholder="sk-ant-...",
        label_visibility="collapsed"
    )

    if api_key != st.session_state.api_key:
        st.session_state.api_key = api_key
        st.session_state.llm_service = LLMService(api_key)
        if api_key:
            st.success(MESSAGES["api_connected"])

    if not st.session_state.api_key:
        st.info(MESSAGES["api_not_set"])

    st.markdown("---")

    # 유물 목록
    st.markdown(f"### 📜 {UI_LABELS['artifact_list']}")

    for name in get_artifact_list():
        if st.button(f"🔹 {name}", key=f"side_{name}", use_container_width=True):
            st.session_state.current_artifact = ARTIFACTS[name]
            response = st.session_state.llm_service.chat(
                f"{name}에 대해 설명해줘",
                ARTIFACTS[name]
            )
            st.session_state.messages.append({"role": "user", "content": name})
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()


# ============================================================
# 💬 메인 채팅 영역
# ============================================================

# 현재 상태 표시
api_status = "✅ 연결됨" if st.session_state.api_key else "⚠️ 미설정"
st.markdown(f"**🤖 API 상태: {api_status}**")

st.markdown("---")

# 초기 메시지
if not st.session_state.messages:
    st.session_state.messages = [{
        "role": "assistant",
        "content": WELCOME_MESSAGE
    }]

# 메시지 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 퀴즈 UI
if st.session_state.current_quiz:
    quiz = st.session_state.current_quiz

    st.markdown("---")
    st.markdown("### 🎯 퀴즈")
    st.markdown(f"**{quiz['question']}**")

    cols = st.columns(2)
    for i, option in enumerate(quiz["options"]):
        col = cols[i % 2]
        with col:
            if st.button(f"{i+1}. {option}", key=f"quiz_{i}", use_container_width=True):
                if i == quiz["correct_index"]:
                    result = f"{MESSAGES['quiz_correct']}\n\n{quiz['explanation']}"
                else:
                    correct_answer = quiz['options'][quiz['correct_index']]
                    result = f"{MESSAGES['quiz_incorrect']}\n\n정답: **{correct_answer}**\n\n{quiz['explanation']}"

                st.session_state.messages.append({"role": "assistant", "content": result})
                st.session_state.current_quiz = None
                st.rerun()

# 사용자 입력
user_input = st.chat_input(UI_LABELS["chat_placeholder"])

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 퀴즈 키워드 확인
    if "퀴즈" in user_input:
        if st.session_state.current_artifact:
            quiz = st.session_state.llm_service.generate_quiz(
                st.session_state.current_artifact
            )
            st.session_state.current_quiz = quiz
            st.session_state.messages.append({
                "role": "assistant",
                "content": "🎯 퀴즈를 준비했습니다! 아래에서 정답을 선택하세요."
            })
        else:
            st.session_state.messages.append({
                "role": "assistant",
                "content": MESSAGES["no_artifact"]
            })
    else:
        # 유물 검색
        artifact = find_artifact(user_input)
        if artifact:
            st.session_state.current_artifact = artifact

        # AI 응답
        with st.spinner(MESSAGES["loading"]):
            response = st.session_state.llm_service.chat(
                user_input,
                st.session_state.current_artifact
            )

        st.session_state.messages.append({"role": "assistant", "content": response})

    st.rerun()


# ============================================================
# 🔻 푸터
# ============================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(212, 175, 55, 0.5); font-size: 12px; padding: 20px 0;">
    🏛️ Museum AI Guide | Powered by Claude API
</div>
""", unsafe_allow_html=True)
