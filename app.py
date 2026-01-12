"""
🏛️ 박물관 유물 퀴즈 챗봇
========================

실행: streamlit run app.py
"""

import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

import streamlit as st

from config.styles import generate_css, get_header_html
from config.settings import APP_CONFIG
from data.artifacts import ARTIFACTS, get_random_artifacts, generate_dynamic_quiz
from services.llm_service import LLMService


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

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False

if "llm_service" not in st.session_state:
    # 환경변수에서 API 키 로드
    api_key = os.getenv("GEMINI_API_KEY", "")
    st.session_state.llm_service = LLMService(api_key)
    if api_key:
        print(f"✅ API 키 로드됨: {api_key[:20]}...")
    else:
        print("⚠️ API 키가 없습니다")

# API 키가 있는데 client가 없으면 다시 초기화
api_key = os.getenv("GEMINI_API_KEY", "")
if api_key and not st.session_state.llm_service.client:
    st.session_state.llm_service = LLMService(api_key)
    print("🔄 LLM 서비스 재초기화")

if "user_question" not in st.session_state:
    st.session_state.user_question = ""

if "selected_ids" not in st.session_state:
    st.session_state.selected_ids = set()

if "selected_answer" not in st.session_state:
    st.session_state.selected_answer = None

if "generated_quizzes" not in st.session_state:
    st.session_state.generated_quizzes = {}

if "quiz_generating" not in st.session_state:
    st.session_state.quiz_generating = False


# ============================================================
# 🔧 유틸리티 함수
# ============================================================

def toggle_artifact_selection(artifact_id: str):
    """유물 선택 토글"""
    if artifact_id in st.session_state.selected_ids:
        st.session_state.selected_ids.remove(artifact_id)
    else:
        st.session_state.selected_ids.add(artifact_id)


def add_message(role: str, content: str):
    """채팅 히스토리에 메시지 추가"""
    st.session_state.chat_history.append({
        "role": role,
        "content": content
    })


def display_chat_history():
    """채팅 히스토리 표시"""
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"], avatar="🏛️" if msg["role"] == "assistant" else "👤"):
            st.markdown(msg["content"], unsafe_allow_html=True)


def get_encouragement_message(score: int, total: int) -> str:
    """점수에 따른 응원 메시지"""
    percentage = (score / total) * 100

    if percentage == 100:
        return "🎉 완벽해요! 당신은 진정한 문화재 박사입니다!"
    elif percentage >= 80:
        return "👏 훌륭해요! 우리 문화재에 대해 잘 알고 계시네요!"
    elif percentage >= 60:
        return "😊 좋아요! 조금만 더 공부하면 문화재 전문가가 될 수 있어요!"
    elif percentage >= 40:
        return "💪 괜찮아요! 박물관을 방문해서 직접 유물을 감상해보는 건 어떨까요?"
    else:
        return "📚 아쉽지만 괜찮아요! 이번 기회에 우리 문화재에 관심을 가져보세요!"


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
# ⚙️ 사이드바: API 키 설정
# ============================================================

with st.sidebar:
    st.markdown("## 🏛️ 박물관 퀴즈")
    st.markdown("---")

    st.info("🤖 AI 맞춤 해설이 활성화되어 있습니다.")

    st.markdown("---")
    st.markdown("### 📊 현재 진행 상황")

    if st.session_state.stage == "select":
        st.markdown("📝 유물 선택 중...")
    elif st.session_state.stage == "quiz":
        total = len(st.session_state.selected_artifacts)
        current = st.session_state.current_quiz_index
        if total > 0:
            st.markdown(f"🎯 퀴즈 진행 중: {current + 1} / {total}")
            st.progress(min((current + 1) / total, 1.0))
        else:
            st.markdown("🎯 퀴즈 준비 중...")
    elif st.session_state.stage == "result":
        st.markdown(f"🏆 완료! 점수: {st.session_state.score}/{len(st.session_state.selected_artifacts)}")


# ============================================================
# 💬 채팅 컨테이너
# ============================================================

chat_container = st.container()

