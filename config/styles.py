"""
🎨 styles.py - 디자이너 전용 파일
==================================

이 파일만 수정하면 앱 전체 디자인이 바뀝니다!
다른 파일은 건드리지 않아도 됩니다.

수정 후 저장 → git add . → git commit -m "스타일 변경" → git push
"""

# ============================================================
# 🎨 색상 (Colors) - 흰색/파란색 테마
# ============================================================

COLORS = {
    # 메인 색상
    "primary": "#3b82f6",           # 파란색 (버튼, 강조)
    "primary_light": "#bae6fd",     # 연한 하늘색
    "primary_dark": "#2563eb",      # 진한 파란색

    # 배경 색상
    "background": "#ffffff",        # 메인 배경 (흰색)
    "background_light": "#f0f9ff",  # 밝은 배경 (아주 연한 하늘색)
    "surface": "rgba(255, 255, 255, 0.95)",  # 카드/박스 배경

    # 텍스트 색상
    "text": "#1f2937",              # 기본 텍스트 (어두운 회색)
    "text_secondary": "rgba(59, 130, 246, 0.7)",  # 보조 텍스트 (연한 파랑)
    "text_on_primary": "#ffffff",   # 버튼 위 텍스트 (흰색)

    # 보더/라인
    "border": "rgba(59, 130, 246, 0.3)",
    "border_light": "rgba(59, 130, 246, 0.15)",

    # 상태 색상
    "success": "#4ade80",           # 성공 (초록)
    "error": "#f87171",             # 에러 (빨강)
    "warning": "#fbbf24",           # 경고 (노랑)
    "info": "#60a5fa",              # 정보 (파랑)
}


# ============================================================
# 🔤 폰트 (Fonts)
# ============================================================

FONTS = {
    # Google Fonts URL (앱에서 자동 로드)
    "import_url": "https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700&family=Pretendard:wght@400;500;600;700&display=swap",

    # 폰트 패밀리
    "primary": "'Noto Sans KR', 'Pretendard', sans-serif",
    "heading": "'Noto Sans KR', sans-serif",

    # 폰트 크기
    "size_xs": "11px",
    "size_sm": "12px",
    "size_base": "14px",
    "size_lg": "16px",
    "size_xl": "18px",
    "size_2xl": "24px",
    "size_3xl": "28px",
}


# ============================================================
# 📐 간격 & 크기 (Spacing & Sizing)
# ============================================================

SPACING = {
    "xs": "4px",
    "sm": "8px",
    "md": "12px",
    "lg": "16px",
    "xl": "20px",
    "2xl": "24px",
    "3xl": "32px",
}

SIZING = {
    "border_radius": "15px",
    "border_radius_sm": "10px",
    "border_radius_lg": "20px",
    "border_radius_full": "50%",

    "button_height": "48px",
    "input_height": "48px",
    "header_height": "70px",
    "footer_height": "140px",
}


# ============================================================
# 🌟 그림자 & 효과 (Shadows & Effects)
# ============================================================

EFFECTS = {
    "shadow_sm": "0 2px 8px rgba(0, 0, 0, 0.08)",
    "shadow_md": "0 4px 15px rgba(0, 0, 0, 0.1)",
    "shadow_lg": "0 4px 20px rgba(0, 0, 0, 0.15)",
    "shadow_blue": "0 4px 15px rgba(59, 130, 246, 0.3)",

    "transition": "all 0.2s ease",
    "transition_slow": "all 0.3s ease",
}


# ============================================================
# 💬 채팅 버블 스타일
# ============================================================

CHAT_BUBBLE = {
    # 사용자 메시지 (오른쪽)
    "user": {
        "background": f"linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%)",
        "text_color": COLORS["text_on_primary"],
        "border_radius": "20px 20px 4px 20px",
        "max_width": "75%",
        "align": "flex-end",
    },

    # AI 메시지 (왼쪽)
    "assistant": {
        "background": COLORS["surface"],
        "text_color": COLORS["text"],
        "border": f"1px solid {COLORS['border_light']}",
        "border_radius": "20px 20px 20px 4px",
        "max_width": "85%",
        "align": "flex-start",
    },
}


# ============================================================
# 🎯 컴포넌트별 스타일
# ============================================================

