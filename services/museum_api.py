"""
🏛️ museum_api.py - 국립중앙박물관 API 서비스
=============================================

e뮤지엄 공공데이터 API 연동 로직입니다.
API 문서: https://www.data.go.kr/data/3036708/openapi.do
"""

import requests
import xml.etree.ElementTree as ET
from urllib.parse import unquote


class MuseumAPIService:
    """국립중앙박물관 e뮤지엄 API 서비스"""

    BASE_URL = "http://www.emuseum.go.kr/openapi"

    def __init__(self, service_key: str):
        # 디코딩된 키를 그대로 사용
        self.service_key = service_key

    def _parse_response(self, response_text: str) -> dict:
        """XML 또는 JSON 응답 파싱"""
        # 빈 응답 체크
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

        # 자식 요소가 있는 경우
        if len(element):
            for child in element:
                child_data = self._xml_to_dict(child)
                tag = child.tag

                # 같은 태그가 여러 개면 리스트로
                if tag in result:
                    if not isinstance(result[tag], list):
                        result[tag] = [result[tag]]
                    result[tag].append(child_data)
                else:
                    result[tag] = child_data
        else:
            # 텍스트 값
            result = element.text if element.text else ""

        return result

    def get_codes(self, parent_code: str = "PS01", page: int = 1, rows: int = 10) -> dict:
        """
        코드 목록 조회
        - PS01: 시대 코드
        - PS02: 재질 코드
        - PS03: 지정구분 코드
        """
        url = f"{self.BASE_URL}/code"
        params = {
            "serviceKey": self.service_key,
            "pageNo": str(page),
            "numOfRows": str(rows),
            "parentCode": parent_code
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            print(f"[DEBUG] Status: {response.status_code}")
            print(f"[DEBUG] URL: {response.url}")
            print(f"[DEBUG] Content-Type: {response.headers.get('Content-Type', 'N/A')}")
            print(f"[DEBUG] Response (first 500 chars):\n{response.text[:500]}")

            if response.status_code != 200:
                return {"error": f"HTTP {response.status_code}", "body": response.text[:200]}

            return self._parse_response(response.text)
        except requests.RequestException as e:
            print(f"API 요청 오류: {e}")
            return {"error": str(e)}

    def get_relic_list(
        self,
        page: int = 1,
        rows: int = 10,
        search_word: str = ""
    ) -> dict:
        """
        유물 목록 조회
        """
        url = f"{self.BASE_URL}/relic"
        params = {
            "serviceKey": self.service_key,
            "pageNo": str(page),
            "numOfRows": str(rows),
        }

        if search_word:
            params["searchWord"] = search_word

        try:
            response = requests.get(url, params=params, timeout=10)
            print(f"[DEBUG] Status: {response.status_code}")
            print(f"[DEBUG] URL: {response.url}")
            print(f"[DEBUG] Content-Type: {response.headers.get('Content-Type', 'N/A')}")
            print(f"[DEBUG] Response (first 500 chars):\n{response.text[:500]}")

            if response.status_code != 200:
                return {"error": f"HTTP {response.status_code}", "body": response.text[:200]}

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
    print("=== 코드 목록 조회 테스트 ===")
    print("=" * 50)
    codes = api.get_codes()
    print("\n결과:", codes)

    print("\n" + "=" * 50)
    print("=== 유물 목록 조회 테스트 ===")
    print("=" * 50)
    relics = api.get_relic_list()
    print("\n결과:", relics)
