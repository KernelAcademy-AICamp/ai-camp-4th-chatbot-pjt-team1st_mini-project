"""
앱 설정
"""

APP_CONFIG = {
    "title": "박물관 AI 가이드",
    "title_en": "Museum AI Guide",
    "icon": "🏛️",
    "layout": "centered",
}

SUPPORTED_LANGUAGES = {
    "ko": "🇰🇷 한국어",
    "en": "🇺🇸 English",
    "zh": "🇨🇳 中文",
    "ja": "🇯🇵 日本語"
}

DEFAULT_LANGUAGE = "ko"

AI_CONFIG = {
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "temperature": 0.7,
}