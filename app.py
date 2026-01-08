"""
🏛️ 박물관 유물 안내 AI 챗봇
============================

실행: python -m streamlit run app.py
"""

import streamlit as st
import random

# 설정 파일들 import
from config.styles import generate_css, get_header_html
from config.prompts import WELCOME_MESSAGES, MESSAGES, UI_LABELS
from config.settings import APP_CONFIG, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE

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

if "language" not in st.session_state:
    st.session_state.language = DEFAULT_LANGUAGE

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
    lang = st.session_state.language
    
    st.markdown(f"## ⚙️ {UI_LABELS['settings'].get(lang, 'Settings')}")
    
    # 언어 선택
    st.markdown(f"### 🌐 {UI_LABELS['language_select'].get(lang, 'Language')}")
    
    selected_lang = st.selectbox(
        UI_LABELS['language_select'].get(lang, 'Language'),
        options=list(SUPPORTED_LANGUAGES.keys()),
        format_func=lambda x: SUPPORTED_LANGUAGES[x],
        index=list(SUPPORTED_LANGUAGES.keys()).index(st.session_state.language),
        label_visibility="collapsed"
    )
    
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.session_state.messages = [{
            "role": "assistant",
            "content": WELCOME_MESSAGES[selected_lang]
        }]
        st.rerun()
    
    st.markdown("---")
    
    # API 키 설정
    st.markdown(f"### 🔑 {UI_LABELS['api_key_label'].get(lang, 'API Key')}")
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
            st.success(MESSAGES["api_connected"].get(lang, "✅ Connected!"))
    
    if not st.session_state.api_key:
        st.info(MESSAGES["api_not_set"].get(lang, "💡 Basic features work without API key."))
    
    st.markdown("---")
    
    # 유물 목록
    st.markdown(f"### 📜 {UI_LABELS['artifact_list'].get(lang, 'Artifacts')}")
    
    for name in get_artifact_list():
        if st.button(f"🔹 {name}", key=f"side_{name}", use_container_width=True):
            st.session_state.current_artifact = ARTIFACTS[name]
            response = st.session_state.llm_service.chat(
                f"{name}에 대해 설명해줘",
                st.session_state.language,
                ARTIFACTS[name]
            )
            st.session_state.messages.append({"role": "user", "content": name})
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()


# ============================================================
# 💬 메인 채팅 영역
# ============================================================

# 현재 상태 표시
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**🌐 {SUPPORTED_LANGUAGES[st.session_state.language]}**")
with col2:
    api_status = "✅" if st.session_state.api_key else "⚠️"
    st.markdown(f"**🤖 API: {api_status}**")

st.markdown("---")

# 초기 메시지
if not st.session_state.messages:
    st.session_state.messages = [{
        "role": "assistant",
        "content": WELCOME_MESSAGES[st.session_state.language]
    }]

# 메시지 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 퀴즈 UI
if st.session_state.current_quiz:
    quiz = st.session_state.current_quiz
    
    st.markdown("---")
    st.markdown(f"### 🎯 Quiz")
    st.markdown(f"**{quiz['question']}**")
    
    cols = st.columns(2)
    for i, option in enumerate(quiz["options"]):
        col = cols[i % 2]
        with col:
            if st.button(f"{i+1}. {option}", key=f"quiz_{i}", use_container_width=True):
                lang = st.session_state.language
                
                if i == quiz["correct_index"]:
                    result = f"{MESSAGES['quiz_correct'].get(lang, '🎉 Correct!')}\n\n{quiz['explanation']}"
                else:
                    correct_answer = quiz['options'][quiz['correct_index']]
                    result = f"{MESSAGES['quiz_incorrect'].get(lang, '❌ Not quite!')}\n\n정답: **{correct_answer}**\n\n{quiz['explanation']}"
                
                st.session_state.messages.append({"role": "assistant", "content": result})
                st.session_state.current_quiz = None
                st.rerun()

# 사용자 입력
lang = st.session_state.language
user_input = st.chat_input(UI_LABELS["chat_placeholder"].get(lang, "Ask about an artifact..."))

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 퀴즈 키워드 확인
    quiz_keywords = ["퀴즈", "quiz", "测验", "クイズ"]
    
    if any(kw in user_input.lower() for kw in quiz_keywords):
        if st.session_state.current_artifact:
            quiz = st.session_state.llm_service.generate_quiz(
                st.session_state.current_artifact,
                st.session_state.language
            )
            st.session_state.current_quiz = quiz
            st.session_state.messages.append({
                "role": "assistant",
                "content": "🎯 퀴즈를 준비했습니다! 아래에서 정답을 선택하세요."
            })
        else:
            st.session_state.messages.append({
                "role": "assistant",
                "content": MESSAGES["no_artifact"].get(lang, "Please select an artifact first!")
            })
    else:
        # 유물 검색
        artifact = find_artifact(user_input)
        if artifact:
            st.session_state.current_artifact = artifact
        
        # AI 응답
        with st.spinner(MESSAGES["loading"].get(lang, "Thinking...")):
            response = st.session_state.llm_service.chat(
                user_input,
                st.session_state.language,
                st.session_state.current_artifact
            )
        
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.rerun()


# ============================================================
# 📷 이미지 업로드
# ============================================================

st.markdown("---")
st.markdown(f"### 📷 {UI_LABELS['upload_image'].get(st.session_state.language, 'Upload Image')}")

uploaded_file = st.file_uploader(
    "Upload",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)

if uploaded_file:
    from PIL import Image
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(image, use_container_width=True)
    
    with col2:
        st.info("🔍 이미지 분석 중... (데모: 랜덤 유물 선택)")
        
        # 데모: 랜덤 유물 선택 (실제로는 OCR 사용)
        random_key = random.choice(list(ARTIFACTS.keys()))
        random_artifact = ARTIFACTS[random_key]
        
        st.session_state.current_artifact = random_artifact
        
        response = st.session_state.llm_service.chat(
            f"{random_artifact['name']}에 대해 설명해줘",
            st.session_state.language,
            random_artifact
        )
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"✨ 유물을 인식했습니다: **{random_artifact['name']}**\n\n{response}"
        })
        
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
