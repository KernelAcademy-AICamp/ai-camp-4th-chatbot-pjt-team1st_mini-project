"""
📚 artifacts.py - 유물 데이터
==============================

유물 정보를 추가/수정하는 파일입니다.
국립중앙박물관 API 연동 또는 하드코딩 데이터 사용
"""

import os
import random


# ============================================================
# 🌐 API에서 유물 가져오기
# ============================================================

def fetch_artifacts_from_api(count: int = 10) -> list:
    """
    국립중앙박물관 API에서 유물 목록 가져오기

    Returns:
        list: 유물 목록 (API 실패 시 빈 리스트)
    """
    try:
        from services.museum_api import get_museum_service

        service = get_museum_service()
        if not service.service_key:
            print("⚠️ MUSEUM_API_KEY가 없어서 기본 데이터를 사용합니다.")
            return []

        artifacts = service.get_random_artifacts(count=count)
        if artifacts:
            print(f"✅ API에서 {len(artifacts)}개 유물 로드 완료")
            return artifacts

    except Exception as e:
        print(f"⚠️ API 로드 실패: {e}")

    return []


# ============================================================
# 📜 국립중앙박물관 소장 국보 데이터베이스 (15개)
# ============================================================

ARTIFACTS = {
    "금동미륵보살반가사유상_78호": {
        "id": "NMK-001",
        "name": "금동미륵보살반가사유상",
        "period": "삼국시대 (6세기)",
        "material": "금동 (청동에 금도금)",
        "location": "국립중앙박물관",
        "gallery": "사유의 방 (2층)",
        "designation": "국보 제78호",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Pensive_Bodhisattva_01.jpg/440px-Pensive_Bodhisattva_01.jpg",
        "description": "높이 83.2cm의 반가사유상으로, 부드러운 미소와 섬세한 표현이 특징입니다. 삼국시대 불교 조각의 최고 걸작으로 국보 83호와 함께 '사유의 방'에 전시되어 있습니다.",
        "quiz": {
            "question": "국보 제78호 반가사유상이 현재 전시된 곳은?",
            "options": ["불교조각실", "사유의 방", "선사고대관", "서화관"],
            "answer": 1,
            "explanation": "국보 제78호와 83호 반가사유상은 2021년 개관한 '사유의 방'에 나란히 전시되어 있습니다."
        }
    },

    "금동미륵보살반가사유상_83호": {
        "id": "NMK-002",
        "name": "금동미륵보살반가사유상",
        "period": "삼국시대 (7세기)",
        "material": "금동 (청동에 금도금)",
        "location": "국립중앙박물관",
        "gallery": "사유의 방 (2층)",
        "designation": "국보 제83호",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Korea-National_Treasure_83-Geumdong_Mireukbosal_Bangasayusang-01.jpg/440px-Korea-National_Treasure_83-Geumdong_Mireukbosal_Bangasayusang-01.jpg",
        "description": "높이 93.5cm의 대형 반가사유상입니다. 한쪽 다리를 다른 쪽 무릎 위에 올리고, 손가락을 뺨에 댄 채 깊은 생각에 잠긴 모습이 특징입니다.",
        "quiz": {
            "question": "'반가사유'는 어떤 자세를 의미할까요?",
            "options": ["두 손을 모아 기도하는 자세", "한쪽 다리를 올리고 생각하는 자세", "누워서 명상하는 자세", "서서 설법하는 자세"],
            "answer": 1,
            "explanation": "반가사유는 한쪽 다리를 다른 쪽 무릎 위에 올리고 손가락을 뺨에 댄 채 깊은 생각에 잠긴 자세를 말합니다."
        }
    },

    "경천사십층석탑": {
        "id": "NMK-003",
        "name": "경천사 십층석탑",
        "period": "고려 (1348년)",
        "material": "대리석",
        "location": "국립중앙박물관",
        "gallery": "역사의 길 (1층 로비)",
        "designation": "국보 제86호",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Ten-story_Stone_Pagoda_of_Gyeongcheonsa_Temple_Site.jpg/440px-Ten-story_Stone_Pagoda_of_Gyeongcheonsa_Temple_Site.jpg",
        "description": "높이 약 13.5m의 대리석 석탑입니다. 원나라 양식의 영향을 받았으며, 전체에 불·보살·나한 등이 섬세하게 조각되어 있습니다. 일제강점기 일본 반출 후 반환되었습니다.",
        "quiz": {
            "question": "경천사 십층석탑의 재료는 무엇일까요?",
            "options": ["화강암", "대리석", "사암", "현무암"],
            "answer": 1,
            "explanation": "경천사 십층석탑은 대리석으로 만들어진 석탑으로, 고려 후기 원나라의 영향을 받은 양식입니다."
        }
    },

    "금관총금관": {
        "id": "NMK-004",
        "name": "금관총 금관",
        "period": "신라 (5-6세기)",
        "material": "금, 옥",
        "location": "국립중앙박물관",
        "gallery": "선사고대관 신라실 (1층)",
        "designation": "국보 제87호",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Gold_Crown_from_Geumgwanchong.jpg/440px-Gold_Crown_from_Geumgwanchong.jpg",
        "description": "1921년 경주 금관총에서 발견된 신라 금관입니다. 나뭇가지 모양(出자형)과 사슴뿔 모양의 세움 장식이 특징이며, 신라 왕족의 권위를 상징합니다.",
        "quiz": {
            "question": "신라 금관의 세움 장식은 어떤 모양을 하고 있을까요?",
            "options": ["꽃과 나비 모양", "나뭇가지와 사슴뿔 모양", "구름과 달 모양", "파도와 물고기 모양"],
            "answer": 1,
            "explanation": "신라 금관은 나뭇가지 모양(出자형)과 사슴뿔 모양의 세움 장식이 특징이며, 이는 하늘과 땅을 연결하는 의미를 담고 있습니다."
        }
    },

    "도기기마인물형뿔잔": {
        "id": "NMK-005",
        "name": "도기 기마인물형 뿔잔",
        "period": "신라 (5-6세기)",
        "material": "토기",
        "location": "국립중앙박물관",
        "gallery": "선사고대관 신라실 (1층)",
        "designation": "국보 제91호",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Silla_-_Warrior_on_Horseback_-_01.jpg/440px-Silla_-_Warrior_on_Horseback_-_01.jpg",
        "description": "경주 금령총에서 출토된 말을 탄 인물 형상의 토기입니다. 주인상과 하인상 두 점이 한 쌍을 이루며, 신라의 뛰어난 토기 제작 기술을 보여줍니다.",
        "quiz": {
            "question": "기마인물형 토기가 출토된 무덤의 이름은?",
            "options": ["천마총", "금관총", "금령총", "황남대총"],
            "answer": 2,
            "explanation": "국보 제91호 기마인물형 토기는 경주 금령총에서 주인상과 하인상 두 점이 함께 출토되었습니다."
        }
    },

    "청동은입사포류수금문정병": {
        "id": "NMK-006",
        "name": "청동 은입사 포류수금문 정병",
        "period": "고려 (12세기)",
        "material": "청동, 은",
        "location": "국립중앙박물관",
        "gallery": "조각공예관 금속공예실 (3층)",
        "designation": "국보 제92호",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Bronze_Kundika_with_Silver_Inlaid_Willow_and_Waterfowl_Design.jpg/440px-Bronze_Kundika_with_Silver_Inlaid_Willow_and_Waterfowl_Design.jpg",
        "description": "높이 37.5cm의 정병으로, 은입사 기법으로 버드나무와 물새 무늬를 새겼습니다. 고려시대 금속공예의 정수를 보여주는 걸작입니다.",
        "quiz": {
            "question": "'은입사' 기법은 어떤 기술일까요?",
            "options": ["은을 녹여 붓는 기술", "은실로 그림을 새기는 기술", "은가루를 뿌리는 기술", "은박을 붙이는 기술"],
            "answer": 1,
            "explanation": "은입사는 금속 기물에 홈을 파고 은실을 끼워 넣어 문양을 만드는 고려시대의 정교한 금속공예 기법입니다."
        }
    },

    "백자달항아리": {
        "id": "NMK-007",
        "name": "백자 달항아리",
        "period": "조선 (18세기)",
        "material": "백자",
        "location": "국립중앙박물관",
        "gallery": "조각공예관 도자공예실 (3층)",
        "designation": "국보 제309호",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/White_Porcelain_Moon_Jar.jpg/440px-White_Porcelain_Moon_Jar.jpg",
        "description": "높이 약 40cm의 둥근 백자 항아리입니다. 보름달처럼 풍만한 형태가 특징이며, 조선 백자의 순수한 아름다움을 대표합니다.",
        "quiz": {
            "question": "백자 달항아리의 이름이 '달항아리'인 이유는?",
            "options": ["달 그림이 그려져 있어서", "달빛 아래에서 만들어서", "보름달처럼 둥글어서", "달에게 바치는 제기여서"],
            "answer": 2,
            "explanation": "달항아리는 보름달처럼 둥글고 풍만한 형태 때문에 붙여진 이름으로, 조선 백자의 미학을 대표합니다."
        }
    },

    "금동연가칠년명여래입상": {
        "id": "NMK-008",
        "name": "금동연가7년명여래입상",
        "period": "고구려 (539년)",
        "material": "금동",
        "location": "국립중앙박물관",
        "gallery": "선사고대관 고구려실 (1층)",
        "designation": "국보 제119호",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Gilt-bronze_Standing_Buddha_with_Inscription_of_Year_Yeonga_7.jpg/440px-Gilt-bronze_Standing_Buddha_with_Inscription_of_Year_Yeonga_7.jpg",
        "description": "고구려 불상 중 유일하게 제작 연도가 새겨진 불상입니다. '연가 7년(539년)'이라는 명문이 있어 고구려 불교 미술 연구에 매우 중요합니다.",
        "quiz": {
            "question": "이 불상이 특별한 이유는?",
            "options": ["가장 큰 불상이어서", "제작 연도가 새겨진 유일한 고구려 불상이어서", "금으로만 만들어져서", "여왕이 만들었기 때문에"],
            "answer": 1,
            "explanation": "이 불상은 '연가 7년(539년)'이라는 명문이 새겨진 고구려 유일의 불상으로, 고구려 불교 미술 연구에 매우 중요합니다."
        }
    },

    "다뉴세문경": {
        "id": "NMK-009",
        "name": "다뉴세문경",
        "period": "청동기시대 (기원전 4-3세기)",
        "material": "청동",
        "location": "국립중앙박물관",
        "gallery": "선사고대관 청동기실 (1층)",
        "designation": "국보 제141호",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Multi-knobbed_Fine-patterned_Mirror.jpg/440px-Multi-knobbed_Fine-patterned_Mirror.jpg",
        "description": "여러 개의 꼭지(多鈕)가 달린 청동 거울로, 머리카락보다 가는 1만 3천여 개의 선으로 동심원 무늬를 새겼습니다. 청동기시대 금속공예의 최고 걸작입니다.",
        "quiz": {
            "question": "다뉴세문경의 '세문'은 무엇을 의미할까요?",
            "options": ["세 가지 문양", "가느다란 선 무늬", "세상의 무늬", "새의 무늬"],
            "answer": 1,
            "explanation": "'세문(細文)'은 가느다란 선 무늬를 뜻합니다. 다뉴세문경에는 머리카락보다 가는 1만 3천여 개의 선이 새겨져 있습니다."
        }
    },

    "인왕제색도": {
        "id": "NMK-010",
        "name": "인왕제색도",
        "period": "조선 (1751년)",
        "material": "종이에 수묵",
        "location": "국립중앙박물관",
        "gallery": "서화관 (2층)",
        "designation": "국보 제216호",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Inwangjesaekdo.jpg/440px-Inwangjesaekdo.jpg",
        "description": "겸재 정선이 76세에 그린 진경산수화의 걸작입니다. 비 갠 후 인왕산의 모습을 담았으며, 이건희 컬렉션으로 2021년 국립중앙박물관에 기증되었습니다.",
        "quiz": {
            "question": "'인왕제색'의 뜻은 무엇일까요?",
            "options": ["인왕산의 가을 풍경", "인왕산 비가 개다", "인왕산의 봄날", "인왕산의 달빛"],
            "answer": 1,
            "explanation": "'인왕제색(仁王霽色)'은 '인왕산 비가 개다'라는 뜻으로, 비 온 뒤 맑아진 인왕산의 모습을 그린 작품입니다."
        }
    },

    "금동관음보살입상": {
        "id": "NMK-011",
        "name": "금동관음보살입상",
        "period": "백제 (7세기)",
        "material": "금동",
        "location": "국립중앙박물관",
        "gallery": "조각공예관 불교조각실 (3층)",
        "designation": "국보 제128호",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Gilt-bronze_Standing_Avalokitesvara_Bodhisattva.jpg/440px-Gilt-bronze_Standing_Avalokitesvara_Bodhisattva.jpg",
        "description": "높이 15.2cm의 백제 보살상입니다. 삼면보관을 쓰고 있으며, 부드럽고 유연한 자태가 백제 불상의 특징을 잘 보여줍니다. 이건희 컬렉션으로 기증되었습니다.",
        "quiz": {
            "question": "이 불상이 보여주는 백제 불상의 특징은?",
            "options": ["강인하고 힘찬 모습", "부드럽고 유연한 자태", "화려한 장식", "거대한 크기"],
            "answer": 1,
            "explanation": "백제 불상은 부드럽고 유연한 자태가 특징이며, 이 관음보살입상은 그 특징을 잘 보여주는 대표작입니다."
        }
    },

    "백자청화매죽문항아리": {
        "id": "NMK-012",
        "name": "백자 청화매죽문 항아리",
        "period": "조선 (15세기)",
        "material": "백자",
        "location": "국립중앙박물관",
        "gallery": "조각공예관 도자공예실 (3층)",
        "designation": "국보 제219호",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Blue_and_White_Porcelain_Jar_with_Plum_and_Bamboo_Design.jpg/440px-Blue_and_White_Porcelain_Jar_with_Plum_and_Bamboo_Design.jpg",
        "description": "청화안료로 매화와 대나무를 그린 조선 초기 백자입니다. 세련된 문양과 조형미가 뛰어나 조선 청화백자의 대표작으로 평가됩니다. 이건희 컬렉션으로 기증되었습니다.",
        "quiz": {
            "question": "'청화백자'의 '청화'는 무엇을 의미할까요?",
            "options": ["푸른 꽃무늬", "코발트 안료로 그린 푸른 그림", "맑은 하늘색 유약", "청자와 백자의 결합"],
            "answer": 1,
            "explanation": "'청화'는 코발트 안료로 그린 푸른색 그림을 말합니다. 청화백자는 백자에 푸른 안료로 그림을 그린 도자기입니다."
        }
    },

    "진흥왕북한산순수비": {
        "id": "NMK-013",
        "name": "진흥왕 북한산 순수비",
        "period": "신라 (555년 추정)",
        "material": "화강암",
        "location": "국립중앙박물관",
        "gallery": "선사고대관 신라실 (1층)",
        "designation": "국보 제3호",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Bukhansan_Silla_Jinheung_Sunsubi.jpg/440px-Bukhansan_Silla_Jinheung_Sunsubi.jpg",
        "description": "신라 진흥왕이 북한산 지역을 순행한 기념으로 세운 비석입니다. 원래 북한산 비봉에 있었으나 야외 훼손을 막기 위해 박물관으로 옮겨졌습니다.",
        "quiz": {
            "question": "진흥왕 순수비가 세워진 이유는?",
            "options": ["왕의 업적을 기리기 위해", "새로 개척한 영토를 순행한 기념으로", "불교를 전파하기 위해", "전쟁 승리를 기념하기 위해"],
            "answer": 1,
            "explanation": "순수비는 왕이 새로 개척한 영토를 직접 돌아보며(순수) 세운 기념비입니다. 진흥왕의 영토 확장을 보여주는 중요한 사료입니다."
        }
    },

    "수월관음도": {
        "id": "NMK-014",
        "name": "수월관음도",
        "period": "고려 (14세기)",
        "material": "비단에 채색",
        "location": "국립중앙박물관",
        "gallery": "서화관 불교회화실 (2층)",
        "designation": "국보",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Korea-Goryeo-Avalokitesvara-Water_Moon-Kagami_jinja-01.jpg/440px-Korea-Goryeo-Avalokitesvara-Water_Moon-Kagami_jinja-01.jpg",
        "description": "물가 바위에 앉아 있는 관음보살을 그린 고려 불화입니다. 섬세한 필치와 화려한 색채가 특징이며, 고려 불교 회화의 최고 걸작으로 평가됩니다.",
        "quiz": {
            "question": "'수월관음'은 어떤 모습의 관음보살일까요?",
            "options": ["달빛 아래 서 있는 모습", "물가 바위에 앉아 있는 모습", "연꽃 위에 앉은 모습", "구름을 타고 있는 모습"],
            "answer": 1,
            "explanation": "'수월관음'은 물가(水) 달빛(月) 아래 바위에 앉아 중생을 구제하는 관음보살의 모습을 말합니다."
        }
    },

    "청자상감모란문표형병": {
        "id": "NMK-015",
        "name": "청자 상감모란문 표형병",
        "period": "고려 (12세기)",
        "material": "청자",
        "location": "국립중앙박물관",
        "gallery": "조각공예관 도자공예실 (3층)",
        "designation": "국보 제116호",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Celadon_Gourd-shaped_Bottle_with_Inlaid_Peony_Design.jpg/440px-Celadon_Gourd-shaped_Bottle_with_Inlaid_Peony_Design.jpg",
        "description": "표주박 모양의 고려청자로, 상감 기법으로 모란 무늬를 새겼습니다. 비취색 유약과 세련된 형태가 고려청자의 아름다움을 대표합니다.",
        "quiz": {
            "question": "고려청자의 '상감 기법'은 어떤 방식일까요?",
            "options": ["표면에 그림을 그리는 방식", "표면을 파낸 후 다른 색 흙을 채워 넣는 방식", "금박을 입히는 방식", "유약을 두껍게 바르는 방식"],
            "answer": 1,
            "explanation": "상감 기법은 표면을 파낸 후 백토나 자토를 채워 넣어 무늬를 만드는 고려 고유의 기술입니다."
        }
    }
}


