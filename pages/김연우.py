import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="2026 학사일정",
    page_icon="📚",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #FFF9D6;
}
</style>
""", unsafe_allow_html=True)

st.title("📚 2026 학사일정 캘린더")

default_data = [
    ["2026-03-01", "삼일절"],
    ["2026-03-02", "대체공휴일(삼일절)"],
    ["2026-03-03", "개학, 입학식"],
    ["2026-03-24", "전국연합학력평가(1,2,3학년)"],
    ["2026-03-26", "교육과정 설명회"],
    ["2026-04-22", "개교기념일(오전수업)"],
    ["2026-05-07", "전국연합학력평가(3학년)"],
    ["2026-06-04", "대학수학능력시험 모의평가(3학년), 전국연합학력평가(1,2학년)"],
    ["2026-07-08", "전국연합학력평가(3학년)"],
    ["2026-07-21", "방학식"],
    ["2026-08-19", "개학식"],
    ["2026-09-02", "대학수학능력시험 모의평가(3학년), 전국연합학력평가(1,2학년)"],
    ["2026-10-20", "전국연합학력평가(1,2,3학년)"],
    ["2026-11-19", "대학수학능력시험"],
    ["2027-01-01", "신정"],
    ["2027-01-08", "종업식, 졸업식"]
]

if "schedule" not in st.session_state:
    st.session_state.schedule = pd.DataFrame(
        default_data,
        columns=["날짜", "일정"]
    )

st.sidebar.header("일정 추가")

new_date = st.sidebar.date_input("날짜")
new_event = st.sidebar.text_input("일정 내용")

if st.sidebar.button("추가"):
    if new_event.strip():
        new_row = pd.DataFrame(
            [[str(new_date), new_event]],
            columns=["날짜", "일정"]
        )

        st.session_state.schedule = pd.concat(
            [st.session_state.schedule, new_row],
            ignore_index=True
        )

        st.sidebar.success("일정 추가 완료")

st.subheader("📅 학사일정")

st.dataframe(
    st.session_state.schedule.sort_values("날짜"),
    use_container_width=True
)

st.info("사이드바에서 새로운 일정을 추가할 수 있습니다.")
