import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
import facility

# OpenAI 객체 초기화
load_dotenv()
key = os.getenv('API_KEY')
client = OpenAI(api_key=key)

# Streamlit 애플리케이션
def main():
    st.title("데이트 운동 및 시설 추천기")
    st.write("사용자와 연인의 정보를 입력해보세요. 적합한 운동과 주변 시설을 추천해드립니다!")

    # 사용자 입력
    age_group = st.selectbox("사용자의 연령대", ["10대", "20대", "30대", "40대", "50대 이상"])
    favorite_exercise = st.text_input("사용자가 좋아하는 운동 (예: 요가, 조깅)")
    partner_favorite_exercise = st.text_input("연인이 좋아하는 운동 (예: 테니스, 사이클)")
    station_name = st.text_input("추천받을 위치 주변 지하철역을 입력해주세요")

    if st.button("운동 및 시설 추천받기"):
        if not (age_group and favorite_exercise and partner_favorite_exercise and station_name):
            st.warning("모든 정보를 입력해주세요!")
        else:
            # 운동 추천
            recommendations = recommend_exercise(age_group, favorite_exercise, partner_favorite_exercise)
            st.subheader("추천 운동")
            st.write(recommendations)

            # facility.py에서 station_name 기반 데이터프레임 가져오기
            result_df = facility.main(station_name)
            st.subheader("추천 시설")
            if not result_df.empty:
                st.write(result_df)
            else:
                st.write(f"{station_name} 근처에 추천할 시설이 없습니다.")

# OpenAI를 통한 운동 추천 함수
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


if __name__ == "__main__":
    main()
