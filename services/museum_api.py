"""
🏛️ museum_api.py - 국립중앙박물관 API 서비스
=============================================

전국 박물관 유물정보 API 연동 로직입니다.
API 문서: https://www.data.go.kr/data/3036708/openapi.do
"""

import requests
import xml.etree.ElementTree as ET


class MuseumAPIService:
    """국립중앙박물관 e뮤지엄 API 서비스"""

    BASE_URL = "http://www.emuseum.go.kr/openapi"

    def __init__(self, service_key: str):
        self.service_key = service_key

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

    def get_relic_list(
        self,
        page: int = 1,
        rows: int = 10,
        name: str = "",
        museum_code: str = "",
        nationality_code: str = "",
        material_code: str = ""
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

        try:
            response = requests.get(url, params=params, timeout=10)
            print(f"[DEBUG] Status: {response.status_code}")
            print(f"[DEBUG] URL: {response.url}")
            print(f"[DEBUG] Content-Type: {response.headers.get('Content-Type', 'N/A')}")
            print(f"[DEBUG] Response (first 800 chars):\n{response.text[:800]}")

            if response.status_code != 200:
                return {"error": f"HTTP {response.status_code}", "body": response.text[:200]}

            return self._parse_response(response.text)
        except requests.RequestException as e:
            print(f"API 요청 오류: {e}")
            return {"error": str(e)}

    def get_relic_detail(self, relic_id: str) -> dict:
        """
        소장품 상세 정보 조회

        Parameters:
        - relic_id: 소장품 고유 키 (예: PS0100100100100240600000)
        """
        url = f"{self.BASE_URL}/relic/list"
        params = {
            "serviceKey": self.service_key,
            "pageNo": "1",
            "numOfRows": "1",
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


# 테스트용 코드
if __name__ == "__main__":
    # API 키 (디코딩된 키 사용)
    SERVICE_KEY = "2dkzbWitdGYvTjiqU25D9p/H2EbpBg6QKLJO44+kOV63KqT/9iQb3xRvCiDbBpH138+W8dGkNfGE4SC1RoPBIg=="

    api = MuseumAPIService(SERVICE_KEY)

    print("=" * 50)
    print("=== 소장품 목록 조회 테스트 ===")
    print("=" * 50)
    relics = api.get_relic_list(rows=5)
    print("\n결과:", relics)

    print("\n" + "=" * 50)
    print("=== 금관 검색 테스트 ===")
    print("=" * 50)
    search_result = api.get_relic_list(name="금관", rows=5)
    print("\n결과:", search_result)
