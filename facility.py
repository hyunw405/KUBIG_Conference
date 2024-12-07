import math
import pandas as pd
import requests
import app

# 지구상의 두 좌표 사이의 거리 계산 (Haversine formula)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # 지구 반지름 (km)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c * 1000  # km를 m로 변환
    return distance

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
    unique_facilities = {}
    for _, row in facilities_data.iterrows():
        facility_name = row['SVCH_FCLTY_NM']
        facility_lat = row['SVCH_FCLTY_LA']
        facility_lon = row['SVCH_FCLTY_LO']
        facility_cat = row['SVCH_FCLTY_ITEM_NM']
        distance = haversine(lat, lon, facility_lat, facility_lon)
        if distance <= radius:
            # 중복 방지를 위해 이름을 키로 사용
            if facility_name not in unique_facilities:
                unique_facilities[facility_name] = {
                    "name": facility_name,
                    "address": row['SVCH_FCLTY_ADDR'],
                    "latitude": facility_lat,
                    "longitude": facility_lon,
                    "distance": distance,
                    "category": facility_cat
                }
    return list(unique_facilities.values())

# 메인 함수
def main():
    API_KEY = "48afb747b9bf9aba1c2afe045a8ed165"  # 발급받은 REST API 키

    station_name = app.get_station_name()
    
    # 1. 지하철역 좌표 가져오기
    station_coordinates = get_station_coordinates(station_name, API_KEY)
    if not station_coordinates:
        print("지하철역의 위도와 경도를 가져오지 못했습니다.")
        return
    
    station_lat, station_lon = station_coordinates
    
    # 2. 시설 데이터 불러오기
    facilities_data = pd.read_csv('/Users/gimminjae/Downloads/스포츠강좌이용권시설인접대중교통정보.csv')

    # 3. 반경 1.5km 내 시설 검색 (중복 제거)
    nearby_facilities = find_nearby_facilities(station_lat, station_lon, facilities_data)
    
    # 4. 결과 리스트로 저장
    result_list = [
        {
            "name": facility['name'],
            "address": facility['address'],
            "latitude": facility['latitude'],
            "longitude": facility['longitude'],
            "distance": facility['distance'],
            "category": facility['category']
        }
        for facility in nearby_facilities
    ]
    
    # 5. DataFrame 형식으로 결과 출력
    if result_list:
        df = pd.DataFrame(result_list)
        print("\n[반경 1.5km 내 체육 시설 목록]")
        print(df)
    else:
        print(f"[{station_name}] 반경 1.5km 내 체육 시설이 없습니다.")

if __name__ == "__main__":
    main()
