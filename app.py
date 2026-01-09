"""
🏛️ 박물관 유물 퀴즈
====================

실행: streamlit run app.py
"""

import streamlit as st

from config.styles import generate_css, get_header_html
from config.settings import APP_CONFIG
from data.artifacts import ARTIFACTS, get_random_artifacts


# ============================================================
# 📱 페이지 설정
# ============================================================

st.set_page_config(
    page_title=f"{APP_CONFIG['icon']} {APP_CONFIG['title']}",
    page_icon=APP_CONFIG["icon"],
    layout=APP_CONFIG["layout"]
)

st.markdown(generate_css(), unsafe_allow_html=True)


# ============================================================
# 💾 세션 상태 초기화
# ============================================================

if "stage" not in st.session_state:
    st.session_state.stage = "select"  # select, quiz, result

if "available_artifacts" not in st.session_state:
    st.session_state.available_artifacts = get_random_artifacts(10)

if "selected_artifacts" not in st.session_state:
    st.session_state.selected_artifacts = []

if "current_quiz_index" not in st.session_state:
    st.session_state.current_quiz_index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "answers" not in st.session_state:
    st.session_state.answers = []


# ============================================================
# 🖥️ 헤더
# ============================================================

st.markdown(
    get_header_html(
        "박물관 유물 퀴즈",
        "Museum Artifact Quiz"
    ),
    unsafe_allow_html=True
)


# ============================================================
# 📝 Stage 1: 유물 선택
# ============================================================

if st.session_state.stage == "select":
    st.markdown("## 📜 퀴즈를 풀고 싶은 유물을 선택하세요")
    st.markdown("**최소 3개 ~ 최대 10개**를 선택할 수 있습니다.")
    st.markdown("---")

    # 체크박스로 유물 선택
    selected = []

    cols = st.columns(2)
    for i, artifact in enumerate(st.session_state.available_artifacts):
        col = cols[i % 2]
        with col:
            if st.checkbox(
                f"**{artifact['name']}**\n\n{artifact['period']} | {artifact['designation']}",
                key=f"select_{artifact['id']}"
            ):
                selected.append(artifact)

    st.markdown("---")

    # 선택 개수 표시
    select_count = len(selected)

    if select_count < 3:
        st.warning(f"⚠️ {select_count}개 선택됨 (최소 3개 필요)")
    elif select_count > 10:
        st.error(f"❌ {select_count}개 선택됨 (최대 10개까지)")
    else:
        st.success(f"✅ {select_count}개 선택됨")

    # 시작 버튼
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 퀴즈 시작!", use_container_width=True, disabled=(select_count < 3 or select_count > 10)):
            st.session_state.selected_artifacts = selected
            st.session_state.current_quiz_index = 0
            st.session_state.score = 0
            st.session_state.answers = []
            st.session_state.stage = "quiz"
            st.rerun()


# ============================================================
# 🎯 Stage 2: 퀴즈 진행
# ============================================================

elif st.session_state.stage == "quiz":
    total = len(st.session_state.selected_artifacts)
    current = st.session_state.current_quiz_index

    if current < total:
        artifact = st.session_state.selected_artifacts[current]
        quiz = artifact["quiz"]

        # 진행 상황 표시
        st.markdown(f"### 문제 {current + 1} / {total}")
        st.progress((current + 1) / total)

        # 유물 정보
        st.markdown(f"""
        <div style="background: rgba(212, 175, 55, 0.1); padding: 15px; border-radius: 10px; margin: 10px 0;">
            <strong>🏛️ {artifact['name']}</strong><br>
            <span style="color: #888;">{artifact['period']} | {artifact['designation']}</span>
        </div>
        """, unsafe_allow_html=True)

        # 질문
        st.markdown(f"### ❓ {quiz['question']}")
        st.markdown("---")

        # 선택지 버튼
        for i, option in enumerate(quiz["options"]):
            if st.button(f"{i + 1}. {option}", key=f"option_{current}_{i}", use_container_width=True):
                # 정답 체크
                is_correct = (i == quiz["answer"])

                if is_correct:
                    st.session_state.score += 1

                st.session_state.answers.append({
                    "artifact": artifact["name"],
                    "question": quiz["question"],
                    "user_answer": option,
                    "correct_answer": quiz["options"][quiz["answer"]],
                    "is_correct": is_correct,
                    "explanation": quiz["explanation"]
                })

                st.session_state.current_quiz_index += 1
                st.rerun()

    else:
        # 모든 퀴즈 완료 -> 결과 화면으로
        st.session_state.stage = "result"
        st.rerun()