COMPONENTS = {
    # 헤더
    "header": {
        "background": f"linear-gradient(180deg, rgba(59, 130, 246, 0.1) 0%, transparent 100%)",
        "border_bottom": f"1px solid {COLORS['border_light']}",
        "padding": SPACING["xl"],
    },

    # 사이드바
    "sidebar": {
        "background": COLORS["background"],
        "width": "300px",
    },

    # 버튼
    "button_primary": {
        "background": f"linear-gradient(135deg, {COLORS['primary']}, {COLORS['primary_dark']})",
        "color": COLORS["text_on_primary"],
        "border": "none",
        "border_radius": SIZING["border_radius_sm"],
        "font_weight": "600",
    },

    "button_secondary": {
        "background": f"rgba(59, 130, 246, 0.1)",
        "color": COLORS["primary"],
        "border": f"1px solid {COLORS['border']}",
        "border_radius": SIZING["border_radius_sm"],
    },

    # 입력 필드
    "input": {
        "background": "#f8fafc",
        "color": COLORS["text"],
        "border": f"1px solid {COLORS['border']}",
        "border_radius": SIZING["border_radius_lg"],
    },

    # 카드
    "card": {
        "background": COLORS["surface"],
        "border": f"1px solid {COLORS['border_light']}",
        "border_radius": SIZING["border_radius"],
        "padding": SPACING["xl"],
        "shadow": EFFECTS["shadow_md"],
    },
}


# ============================================================
# 📱 CSS 생성 함수 (건드리지 마세요!)
# ============================================================

