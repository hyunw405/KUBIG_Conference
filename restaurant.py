import requests
import pandas as pd

# 카카오맵 API를 사용하여 장소 검색
def search_places(category_group_code, lat, lon, radius, api_key):
    url = "https://dapi.kakao.com/v2/local/search/category.json"
    headers = {"Authorization": f"KakaoAK {api_key}"}
    params = {
        "category_group_code": category_group_code,
        "x": lon,
        "y": lat,
        "radius": radius,
        "sort": "distance"  # 거리순 정렬
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['documents']
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []

# 메인 함수
def main():
    API_KEY = "48afb747b9bf9aba1c2afe045a8ed165"  # 발급받은 카카오 REST API 키
    
    # 사용자 입력: 위도, 경도
    facility_lat = float(input("위도를 입력하세요: "))
    facility_lon = float(input("경도를 입력하세요: "))
    radius = 500  # 반경 500m

    # 주변 식당 검색
    restaurants = search_places("FD6", facility_lat, facility_lon, radius, API_KEY)

    # 결과 출력 및 저장
    if restaurants:
        # 데이터프레임 생성
        df = pd.DataFrame(restaurants)
        output_file = "nearby_restaurants.csv"
        df.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"결과가 '{output_file}'로 저장되었습니다.")
        print("500m 내 식당 목록:")
        for idx, restaurant in enumerate(restaurants, start=1):
            print(f"{idx}. {restaurant['place_name']} - {restaurant.get('road_address_name', '주소 정보 없음')}")
    else:
        print("반경 내 식당이 없습니다.")

if __name__ == "__main__":
    main()