with chat_container:
    # 기존 채팅 히스토리 표시
    display_chat_history()

    # ============================================================
    # 📝 Stage 1: 유물 선택
    # ============================================================

    if st.session_state.stage == "select":
        # 초기 인사 메시지 (한 번만 추가)
        if not st.session_state.chat_history:
            with st.chat_message("assistant", avatar="🏛️"):
                st.markdown("""
안녕하세요! 박물관 유물 퀴즈에 오신 것을 환영합니다! 🏛️

아래에서 **퀴즈를 풀고 싶은 유물을 선택**해주세요.
**최소 3개 ~ 최대 10개**를 선택할 수 있습니다.
                """)

        st.markdown("---")
        st.markdown("### 📜 유물 선택 (클릭하여 선택/해제)")

        # 카드 리스트 형태로 유물 표시
        for i, artifact in enumerate(st.session_state.available_artifacts):
            is_selected = artifact['id'] in st.session_state.selected_ids

            # 카드 스타일 컨테이너
            card_bg = "rgba(59, 130, 246, 0.1)" if is_selected else "rgba(248, 250, 252, 0.95)"
            card_border = "2px solid #3B82F6" if is_selected else "1px solid #E2E8F0"

            col1, col2, col3 = st.columns([1, 4, 1])

            with col1:
                # 왼쪽: 이미지 영역
                image_url = artifact.get('image_url', '')
                if image_url:
                    try:
                        st.image(image_url, width=70)
                    except Exception:
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            border-radius: 8px;
                            padding: 15px;
                            text-align: center;
                            color: white;
                            font-size: 24px;
                            height: 70px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        ">🏛️</div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        border-radius: 8px;
                        padding: 15px;
                        text-align: center;
                        color: white;
                        font-size: 24px;
                        height: 70px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    ">🏛️</div>
                    """, unsafe_allow_html=True)

            with col2:
                # 가운데: 유물 정보
                st.markdown(f"""
                <div style="padding: 5px 0;">
                    <div style="font-weight: 600; font-size: 16px; color: #1E293B;">
                        {'✅ ' if is_selected else ''}{artifact['name']}
                    </div>
                    <div style="font-size: 13px; color: #64748B; margin-top: 4px;">
                        📍 {artifact.get('gallery', '국립중앙박물관')}
                    </div>
                    <div style="font-size: 12px; color: #94A3B8; margin-top: 2px;">
                        {artifact.get('designation', '')} · {artifact['period']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                # 오른쪽: 선택 버튼
                if st.button(
                    "✓" if is_selected else "○",
                    key=f"select_{artifact['id']}",
                    type="primary" if is_selected else "secondary"
                ):
                    toggle_artifact_selection(artifact['id'])
                    st.rerun()

            # 구분선
            st.markdown("<hr style='margin: 8px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

        # 선택된 유물 리스트 생성
        selected = [a for a in st.session_state.available_artifacts if a['id'] in st.session_state.selected_ids]

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
            # 퀴즈 생성 중이면 버튼 비활성화
            is_generating = st.session_state.quiz_generating
            button_disabled = (select_count < 3 or select_count > 10 or is_generating)
            button_label = "⏳ 퀴즈 생성 중..." if is_generating else "🎯 퀴즈 시작!"

            if st.button(button_label, use_container_width=True, disabled=button_disabled):
                # 중복 클릭 방지
                st.session_state.quiz_generating = True

                # 선택된 유물 저장 (먼저!)
                st.session_state.selected_artifacts = selected

                # 선택 메시지 추가
                artifact_names = ", ".join([a["name"] for a in selected])
                add_message("user", f"**{select_count}개의 유물을 선택했습니다:**\n{artifact_names}")
                add_message("assistant", f"좋아요! {select_count}개의 유물에 대한 퀴즈를 생성할게요. 잠시만 기다려주세요... ⏳")

                st.rerun()  # 로딩 상태 표시를 위해 먼저 rerun

        # 퀴즈 생성 처리 (버튼 클릭 후 별도로 처리)
        if st.session_state.quiz_generating and st.session_state.stage == "select":
            with st.spinner("🤖 AI가 퀴즈를 생성하고 있어요..."):
                llm = st.session_state.llm_service
                generated_quizzes = {}

                for artifact in st.session_state.selected_artifacts:
                    quiz = generate_dynamic_quiz(artifact, llm)
                    generated_quizzes[artifact['id']] = quiz

                st.session_state.generated_quizzes = generated_quizzes
                st.session_state.current_quiz_index = 0
                st.session_state.score = 0
                st.session_state.answers = []
                st.session_state.stage = "quiz"
                st.session_state.quiz_started = True
                st.session_state.quiz_generating = False  # 생성 완료

                # 시작 메시지 업데이트
                st.session_state.chat_history[-1]["content"] = "좋아요! 퀴즈를 시작할게요. 준비되셨나요? 🎯"
                st.rerun()


    # ============================================================
    # 🎯 Stage 2: 퀴즈 진행
    # ============================================================

    elif st.session_state.stage == "quiz":
        total = len(st.session_state.selected_artifacts)
        current = st.session_state.current_quiz_index

        if current < total:
            artifact = st.session_state.selected_artifacts[current]
            # 동적 생성된 퀴즈 사용 (없으면 기존 퀴즈)
            quiz = st.session_state.get("generated_quizzes", {}).get(
                artifact['id'], artifact.get("quiz", {})
            )

            # 현재 문제를 채팅 형식으로 표시
            with st.chat_message("assistant", avatar="🏛️"):
                st.markdown(f"""
**문제 {current + 1} / {total}**

---

🏛️ **{artifact['name']}**
<span style="color: #888; font-size: 14px;">{artifact['period']} | {artifact['designation']}</span>

---

### ❓ {quiz['question']}
                """, unsafe_allow_html=True)

            # 진행 상황 바
            st.progress((current + 1) / total)

            # 주관식 입력 (궁금한 점)
            st.markdown("---")
            st.markdown("### 💬 궁금한 점이 있나요? (선택사항)")
            user_question = st.text_area(
                "이 유물에 대해 궁금한 점을 자유롭게 작성해주세요.",
                placeholder="예: 이 유물은 어떻게 발견되었나요? / 비슷한 유물이 또 있나요? / 실제로 어디서 볼 수 있나요?",
                key=f"question_{current}",
                height=80,
                label_visibility="collapsed"
            )

            st.markdown("---")
            st.markdown("### 정답을 선택하세요:")

            # 버튼 스타일 선택지 표시
            for i, option in enumerate(quiz["options"]):
                is_selected = st.session_state.selected_answer == i

                # 선택된 상태 표시 (체크 아이콘 + primary 스타일)
                btn_label = f"{'✓ ' if is_selected else ''}{i + 1}. {option}"
                btn_type = "primary" if is_selected else "secondary"

                if st.button(
                    btn_label,
                    key=f"option_{current}_{i}",
                    use_container_width=True,
                    type=btn_type
                ):
                    st.session_state.selected_answer = i
                    st.rerun()

            # 제출 버튼
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit_disabled = st.session_state.selected_answer is None
                if st.button("✅ 정답 제출", key=f"submit_{current}", use_container_width=True, disabled=submit_disabled):
                    # 선택한 답 인덱스 추출
                    selected_index = st.session_state.selected_answer
                    selected_answer = quiz["options"][selected_index]

                    # 정답 체크
                    is_correct = (selected_index == quiz["answer"])

                    if is_correct:
                        st.session_state.score += 1

                    # 사용자 답변 메시지 추가
                    user_msg = f"**{selected_index + 1}번:** {selected_answer}"
                    if user_question and user_question.strip():
                        user_msg += f"\n\n💬 **궁금한 점:** {user_question}"
                    add_message("user", user_msg)

                    # 맞춤 해설 생성 (LLM 사용)
                    enhanced_explanation = st.session_state.llm_service.generate_enhanced_explanation(
                        artifact=artifact,
                        quiz=quiz,
                        is_correct=is_correct,
                        user_question=user_question
                    )

                    # 결과 메시지 추가
                    if is_correct:
                        result_msg = f"""
✅ **정답입니다!**

{enhanced_explanation}
                        """
                    else:
                        result_msg = f"""
❌ **아쉽네요!**

정답은 **{quiz['options'][quiz['answer']]}** 입니다.

{enhanced_explanation}
                        """

                    add_message("assistant", result_msg)

                    st.session_state.answers.append({
                        "artifact": artifact["name"],
                        "question": quiz["question"],
                        "user_answer": selected_answer,
                        "correct_answer": quiz["options"][quiz["answer"]],
                        "is_correct": is_correct,
                        "user_question": user_question,
                        "explanation": enhanced_explanation
                    })

                    st.session_state.current_quiz_index += 1
                    st.session_state.selected_answer = None  # 다음 문제를 위해 선택 초기화
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

        # 결과 메시지 (한 번만 추가)
        result_already_shown = any("🏆 퀴즈 완료!" in msg.get("content", "") for msg in st.session_state.chat_history)

        if not result_already_shown:
            encouragement = get_encouragement_message(score, total)

            result_content = f"""
### 🏆 퀴즈 완료!

---

<div style="text-align: center; padding: 20px; background: rgba(59, 130, 246, 0.15); border-radius: 15px; margin: 15px 0;">
    <h1 style="font-size: 42px; margin: 0; color: #3b82f6;">{score} / {total}</h1>
    <p style="font-size: 16px; color: #888;">{total}개 중 {score}개 정답!</p>
</div>

{encouragement}

---

모든 문제를 확인하셨다면 **'나가기'**라고 입력해주세요.
또는 아래 버튼으로 다시 도전할 수 있어요!
            """
            add_message("assistant", result_content)
            st.rerun()

        # 상세 결과 보기
        with st.expander("📋 상세 결과 보기"):
            for i, answer in enumerate(st.session_state.answers):
                icon = "✅" if answer["is_correct"] else "❌"
                user_q = answer.get("user_question", "")
                user_q_display = f"\n- 💬 내 질문: {user_q}" if user_q else ""

                st.markdown(f"""
**{i + 1}. {answer['artifact']}** {icon}

- 문제: {answer['question']}
- 내 답: {answer['user_answer']}
- 정답: {answer['correct_answer']}{user_q_display}
- 해설: {answer['explanation']}

---
                """)

        # 다시 하기 버튼
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 다시 도전하기", use_container_width=True):
                # 새 게임 시작 메시지
                add_message("user", "다시 도전할게요!")
                add_message("assistant", "좋아요! 새로운 유물들로 다시 시작해볼까요? 🏛️")

                st.session_state.stage = "select"
                st.session_state.available_artifacts = get_random_artifacts(10)
                st.session_state.selected_artifacts = []
                st.session_state.selected_ids = set()
                st.session_state.current_quiz_index = 0
                st.session_state.score = 0
                st.session_state.answers = []
                st.session_state.quiz_started = False
                st.rerun()


# ============================================================
# 💬 채팅 입력
# ============================================================

user_input = st.chat_input("메시지를 입력하세요...")

if user_input:
    add_message("user", user_input)

    if st.session_state.stage == "result":
        if "나가기" in user_input:
            add_message("assistant", "👋 감사합니다! 박물관 유물 퀴즈를 즐겨주셔서 감사해요. 다음에 또 만나요!")
            st.balloons()
        else:
            add_message("assistant", "🏛️ 퀴즈가 종료되었습니다. **'나가기'**를 입력하거나 **'다시 도전하기'** 버튼을 눌러주세요.")
    else:
        add_message("assistant", "🏛️ 먼저 유물을 선택하고 퀴즈를 진행해주세요!")

    st.rerun()


# ============================================================
# 🔻 푸터
# ============================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(59, 130, 246, 0.6); font-size: 12px; padding: 20px 0;">
    🏛️ Museum Artifact Quiz | Powered by Streamlit
</div>
""", unsafe_allow_html=True)
