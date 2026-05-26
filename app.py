import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="수행평가 알리미",
    page_icon="📚"
)

st.title("📚 수행평가 알리미")

# 수행평가 데이터
tasks = {
    "1학년": {
        "수학": {
            "내용": "함수 발표",
            "날짜": "6월 10일",
            "준비물": "PPT"
        },
        "영어": {
            "내용": "영어 에세이",
            "날짜": "6월 15일",
            "준비물": "A4 2장"
        }
    },
    "2학년": {
        "과학": {
            "내용": "실험 보고서",
            "날짜": "6월 20일",
            "준비물": "실험 사진"
        }
    }
}

# 학년 선택
grade = st.selectbox(
    "학년 선택",
    list(tasks.keys())
)

# 과목 선택
subject = st.selectbox(
    "과목 선택",
    list(tasks[grade].keys())
)

# 정보 출력
info = tasks[grade][subject]

st.subheader("📌 수행평가 정보")

st.write(f"**내용:** {info['내용']}")
st.write(f"**날짜:** {info['날짜']}")
st.write(f"**준비물:** {info['준비물']}")

st.success("정상적으로 불러왔습니다!")
