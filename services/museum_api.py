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

        국립중앙박물관 API에서 소장품을 가져와서 랜덤으로 선택
        """
        if not self.service_key:
            print("⚠️ MUSEUM_API_KEY가 설정되지 않았습니다.")
            return []

        # 랜덤 페이지에서 소장품 가져오기
        random_page = random.randint(1, 20)
        artifacts = self.fetch_artifacts(page=random_page, rows=50)

        if not artifacts:
            # 첫 페이지 시도
            artifacts = self.fetch_artifacts(page=1, rows=50)

        if not artifacts:
            print("⚠️ API에서 소장품을 가져오지 못했습니다.")
            return []

        # 랜덤 선택
        selected = random.sample(
            artifacts,
            min(count, len(artifacts))
        )

        # 표준 형식으로 변환
        return [self._convert_to_standard_format(a) for a in selected]

    def _convert_to_standard_format(self, api_artifact: dict) -> dict:
        """API 데이터를 앱 표준 형식으로 변환"""

        artifact_id = api_artifact.get("id", f"API-{random.randint(1000, 9999)}")
        name = api_artifact.get("name", api_artifact.get("nameKr", "알 수 없음"))

        return {
            "id": artifact_id,
            "name": name,
            "name_kr": api_artifact.get("nameKr", name),
            "name_cn": api_artifact.get("nameCn", ""),
            "name_en": api_artifact.get("nameEn", ""),
            "period": api_artifact.get("nationality", api_artifact.get("era", "시대 미상")),
            "material": api_artifact.get("material", ""),
            "location": "국립중앙박물관",
            "designation": api_artifact.get("designation", ""),
            "description": api_artifact.get("content", api_artifact.get("description", "")),
            "image_url": api_artifact.get("imageUrl", ""),
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

