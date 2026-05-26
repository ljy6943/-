import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="수행평가 알리미",
    page_icon="📚",
    layout="centered"
)

# 제목
st.title("📚 수행평가 알리미")
st.write("학년과 과목을 선택하세요.")

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
    },

    "3학년": {
        "국어": {
            "내용": "독서 감상문",
            "날짜": "6월 25일",
            "준비물": "독서 노트"
        },
        "사회": {
            "내용": "토론 발표",
            "날짜": "6월 28일",
            "준비물": "발표 자료"
        }
    }
}

# 학년 선택
grade = st.selectbox(
    "학년 선택",
    list(tasks.keys())
)

# 과목 목록 가져오기
subjects = list(tasks[grade].keys())

# 과목이 있는지 확인
if subjects:

    # 과목 선택
    subject = st.selectbox(
        "과목 선택",
        subjects
    )

    # 버튼
    if st.button("수행평가 확인하기"):

        info = tasks[grade][subject]

        st.subheader("📌 수행평가 정보")

        st.write(f"**과목:** {subject}")
        st.write(f"**내용:** {info['내용']}")
        st.write(f"**날짜:** {info['날짜']}")
        st.write(f"**준비물:** {info['준비물']}")

        st.success("정상적으로 불러왔습니다!")

else:
    st.error("등록된 과목이 없습니다.")
