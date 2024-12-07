import math
import pandas as pd
import requests

# 지구상의 두 좌표 사이의 거리 계산 (Haversine formula)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # 지구 반지름 (km)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c * 1000  # km를 m로 변환

# 지하철역 좌표 가져오기
def get_station_coordinates(station_name, api_key):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {api_key}"}
    params = {"query": station_name, "category_group_code": "SW8"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['documents']:
            place = data['documents'][0]
            return float(place['y']), float(place['x'])  # 위도, 경도 반환
        else:
            print(f"No results found for {station_name}")
            return None
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# 반경 내 체육 시설 검색
def find_nearby_facilities(lat, lon, facilities_data, radius=1500):
    unique_facilities = []
    for _, row in facilities_data.iterrows():
        distance = haversine(lat, lon, row['PBTRNSP_FCLTY_LA'], row['PBTRNSP_FCLTY_LO'])
        if distance <= radius:
            unique_facilities.append(row)
    return pd.DataFrame(unique_facilities)

# 메인 함수
def final(station_name):
    API_KEY = "48afb747b9bf9aba1c2afe045a8ed165"  # 카카오 API 키를 입력하세요

    # 1. 지하철역 좌표 가져오기
    station_coordinates = get_station_coordinates(station_name, API_KEY)
    if not station_coordinates:
        return pd.DataFrame()  # 좌표를 가져오지 못하면 빈 데이터프레임 반환

    station_lat, station_lon = station_coordinates

    file_path = r"C:\Users\hwpte\Downloads\체육시설대중교통.csv"

    # 2. 시설 데이터 로드
    facilities_data = pd.read_csv(file_path)

    # 3. 반경 1.5km 내 시설 검색
    nearby_facilities = find_nearby_facilities(station_lat, station_lon, facilities_data)

    return nearby_facilities