def generate_css() -> str:
    """위 설정값들로 CSS를 생성합니다."""

    return f"""
    <style>
        /* Google Fonts 로드 */
        @import url('{FONTS["import_url"]}');

        /* 전체 앱 배경 */
        .stApp {{
            background: linear-gradient(180deg, {COLORS["background"]} 0%, {COLORS["background_light"]} 50%, {COLORS["background"]} 100%);
            font-family: {FONTS["primary"]};
        }}

        /* 헤더 */
        .main-header {{
            background: {COMPONENTS["header"]["background"]};
            padding: {COMPONENTS["header"]["padding"]};
            border-radius: {SIZING["border_radius"]};
            border: 1px solid {COLORS["border"]};
            margin-bottom: {SPACING["xl"]};
        }}

        .main-header h1 {{
            color: {COLORS["primary_dark"]} !important;
            font-family: {FONTS["heading"]};
            font-size: {FONTS["size_3xl"]};
            margin: 0 !important;
        }}

        .main-header p {{
            color: {COLORS["text_secondary"]};
            font-size: {FONTS["size_sm"]};
            margin: {SPACING["xs"]} 0 0 0;
        }}

        /* 텍스트 색상 */
        .stMarkdown {{
            color: {COLORS["text"]};
        }}

        h1, h2, h3, h4 {{
            color: {COLORS["primary_dark"]} !important;
        }}

        /* 입력 필드 */
        .stTextInput input, .stTextArea textarea {{
            background: {COMPONENTS["input"]["background"]} !important;
            color: {COMPONENTS["input"]["color"]} !important;
            border: {COMPONENTS["input"]["border"]} !important;
            border-radius: {COMPONENTS["input"]["border_radius"]} !important;
        }}

        .stTextInput input::placeholder {{
            color: {COLORS["text_secondary"]} !important;
        }}

        /* 버튼 - Primary */
        .stButton > button {{
            background: {COMPONENTS["button_primary"]["background"]} !important;
            color: {COMPONENTS["button_primary"]["color"]} !important;
            border: {COMPONENTS["button_primary"]["border"]} !important;
            border-radius: {COMPONENTS["button_primary"]["border_radius"]} !important;
            font-weight: {COMPONENTS["button_primary"]["font_weight"]} !important;
            transition: {EFFECTS["transition"]};
        }}

        .stButton > button:hover {{
            box-shadow: {EFFECTS["shadow_blue"]};
            transform: translateY(-1px);
        }}

        /* 파일 업로더 */
        .stFileUploader {{
            background: rgba(59, 130, 246, 0.05);
            border: 2px dashed {COLORS["border"]};
            border-radius: {SIZING["border_radius"]};
            padding: {SPACING["xl"]};
        }}

        /* 셀렉트박스 */
        .stSelectbox > div > div {{
            background: {COMPONENTS["input"]["background"]} !important;
            border: {COMPONENTS["input"]["border"]} !important;
        }}

        /* 사이드바 */
        section[data-testid="stSidebar"] {{
            background: {COLORS["background"]} !important;
        }}

        section[data-testid="stSidebar"] .stMarkdown {{
            color: {COLORS["text"]};
        }}

        /* Expander */
        .streamlit-expanderHeader {{
            background: rgba(59, 130, 246, 0.1) !important;
            border-radius: {SIZING["border_radius_sm"]} !important;
        }}

        /* 채팅 메시지 컨테이너 */
        .stChatMessage {{
            background: transparent !important;
        }}

        /* 스크롤바 */
        ::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}

        ::-webkit-scrollbar-track {{
            background: transparent;
        }}

        ::-webkit-scrollbar-thumb {{
            background: {COLORS["border"]};
            border-radius: 3px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: {COLORS["primary"]};
        }}

        /* 링크 */
        a {{
            color: {COLORS["primary"]} !important;
        }}

        /* 테이블 */
        table {{
            color: {COLORS["text"]} !important;
        }}

        th {{
            background: rgba(59, 130, 246, 0.15) !important;
            color: {COLORS["primary_dark"]} !important;
        }}

        td {{
            background: {COLORS["surface"]} !important;
        }}

        /* 애니메이션 */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .fade-in {{
            animation: fadeIn 0.3s ease-out;
        }}

        /* 체크박스 스타일 개선 */
        .stCheckbox {{
            background: rgba(59, 130, 246, 0.05) !important;
            border: 1px solid rgba(59, 130, 246, 0.2) !important;
            border-radius: 12px !important;
            padding: 12px 15px !important;
            margin: 5px 0 !important;
            transition: all 0.2s ease !important;
        }}

        .stCheckbox:hover {{
            background: rgba(59, 130, 246, 0.1) !important;
            border-color: rgba(59, 130, 246, 0.4) !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
        }}

        .stCheckbox label {{
            color: {COLORS["text"]} !important;
            font-size: 14px !important;
        }}

        .stCheckbox [data-testid="stCheckbox"] {{
            gap: 12px !important;
        }}

        /* 체크박스 아이콘 */
        .stCheckbox svg {{
            fill: {COLORS["primary"]} !important;
        }}

        /* 선택된 체크박스 */
        .stCheckbox:has(input:checked) {{
            background: rgba(59, 130, 246, 0.15) !important;
            border-color: {COLORS["primary"]} !important;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
        }}

        /* 유물 카드 스타일 */
        .artifact-card {{
            background: rgba(248, 250, 252, 0.9);
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 15px;
            padding: 15px 20px;
            margin: 8px 0;
            transition: all 0.2s ease;
            cursor: pointer;
        }}

        .artifact-card:hover {{
            background: rgba(59, 130, 246, 0.08);
            border-color: rgba(59, 130, 246, 0.4);
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.15);
        }}

        .artifact-card.selected {{
            background: rgba(59, 130, 246, 0.12);
            border-color: {COLORS["primary"]};
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
        }}

        .artifact-card h4 {{
            color: {COLORS["primary_dark"]} !important;
            margin: 0 0 5px 0 !important;
            font-size: 16px !important;
        }}

        .artifact-card p {{
            color: {COLORS["text_secondary"]} !important;
            margin: 0 !important;
            font-size: 13px !important;
        }}

        /* Progress bar 파란색 */
        .stProgress > div > div > div {{
            background: linear-gradient(90deg, {COLORS["primary"]}, {COLORS["primary_dark"]}) !important;
        }}

        /* Success/Warning/Error 메시지 */
        .stSuccess {{
            background: rgba(74, 222, 128, 0.1) !important;
            border: 1px solid rgba(74, 222, 128, 0.3) !important;
        }}

        .stWarning {{
            background: rgba(251, 191, 36, 0.1) !important;
            border: 1px solid rgba(251, 191, 36, 0.3) !important;
        }}

        .stError {{
            background: rgba(248, 113, 113, 0.1) !important;
            border: 1px solid rgba(248, 113, 113, 0.3) !important;
        }}
    </style>
    """


# ============================================================
# 🏷️ HTML 컴포넌트 템플릿
# ============================================================

def get_header_html(title: str, subtitle: str = "") -> str:
    """헤더 HTML 생성"""
    return f"""
    <div class="main-header">
        <h1>🏛️ {title}</h1>
        <p>{subtitle}</p>
    </div>
    """


def get_card_html(content: str, title: str = "") -> str:
    """카드 컴포넌트 HTML 생성"""
    title_html = f"<h4>{title}</h4>" if title else ""
    return f"""
    <div style="
        background: {COLORS["surface"]};
        border: 1px solid {COLORS["border_light"]};
        border-radius: {SIZING["border_radius"]};
        padding: {SPACING["xl"]};
        margin: {SPACING["md"]} 0;
    ">
        {title_html}
        {content}
    </div>
    """


def get_badge_html(text: str, color: str = "primary") -> str:
    """배지 HTML 생성"""
    bg_color = COLORS.get(color, COLORS["primary"])
    return f"""
    <span style="
        background: {bg_color};
        color: {COLORS["text_on_primary"]};
        padding: 4px 12px;
        border-radius: 20px;
        font-size: {FONTS["size_sm"]};
        font-weight: 500;
    ">{text}</span>
    """
