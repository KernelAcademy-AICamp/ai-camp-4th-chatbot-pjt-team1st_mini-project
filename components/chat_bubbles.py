"""
💬 Chat Bubble 컴포넌트
=======================

채팅 버블 타입별 관리

타입:
- A: 일반 채팅 버블 (버튼 없음)
- B: 채팅 버블 + 바로 아래 버튼
- C: 채팅 버블 + 선택지 버튼들 (퀴즈용)
"""

from datetime import datetime


# ============================================================
# 🎨 스타일 상수
# ============================================================

BUBBLE_STYLES = {
    "bot": {
        "bg_color": "#e7eef7",
        "text_color": "#333333",
        "border_radius": "0 10px 10px 10px",
        "max_width": "343px"
    },
    "user": {
        "bg_color": "#246beb",
        "text_color": "#ffffff",
        "border_radius": "10px 10px 0 10px",
        "max_width": "307px"
    },
    "button": {
        "bg_color": "#ffffff",
        "text_color": "#333333",
        "border": "1px solid #cccccc",
        "border_radius": "1000px",
        "shadow": "0px 2px 4px 0px rgba(0,0,0,0.04)"
    }
}


# ============================================================
# 🅰️ Type A: 일반 채팅 버블
# ============================================================

def render_type_a_bot(content: str, sender: str = "국립중앙박물관", timestamp: str = None, profile_img: str = "app/static/images/profile.png") -> str:
    """
    Type A - 봇 메시지 (버튼 없음)
    
    Args:
        content: 메시지 내용
        sender: 발신자 이름
        timestamp: 시간 (없으면 현재 시간)
        profile_img: 프로필 이미지 경로
    
    Returns:
        HTML 문자열
    """
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M")
    
    # 특수문자 이스케이프
    content = content.replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
    
    return f'''
    <div class="chat-turn type-a">
        <div class="bot-message-container">
            <div class="bot-header">
                <div class="bot-avatar">
                    <img src="{profile_img}" alt="profile">
                </div>
                <div class="bot-info">
                    <span class="bot-name">{sender}</span>
                    <span class="bot-timestamp">{timestamp}</span>
                </div>
            </div>
            <div class="bot-bubble">
                <p>{content}</p>
            </div>
        </div>
    </div>
    '''


def render_type_a_user(content: str, timestamp: str = None) -> str:
    """
    Type A - 사용자 메시지
    
    Args:
        content: 메시지 내용
        timestamp: 시간 (없으면 현재 시간)
    
    Returns:
        HTML 문자열
    """
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M")
    
    # 특수문자 이스케이프
    content = content.replace("<", "&lt;").replace(">", "&gt;")
    
    return f'''
    <div class="chat-turn type-a">
        <div class="user-message-container">
            <span class="user-timestamp">{timestamp}</span>
            <div class="user-bubble">
                <p>{content}</p>
            </div>
        </div>
    </div>
    '''


# ============================================================
# 🅱️ Type B: 채팅 버블 + 단일 버튼
# ============================================================

def render_type_b_bot(content: str, button_text: str, button_key: str = None, sender: str = "국립중앙박물관", timestamp: str = None, profile_img: str = "app/static/images/profile.png") -> dict:
    """
    Type B - 봇 메시지 + 바로 아래 버튼
    
    Args:
        content: 메시지 내용
        button_text: 버튼 텍스트
        button_key: 버튼 고유 키 (Streamlit용)
        sender: 발신자 이름
        timestamp: 시간
        profile_img: 프로필 이미지 경로
    
    Returns:
        dict: {"html": HTML문자열, "button": {"text": 버튼텍스트, "key": 키}}
    """
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M")
    
    # 특수문자 이스케이프
    content = content.replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
    
    html = f'''
    <div class="chat-turn type-b">
        <div class="bot-message-container">
            <div class="bot-header">
                <div class="bot-avatar">
                    <img src="{profile_img}" alt="profile">
                </div>
                <div class="bot-info">
                    <span class="bot-name">{sender}</span>
                    <span class="bot-timestamp">{timestamp}</span>
                </div>
            </div>
            <div class="bot-bubble">
                <p>{content}</p>
            </div>
        </div>
    </div>
    '''
    
    return {
        "html": html,
        "button": {
            "text": button_text,
            "key": button_key or f"btn_{timestamp}"
        }
    }


# ============================================================
# 🅲 Type C: 채팅 버블 + 다중 버튼 (선택지)
# ============================================================

def render_type_c_bot(content: str, buttons: list, sender: str = "국립중앙박물관", timestamp: str = None, profile_img: str = "app/static/images/profile.png") -> dict:
    """
    Type C - 봇 메시지 + 여러 선택 버튼
    
    Args:
        content: 메시지 내용
        buttons: [{"text": "버튼1", "key": "btn1"}, ...]
        sender: 발신자 이름
        timestamp: 시간
        profile_img: 프로필 이미지 경로
    
    Returns:
        dict: {"html": HTML문자열, "buttons": [{"text": 텍스트, "key": 키}, ...]}
    """
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M")
    
    # 특수문자 이스케이프
    content = content.replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
    
    html = f'''
    <div class="chat-turn type-c">
        <div class="bot-message-container">
            <div class="bot-header">
                <div class="bot-avatar">
                    <img src="{profile_img}" alt="profile">
                </div>
                <div class="bot-info">
                    <span class="bot-name">{sender}</span>
                    <span class="bot-timestamp">{timestamp}</span>
                </div>
            </div>
            <div class="bot-bubble">
                <p>{content}</p>
            </div>
        </div>
    </div>
    '''
    
    return {
        "html": html,
        "buttons": buttons
    }


# ============================================================
# 🔧 유틸리티 함수
# ============================================================

def get_bubble_css() -> str:
    """
    채팅 버블 CSS 반환
    """
    return '''
    /* ===== 채팅 턴 공통 ===== */
    .chat-turn {
        display: flex;
        flex-direction: column;
        gap: 13px;
        margin-bottom: 13px;
        width: 100%;
        max-width: 363px;
    }
    
    /* ===== 봇 메시지 ===== */
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
    }
    
    .bot-bubble p {
        font-family: 'Pretendard', sans-serif;
        font-size: 16px;
        font-weight: 400;
        color: #333333;
        line-height: 1.4;
        margin: 0;
    }
    
    /* ===== 사용자 메시지 ===== */
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
    '''


# ============================================================
# 📦 메시지 데이터 구조
# ============================================================

"""
메시지 데이터 구조 예시:

# Type A (일반 메시지)
{
    "type": "A",
    "role": "assistant",  # 또는 "user"
    "content": "메시지 내용",
    "timestamp": "14:35",
    "sender": "국립중앙박물관"
}

# Type B (메시지 + 단일 버튼)
{
    "type": "B",
    "role": "assistant",
    "content": "메시지 내용",
    "button": {
        "text": "버튼 텍스트",
        "action": "action_name"  # 또는 콜백 함수명
    },
    "timestamp": "14:35",
    "sender": "국립중앙박물관"
}

# Type C (메시지 + 다중 버튼)
{
    "type": "C",
    "role": "assistant",
    "content": "메시지 내용",
    "buttons": [
        {"text": "선택1", "action": "action1"},
        {"text": "선택2", "action": "action2"}
    ],
    "timestamp": "14:35",
    "sender": "국립중앙박물관"
}
"""
