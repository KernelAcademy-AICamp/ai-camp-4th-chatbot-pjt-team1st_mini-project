"""
🤖 llm_service.py - AI 서비스
==============================

Claude API 연동 로직입니다.
개발자만 수정합니다.
"""

import json
import re
from config.prompts import (
    SYSTEM_PROMPT,
    ARTIFACT_CONTEXT,
    QUIZ_PROMPT,
    MESSAGES
)
from config.settings import AI_CONFIG


class LLMService:
    """Claude API 연동 서비스"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.client = None

        if api_key:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=api_key)
            except ImportError:
                print("⚠️ anthropic 패키지를 설치해주세요: pip install anthropic")

    def build_system_prompt(self, artifact: dict = None) -> str:
        """시스템 프롬프트 생성"""

        # 기본 프롬프트
        system_prompt = SYSTEM_PROMPT

        # 유물 정보 추가
        if artifact:
            artifact_context = ARTIFACT_CONTEXT.format(
                name=artifact.get("name", ""),
                name_en=artifact.get("name_en", ""),
                period=artifact.get("period", ""),
                material=artifact.get("material", ""),
                location=artifact.get("location", ""),
                description=artifact.get("description", ""),
                fun_facts=", ".join(artifact.get("fun_facts", []))
            )
            system_prompt += artifact_context

        return system_prompt

    def chat(self, user_message: str, artifact: dict = None) -> str:
        """LLM과 대화"""

        system_prompt = self.build_system_prompt(artifact)

        # API 클라이언트가 있으면 실제 호출
        if self.client:
            try:
                response = self.client.messages.create(
                    model=AI_CONFIG["model"],
                    max_tokens=AI_CONFIG["max_tokens"],
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": user_message}
                    ]
                )
                return response.content[0].text
            except Exception as e:
                return f"API 오류: {str(e)}"

        # API 없으면 기본 응답
        return self._fallback_response(user_message, artifact)

    def generate_quiz(self, artifact: dict) -> dict:
        """퀴즈 생성"""

        if self.client:
            try:
                prompt = QUIZ_PROMPT.format(
                    artifact_name=artifact["name"]
                )

                response = self.client.messages.create(
                    model=AI_CONFIG["model"],
                    max_tokens=500,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )

                # JSON 파싱
                response_text = response.content[0].text
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            except Exception as e:
                print(f"퀴즈 생성 오류: {e}")

        # 폴백: 기본 퀴즈
        return self._fallback_quiz(artifact)

    def _fallback_response(self, user_message: str, artifact: dict = None) -> str:
        """API 없을 때 기본 응답"""

        if artifact:
            return f"""## {artifact['name']}

**시대**: {artifact['period']}
**재료**: {artifact['material']}
**위치**: {artifact['location']}

{artifact['description']}

💡 **알고 계셨나요?**
{chr(10).join('• ' + fact for fact in artifact.get('fun_facts', []))}

더 궁금한 점이 있으시면 질문해 주세요! "퀴즈"라고 입력하면 퀴즈를 풀 수 있어요 🎯"""

        return MESSAGES["artifact_not_found"]

    def _fallback_quiz(self, artifact: dict) -> dict:
        """기본 퀴즈 (API 없을 때)"""

        return {
            "question": f"'{artifact['name']}'은(는) 언제 만들어졌나요?",
            "options": ["삼국시대", "고려시대", "조선시대", "근대"],
            "correct_index": 0,
            "explanation": f"이 유물은 {artifact['period']}에 만들어졌습니다."
        }
