"""
🏛️ museum_api.py - 국립중앙박물관 API 서비스
=============================================

국립중앙박물관 e뮤지엄 API 연동 로직입니다.
API 문서: https://www.emuseum.go.kr/openapi
"""

import os
import random
import requests
import xml.etree.ElementTree as ET


class MuseumAPIService:
    """국립중앙박물관 e뮤지엄 API 서비스"""

    BASE_URL = "http://www.emuseum.go.kr/openapi"

    # 국립중앙박물관 코드
    NATIONAL_MUSEUM_CODE = "PS01001001"

    # 국립중앙박물관 주요 유물 ID 목록 (ID로만 조회 가능)
    ARTIFACT_IDS = [
        "PS0100100100100240600000",  # 대당평백제비 탁본
        "PS0100100100100012300000",  # 금동미륵보살반가사유상
        "PS0100100100100015700000",  # 백자 달항아리
        "PS0100100100100000100000",  # 반가사유상
        "PS0100100100100001200000",  # 청자 상감운학문 매병
        "PS0100100100100003500000",  # 금관
        "PS0100100100100009800000",  # 경천사지 십층석탑
        "PS0100100100100005600000",  # 청동은입사포류수금문정병
        "PS0100100100100007800000",  # 금동연가7년명여래입상
        "PS0100100100100011200000",  # 천마총 금관
        "PS0100100100100018900000",  # 고려청자
        "PS0100100100100022300000",  # 분청사기
        "PS0100100100100025600000",  # 조선백자
        "PS0100100100100028900000",  # 신라 토기
        "PS0100100100100031200000",  # 고구려 벽화
    ]

    def __init__(self, service_key: str = None):
        self.service_key = service_key or os.getenv("MUSEUM_API_KEY", "")

    def _parse_response(self, response_text: str) -> dict:
        """XML 또는 JSON 응답 파싱"""
        if not response_text or not response_text.strip():
            return {"error": "빈 응답"}

        # JSON 시도
        try:
            import json
            return json.loads(response_text)
        except:
            pass

        # XML 파싱 시도
        try:
            root = ET.fromstring(response_text)
            return self._xml_to_dict(root)
        except Exception as e:
            pass

        return {"raw": response_text[:500]}

    def _xml_to_dict(self, element) -> dict:
        """XML Element를 딕셔너리로 변환"""
        result = {}

        if len(element):
            for child in element:
                child_data = self._xml_to_dict(child)
                tag = child.tag

                if tag in result:
                    if not isinstance(result[tag], list):
                        result[tag] = [result[tag]]
                    result[tag].append(child_data)
                else:
                    result[tag] = child_data
        else:
            result = element.text if element.text else ""

        return result

    def _parse_list_response(self, response_text: str) -> list:
        """XML 응답에서 소장품 목록 파싱"""
        artifacts = []

        try:
            root = ET.fromstring(response_text)

            # 결과 코드 확인
            result_code = root.find(".//resultCode")
            if result_code is not None and result_code.text != "0000":
                result_msg = root.find(".//resultMsg")
                print(f"API 오류: {result_msg.text if result_msg is not None else 'Unknown'}")
                return []

            total_count = root.find(".//totalCount")
            if total_count is not None:
                print(f"총 소장품 수: {total_count.text}")

            # data 요소들 순회
            for data in root.findall(".//data"):
                artifact = {}

                for item in data.findall("item"):
                    key = item.get("key")
                    value = item.get("value", "")
                    if key and value:
                        artifact[key] = value

                if artifact and artifact.get("name"):
                    artifacts.append(artifact)

        except ET.ParseError as e:
            print(f"XML 파싱 오류: {e}")

        return artifacts

    def get_relic_list(
        self,
        page: int = 1,
        rows: int = 10,
        name: str = "",
        museum_code: str = "",
        nationality_code: str = "",
        material_code: str = "",
        designation_code: str = ""
    ) -> dict:
        """
        소장품 목록 조회

        Parameters:
        - page: 페이지 번호
        - rows: 한 페이지 결과 수
        - name: 명칭 검색어 (예: "금관")
        - museum_code: 박물관 코드
        - nationality_code: 국적/시대 코드
        - material_code: 재질 코드
        - designation_code: 지정구분 코드 (국보: PS12001, 보물: PS12002)
        """
        url = f"{self.BASE_URL}/relic/list"
        params = {
            "serviceKey": self.service_key,
            "pageNo": str(page),
            "numOfRows": str(rows),
        }

        if name:
            params["name"] = name
        if museum_code:
            params["museumCode"] = museum_code
        if nationality_code:
            params["nationalityCode"] = nationality_code
        if material_code:
            params["materialCode"] = material_code
        if designation_code:
            params["designationCode"] = designation_code

        try:
            response = requests.get(url, params=params, timeout=10)
            print(f"[DEBUG] Status: {response.status_code}")
            print(f"[DEBUG] URL: {response.url}")

            if response.status_code != 200:
                return {"error": f"HTTP {response.status_code}", "body": response.text[:200]}

            return self._parse_response(response.text)
        except requests.RequestException as e:
            print(f"API 요청 오류: {e}")
            return {"error": str(e)}

    def fetch_artifacts(
        self,
        page: int = 1,
        rows: int = 50,
        museum_code: str = None
    ) -> list:
        """
        소장품 목록을 리스트로 가져오기

        Parameters:
        - page: 페이지 번호
        - rows: 가져올 개수
        - museum_code: 박물관 코드 (기본: 국립중앙박물관)
        """
        if not self.service_key:
            print("⚠️ MUSEUM_API_KEY가 설정되지 않았습니다.")
            return []

        url = f"{self.BASE_URL}/relic/list"
        params = {
            "serviceKey": self.service_key,
            "pageNo": str(page),
            "numOfRows": str(rows),
            "museumCode": museum_code or self.NATIONAL_MUSEUM_CODE,
        }

        try:
            response = requests.get(url, params=params, timeout=10)

            if response.status_code != 200:
                print(f"API 오류: HTTP {response.status_code}")
                return []

            return self._parse_list_response(response.text)

        except requests.RequestException as e:
            print(f"API 요청 오류: {e}")
            return []

    def get_random_artifacts(self, count: int = 10) -> list:
        """
        랜덤으로 소장품 가져오기

        미리 정의된 유물 ID 목록에서 랜덤 선택 후 API로 상세 조회
        """
        if not self.service_key:
            print("⚠️ MUSEUM_API_KEY가 설정되지 않았습니다.")
            return []

        # 랜덤으로 ID 선택
        selected_ids = random.sample(
            self.ARTIFACT_IDS,
            min(count, len(self.ARTIFACT_IDS))
        )

        artifacts = []
        for artifact_id in selected_ids:
            artifact = self.fetch_artifact_by_id(artifact_id)
            if artifact:
                artifacts.append(artifact)

        if not artifacts:
            print("⚠️ API에서 소장품을 가져오지 못했습니다.")
            return []

        print(f"✅ API에서 {len(artifacts)}개 유물 로드 완료")
        return artifacts

    def fetch_artifact_by_id(self, artifact_id: str) -> dict | None:
        """
        ID로 소장품 상세 조회

        Parameters:
        - artifact_id: 소장품 고유 ID
        """
        url = f"{self.BASE_URL}/relic/list"
        params = {
            "serviceKey": self.service_key,
            "pageNo": "1",
            "numOfRows": "1",
            "id": artifact_id
        }

        try:
            response = requests.get(url, params=params, timeout=10)

            if response.status_code != 200:
                print(f"API 오류: HTTP {response.status_code}")
                return None

            # XML 파싱
            artifacts = self._parse_list_response(response.text)
            if artifacts:
                return self._convert_to_standard_format(artifacts[0])

        except requests.RequestException as e:
            print(f"API 요청 오류: {e}")

        return None

    def _convert_to_standard_format(self, api_artifact: dict) -> dict:
        """API 데이터를 앱 표준 형식으로 변환"""

        artifact_id = api_artifact.get("id", f"API-{random.randint(1000, 9999)}")

        # 이름: nameKr > name 순서로 시도
        name = api_artifact.get("nameKr") or api_artifact.get("name", "알 수 없음")

        # 시대/국적: nationalityName1 필드 사용
        period = api_artifact.get("nationalityName1", "시대 미상")

        # 재질: materialName1 필드 사용
        material = api_artifact.get("materialName1", "")

        # 설명: desc 필드 사용
        description = api_artifact.get("desc", "")

        # 이미지: imgUri 또는 imgThumUriL 사용
        image_url = api_artifact.get("imgUri") or api_artifact.get("imgThumUriL", "")

        # 용도/분류
        purpose = api_artifact.get("purposeName2", api_artifact.get("purposeName1", ""))

        return {
            "id": artifact_id,
            "name": name,
            "name_kr": api_artifact.get("nameKr", name),
            "name_cn": api_artifact.get("nameCn", ""),
            "name_en": api_artifact.get("nameEn", ""),
            "period": period,
            "material": material,
            "location": "국립중앙박물관",
            "designation": purpose,  # 용도를 지정구분 대신 사용
            "description": description,
            "image_url": image_url,
            # 퀴즈는 나중에 Gemini로 생성
            "quiz": None,
            # 원본 API 데이터 보관
            "_raw": api_artifact
        }

    def get_relic_detail(self, relic_id: str) -> dict:
        """
        소장품 상세 정보 조회

        Parameters:
        - relic_id: 소장품 고유 키 (예: PS0100100100100240600000)
        """
        url = f"{self.BASE_URL}/relic/detail"
        params = {
            "serviceKey": self.service_key,
            "id": relic_id
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            print(f"[DEBUG] Status: {response.status_code}")
            print(f"[DEBUG] URL: {response.url}")

            if response.status_code != 200:
                return {"error": f"HTTP {response.status_code}"}

            return self._parse_response(response.text)
        except requests.RequestException as e:
            print(f"API 요청 오류: {e}")
            return {"error": str(e)}


# 싱글톤 인스턴스
_museum_service = None


def get_museum_service() -> MuseumAPIService:
    """Museum API 서비스 인스턴스 반환"""
    global _museum_service
    if _museum_service is None:
        api_key = os.getenv("MUSEUM_API_KEY", "")
        _museum_service = MuseumAPIService(api_key)
    return _museum_service


# 테스트용 코드
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv("MUSEUM_API_KEY")
    if not api_key:
        print("⚠️ .env 파일에 MUSEUM_API_KEY를 설정해주세요.")
        exit(1)

    api = MuseumAPIService(api_key)

    print("=" * 50)
    print("=== 소장품 목록 조회 테스트 ===")
    print("=" * 50)

    artifacts = api.get_random_artifacts(count=5)
    print(f"\n가져온 소장품 수: {len(artifacts)}")

    for i, artifact in enumerate(artifacts, 1):
        print(f"\n{i}. {artifact['name']}")
        print(f"   시대: {artifact['period']}")
        print(f"   재질: {artifact['material']}")

