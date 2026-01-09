"""
🏛️ museum_api.py - 국립중앙박물관 API 서비스
=============================================

e뮤지엄 공공데이터 API 연동 로직입니다.
API 문서: https://www.data.go.kr/data/3036708/openapi.do
"""

import requests
import xml.etree.ElementTree as ET
from typing import Optional


class MuseumAPIService:
    """국립중앙박물관 e뮤지엄 API 서비스"""

    BASE_URL = "http://www.emuseum.go.kr/openapi"

    def __init__(self, service_key: str):
        self.service_key = service_key

    def _parse_response(self, response_text: str) -> dict:
        """XML 또는 JSON 응답 파싱"""
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
        except:
            pass

        return {"raw": response_text}

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
        등
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
            print(f"[DEBUG] Response (first 500 chars): {response.text[:500]}")

            return self._parse_response(response.text)
        except requests.RequestException as e:
            print(f"API 요청 오류: {e}")
            return {"error": str(e)}

    def get_relic_list(
        self,
        page: int = 1,
        rows: int = 10,
        era_code: str = "",
        material_code: str = ""
    ) -> dict:
        """
        유물 목록 조회
        """
        url = f"{self.BASE_URL}/relic/list"
        params = {
            "serviceKey": self.service_key,
            "pageNo": str(page),
            "numOfRows": str(rows),
        }

        if era_code:
            params["eraCode"] = era_code
        if material_code:
            params["materialCode"] = material_code

        try:
            response = requests.get(url, params=params, timeout=10)
            print(f"[DEBUG] Status: {response.status_code}")
            print(f"[DEBUG] URL: {response.url}")
            print(f"[DEBUG] Response (first 500 chars): {response.text[:500]}")

            return self._parse_response(response.text)
        except requests.RequestException as e:
            print(f"API 요청 오류: {e}")
            return {"error": str(e)}


# 테스트용 코드
if __name__ == "__main__":
    # API 키 직접 입력 (테스트용)
    SERVICE_KEY = "2dkzbWitdGYvTjiqU25D9p%2FH2EbpBg6QKLJO44%2BkOV63KqT%2F9iQb3xRvCiDbBpH138%2BW8dGkNfGE4SC1RoPBIg%3D%3D"

    api = MuseumAPIService(SERVICE_KEY)

    print("=== 코드 목록 조회 ===")
    codes = api.get_codes()
    print(codes)
