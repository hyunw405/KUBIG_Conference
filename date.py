import os
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

# API 키 로드

# load .env file

load_dotenv()

key = os.getenv('API_KEY')

# 운동 추천 함수
def recommend_exercise(height, weight, age_group, favorite_exercise, partner_favorite_exercise):
    client = OpenAI(
    api_key = key,
)

    # 사용자 입력 기반 프롬프트 생성
    prompt = f"""
    사용자와 연인이 함께 할 수 있는 운동을 추천해주세요. 
    고려사항은 아래와 같습니다:

    1. 사용자 키: {height}cm, 몸무게: {weight}kg
    2. 연령대: {age_group}
    3. 사용자 선호 운동: {favorite_exercise}
    4. 연인의 선호 운동: {partner_favorite_exercise}
    
    조건:
    - 데이트로 적합한 운동일 것.
    - 신체 정보와 연령대를 고려해 너무 과격하지 않으면서 즐거운 활동일 것.
    - 추천 결과는 간단히 제목과 이유를 나열.
    - 예시 형식: "운동명: 간단한 설명"
    """
    try:
        # OpenAI API 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"추천 중 오류가 발생했습니다: {e}"

# Streamlit 애플리케이션
def main():
    st.title("데이트 운동 추천기")
    st.write("사용자와 연인의 정보를 입력해보세요. 데이트로 적합한 운동을 추천해드립니다!")

    # 사용자 입력 받기
    height = st.number_input("사용자의 키 (cm)", min_value=100, max_value=250, step=1)
    weight = st.number_input("사용자의 몸무게 (kg)", min_value=30, max_value=200, step=1)
    age_group = st.selectbox("사용자의 연령대", ["10대", "20대", "30대", "40대", "50대 이상"])
    favorite_exercise = st.text_input("사용자가 좋아하는 운동 (예: 요가, 조깅)")
    partner_favorite_exercise = st.text_input("연인이 좋아하는 운동 (예: 테니스, 사이클)")

    # 운동 추천 버튼
    if st.button("운동 추천받기"):
        if not (height and weight and age_group and favorite_exercise and partner_favorite_exercise):
            st.warning("모든 정보를 입력해주세요!")
        else:
            recommendations = recommend_exercise(height, weight, age_group, favorite_exercise, partner_favorite_exercise)
            st.subheader("추천 결과")
            st.write(recommendations)

# 실행
if __name__ == "__main__":
    main()
