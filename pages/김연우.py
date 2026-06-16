import streamlit as st
import pandas as pd
import calendar

st.set_page_config(
    page_title="2026 학사일정 캘린더",
    page_icon="📚",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #FFF9D6;
}
.day-box{
    border:1px solid #cccccc;
    border-radius:8px;
    padding:5px;
    min-height:120px;
    background:white;
}
.event{
    background:#ffe8a3;
    border-radius:5px;
    padding:2px;
    margin-top:2px;
    font-size:12px;
}
</style>
""", unsafe_allow_html=True)

DEFAULT_EVENTS = [
    ["2026-03-01","삼일절"],
    ["2026-03-02","대체공휴일(삼일절)"],
    ["2026-03-03","개학, 입학식"],
    ["2026-03-24","전국연합학력평가"],
    ["2026-03-26","교육과정 설명회"],
    ["2026-04-22","개교기념일"],
    ["2026-05-07","전국연합학력평가(3학년)"],
    ["2026-06-04","수능모의평가"],
    ["2026-07-21","방학식"],
    ["2026-08-19","개학식"],
    ["2026-09-02","수능모의평가"],
    ["2026-10-20","전국연합학력평가"],
    ["2026-11-19","대학수학능력시험"],
    ["2027-01-01","신정"],
    ["2027-01-08","종업식, 졸업식"]
]

if "events" not in st.session_state:
    st.session_state.events = pd.DataFrame(
        DEFAULT_EVENTS,
        columns=["date","title"]
    )

st.title("📚 2026 학사일정 캘린더")

with st.sidebar:
    st.header("일정 추가")

    new_date = st.date_input("날짜")
    new_title = st.text_input("일정")

    if st.button("추가"):
        if new_title.strip():
            new_row = pd.DataFrame(
                [[new_date.strftime("%Y-%m-%d"), new_title]],
                columns=["date","title"]
            )

            st.session_state.events = pd.concat(
                [st.session_state.events,new_row],
                ignore_index=True
            )

            st.success("추가 완료")

year = st.selectbox(
    "연도",
    [2026, 2027]
)

month = st.selectbox(
    "월",
    list(range(1,13)),
    index=2
)

st.subheader(f"{year}년 {month}월")

days = ["월","화","수","목","금","토","일"]

header = st.columns(7)
for i, d in enumerate(days):
    header[i].markdown(f"**{d}**")

cal = calendar.monthcalendar(year, month)

for week in cal:
    cols = st.columns(7)

    for i, day in enumerate(week):

        if day == 0:
            cols[i].write("")
            continue

        current_date = f"{year}-{month:02d}-{day:02d}"

        day_events = st.session_state.events[
            st.session_state.events["date"] == current_date
        ]

        html = f"""
        <div class='day-box'>
        <b>{day}</b>
        """

        for _, row in day_events.iterrows():
            html += f"""
            <div class='event'>
            {row['title']}
            </div>
            """

        html += "</div>"

        cols[i].markdown(
            html,
            unsafe_allow_html=True
        )

st.divider()

st.subheader("전체 일정")

st.dataframe(
    st.session_state.events.sort_values("date"),
    use_container_width=True
)