# ============================================================
# 🔍 유물 검색 함수
# ============================================================

def find_artifact(text: str) -> dict | None:
    """텍스트에서 유물을 찾습니다."""
    if not text:
        return None

    for key, artifact in ARTIFACTS.items():
        if key in text or artifact["name"] in text:
            return artifact

    return None


def get_artifact_list() -> list:
    """유물 목록을 반환합니다."""
    return list(ARTIFACTS.keys())


def get_artifact_by_id(artifact_id: str) -> dict | None:
    """ID로 유물을 찾습니다."""
    for artifact in ARTIFACTS.values():
        if artifact.get("id") == artifact_id:
            return artifact
    return None


def get_random_artifacts(count: int = 10, use_api: bool = True) -> list:
    """
    랜덤으로 유물을 선택합니다.

    Parameters:
        count: 가져올 유물 개수
        use_api: API 사용 여부 (기본 True - API 우선 사용)

    Returns:
        list: 유물 목록
    """
    # API에서 가져오기 시도
    if use_api:
        api_artifacts = fetch_artifacts_from_api(count=count)
        if api_artifacts:
            # API 유물에 퀴즈 생성
            return _add_quizzes_to_artifacts(api_artifacts)

    # 기본: 하드코딩된 데이터 사용
    print("📚 기본 유물 데이터를 사용합니다.")
    keys = list(ARTIFACTS.keys())
    selected = random.sample(keys, min(count, len(keys)))
    return [ARTIFACTS[key] for key in selected]


