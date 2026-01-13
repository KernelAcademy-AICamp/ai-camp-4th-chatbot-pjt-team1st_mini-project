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
from data.artifacts import ARTIFACTS, find_artifact, get_artifact_list, get_artifact_by_id

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
        max-width: 393px !important;
        min-width: 393px !important;
        width: 393px !important;
    }
    
    /* Streamlit 기본 패딩/마진 완전 제거 */
    .main {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    .main .block-container,
    .block-container,
    [data-testid="stAppViewBlockContainer"],
    [data-testid="stVerticalBlock"],
    [data-testid="stVerticalBlockBorderWrapper"],
    .stMarkdown,
    .element-container,
    section.main > div {
        padding: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        margin: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        max-width: 393px !important;
        min-width: 393px !important;
        width: 393px !important;
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
        margin-left: 0 !important;
        margin-right: 0 !important;
        padding: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        gap: 0 !important;
    }
    
    div[data-testid="stVerticalBlockBorderWrapper"] {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Streamlit 내부 컨테이너 - 모든 padding/margin 제거 */
    div[data-testid="stAppViewContainer"],
    div[data-testid="stMain"],
    section.main,
    section.main > div,
    section.main > div > div,
    section.main > div > div > div {
        padding: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        margin: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
    }
    
    /* 상단 여백 완전 제거 */
    .stApp > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* iframe 내부 컨테이너도 */
    iframe {
        margin: 0 !important;
        padding: 0 !important;
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
    
    /* ===== Type C: 퀴즈 생성 중 스타일 ===== */
    .quiz-generation-status {
        background: #e7eef7;
        padding: 15px;
        border-radius: 0 10px 10px 10px;
        max-width: 343px;
        margin-left: 34px;
        display: flex;
        flex-direction: column;
        gap: 16px;
    }
    
    .loading-header {
        display: flex;
        align-items: center;
        gap: 8.444px;
    }
    
    .loading-spinner {
        width: 36.751px;
        height: 36.751px;
        background-image: url('app/static/images/icon_loading.svg');
        background-size: contain;
        background-repeat: no-repeat;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .loading-text {
        font-family: 'Pretendard', sans-serif;
        font-size: 16px;
        font-weight: 600;
        color: #333333;
        line-height: 1.4;
        margin: 0;
    }
    
    .progress-section {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    
    .progress-bar {
        background: #246beb;
        height: 8px;
        border-radius: 1000px;
        width: 100%;
    }
    
    .progress-text {
        font-family: 'Pretendard', sans-serif;
        font-size: 13px;
        font-weight: 400;
        color: #7a7a7a;
        line-height: 1.4;
        margin: 0;
    }
    
    .generation-steps {
        display: flex;
        flex-direction: column;
        gap: 8px;
        padding-top: 8px;
    }
    
    .step-item {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .step-dot {
        width: 8px;
        height: 8px;
        background: #246beb;
        border-radius: 50%;
        flex-shrink: 0;
    }
    
    .step-item p {
        font-family: 'Pretendard', sans-serif;
        font-size: 14px;
        font-weight: 400;
        color: #333333;
        line-height: 1.4;
        margin: 0;
    }
    
    /* 상태별 스타일 */
    .step-item.active .step-dot {
        background: #246beb;
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    .step-item.active p {
        color: #246beb;
        font-weight: 500;
    }
    
    .step-item.completed .step-dot {
        background: #4caf50;
    }
    
    .step-item.completed p {
        color: #4caf50;
    }
    
    .step-item:not(.active):not(.completed) .step-dot {
        background: #cccccc;
    }
    
    .step-item:not(.active):not(.completed) p {
        color: #999999;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Type C_1 버튼 래퍼 */
    .type-c-1-button-wrapper {
        margin-top: 13px;
        margin-left: 34px;
    }
    
    /* Type C_1 Style 2 버튼 */
    .type-c-1-button.style2-button {
        background: #246beb !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 10px 12px 10px !important;
        height: auto !important;
        font-family: 'Pretendard', sans-serif !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        letter-spacing: 0.32px !important;
        line-height: 1.3 !important;
        box-shadow: none !important;
        cursor: pointer;
        transition: background 0.2s;
    }
    
    .type-c-1-button.style2-button:hover {
        background: #1a5ad4 !important;
    }
    
    /* ===== Type C_2: 퀴즈 생성 완료 스타일 ===== */
    .quiz-completion-status {
        background: #e7eef7;
        padding: 15px;
        border-radius: 0 10px 10px 10px;
        max-width: 343px;
        margin-left: 34px;
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    
    .completion-header {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .completion-icon {
        width: 24px;
        height: 24px;
    }
    
    .completion-text {
        font-family: 'Pretendard', sans-serif;
        font-size: 16px;
        font-weight: 600;
        color: #333333;
        line-height: 1.4;
        margin: 0;
    }
    
    .quiz-info-card {
        background: #ffffff;
        border-radius: 10px;
        padding: 16px;
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    
    .quiz-info-row {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .quiz-info-icon {
        width: 16px;
        height: 16px;
    }
    
    .quiz-info-title {
        font-family: 'Pretendard', sans-serif;
        font-size: 14px;
        font-weight: 600;
        color: #333333;
        line-height: 1.4;
        margin: 0;
    }
    
    .quiz-info-subtitle {
        font-family: 'Pretendard', sans-serif;
        font-size: 13px;
        font-weight: 400;
        color: #7a7a7a;
        line-height: 1.4;
        margin: 0;
        text-align: center;
        padding: 0 24px;
    }
    
    .quiz-start-button-wrapper {
        width: 100%;
    }
    
    .quiz-start-button {
        background: #246beb;
        color: #ffffff;
        border: none;
        border-radius: 10px;
        padding: 12px 0;
        width: 100%;
        font-family: 'Pretendard', sans-serif;
        font-size: 16px;
        font-weight: 500;
        cursor: pointer;
        transition: background 0.2s;
    }
    
    .quiz-start-button:hover {
        background: #1a5ad4;
    }
    
    /* ===== Type D: 퀴즈 문제 스타일 ===== */
    .quiz-question-content {
        background: #e7eef7;
        padding: 15px;
        border-radius: 0 10px 10px 10px;
        max-width: 343px;
        margin-left: 34px;
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    
    .artifact-info-card {
        background: #ffffff;
        border: 1px solid #dddddd;
        border-radius: 8px;
        padding: 1px;
        display: flex;
        gap: 12px;
        align-items: flex-start;
    }
    
    .artifact-image {
        width: 80px;
        height: 80px;
        border-radius: 8px;
        object-fit: cover;
        flex-shrink: 0;
    }
    
    .artifact-info {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 3px;
        justify-content: center;
        height: 80px;
    }
    
    .artifact-title {
        font-family: 'Pretendard', sans-serif;
        font-size: 14px;
        font-weight: 700;
        color: #161617;
        line-height: 1.3;
        margin: 0;
    }
    
    .artifact-period {
        font-family: 'Pretendard', sans-serif;
        font-size: 12px;
        font-weight: 400;
        color: #7a7a7a;
        line-height: 1.3;
        margin: 0;
    }
    
    .quiz-choices {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    
    .quiz-choice-item {
        background: #ffffff;
        border-radius: 8px;
        height: 44px;
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 0 15px;
        cursor: pointer;
        transition: background 0.2s;
    }
    
    .quiz-choice-item:hover {
        background: #f5f5f5;
    }
    
    .quiz-choice-radio {
        width: 20px;
        height: 20px;
        border: 2px solid #d1d5db;
        border-radius: 50%;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }
    
    .quiz-choice-radio.selected {
        border-color: #246beb;
    }
    
    .quiz-choice-radio.selected::after {
        content: '';
        width: 10px;
        height: 10px;
        background: #246beb;
        border-radius: 50%;
    }
    
    .quiz-choice-text {
        font-family: 'Pretendard', sans-serif;
        font-size: 13px;
        font-weight: 400;
        color: #333333;
        line-height: 1.4;
        margin: 0;
        flex: 1;
    }
    
    .quiz-submit-button-wrapper {
        margin-top: 12px;
    }
    
    .quiz-submit-button {
        background: #246beb;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 12px 0;
        width: 100%;
        font-family: 'Pretendard', sans-serif;
        font-size: 16px;
        font-weight: 500;
        letter-spacing: 0.32px;
        line-height: 1.3;
        cursor: pointer;
        transition: background 0.2s;
    }
    
    .quiz-submit-button:hover {
        background: #1a5ad4;
    }
    
    /* ===== Type E_1/E_2: 퀴즈 피드백 스타일 ===== */
    .quiz-feedback-bubble {
        background: #e7eef7;
        padding: 15px;
        border-radius: 0 10px 10px 10px;
        max-width: 343px;
        margin-left: 34px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    
    .feedback-title {
        font-family: 'Pretendard', sans-serif;
        font-size: 16px;
        font-weight: 700;
        color: #333333;
        line-height: 1.4;
        margin: 0;
    }
    
    .feedback-explanation {
        font-family: 'Pretendard', sans-serif;
        font-size: 16px;
        font-weight: 400;
        color: #333333;
        line-height: 1.4;
        margin: 0;
    }
    
    /* ===== Type F_1/F_2: 마지막 퀴즈 피드백 스타일 ===== */
    /* Type E와 동일한 스타일 사용, 버튼만 추가 */
    .quiz-final-button-wrapper {
        margin-top: 15px; /* 버블과 버튼 사이 간격 */
        margin-left: 34px; /* 버블과 정렬 */
    }
    
    /* ===== Type G: 퀴즈 결과 스타일 ===== */
    .quiz-result-container {
        background: #e7eef7;
        padding: 15px;
        border-radius: 0 10px 10px 10px;
        max-width: 343px;
        margin-left: 34px;
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    
    .quiz-result-header {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .quiz-result-trophy {
        width: 24px;
        height: 24px;
        object-fit: contain;
    }
    
    .quiz-result-title {
        font-family: 'Pretendard', sans-serif;
        font-size: 16px;
        font-weight: 600; /* SemiBold */
        color: #333333;
        line-height: 1.4;
        margin: 0;
    }
    
    .quiz-result-card {
        background: #ffffff;
        border-radius: 10px;
        padding: 16px;
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    
    .quiz-result-score-row {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .quiz-result-icon {
        width: 16px;
        height: 16px;
        object-fit: contain;
    }
    
    .quiz-result-score {
        font-family: 'Pretendard', sans-serif;
        font-size: 14px;
        font-weight: 600; /* SemiBold */
        color: #333333;
        line-height: 1.4;
        margin: 0;
    }
    
    .quiz-result-encouragement {
        font-family: 'Pretendard', sans-serif;
        font-size: 13px;
        font-weight: 400;
        color: #7a7a7a;
        line-height: 1.4;
        margin: 0;
        text-align: center;
        padding: 0 24px;
    }
    
    .quiz-result-button-wrapper {
        width: 100%;
    }
    
    .quiz-result-button {
        background: #246beb;
        color: #ffffff;
        border: none;
        border-radius: 10px;
        padding: 12px 0;
        width: 100%;
        font-family: 'Pretendard', sans-serif;
        font-size: 16px;
        font-weight: 500;
        cursor: pointer;
    }
    
    .quiz-result-button:hover {
        background: #1a5ad4;
    }
    
    /* ===== Type B: 투어 선택 카드 ===== */
    .tour-selection-card {
        background: #ffffff;
        border: 2px solid #f3f3f3;
        border-radius: 12px;
        width: 343px;
        height: 175px;
        margin-left: 34px;
        margin-top: 13px;
        padding: 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
    }
    
    .tour-card-content {
        width: 314px;
        display: flex;
        flex-direction: column;
        gap: 16px;
        align-items: center;
    }
    
    .tour-card-header {
        display: flex;
        flex-direction: column;
        gap: 4px;
        align-items: flex-start;
        width: 264px;
    }
    
    .tour-card-title {
        font-family: 'Pretendard', sans-serif;
        font-size: 15px;
        font-weight: 700; /* Bold */
        color: #161617;
        line-height: 1.4;
        margin: 0;
    }
    
    .tour-card-subtitle {
        font-family: 'Pretendard', sans-serif;
        font-size: 15px;
        font-weight: 400;
        color: #b1b2b7;
        line-height: 1.4;
        margin: 0;
        text-align: center;
    }
    
    .tour-card-button-wrapper {
        width: 313px;
    }
    
    .tour-card-button {
        background: #246beb;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 10px 10px 12px 10px;
        width: 100%;
        font-family: 'Pretendard', sans-serif;
        font-size: 16px;
        font-weight: 500;
        letter-spacing: 0.32px;
        line-height: 1.3;
        cursor: pointer;
    }
    
    .tour-card-button:hover {
        background: #1a5ad4;
    }
    
    .tour-card-link {
        display: flex;
        align-items: center;
        gap: 8px;
        font-family: 'Pretendard', sans-serif;
        font-size: 15px;
        font-weight: 400;
        color: #4b4b4b;
        line-height: 1.3;
        cursor: pointer;
        text-decoration: none;
    }
    
    .tour-card-link-icon {
        width: 6px;
        height: 10px;
        object-fit: contain;
    }
    
    /* ===== 바텀시트 Type B: 유물 선택 ===== */
    .bottom-sheet-b-item {
        display: flex;
        gap: 11px;
        align-items: center;
        padding: 0 15px 0 15px;
        cursor: pointer;
        transition: background 0.2s;
    }
    
    .bottom-sheet-b-item:hover {
        background: #f9f9f9;
    }
    
    .bottom-sheet-b-item-image {
        width: 80px;
        height: 80px;
        background: #f5f5f5;
        border-radius: 8px;
        object-fit: cover;
        flex-shrink: 0;
    }
    
    .bottom-sheet-b-item-content {
        display: flex;
        flex-direction: column;
        gap: 6px;
        flex: 1;
        min-width: 0;
    }
    
    .bottom-sheet-b-item-details {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }
    
    .bottom-sheet-b-item-badge {
        background: #d9dddf;
        border-radius: 1000px;
        padding: 10px;
        width: fit-content;
        height: 19px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .bottom-sheet-b-item-badge-text {
        font-family: 'Pretendard', sans-serif;
        font-size: 13px;
        font-weight: 400;
        color: #345a6a;
        line-height: 1.4;
        margin: 0;
    }
    
    .bottom-sheet-b-item-title {
        font-family: 'Pretendard', sans-serif;
        font-size: 15px;
        font-weight: 700; /* Bold */
        color: #161617;
        line-height: 1.4;
        margin: 0;
    }
    
    .bottom-sheet-b-item-info {
        display: flex;
        align-items: center;
        gap: 1px;
    }
    
    .bottom-sheet-b-item-info-icon {
        width: 14px;
        height: 14px;
        object-fit: contain;
    }
    
    .bottom-sheet-b-item-info-text {
        font-family: 'Pretendard', sans-serif;
        font-size: 15px;
        font-weight: 400;
        color: #b1b2b7;
        line-height: 1.4;
        margin: 0;
    }
    
    .bottom-sheet-b-item-checkbox {
        width: 20px;
        height: 20px;
        border: 1px solid #b1b2b7;
        border-radius: 4px;
        background: #ffffff;
        flex-shrink: 0;
        cursor: pointer;
        position: relative;
    }
    
    .bottom-sheet-b-item-checkbox.checked {
        background: #246beb;
        border-color: #246beb;
    }
    
    .bottom-sheet-b-item-checkbox.checked::after {
        content: '✓';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: #ffffff;
        font-size: 14px;
        font-weight: bold;
    }
    
    .bottom-sheet-b-button-wrapper {
        padding: 22px 15px 44px 15px;
        width: 100%;
        box-sizing: border-box;
    }
    
    .bottom-sheet-b-button {
        background: #355a6a;
        color: #ffffff;
        border: none;
        border-radius: 10px;
        padding: 18px 10px;
        width: 100%;
        font-family: 'Pretendard', sans-serif;
        font-size: 18px;
        font-weight: 600; /* SemiBold */
        letter-spacing: -0.54px;
        line-height: 1.4;
        cursor: pointer;
    }
    
    .bottom-sheet-b-button:hover {
        background: #2d4a57;
    }
    
    /* ===== 바텀시트 Type A: 연령 선택 ===== */
    .bottom-sheet-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        z-index: 1000;
        display: none;
        animation: fadeIn 0.3s ease;
    }
    
    .bottom-sheet-overlay.show {
        display: block;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideUp {
        from { transform: translateY(100%); }
        to { transform: translateY(0); }
    }
    
    .bottom-sheet {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #ffffff;
        border-radius: 10px 10px 0 0;
        box-shadow: 0px -4px 4px 0px rgba(0, 0, 0, 0.02);
        z-index: 1001;
        max-height: 80vh;
        overflow-y: auto;
        display: none;
        animation: slideUp 0.3s ease;
    }
    
    /* 바텀시트 Type B: 초기 6개만 표시, 스크롤 가능 */
    #bottom-sheet-b {
        max-height: calc(6 * 91px + 40px + 84px); /* 6개 항목(80px 이미지 + 11px gap) + 핸들(40px) + 버튼(84px) */
        overflow-y: hidden; /* 초기에는 스크롤 숨김 */
    }
    
    #bottom-sheet-b.show {
        max-height: calc(10 * 91px + 40px + 84px); /* 10개 항목 + 핸들 + 버튼 */
        overflow-y: auto; /* 스크롤 가능 */
    }
    
    /* 바텀시트 Type B content 영역 */
    #bottom-sheet-b .bottom-sheet-content {
        display: flex;
        flex-direction: column;
        gap: 11px;
        padding: 0;
        max-height: calc(6 * 91px); /* 초기 6개 항목 높이 */
        overflow-y: auto; /* 스크롤 가능 */
        -webkit-overflow-scrolling: touch; /* iOS 부드러운 스크롤 */
    }
    
    #bottom-sheet-b.show .bottom-sheet-content {
        max-height: calc(10 * 91px); /* 스크롤 시 10개 항목 높이 */
    }
    
    .bottom-sheet.show {
        display: block;
    }
    
    .bottom-sheet-handle {
        width: 100%;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        padding-top: 18px;
        box-sizing: border-box;
    }
    
    .bottom-sheet-handle-bar {
        width: 40px;
        height: 4px;
        background: #e1e1e1;
        border-radius: 100px;
    }
    
    .bottom-sheet-content {
        padding: 22px 0 0 0;
    }
    
    .bottom-sheet-item {
        height: 58px;
        border-bottom: 1px solid #f3f4f6;
        display: flex;
        align-items: center;
        padding: 0 15px;
        cursor: pointer;
        transition: background 0.2s;
    }
    
    .bottom-sheet-item:last-child {
        border-bottom: none;
        height: 57px;
    }
    
    .bottom-sheet-item:hover {
        background: #f9f9f9;
    }
    
    .bottom-sheet-item-text {
        font-family: 'Pretendard', sans-serif;
        font-size: 15px;
        font-weight: 700; /* Bold */
        color: #161617;
        line-height: 1.4;
        margin: 0;
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
    
    /* Style 1 버튼 (HTML 직접 렌더링용) */
    .style1-button {
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
        cursor: pointer !important;
    }
    
    .style1-button:hover {
        background: #f5f5f5 !important;
        border-color: #999999 !important;
    }
    
    /* ===== Style 2 - Primary 버튼 ===== */
    /* 사용: st.button("텍스트", type="primary") */
    .stButton > button[kind="primary"] {
        background: #246beb !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 10px 12px 10px !important;
        height: auto !important;
        font-family: 'Pretendard', sans-serif !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        letter-spacing: 0.32px !important;
        line-height: 1.3 !important;
        box-shadow: none !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: #1a5ad4 !important;
    }
    
    /* Style 2 버튼 (HTML 직접 렌더링용) */
    .style2-button {
        background: #246beb !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 10px 12px 10px !important;
        font-family: 'Pretendard', sans-serif !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        letter-spacing: 0.32px !important;
        line-height: 1.3 !important;
        height: auto !important;
        min-width: fit-content !important;
        box-shadow: none !important;
        cursor: pointer !important;
    }
    
    .style2-button:hover {
        background: #1a5ad4 !important;
    }
    
    /* ===== Style 3 - 퀴즈 생성 버튼 ===== */
    /* 사용: with st.container(key="style3"): st.button("텍스트") */
    [data-testid="stVerticalBlock"]:has(> [data-testid="element-container"] > [data-testid="stMarkdown"] > [data-key="style3"]),
    div[data-testid="element-container"]:has([data-key="style3"]) + div .stButton > button,
    [data-key="style3"] .stButton > button {
        background: #355a6a !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 18px 10px !important;
        height: auto !important;
        font-family: 'Pretendard', sans-serif !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        letter-spacing: -0.54px !important;
        line-height: 1.4 !important;
        box-shadow: none !important;
        width: 100% !important;
    }
    
    [data-key="style3"] .stButton > button:hover {
        background: #2a4855 !important;
    }
    
    /* ===== Style 4 - 도우미 선택 카드 ===== */
    /* Streamlit 컨테이너가 Stage 1을 감싸는 경우 스타일 제거 */
    .element-container:has(.stage-1-container),
    [data-testid="stMarkdown"]:has(.stage-1-container),
    [data-testid="stVerticalBlock"]:has(.stage-1-container),
    [data-testid="stVerticalBlock"] > [data-testid="element-container"]:has(.stage-1-container) {
        padding: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        margin: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
    }
    
    /* Stage 1: 도우미 선택 화면 */
    .stage-1-container {
        margin-top: 150px;
        margin-bottom: 105px;
        margin-left: 0 !important;
        margin-right: 0 !important;
        background: #ffffff;
        padding: 0 !important;
        height: 597px;
        position: relative;
        overflow: hidden;
        width: 393px;
        box-sizing: border-box;
    }
    
    .stage-1-background-image {
        position: absolute;
        left: 0;
        top: 247px;
        width: 393px;
        height: 201px;
        object-fit: cover;
        pointer-events: none;
        z-index: 0;
        display: none;
    }
    
    /* 제목 영역 - Figma: width 393px, 중앙정렬, padding 10px 15px */
    .stage-1-title {
        position: absolute;
        left: 0;
        top: 153px; /* 393x597 컨테이너 내부 기준 */
        width: 393px;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px 15px;
        box-sizing: border-box;
        font-family: 'Pretendard', sans-serif !important;
        font-size: 22px !important;
        font-weight: 600 !important;
        color: #07364A !important;
        line-height: 140% !important;
        letter-spacing: -0.22px !important;
        margin: 0;
        white-space: nowrap;
        z-index: 1;
    }
    
    /* 정보 텍스트 영역 - Figma: width 393px, 중앙정렬, padding 0 15px */
    .stage-1-info {
        position: absolute;
        left: 0;
        top: 372px; /* 367px + 5px = 372px */
        width: 393px;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 3px;
        padding: 0 15px;
        box-sizing: border-box;
        z-index: 2;
    }
    
    .stage-1-info-icon {
        width: 16px !important;
        height: 16px !important;
        min-width: 16px !important;
        min-height: 16px !important;
        object-fit: contain !important;
        flex-shrink: 0 !important;
        margin-top: -5px !important; /* 아이콘 살짝 위로 */
    }
    
    .stage-1-info-text {
        font-family: 'Pretendard', sans-serif !important;
        font-size: 13px !important;
        font-weight: 400 !important; /* Regular */
        color: #b1b2b7 !important;
        line-height: 1.4 !important;
        letter-spacing: -0.13px !important;
        margin: 0 !important;
        white-space: nowrap;
    }
    
    /* 카드 컨테이너 - Figma: 중앙정렬, gap 15px, padding 0 15px */
    .helper-cards-container {
        position: absolute;
        left: 0;
        top: 408px; /* 393x597 컨테이너 내부 기준 */
        width: 393px;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px;
        padding: 0 15px;
        box-sizing: border-box;
        z-index: 1;
    }
    
    /* 카드 wrapper - flex 아이템 */
    .helper-card-wrapper {
        flex-shrink: 0;
    }
    
    .helper-card {
        position: relative;
        width: 174px;
        height: 174px;
        border-radius: 20px;
        overflow: hidden;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .helper-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* 흰색 배경 카드 (안내 도우미) */
    .helper-card-light {
        background: #ffffff;
        border: 2px solid #e4e4e4;
    }
    
    /* 흰색 배경 카드 (학습 도우미) - 이미지 뒤 배경 흰색 */
    .helper-card-dark {
        background: #ffffff;
        border: 2px solid #e1e1e1;
    }
    
    .helper-card-image {
        position: absolute;
        object-fit: cover;
        object-position: center;
        pointer-events: none;
        display: block;
        flex-shrink: 0;
        flex-grow: 0;
    }
    
    /* 영희 카드 이미지: 카드 174x174 내에서 커버 */
    .helper-card-light .helper-card-image {
        position: absolute !important;
        left: 0 !important;
        top: 0 !important;
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important;
        object-position: center top !important;
        pointer-events: none !important;
    }
    
    /* 철수 카드 이미지: 카드 174x174 내에서 커버 */
    .helper-card-dark .helper-card-image {
        position: absolute !important;
        left: 0 !important;
        top: 0 !important;
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important;
        object-position: center top !important;
        pointer-events: none !important;
    }
    
    .helper-card-gradient {
        position: absolute;
        top: 56px; /* Figma: top: 56px */
        left: -2px; /* border offset */
        width: 174px;
        height: 116px;
        background: linear-gradient(to bottom, rgba(254,254,254,0) 0%, rgba(0,0,0,0.9) 100%);
        pointer-events: none;
    }
    
    .helper-card-name {
        position: absolute;
        top: 132px; /* Figma: top: 132px */
        left: 10px;
        font-family: 'Pretendard', sans-serif !important;
        font-size: 18px !important;
        font-weight: 400 !important; /* Regular - weight 낮춤 */
        color: #ffffff !important;
        text-shadow: 0px 0px 4px rgba(0,0,0,0.3);
        line-height: 1.4 !important;
        white-space: nowrap;
        z-index: 2;
        pointer-events: none;
    }
    
    .helper-card-badge {
        position: absolute !important;
        top: 9px !important;
        right: 9px !important;
        width: 36px !important;
        height: 36px !important;
        min-width: 36px !important;
        min-height: 36px !important;
        max-width: 36px !important;
        max-height: 36px !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0 !important;
        box-sizing: border-box !important;
        z-index: 3;
        pointer-events: none;
        overflow: hidden;
    }
    
    .helper-card-badge.blue {
        background: #4a90e2 !important;
    }
    
    .helper-card-badge.purple {
        background: #9b59b6 !important;
    }
    
    .helper-card-badge img {
        width: 36px !important;
        height: 36px !important;
        min-width: 36px !important;
        min-height: 36px !important;
        object-fit: contain !important;
        display: block !important;
    }
    
    /* 버튼 스타일 */
    .helper-card-button {
        background: none;
        border: none;
        padding: 0;
        margin: 0;
        cursor: pointer;
        width: 174px;
        height: 174px;
    }
    
    .helper-card-wrapper .stButton {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        opacity: 0 !important;
        z-index: 10 !important;
    }
    
    .helper-card-wrapper .stButton > button {
        width: 100% !important;
        height: 174px !important;
        background: transparent !important;
        border: none !important;
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

# 퀴즈 생성 상태
QUIZ_GENERATION_STATES = {
    "ANALYZING": "analyzing",        # 유물 정보 분석 중
    "GENERATING": "generating",      # 난이도 맞춤 문제 생성 중
    "REVIEWING": "reviewing",        # 최종 검토 중
    "COMPLETED": "completed"         # 완료
}


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
    
    # 선택된 도우미 (None, "영희", "철수")
    if "selected_helper" not in st.session_state:
        st.session_state.selected_helper = None
    
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

def add_bot_message(content: str, sender: str = "철수", msg_type: str = "A", button: dict = None, artifact_count: int = None, generation_state: str = None, difficulty: str = None, question: str = None, artifact_info: dict = None, choices: list = None, selected_choice: int = None, explanation: str = None, correct_count: int = None, total_questions: int = None, encouragement_text: str = None, tour_title: str = None, tour_artifact_count: int = None):
    """
    봇 메시지 추가
    
    Args:
        content: 메시지 내용
        sender: 발신자
        msg_type: 메시지 타입 (A: 일반, B: 투어선택, C_1: 퀴즈생성중, C_2: 퀴즈생성완료, D: 퀴즈문제, E_1: 정답피드백, E_2: 오답피드백, F_1: 마지막정답피드백, F_2: 마지막오답피드백, G: 퀴즈결과)
        button: Type A/B용 - {"text": "버튼텍스트", "action": "액션명"}
        tour_title: Type B용 - 투어 제목 (예: "4학년 2반 현장학습 유물 경로")
        tour_artifact_count: Type B용 - 투어의 유물 개수
        content (Type B): "오~ {user_type}이구나! 네가 만들어둔 전시투어 중에서 오늘 퀴즈로 풀어볼 투어를 골라줘!" 형식 사용
        artifact_count: Type C_1/C_2용 - 유물 개수 (퀴즈 개수와 동일)
        generation_state: Type C_1용 - 생성 상태 ("analyzing", "generating", "reviewing", "completed")
        difficulty: Type C_2용 - 난이도 (user_type 사용, 예: "초등학생")
        question: Type D용 - 문제 텍스트
        artifact_info: Type D용 - {"name": "유물명", "period": "시대", "image": "이미지경로"}
        choices: Type D용 - [{"text": "선택지1"}, {"text": "선택지2"}, ...]
        selected_choice: Type D용 - 선택된 선택지 인덱스 (0부터 시작)
        explanation: Type E_1/E_2/F_1/F_2용 - 피드백 설명 (Gemini 생성, 최대 80자)
        correct_count: Type G용 - 맞춘 문제 수
        total_questions: Type G용 - 전체 문제 수
        encouragement_text: Type G용 - 격려 문구 (System Prompt로 제어, 예: "정말 잘했어~ 10문제 중 4문제나 맞췄네!")
    """
    msg = {
        "role": "assistant",
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M"),
        "sender": sender,
        "type": msg_type
    }
    
    if msg_type in ["A", "B"] and button:
        msg["button"] = button
    
    if msg_type == "B":
        if tour_title:
            msg["tour_title"] = tour_title
        if tour_artifact_count is not None:
            msg["tour_artifact_count"] = tour_artifact_count
    elif msg_type == "C_1":
        if artifact_count is not None:
            msg["artifact_count"] = artifact_count
        if generation_state:
            msg["generation_state"] = generation_state
        else:
            # 기본값: 첫 번째 상태
            msg["generation_state"] = QUIZ_GENERATION_STATES["ANALYZING"]
    elif msg_type == "C_2":
        if artifact_count is not None:
            msg["artifact_count"] = artifact_count
        if difficulty:
            msg["difficulty"] = difficulty
        else:
            # 기본값: 세션 상태에서 가져오기
            msg["difficulty"] = st.session_state.get("user_type", "")
    elif msg_type == "D":
        if question:
            msg["question"] = question
        if artifact_info:
            msg["artifact_info"] = artifact_info
        if choices:
            msg["choices"] = choices
        if selected_choice is not None:
            msg["selected_choice"] = selected_choice
    elif msg_type in ["E_1", "E_2", "F_1", "F_2"]:
        if explanation:
            msg["explanation"] = explanation
    elif msg_type == "G":
        if correct_count is not None:
            msg["correct_count"] = correct_count
        if total_questions is not None:
            msg["total_questions"] = total_questions
        if encouragement_text:
            msg["encouragement_text"] = encouragement_text
    
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

def render_stage_1():
    """Stage 1: 도우미 선택 화면"""
    # 도우미 선택 처리
    query_params = st.query_params
    if "select_helper" in query_params:
        helper_name = query_params["select_helper"]
        if helper_name in ["영희", "철수"]:
            st.session_state.selected_helper = helper_name
            del st.query_params["select_helper"]
            st.rerun()
    
    # Stage 1 HTML 렌더링
    stage1_html = f'''
    <div class="stage-1-container">
        <img src="app/static/images/stage1_background.png" alt="" class="stage-1-background-image" />
        <p class="stage-1-title">도우미를 선택해보세요</p>
        <div class="stage-1-info">
            <img src="app/static/images/icon_warning.png" alt="" class="stage-1-info-icon" />
            <p class="stage-1-info-text">AI가 생성한 대화는 사실과 다를 수 있어요.</p>
        </div>
        <div class="helper-cards-container">
            <div class="helper-card-wrapper">
                <button class="helper-card-button" onclick="selectHelper('영희')">
                    <div class="helper-card helper-card-light">
                        <img src="app/static/images/helper_younghee.png" alt="" class="helper-card-image" />
                        <div class="helper-card-gradient"></div>
                        <p class="helper-card-name">안내 도우미 영희</p>
                        <div class="helper-card-badge blue">
                            <img src="app/static/images/icon_location.png" alt="" />
                        </div>
                    </div>
                </button>
            </div>
            <div class="helper-card-wrapper">
                <button class="helper-card-button" onclick="selectHelper('철수')">
                    <div class="helper-card helper-card-dark">
                        <img src="app/static/images/helper_chulsoo.png" alt="" class="helper-card-image" />
                        <div class="helper-card-gradient"></div>
                        <p class="helper-card-name">학습 도우미 철수</p>
                        <div class="helper-card-badge purple">
                            <img src="app/static/images/icon_study.png" alt="" />
                        </div>
                    </div>
                </button>
            </div>
        </div>
    </div>
    
    <script>
        function selectHelper(helperName) {{
            const url = new URL(window.location);
            url.searchParams.set('select_helper', helperName);
            window.location.href = url.toString();
        }}
    </script>
    '''
    
    return stage1_html

def handle_greeting():
    """Stage_2_1: 채팅 시작 (철수 선택 후)"""
    if len(st.session_state.messages) == 0:
        # Stage_2_1 메시지: 봇 메시지 2개 + 연령 선택하기 버튼
        add_bot_message(
            "안녕하세요! 국립중앙박물관 학습 도우미 철수입니다. 방금 관람하신 전시 내용을 퀴즈로 가볍게 되짚어보실 수 있어요.",
            msg_type="A"
        )
        add_bot_message(
            "저한테 연령대를 알려주시면, 이해하기 편한 난이도로 퀴즈를 준비해 드릴게요.",
            msg_type="A",
            button={"text": "연령 선택하기", "action": "select_user_type"}
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
        
        # Type B 메시지 생성 (투어 선택)
        user_type = st.session_state.user_type or "초등학생"
        content = get_tone_text(
            f"오~ {user_type}이구나! 네가 만들어둔 전시투어 중에서 오늘 퀴즈로 풀어볼 투어를 골라줘!",
            f"오~ {user_type}이구나! 네가 만들어둔 전시투어 중에서 오늘 퀴즈로 풀어볼 투어를 골라줘!"
        )
        
        # 투어 정보 (임시 데이터 - 실제로는 사용자의 투어 데이터 사용)
        tour_title = "4학년 2반 현장학습 유물 경로"  # 실제로는 사용자의 투어 제목
        tour_artifact_count = len(st.session_state.user_artifacts)
        
        add_bot_message(
            content=content,
            msg_type="B",
            button={"text": "이 투어에서 유물 선택하기", "action": "select_tour_artifacts"},
            tour_title=tour_title,
            tour_artifact_count=tour_artifact_count
        )
        st.session_state.current_step = STEPS["ARTIFACT_SELECT"]
    else:
        add_user_message("아니, 아직..." if st.session_state.user_type in ["어린이", "초등학생"] else "아니요, 아직이요...")
        
        msg = get_tone_text(
            "앗, 전시투어를 먼저 만들어주세요! 🏛️\n전시투어에 유물을 담아야 퀴즈를 풀 수 있어요.\n\n다음에 다시 만나요! 👋",
            "앗, 전시투어를 먼저 만들어줘! 🏛️\n전시투어에 유물을 담아야 퀴즈를 풀 수 있어.\n\n다음에 다시 만나자! 👋"
        )
        add_bot_message(msg)
        st.session_state.current_step = STEPS["END"]

def update_quiz_generation_state(state: str):
    """Type C_1 메시지의 생성 상태 업데이트"""
    # 마지막 Type C_1 메시지 찾기
    for i in range(len(st.session_state.messages) - 1, -1, -1):
        msg = st.session_state.messages[i]
        if msg.get("type") == "C_1":
            msg["generation_state"] = state
            break

def handle_artifact_selection(selected: list):
    """유물 선택 처리"""
    st.session_state.selected_artifacts = selected
    selected_names = ", ".join(selected)
    
    # 유물 개수 변수
    artifact_count = len(selected)
    add_user_message(f"총 {artifact_count}개 선택 완료")
    
    # Type C_1: 퀴즈 생성 중 로딩 상태 표시 (초기 상태: analyzing)
    add_bot_message(
        content="",  # Type C_1는 content가 비어있고 구조가 다름
        msg_type="C_1",
        artifact_count=artifact_count,
        generation_state=QUIZ_GENERATION_STATES["ANALYZING"]
    )
    
    # 상태 업데이트: 유물 정보 분석 중 (이미 설정됨)
    # TODO: Gemini API 호출 전에 상태 업데이트
    # update_quiz_generation_state(QUIZ_GENERATION_STATES["ANALYZING"])
    # st.rerun()
    
    # 퀴즈 생성
    # TODO: Gemini API 호출 전에 상태 업데이트
    # update_quiz_generation_state(QUIZ_GENERATION_STATES["GENERATING"])
    # st.rerun()
    
    quizzes = []
    for artifact_name in selected:
        quiz = generate_quiz(artifact_name)
        if quiz:
            quizzes.append(quiz)
    
    # TODO: 퀴즈 생성 완료 후 상태 업데이트
    # update_quiz_generation_state(QUIZ_GENERATION_STATES["REVIEWING"])
    # st.rerun()
    
    st.session_state.quiz_progress = {
        "current_index": 0,
        "total_questions": len(quizzes),
        "correct_count": 0,
        "wrong_answers": [],
        "quizzes": quizzes
    }
    
    # TODO: 최종 검토 완료 후 상태 업데이트
    # update_quiz_generation_state(QUIZ_GENERATION_STATES["COMPLETED"])
    # st.rerun()
    
    # Type C_1을 Type C_2로 변경 (퀴즈 생성 완료)
    for i in range(len(st.session_state.messages) - 1, -1, -1):
        msg = st.session_state.messages[i]
        if msg.get("type") == "C_1":
            msg["type"] = "C_2"
            msg["artifact_count"] = artifact_count  # 퀴즈 개수 = 유물 개수
            msg["difficulty"] = st.session_state.get("user_type", "")  # user_type 사용
            break
    
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
    i = 0
    
    while i < len(st.session_state.messages):
        msg = st.session_state.messages[i]
        msg_type = msg.get("type", "A")
        
        # Type D를 만나면 Quiz Session 시작 (Type D + 사용자 답변 + Type E_1/E_2)
        if msg["role"] == "assistant" and msg_type == "D":
            # Quiz Session 시작
            message_parts.append('<div class="chat-session-wrapper">')
            
            # Type D 렌더링
            sender = msg.get("sender", "철수")
            timestamp = msg.get("timestamp", datetime.now().strftime("%H:%M"))
            question = msg.get("question", "")
            artifact_info = msg.get("artifact_info", {})
            choices = msg.get("choices", [])
            selected_choice = msg.get("selected_choice", None)
            
            artifact_name = artifact_info.get("name", "")
            artifact_period = artifact_info.get("period", "")
            artifact_image = artifact_info.get("image", "app/static/images/default_artifact.png")
            
            # 선택지 HTML 생성
            choices_html = ""
            for j, choice in enumerate(choices):
                choice_text = choice.get("text", "")
                is_selected = (j == selected_choice) if selected_choice is not None else False
                selected_class = "selected" if is_selected else ""
                
                choices_html += (
                    f'<div class="quiz-choice-item" data-choice-index="{j}">'
                    f'<div class="quiz-choice-radio {selected_class}"></div>'
                    f'<p class="quiz-choice-text">{choice_text}</p>'
                    '</div>'
                )
            
            message_parts.append(
                f'<div class="chat-turn type-d">'
                '<div class="bot-message-container">'
                '<div class="bot-content-wrapper">'
                '<div class="bot-header"><div class="bot-avatar">'
                '<img src="app/static/images/profile.png" alt="profile"></div>'
                f'<div class="bot-info"><span class="bot-name">{sender}</span>'
                f'<span class="bot-timestamp">{timestamp}</span></div></div>'
                '<div class="bot-bubble">'
                f'<p>{question}</p>'
                '</div>'
                '<div class="quiz-question-content">'
                '<div class="artifact-info-card">'
                f'<img class="artifact-image" src="{artifact_image}" alt="{artifact_name}" />'
                '<div class="artifact-info">'
                f'<p class="artifact-title">{artifact_name}</p>'
                f'<p class="artifact-period">{artifact_period}</p>'
                '</div>'
                '</div>'
                '<div class="quiz-choices">'
                f'{choices_html}'
                '</div>'
                '<div class="quiz-submit-button-wrapper">'
                '<button class="quiz-submit-button" onclick="handleQuizSubmit()">정답 제출하기</button>'
                '</div>'
                '</div>'
                '</div></div></div>'
            )
            
            i += 1
            
            # 다음 메시지가 사용자 답변인지 확인
            if i < len(st.session_state.messages) and st.session_state.messages[i]["role"] == "user":
                user_msg = st.session_state.messages[i]
                user_timestamp = user_msg.get("timestamp", datetime.now().strftime("%H:%M"))
                user_content = user_msg["content"].replace("<", "&lt;").replace(">", "&gt;")
                
                message_parts.append(
                    '<div class="chat-turn type-a">'
                    '<div class="user-message-container">'
                    f'<span class="user-timestamp">{user_timestamp}</span>'
                    f'<div class="user-bubble"><p>{user_content}</p></div>'
                    '</div></div>'
                )
                i += 1
            
            # 다음 메시지가 Type E_1, E_2, F_1, F_2인지 확인
            if i < len(st.session_state.messages) and st.session_state.messages[i]["role"] == "assistant":
                feedback_msg = st.session_state.messages[i]
                feedback_type = feedback_msg.get("type", "")
                
                if feedback_type in ["E_1", "E_2", "F_1", "F_2"]:
                    sender = feedback_msg.get("sender", "철수")
                    timestamp = feedback_msg.get("timestamp", datetime.now().strftime("%H:%M"))
                    explanation = feedback_msg.get("explanation", "")
                    
                    # Type F는 마지막 질문이므로 두 번째 버블 텍스트가 다름
                    if feedback_type in ["F_1", "F_2"]:
                        fixed_text = "궁금한 게 있으면 지금 바로 물어봐도 돼 😊<br>없으면 나한테 얘기해줘~ 퀴즈를 종료할게! 아래 버튼을 눌러서 퀴즈를 종료할 수도 있어."
                    else:
                        fixed_text = "궁금한 게 있으면 지금 바로 물어봐도 돼 😊<br>없으면 나한테 얘기해줘~ 다음 퀴즈로 넘어갈게!"
                    
                    feedback_title = "✅ 정답이야!" if feedback_type in ["E_1", "F_1"] else "😢 아쉽다..."
                    
                    message_parts.append(
                        f'<div class="chat-turn type-{feedback_type.lower()}">'
                        '<div class="bot-message-container">'
                        '<div class="bot-content-wrapper">'
                        '<div class="bot-header"><div class="bot-avatar">'
                        '<img src="app/static/images/profile.png" alt="profile"></div>'
                        f'<div class="bot-info"><span class="bot-name">{sender}</span>'
                        f'<span class="bot-timestamp">{timestamp}</span></div></div>'
                        '<div class="quiz-feedback-bubble">'
                        f'<p class="feedback-title">{feedback_title}</p>'
                        f'<p class="feedback-explanation">{explanation}</p>'
                        '</div>'
                        '<div class="bot-bubble">'
                        f'<p>{fixed_text}</p>'
                        '</div>'
                        '</div></div></div>'
                    )
                    i += 1
            
            # Quiz Session 종료
            message_parts.append('</div>')
            
            # Type E_1/E_2 이후 사용자 질문이 있는지 확인
            # 사용자 질문 + Gemini 답변 = 새로운 Chat Session
            while i < len(st.session_state.messages):
                # 다음 메시지가 사용자 질문인지 확인
                if st.session_state.messages[i]["role"] == "user":
                    # 새로운 Chat Session 시작 (사용자 질문 + Gemini 답변)
                    message_parts.append('<div class="chat-session-wrapper">')
                    
                    # 사용자 질문 추가
                    user_msg = st.session_state.messages[i]
                    user_timestamp = user_msg.get("timestamp", datetime.now().strftime("%H:%M"))
                    user_content = user_msg["content"].replace("<", "&lt;").replace(">", "&gt;")
                    
                    message_parts.append(
                        '<div class="chat-turn type-a">'
                        '<div class="user-message-container">'
                        f'<span class="user-timestamp">{user_timestamp}</span>'
                        f'<div class="user-bubble"><p>{user_content}</p></div>'
                        '</div></div>'
                    )
                    i += 1
                    
                    # 다음 메시지가 Gemini 답변(일반 bot 메시지)인지 확인
                    if i < len(st.session_state.messages) and st.session_state.messages[i]["role"] == "assistant":
                        bot_msg = st.session_state.messages[i]
                        bot_msg_type = bot_msg.get("type", "A")
                        
                        # Type D, E_1, E_2, F_1, F_2가 아닌 일반 메시지만 처리 (Gemini 답변)
                        if bot_msg_type not in ["D", "E_1", "E_2", "F_1", "F_2"]:
                            bot_sender = bot_msg.get("sender", "철수")
                            bot_timestamp = bot_msg.get("timestamp", datetime.now().strftime("%H:%M"))
                            bot_content = bot_msg.get("content", "").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
                            
                            message_parts.append(
                                f'<div class="chat-turn type-{bot_msg_type.lower()}">'
                                '<div class="bot-message-container">'
                                '<div class="bot-content-wrapper">'
                                '<div class="bot-header"><div class="bot-avatar">'
                                '<img src="app/static/images/profile.png" alt="profile"></div>'
                                f'<div class="bot-info"><span class="bot-name">{bot_sender}</span>'
                                f'<span class="bot-timestamp">{bot_timestamp}</span></div></div>'
                                f'<div class="bot-bubble"><p>{bot_content}</p></div>'
                                '</div></div></div>'
                            )
                            i += 1
                        else:
                            # Type D, E_1, E_2, F_1, F_2가 나오면 이 세션 종료하고 다음 루프에서 처리
                            break
                    
                    # Chat Session 종료
                    message_parts.append('</div>')
                else:
                    # 사용자 메시지가 아니면 종료 (다음 Type D나 다른 메시지 처리)
                    break
            
            continue
        
        # 기존 로직: Type D가 아닌 경우
        msg = st.session_state.messages[i]
        msg_type = msg.get("type", "A")
        
        if msg["role"] == "assistant":
            sender = msg.get("sender", "철수")
            timestamp = msg.get("timestamp", datetime.now().strftime("%H:%M"))
            
            # Type C_1: 퀴즈 생성 중 (로딩 상태)
            if msg_type == "C_1":
                # Chat Session 시작
                message_parts.append('<div class="chat-session-wrapper">')
                
                artifact_count = msg.get("artifact_count", 0)
                generation_state = msg.get("generation_state", QUIZ_GENERATION_STATES["ANALYZING"])
                
                # 상태별 클래스 결정
                analyzing_class = "active" if generation_state == QUIZ_GENERATION_STATES["ANALYZING"] else ("completed" if generation_state in [QUIZ_GENERATION_STATES["GENERATING"], QUIZ_GENERATION_STATES["REVIEWING"], QUIZ_GENERATION_STATES["COMPLETED"]] else "")
                generating_class = "active" if generation_state == QUIZ_GENERATION_STATES["GENERATING"] else ("completed" if generation_state in [QUIZ_GENERATION_STATES["REVIEWING"], QUIZ_GENERATION_STATES["COMPLETED"]] else "")
                reviewing_class = "active" if generation_state == QUIZ_GENERATION_STATES["REVIEWING"] else ("completed" if generation_state == QUIZ_GENERATION_STATES["COMPLETED"] else "")
                
                message_parts.append(
                    f'<div class="chat-turn type-c-1">'
                    '<div class="bot-message-container">'
                    '<div class="bot-content-wrapper">'
                    '<div class="bot-header"><div class="bot-avatar">'
                    '<img src="app/static/images/profile.png" alt="profile"></div>'
                    f'<div class="bot-info"><span class="bot-name">{sender}</span>'
                    f'<span class="bot-timestamp">{timestamp}</span></div></div>'
                    '<div class="quiz-generation-status">'
                    '<div class="loading-header">'
                    '<div class="loading-spinner"></div>'
                    '<p class="loading-text">퀴즈를 생성하고 있어요...</p>'
                    '</div>'
                    '<div class="progress-section">'
                    '<div class="progress-bar"></div>'
                    f'<p class="progress-text">선택하신 {artifact_count}개 유물을 분석하고 있어요</p>'
                    '</div>'
                    '<div class="generation-steps">'
                    f'<div class="step-item {analyzing_class}"><div class="step-dot"></div><p>유물 정보 분석 중</p></div>'
                    f'<div class="step-item {generating_class}"><div class="step-dot"></div><p>난이도 맞춤 문제 생성 중</p></div>'
                    f'<div class="step-item {reviewing_class}"><div class="step-dot"></div><p>최종 검토 중</p></div>'
                    '</div>'
                    '</div>'
                    '</div></div>'
                    '<div class="type-c-1-button-wrapper">'
                    '<button class="type-c-1-button style2-button">퀴즈 생성하기</button>'
                    '</div></div>'
                )
                
                i += 1
                
                # 다음 메시지가 사용자 메시지인지 확인하고 같은 세션으로 묶기
                if i < len(st.session_state.messages) and st.session_state.messages[i]["role"] == "user":
                    user_msg = st.session_state.messages[i]
                    user_timestamp = user_msg.get("timestamp", datetime.now().strftime("%H:%M"))
                    user_content = user_msg["content"].replace("<", "&lt;").replace(">", "&gt;")
                    
                    message_parts.append(
                        '<div class="chat-turn type-a">'
                        '<div class="user-message-container">'
                        f'<span class="user-timestamp">{user_timestamp}</span>'
                        f'<div class="user-bubble"><p>{user_content}</p></div>'
                        '</div></div>'
                    )
                    i += 1
                
                # Chat Session 종료
                message_parts.append('</div>')
            # Type C_2: 퀴즈 생성 완료
            elif msg_type == "C_2":
                # Chat Session 시작
                message_parts.append('<div class="chat-session-wrapper">')
                
                # 퀴즈 개수: 유물 개수와 동일
                artifact_count = msg.get("artifact_count", len(st.session_state.get("selected_artifacts", [])))
                quiz_count = artifact_count  # 퀴즈 개수 변수
                
                # 난이도: user_type 사용
                user_type = msg.get("difficulty", st.session_state.get("user_type", ""))
                
                message_parts.append(
                    f'<div class="chat-turn type-c-2">'
                    '<div class="bot-message-container">'
                    '<div class="bot-content-wrapper">'
                    '<div class="bot-header"><div class="bot-avatar">'
                    '<img src="app/static/images/profile.png" alt="profile"></div>'
                    f'<div class="bot-info"><span class="bot-name">{sender}</span>'
                    f'<span class="bot-timestamp">{timestamp}</span></div></div>'
                    '<div class="quiz-completion-status">'
                    '<div class="completion-header">'
                    '<img class="completion-icon" src="app/static/images/icon_check.png" alt="check" />'
                    '<p class="completion-text">퀴즈 생성 완료!</p>'
                    '</div>'
                    '<div class="quiz-info-card">'
                    '<div class="quiz-info-row">'
                    '<img class="quiz-info-icon" src="app/static/images/icon_star.png" alt="star" />'
                    f'<p class="quiz-info-title">총 {quiz_count}개의 문제가 준비되었어요</p>'
                    '</div>'
                    f'<p class="quiz-info-subtitle">{user_type} 난이도로 맞춤 제작된 퀴즈입니다</p>'
                    '</div>'
                    '<div class="quiz-start-button-wrapper">'
                    '<button class="quiz-start-button" onclick="handleQuizStart()">퀴즈 시작하기</button>'
                    '</div>'
                    '</div>'
                    '</div></div></div>'
                )
                
                i += 1
                
                # 다음 메시지가 사용자 메시지인지 확인하고 같은 세션으로 묶기
                if i < len(st.session_state.messages) and st.session_state.messages[i]["role"] == "user":
                    user_msg = st.session_state.messages[i]
                    user_timestamp = user_msg.get("timestamp", datetime.now().strftime("%H:%M"))
                    user_content = user_msg["content"].replace("<", "&lt;").replace(">", "&gt;")
                    
                    message_parts.append(
                        '<div class="chat-turn type-a">'
                        '<div class="user-message-container">'
                        f'<span class="user-timestamp">{user_timestamp}</span>'
                        f'<div class="user-bubble"><p>{user_content}</p></div>'
                        '</div></div>'
                    )
                    i += 1
                
                # Chat Session 종료
                message_parts.append('</div>')
            # Type G: 퀴즈 결과
            elif msg_type == "G":
                # Chat Session 시작
                message_parts.append('<div class="chat-session-wrapper">')
                
                correct_count = msg.get("correct_count", 0)
                total_questions = msg.get("total_questions", 0)
                encouragement_text = msg.get("encouragement_text", f"정말 잘했어~ {total_questions}문제 중 {correct_count}문제나 맞췄네!")
                
                message_parts.append(
                    f'<div class="chat-turn type-g">'
                    '<div class="bot-message-container">'
                    '<div class="bot-content-wrapper">'
                    '<div class="bot-header"><div class="bot-avatar">'
                    '<img src="app/static/images/profile.png" alt="profile"></div>'
                    f'<div class="bot-info"><span class="bot-name">{sender}</span>'
                    f'<span class="bot-timestamp">{timestamp}</span></div></div>'
                    '<div class="quiz-result-container">'
                    '<div class="quiz-result-header">'
                    '<img class="quiz-result-trophy" src="app/static/images/icon_trophy.png" alt="trophy" />'
                    '<p class="quiz-result-title">퀴즈 완료!</p>'
                    '</div>'
                    '<div class="quiz-result-card">'
                    '<div class="quiz-result-score-row">'
                    '<img class="quiz-result-icon" src="app/static/images/icon_star.png" alt="star" />'
                    f'<p class="quiz-result-score">{correct_count}개 / {total_questions}개</p>'
                    '</div>'
                    f'<p class="quiz-result-encouragement">{encouragement_text}</p>'
                    '</div>'
                    '<div class="quiz-result-button-wrapper">'
                    '<button class="quiz-result-button" onclick="handleRetryQuiz()">다시 도전하기</button>'
                    '</div>'
                    '</div>'
                    '</div></div></div>'
                )
                
                i += 1
                
                # 다음 메시지가 사용자 메시지인지 확인하고 같은 세션으로 묶기
                if i < len(st.session_state.messages) and st.session_state.messages[i]["role"] == "user":
                    user_msg = st.session_state.messages[i]
                    user_timestamp = user_msg.get("timestamp", datetime.now().strftime("%H:%M"))
                    user_content = user_msg["content"].replace("<", "&lt;").replace(">", "&gt;")
                    
                    message_parts.append(
                        '<div class="chat-turn type-a">'
                        '<div class="user-message-container">'
                        f'<span class="user-timestamp">{user_timestamp}</span>'
                        f'<div class="user-bubble"><p>{user_content}</p></div>'
                        '</div></div>'
                    )
                    i += 1
                
                # Chat Session 종료
                message_parts.append('</div>')
            else:
                # Type A, B, C_1, C_2: 일반 메시지
                # Chat Session 시작
                message_parts.append('<div class="chat-session-wrapper">')
                
                content = msg["content"].replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
                message_parts.append(
                    f'<div class="chat-turn type-{msg_type.lower()}">'
                    '<div class="bot-message-container">'
                    '<div class="bot-content-wrapper">'
                    '<div class="bot-header"><div class="bot-avatar">'
                    '<img src="app/static/images/profile.png" alt="profile"></div>'
                    f'<div class="bot-info"><span class="bot-name">{sender}</span>'
                    f'<span class="bot-timestamp">{timestamp}</span></div></div>'
                    f'<div class="bot-bubble"><p>{content}</p></div>'
                    '</div></div></div>'
                )
                
                # Type B: 투어 선택 카드 추가
                if msg_type == "B":
                    tour_title = msg.get("tour_title", "")
                    tour_artifact_count = msg.get("tour_artifact_count", 0)
                    button_data = msg.get("button", {})
                    button_text = button_data.get("text", "이 투어에서 유물 선택하기") if button_data else "이 투어에서 유물 선택하기"
                    
                    message_parts.append(
                        '<div class="tour-selection-card">'
                        '<div class="tour-card-content">'
                        '<div class="tour-card-header">'
                        f'<p class="tour-card-title">{tour_title}</p>'
                        f'<p class="tour-card-subtitle">유물 {tour_artifact_count}개</p>'
                        '</div>'
                        '<div class="tour-card-button-wrapper">'
                        f'<button class="tour-card-button" onclick="openBottomSheetB()">{button_text}</button>'
                        '</div>'
                        '<div class="tour-card-link" onclick="handleOtherTourSelect()">'
                        '<span>다른 투어 선택하기</span>'
                        '<img class="tour-card-link-icon" src="app/static/images/icon_arrow_right.png" alt="arrow" />'
                        '</div>'
                        '</div>'
                        '</div>'
                    )
                
                # Type A에 버튼이 있으면 바텀시트 열기 버튼 추가
                if msg_type == "A" and "button" in msg and msg["button"]:
                    button_data = msg["button"]
                    if button_data.get("action") == "select_user_type":
                        message_parts.append(
                            '<div class="type-a-button-wrapper" style="margin-left: 34px; margin-top: 12px;">'
                            f'<button class="style1-button" onclick="openBottomSheetA()">{button_data.get("text", "연령 선택하기")}</button>'
                            '</div>'
                        )
                
                i += 1
                
                # 다음 메시지가 사용자 메시지인지 확인하고 같은 세션으로 묶기
                if i < len(st.session_state.messages) and st.session_state.messages[i]["role"] == "user":
                    user_msg = st.session_state.messages[i]
                    user_timestamp = user_msg.get("timestamp", datetime.now().strftime("%H:%M"))
                    user_content = user_msg["content"].replace("<", "&lt;").replace(">", "&gt;")
                    
                    message_parts.append(
                        '<div class="chat-turn type-a">'
                        '<div class="user-message-container">'
                        f'<span class="user-timestamp">{user_timestamp}</span>'
                        f'<div class="user-bubble"><p>{user_content}</p></div>'
                        '</div></div>'
                    )
                    i += 1
                
                # Chat Session 종료
                message_parts.append('</div>')
        else:
            # 사용자 메시지 (독립적으로 온 경우 - Type D 처리에서 이미 처리됨)
            # Type D 처리에서 이미 처리된 경우가 아니면 여기서 처리
            if i > 0 and st.session_state.messages[i-1].get("type") != "D":
                timestamp = msg.get("timestamp", datetime.now().strftime("%H:%M"))
                content = msg["content"].replace("<", "&lt;").replace(">", "&gt;")
                
                message_parts.append(
                    '<div class="chat-session-wrapper">'
                    '<div class="chat-turn type-a">'
                    '<div class="user-message-container">'
                    f'<span class="user-timestamp">{timestamp}</span>'
                    f'<div class="user-bubble"><p>{content}</p></div>'
                    '</div></div>'
                    '</div>'
                )
            i += 1
    
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


def render_bottom_sheet_type_a():
    """바텀시트 Type A 렌더링 (연령 선택)"""
    # query parameter로 user_type 선택 처리
    query_params = st.query_params
    
    # user_type 선택 처리
    if "select_user_type" in query_params:
        user_type = query_params["select_user_type"]
        if user_type in USER_TYPES:
            st.session_state.user_type = user_type
            # 사용자 메시지 추가
            add_user_message(user_type)
            del st.query_params["select_user_type"]
            st.rerun()
    
    # 바텀시트 HTML 항목 생성
    items_html = ''.join([f'''
            <div class="bottom-sheet-item" onclick="selectUserType('{user_type}')">
                <p class="bottom-sheet-item-text">{user_type}</p>
            </div>
            ''' for user_type in USER_TYPES])
    
    # 바텀시트 HTML (항상 렌더링하되, JavaScript로 표시/숨김 제어)
    bottom_sheet_html = f'''
    <div class="bottom-sheet-overlay" id="bottom-sheet-overlay-a" onclick="closeBottomSheetA()"></div>
    <div class="bottom-sheet" id="bottom-sheet-a">
        <div class="bottom-sheet-handle">
            <div class="bottom-sheet-handle-bar"></div>
        </div>
        <div class="bottom-sheet-content">
            {items_html}
        </div>
    </div>
    
    <script>
        function openBottomSheetA() {{
            document.getElementById('bottom-sheet-overlay-a').classList.add('show');
            document.getElementById('bottom-sheet-a').classList.add('show');
        }}
        
        function closeBottomSheetA() {{
            document.getElementById('bottom-sheet-overlay-a').classList.remove('show');
            document.getElementById('bottom-sheet-a').classList.remove('show');
        }}
        
        function selectUserType(userType) {{
            // Streamlit query parameter로 user_type 전달
            const url = new URL(window.location);
            url.searchParams.set('select_user_type', userType);
            window.location.href = url.toString();
        }}
    </script>
    '''
    
    return bottom_sheet_html


def render_bottom_sheet_type_b():
    """바텀시트 Type B 렌더링 (유물 선택)"""
    import random
    
    # query parameter로 유물 선택 처리
    query_params = st.query_params
    
    # 유물 선택/해제 처리
    if "toggle_artifact" in query_params:
        artifact_name = query_params["toggle_artifact"]
        if artifact_name:
            if "selected_artifacts" not in st.session_state:
                st.session_state.selected_artifacts = []
            
            if artifact_name in st.session_state.selected_artifacts:
                st.session_state.selected_artifacts.remove(artifact_name)
            else:
                st.session_state.selected_artifacts.append(artifact_name)
            
            del st.query_params["toggle_artifact"]
            st.rerun()
    
    # 퀴즈 생성하기 버튼 클릭 처리
    if "create_quiz" in query_params:
        selected = st.session_state.get("selected_artifacts", [])
        if len(selected) >= 3:  # 최소 3개 이상 선택
            handle_artifact_selection(selected)
            del st.query_params["create_quiz"]
            st.rerun()
    
    # ARTIFACTS에서 15개 중 10개를 랜덤으로 선택
    all_artifacts = list(ARTIFACTS.keys())
    if "bottom_sheet_b_artifacts" not in st.session_state:
        # 15개 중 10개를 랜덤으로 선택
        if len(all_artifacts) >= 10:
            st.session_state.bottom_sheet_b_artifacts = random.sample(all_artifacts, 10)
        else:
            st.session_state.bottom_sheet_b_artifacts = all_artifacts
    
    artifacts = st.session_state.bottom_sheet_b_artifacts
    selected_artifacts = st.session_state.get("selected_artifacts", [])
    
    # 유물 항목 HTML 생성
    artifact_items_html = ""
    for artifact_name in artifacts:
        # ARTIFACTS에서 유물 정보 가져오기
        artifact_data = ARTIFACTS.get(artifact_name)
        if not artifact_data:
            # 이름으로 찾기 시도
            artifact_data = find_artifact(artifact_name)
        
        if artifact_data:
            artifact_image = artifact_data.get("image", "app/static/images/default_artifact.png")
            artifact_period = artifact_data.get("period", "")
            artifact_location = artifact_data.get("location", "")
            artifact_room = artifact_data.get("room", "")
            
            # 배지 (연도) - period에서 추출하거나 기본값
            badge_text = artifact_period.split()[0] if artifact_period and artifact_period.split() else "1799"
            
            # 정보 텍스트 형식: "선사·고대관 | 백제(106호)"
            if artifact_location and artifact_room:
                info_text = f"{artifact_location} | {artifact_room}"
            elif artifact_location:
                info_text = artifact_location
            elif artifact_room:
                info_text = artifact_room
            else:
                info_text = ""
            
            # 체크박스 상태
            is_checked = artifact_name in selected_artifacts
            checkbox_class = "checked" if is_checked else ""
            
            artifact_items_html += f'''
            <div class="bottom-sheet-b-item" onclick="toggleArtifact('{artifact_name}')">
                <img class="bottom-sheet-b-item-image" src="{artifact_image}" alt="{artifact_name}" />
                <div class="bottom-sheet-b-item-content">
                    <div class="bottom-sheet-b-item-badge">
                        <p class="bottom-sheet-b-item-badge-text">{badge_text}</p>
                    </div>
                    <div class="bottom-sheet-b-item-details">
                        <p class="bottom-sheet-b-item-title">{artifact_name}</p>
                        <div class="bottom-sheet-b-item-info">
                            <img class="bottom-sheet-b-item-info-icon" src="app/static/images/icon_location.png" alt="location" />
                            <p class="bottom-sheet-b-item-info-text">{info_text}</p>
                        </div>
                    </div>
                </div>
                <div class="bottom-sheet-b-item-checkbox {checkbox_class}" id="checkbox-{artifact_name}"></div>
            </div>
            '''
    
    # 바텀시트 HTML (항상 렌더링하되, JavaScript로 표시/숨김 제어)
    bottom_sheet_html = f'''
    <div class="bottom-sheet-overlay" id="bottom-sheet-overlay-b" onclick="closeBottomSheetB()"></div>
    <div class="bottom-sheet" id="bottom-sheet-b">
        <div class="bottom-sheet-handle">
            <div class="bottom-sheet-handle-bar"></div>
        </div>
        <div class="bottom-sheet-content" style="gap: 11px;">
            {artifact_items_html}
        </div>
        <div class="bottom-sheet-b-button-wrapper">
            <button class="bottom-sheet-b-button" onclick="createQuiz()">퀴즈 생성하기</button>
        </div>
    </div>
    
    <script>
        function openBottomSheetB() {{
            const bottomSheet = document.getElementById('bottom-sheet-b');
            const content = bottomSheet.querySelector('.bottom-sheet-content');
            
            // 초기 상태: 6개 항목만 표시
            content.style.maxHeight = 'calc(6 * 91px)'; // 6개 항목 높이
            content.scrollTop = 0; // 스크롤 위치 초기화
            
            // 스크롤 이벤트: 스크롤 시 10개 항목까지 확장
            let hasScrolled = false;
            const scrollHandler = function() {{
                if (!hasScrolled && content.scrollTop > 0) {{
                    hasScrolled = true;
                    content.style.maxHeight = 'calc(10 * 91px)'; // 10개 항목 높이로 확장
                }}
            }};
            
            // 기존 이벤트 리스너 제거 후 새로 추가
            content.removeEventListener('scroll', scrollHandler);
            content.addEventListener('scroll', scrollHandler, {{ once: false }});
            
            // 바텀시트 표시
            document.getElementById('bottom-sheet-overlay-b').classList.add('show');
            bottomSheet.classList.add('show');
        }}
        
        function closeBottomSheetB() {{
            const bottomSheet = document.getElementById('bottom-sheet-b');
            const content = bottomSheet.querySelector('.bottom-sheet-content');
            
            // 초기 상태로 리셋
            content.style.maxHeight = 'calc(6 * 91px)';
            content.scrollTop = 0;
            
            document.getElementById('bottom-sheet-overlay-b').classList.remove('show');
            bottomSheet.classList.remove('show');
        }}
        
        function toggleArtifact(artifactName) {{
            // 체크박스 토글
            const checkbox = document.getElementById('checkbox-' + artifactName);
            checkbox.classList.toggle('checked');
            
            // Streamlit query parameter로 유물 전달
            const url = new URL(window.location);
            url.searchParams.set('toggle_artifact', artifactName);
            window.location.href = url.toString();
        }}
        
        function createQuiz() {{
            // Streamlit query parameter로 퀴즈 생성 요청
            const url = new URL(window.location);
            url.searchParams.set('create_quiz', 'true');
            window.location.href = url.toString();
        }}
    </script>
    '''
    
    return bottom_sheet_html


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

# Stage 1 또는 채팅 영역 렌더링
if st.session_state.selected_helper is None:
    # Stage 1: 도우미 선택 화면
    st.markdown(render_stage_1(), unsafe_allow_html=True)
else:
    # Stage_2_1 이후: 채팅 영역
    # 그리팅 처리 (철수 선택 후 첫 채팅)
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

# Type F_1, F_2 버튼 처리 (마지막 메시지가 Type F_1 또는 F_2인 경우)
if st.session_state.messages:
    last_msg = st.session_state.messages[-1]
    last_msg_type = last_msg.get("type", "")
    
    # 마지막 메시지가 Type F_1 또는 F_2이고, 아직 사용자가 "퀴즈 종료하기"를 누르지 않은 경우
    if last_msg_type in ["F_1", "F_2"]:
        # 마지막 메시지가 Type F_1 또는 F_2이고, 그 다음 메시지가 사용자 메시지가 아닌 경우에만 버튼 표시
        # (사용자가 버튼을 누르면 사용자 메시지가 추가되고, 그 다음에 Type G가 나올 예정)
        st.markdown('<div class="quiz-final-button-wrapper">', unsafe_allow_html=True)
        if st.button("퀴즈 종료하기", key="quiz_end_button"):
            # 사용자 메시지 추가
            st.session_state.messages.append({
                "role": "user",
                "content": "퀴즈 종료하기",
                "timestamp": datetime.now().strftime("%H:%M")
            })
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# 바텀시트 Type A 렌더링
st.markdown(render_bottom_sheet_type_a(), unsafe_allow_html=True)

# 바텀시트 Type B 렌더링
st.markdown(render_bottom_sheet_type_b(), unsafe_allow_html=True)

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


# 텍스트 입력 필드 (Stage 1에서는 숨김)
if st.session_state.selected_helper is not None:
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
