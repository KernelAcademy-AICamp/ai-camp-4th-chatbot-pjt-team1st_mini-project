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
    LANGUAGE_INSTRUCTIONS, 
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
    
    def build_system_prompt(self, language: str, artifact: dict = None) -> str:
        """시스템 프롬프트 생성"""
        
        # 언어 지시문
        language_instruction = LANGUAGE_INSTRUCTIONS.get(
            language, 
            LANGUAGE_INSTRUCTIONS["en"]
        )
        
        # 기본 프롬프트
        system_prompt = SYSTEM_PROMPT.format(
            language_instruction=language_instruction
        )
        
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
    
    def chat(self, user_message: str, language: str, artifact: dict = None) -> str:
        """LLM과 대화"""
        
        system_prompt = self.build_system_prompt(language, artifact)
        
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
        return self._fallback_response(user_message, language, artifact)
    
    def generate_quiz(self, artifact: dict, language: str) -> dict:
        """퀴즈 생성"""
        
        if self.client:
            try:
                lang_name = {
                    "ko": "한국어", 
                    "en": "English", 
                    "zh": "中文", 
                    "ja": "日本語"
                }.get(language, "English")
                
                prompt = QUIZ_PROMPT.format(
                    artifact_name=artifact["name"],
                    language=lang_name
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
        return self._fallback_quiz(artifact, language)
    
    def _fallback_response(self, user_message: str, language: str, artifact: dict = None) -> str:
        """API 없을 때 기본 응답"""
        
        if artifact:
            if language == "en":
                return f"""## {artifact['name_en']}

**Period**: {artifact['period']}
**Material**: {artifact['material']}
**Location**: {artifact['location']}

{artifact['description']}

💡 **Fun Facts**: 
{chr(10).join('• ' + fact for fact in artifact.get('fun_facts', []))}

Feel free to ask more questions! Type "quiz" to test your knowledge 🎯"""
            
            elif language == "zh":
                return f"""## {artifact.get('name_zh', artifact['name'])}

**时代**: {artifact['period']}
**材料**: {artifact['material']}
**位置**: {artifact['location']}

{artifact['description']}

💡 **趣闻**: 
{chr(10).join('• ' + fact for fact in artifact.get('fun_facts', []))}

如有更多问题请继续询问！输入"测验"可以测试您的理解 🎯"""
            
            elif language == "ja":
                return f"""## {artifact.get('name_ja', artifact['name'])}

**時代**: {artifact['period']}
**材料**: {artifact['material']}
**場所**: {artifact['location']}

{artifact['description']}

💡 **豆知識**: 
{chr(10).join('• ' + fact for fact in artifact.get('fun_facts', []))}

他にも質問があればどうぞ！「クイズ」と入力すると理解度をチェックできます 🎯"""
            
            else:  # 한국어 기본
                return f"""## {artifact['name']}

**시대**: {artifact['period']}
**재료**: {artifact['material']}
**위치**: {artifact['location']}

{artifact['description']}

💡 **알고 계셨나요?**
{chr(10).join('• ' + fact for fact in artifact.get('fun_facts', []))}

더 궁금한 점이 있으시면 질문해 주세요! "퀴즈"라고 입력하면 퀴즈를 풀 수 있어요 🎯"""
        
        return MESSAGES["artifact_not_found"].get(language, MESSAGES["artifact_not_found"]["en"])
    
    def _fallback_quiz(self, artifact: dict, language: str) -> dict:
        """기본 퀴즈 (API 없을 때)"""
        
        if language == "en":
            return {
                "question": f"When was '{artifact['name_en']}' created?",
                "options": ["Three Kingdoms Period", "Goryeo Dynasty", "Joseon Dynasty", "Modern Era"],
                "correct_index": 0,
                "explanation": f"This artifact was created during {artifact['period']}."
            }
        elif language == "zh":
            return {
                "question": f"'{artifact.get('name_zh', artifact['name'])}'是什么时候制作的？",
                "options": ["三国时代", "高丽时代", "朝鲜时代", "近代"],
                "correct_index": 0,
                "explanation": f"这件文物制作于{artifact['period']}。"
            }
        elif language == "ja":
            return {
                "question": f"'{artifact.get('name_ja', artifact['name'])}'はいつ作られましたか？",
                "options": ["三国時代", "高麗時代", "朝鮮時代", "近代"],
                "correct_index": 0,
                "explanation": f"この文化財は{artifact['period']}に作られました。"
            }
        else:
            return {
                "question": f"'{artifact['name']}'은(는) 언제 만들어졌나요?",
                "options": ["삼국시대", "고려시대", "조선시대", "근대"],
                "correct_index": 0,
                "explanation": f"이 유물은 {artifact['period']}에 만들어졌습니다."
            }