def _add_quizzes_to_artifacts(artifacts: list) -> list:
    """
    API에서 가져온 유물에 퀴즈 추가

    Gemini API로 퀴즈를 생성하거나 기본 퀴즈 사용
    """
    for artifact in artifacts:
        if artifact.get("quiz") is None:
            artifact["quiz"] = _generate_quiz_for_artifact(artifact)
    return artifacts


def _generate_quiz_for_artifact(artifact: dict) -> dict:
    """
    유물에 대한 퀴즈 생성

    Gemini API 사용 가능하면 AI 생성, 아니면 기본 퀴즈
    """
    try:
        from services.llm_service import LLMService
        import os

        api_key = os.getenv("GEMINI_API_KEY", "")
        if api_key:
            llm = LLMService(api_key)
            if llm.model:
                return _generate_quiz_with_gemini(llm, artifact)
    except Exception as e:
        print(f"퀴즈 생성 오류: {e}")

    # 기본 퀴즈
    return _create_default_quiz(artifact)


def _generate_quiz_with_gemini(llm, artifact: dict) -> dict:
    """Gemini API로 퀴즈 생성"""
    import json
    import re

    prompt = f"""다음 유물에 대한 4지선다 퀴즈를 만들어주세요.

유물 정보:
- 이름: {artifact.get('name', '알 수 없음')}
- 시대: {artifact.get('period', '시대 미상')}
- 재질: {artifact.get('material', '')}
- 지정: {artifact.get('designation', '')}
- 전시실: {artifact.get('gallery', '')}
- 설명: {artifact.get('description', '')}

다음 JSON 형식으로 정확히 응답해주세요:
{{
    "question": "퀴즈 질문",
    "options": ["선택지1", "선택지2", "선택지3", "선택지4"],
    "answer": 0,
    "explanation": "정답 해설"
}}

주의:
- answer는 정답의 인덱스 (0-3)
- 질문은 유물의 특징, 시대, 재질, 전시 위치 등에 관한 것
- 선택지는 그럴듯해 보이지만 명확히 구분되어야 함
- 너무 쉽거나 너무 어렵지 않은 중간 난이도
"""

    try:
        response = llm.model.generate_content(prompt)
        response_text = response.text

        # JSON 추출
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            quiz = json.loads(json_match.group())
            # 필수 필드 확인
            if all(k in quiz for k in ["question", "options", "answer", "explanation"]):
                return quiz
    except Exception as e:
        print(f"Gemini 퀴즈 생성 실패: {e}")

    return _create_default_quiz(artifact)


