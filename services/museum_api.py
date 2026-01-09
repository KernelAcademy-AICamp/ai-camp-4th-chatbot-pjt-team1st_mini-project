"""
🏛️ museum_api.py - 국립중앙박물관 API 서비스
=============================================

e뮤지엄 공공데이터 API 연동 로직입니다.
API 문서: https://www.data.go.kr/data/3036708/openapi.do
"""

import requests
from typing import Optional


class MuseumAPIService:
    """국립중앙박물관 e뮤지엄 API 서비스"""

    BASE_URL = "http://www.emuseum.go.kr/openapi"

    def __init__(self, service_key: str):
        self.service_key = service_key

    def get_codes(self, parent_code: str = "PS01", page: int = 1, rows: int = 10) -> dict:
        """
        코드 목록 조회
        - PS01: 소장품 분류 코드
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
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"API 요청 오류: {e}")
            return {"error": str(e)}

    def search_relics(
        self,
        keyword: str = "",
        page: int = 1,
        rows: int = 10,
        category: str = ""
    ) -> dict:
        """
        유물 검색
        - keyword: 검색어
        - category: 분류 코드
        """
        url = f"{self.BASE_URL}/relic"
        params = {
            "serviceKey": self.service_key,
            "pageNo": str(page),
            "numOfRows": str(rows),
        }

        if keyword:
            params["searchWord"] = keyword
        if category:
            params["categoryCode"] = category

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"API 요청 오류: {e}")
            return {"error": str(e)}

    def get_relic_detail(self, relic_id: str) -> dict:
        """
        유물 상세 정보 조회
        - relic_id: 유물 ID
        """
        url = f"{self.BASE_URL}/relic/detail"
        params = {
            "serviceKey": self.service_key,
            "relicId": relic_id
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"API 요청 오류: {e}")
            return {"error": str(e)}


# 테스트용 코드
if __name__ == "__main__":
    import os

    # 환경변수에서 API 키 로드 또는 직접 입력
    SERVICE_KEY = os.getenv("MUSEUM_API_KEY", "your_service_key_here")

    api = MuseumAPIService(SERVICE_KEY)

    # 코드 목록 조회 테스트
    print("=== 코드 목록 조회 ===")
    codes = api.get_codes()
    print(codes)

    # 유물 검색 테스트
    print("\n=== 유물 검색 ===")
    relics = api.search_relics(keyword="금관")
    print(relics)
