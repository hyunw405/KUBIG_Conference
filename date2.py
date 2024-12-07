import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
from difflib import SequenceMatcher

# CSV 파일 경로
file_path = r'C:\Users\hwpte\Downloads\안암역_nearby_facilities.csv'

# CSV 파일 읽기
data = pd.read_csv(file_path, encoding ='cp949')

# 시설 이름과 카테고리 추출
facilities = data[['name', 'category']]

# API 키 로드
load_dotenv()
key = os.getenv('API_KEY')

# OpenAI 객체 초기화
client = OpenAI(api_key=key)

# 문자열 유사도 계산 함수
def calculate_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

# 운동 추천 함수
def recommend_exercise(age_group, favorite_exercise, partner_favorite_exercise):
    prompt = f"""
    사용자와 연인이 함께 할 수 있는 운동을 추천해주세요. 
    고려사항은 아래와 같습니다:
    1. 연령대: {age_group}
    2. 사용자 선호 운동: {favorite_exercise} 
    3. 연인의 선호 운동: {partner_favorite_exercise}
    
    조건:
    - 데이트로 적합한 운동일 것.
    - 연령대를 고려해 너무 과격하지 않으면서 즐거운 활동일 것.
    - 추천 결과는 간단히 제목과 이유를 나열.
    - 예시 형식: "운동명: 간단한 설명"
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"추천 중 오류가 발생했습니다: {e}"

# 시설 추천 함수
def recommend_facility(recommended_activity, facilities):
    facilities_copy = facilities.copy()
    facilities_copy['similarity'] = facilities_copy['category'].apply(
        lambda x: calculate_similarity(recommended_activity, x)
    )
    best_match = facilities_copy.sort_values(by='similarity', ascending=False).iloc[0]
    if best_match['similarity'] > 0.5:
        return best_match[['name', 'category']]
    else:
        return "유사한 시설을 찾을 수 없습니다."

# Streamlit 애플리케이션
def main():
    st.title("데이트 운동 및 시설 추천기")
    st.write("사용자와 연인의 정보를 입력해보세요. 적합한 운동과 주변 시설을 추천해드립니다!")

    age_group = st.selectbox("사용자의 연령대", ["10대", "20대", "30대", "40대", "50대 이상"])
    favorite_exercise = st.text_input("사용자가 좋아하는 운동 (예: 요가, 조깅)")
    partner_favorite_exercise = st.text_input("연인이 좋아하는 운동 (예: 테니스, 사이클)")

    if st.button("운동 및 시설 추천받기"):
        if not (age_group and favorite_exercise and partner_favorite_exercise):
            st.warning("모든 정보를 입력해주세요!")
        else:
            recommendations = recommend_exercise(age_group, favorite_exercise, partner_favorite_exercise)
            st.subheader("추천 운동")
            st.write(recommendations)

            recommended_activity = recommendations.split(":")[0].strip()
            facility = recommend_facility(recommended_activity, facilities)
            st.subheader("추천 시설")
            if isinstance(facility, pd.Series):
                st.write(f"시설 이름: {facility['name']}, 카테고리: {facility['category']}")
            else:
                st.write(facility)

if __name__ == "__main__":
    main()