def _create_default_quiz(artifact: dict) -> dict:
    """기본 퀴즈 생성"""
    name = artifact.get('name', '이 유물')
    period = artifact.get('period', '시대 미상')

    return {
        "question": f"'{name}'은(는) 어느 시대의 유물일까요?",
        "options": ["삼국시대", "고려시대", "조선시대", "근현대"],
        "answer": 0,
        "explanation": f"이 유물은 {period}에 제작된 것으로 알려져 있습니다."
    }


# ============================================================
# 🎯 동적 퀴즈 생성 (외부 호출용)
# ============================================================

def generate_dynamic_quiz(artifact: dict, llm_service=None) -> dict:
    """
    유물 정보를 바탕으로 동적으로 퀴즈 생성

    Parameters:
        artifact: 유물 정보 dict
        llm_service: LLMService 인스턴스 (선택)

    Returns:
        dict: 퀴즈 정보 (question, options, answer, explanation)
    """
    # LLM 서비스가 있으면 동적 생성 시도
    if llm_service and llm_service.model:
        try:
            import json
            import re

            prompt = f"""다음 유물 정보를 바탕으로 4지선다 퀴즈를 만들어주세요.

유물 정보:
- 이름: {artifact.get('name', '알 수 없음')}
- 시대: {artifact.get('period', '시대 미상')}
- 재질: {artifact.get('material', '')}
- 지정: {artifact.get('designation', '')}
- 전시실: {artifact.get('gallery', '')}
- 설명: {artifact.get('description', '')}

다음 JSON 형식으로 정확히 응답해주세요:
{{
    "question": "퀴즈 질문",
    "options": ["선택지1", "선택지2", "선택지3", "선택지4"],
    "answer": 0,
    "explanation": "정답 해설 (2-3문장)"
}}

규칙:
- answer는 정답의 인덱스 (0-3)
- 유물의 특징, 시대, 재질, 역사적 의의 등에 관한 문제
- 선택지는 그럴듯하지만 명확히 구분되어야 함
- 설명(description)에 있는 내용을 활용하여 문제 출제
- 기존 하드코딩 퀴즈와 다른 새로운 질문으로 생성
"""

            response = llm_service.model.generate_content(prompt)
            response_text = response.text

            # JSON 추출
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                quiz = json.loads(json_match.group())
                if all(k in quiz for k in ["question", "options", "answer", "explanation"]):
                    print(f"✅ 동적 퀴즈 생성: {artifact.get('name')}")
                    return quiz

        except Exception as e:
            print(f"⚠️ 동적 퀴즈 생성 실패: {e}")

    # 폴백: 하드코딩된 퀴즈 또는 기본 퀴즈
    if artifact.get("quiz"):
        print(f"📝 기존 퀴즈 사용: {artifact.get('name')}")
        return artifact["quiz"]

    return _create_default_quiz(artifact)
