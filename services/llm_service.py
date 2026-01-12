"""
🤖 llm_service.py - AI 서비스
==============================

Google Gemini API 연동 로직입니다.
"""

import json
import re
import os
from config.prompts import (
    SYSTEM_PROMPT,
    ARTIFACT_CONTEXT,
    QUIZ_PROMPT,
    MESSAGES
)
from config.settings import AI_CONFIG


class LLMService:
    """Google Gemini API 연동 서비스"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.client = None
        self.model = None

        if api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-2.0-flash')
                self.client = True  # 클라이언트 활성화 표시
                print("✅ Gemini API 연결됨")
            except ImportError:
                print("⚠️ google-generativeai 패키지를 설치해주세요: pip install google-generativeai")
            except Exception as e:
                print(f"⚠️ Gemini 초기화 오류: {e}")

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

        # Gemini API 호출
        if self.model:
            try:
                full_prompt = f"{system_prompt}\n\n사용자: {user_message}"
                response = self.model.generate_content(full_prompt)
                return response.text
            except Exception as e:
                return f"API 오류: {str(e)}"

        # API 없으면 기본 응답
        return self._fallback_response(user_message, artifact)

    def generate_quiz(self, artifact: dict) -> dict:
        """퀴즈 생성"""

        if self.model:
            try:
                prompt = QUIZ_PROMPT.format(
                    artifact_name=artifact["name"]
                )

                response = self.model.generate_content(prompt)

                # JSON 파싱
                response_text = response.text
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

    def generate_enhanced_explanation(
        self,
        artifact: dict,
        quiz: dict,
        is_correct: bool,
        user_question: str = None
    ) -> str:
        """사용자 질문을 반영한 맞춤 해설 생성"""

        base_explanation = quiz.get("explanation", "")

        # 사용자 질문이 없으면 기본 해설 반환
        if not user_question or not user_question.strip():
            return base_explanation

        # Gemini API로 맞춤 해설 생성
        if self.model:
            try:
                prompt = f"""당신은 박물관 큐레이터입니다.
사용자가 유물 퀴즈를 풀면서 궁금한 점을 질문했습니다.

**유물 정보:**
- 이름: {artifact.get('name', '')}
- 시대: {artifact.get('period', '')}
- 지정: {artifact.get('designation', '')}
- 설명: {artifact.get('description', '')}

**퀴즈 문제:** {quiz.get('question', '')}
**정답 여부:** {'정답' if is_correct else '오답'}
**기본 해설:** {base_explanation}

**사용자의 궁금한 점:** {user_question}

위 정보를 바탕으로:
1. 먼저 기본 해설을 제공하고
2. 사용자의 궁금한 점에 친절하게 답변해주세요
3. 추가로 흥미로운 정보가 있다면 알려주세요

응답은 300자 이내로 간결하게 작성해주세요."""

                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"맞춤 해설 생성 오류: {e}")

        # API 없으면 기본 해설 + 안내 메시지
        return f"""{base_explanation}

💬 **질문하신 내용:** {user_question}
→ API 키를 설정하면 궁금한 점에 대한 맞춤 답변을 받을 수 있어요!"""