# ============================================================
# 🏆 Stage 3: 결과 화면
# ============================================================

elif st.session_state.stage == "result":
    total = len(st.session_state.selected_artifacts)
    score = st.session_state.score

    st.markdown("## 🏆 퀴즈 결과")
    st.markdown("---")

    # 점수 표시
    st.markdown(f"""
    <div style="text-align: center; padding: 30px; background: rgba(212, 175, 55, 0.15); border-radius: 15px; margin: 20px 0;">
        <h1 style="font-size: 48px; margin: 0;">{score} / {total}</h1>
        <p style="font-size: 18px; color: #888;">{total}개 중 {score}개의 정답을 맞췄습니다!</p>
    </div>
    """, unsafe_allow_html=True)

    # 응원 문구
    percentage = (score / total) * 100

    if percentage == 100:
        message = "🎉 완벽해요! 당신은 진정한 문화재 박사입니다!"
    elif percentage >= 80:
        message = "👏 훌륭해요! 우리 문화재에 대해 잘 알고 계시네요!"
    elif percentage >= 60:
        message = "😊 좋아요! 조금만 더 공부하면 문화재 전문가가 될 수 있어요!"
    elif percentage >= 40:
        message = "💪 괜찮아요! 박물관을 방문해서 직접 유물을 감상해보는 건 어떨까요?"
    else:
        message = "📚 아쉽지만 괜찮아요! 이번 기회에 우리 문화재에 관심을 가져보세요!"

    st.markdown(f"""
    <div style="text-align: center; padding: 20px; font-size: 20px;">
        {message}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 상세 결과
    with st.expander("📋 상세 결과 보기"):
        for i, answer in enumerate(st.session_state.answers):
            icon = "✅" if answer["is_correct"] else "❌"
            st.markdown(f"""
            **{i + 1}. {answer['artifact']}**
            - 문제: {answer['question']}
            - 내 답: {answer['user_answer']} {icon}
            - 정답: {answer['correct_answer']}
            - 해설: {answer['explanation']}

            ---
            """)

    st.markdown("---")

    # 마무리 메시지
    st.info("🏛️ 모두 알아봤다면 **'나가기'**라고 응답해주세요.")

    # 다시 하기 버튼
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 다시 도전하기", use_container_width=True):
            st.session_state.stage = "select"
            st.session_state.available_artifacts = get_random_artifacts(10)
            st.session_state.selected_artifacts = []
            st.session_state.current_quiz_index = 0
            st.session_state.score = 0
            st.session_state.answers = []
            st.rerun()

    # 나가기 입력
    user_input = st.chat_input("메시지를 입력하세요...")
    if user_input:
        if "나가기" in user_input:
            st.balloons()
            st.success("👋 감사합니다! 다음에 또 만나요!")
        else:
            st.info("🏛️ 퀴즈가 종료되었습니다. '나가기'를 입력하거나 '다시 도전하기' 버튼을 눌러주세요.")


# ============================================================
# 🔻 푸터
# ============================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(212, 175, 55, 0.5); font-size: 12px; padding: 20px 0;">
    🏛️ Museum Artifact Quiz | Powered by Streamlit
</div>
""", unsafe_allow_html=True)
