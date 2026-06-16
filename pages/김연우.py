```python
import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar
import os

st.set_page_config(
    page_title="천안오성고 학사일정",
    page_icon="📚",
    layout="wide"
)

DATA_FILE = "schedule_data.csv"

DEFAULT_EVENTS = [
    {"date":"2026-03-01","title":"삼일절","category":"공휴일"},
    {"date":"2026-03-02","title":"대체공휴일(삼일절)","category":"공휴일"},
    {"date":"2026-03-03","title":"개학, 입학식","category":"학교행사"},
    {"date":"2026-03-24","title":"전국연합학력평가(1,2,3학년)","category":"시험"},
    {"date":"2026-03-26","title":"교육과정 설명회","category":"학교행사"},

    {"date":"2026-04-22","title":"개교기념일(오전수업)","category":"학교행사"},
    {"date":"2026-04-27","title":"1학기 1회 정기시험","category":"시험"},
    {"date":"2026-04-28","title":"1학기 1회 정기시험","category":"시험"},
    {"date":"2026-04-29","title":"1학기 1회 정기시험","category":"시험"},
    {"date":"2026-04-30","title":"1학기 1회 정기시험","category":"시험"},

    {"date":"2026-05-01","title":"재량휴업일(근로자의 날)","category":"공휴일"},
    {"date":"2026-05-04","title":"재량휴업일","category":"공휴일"},
    {"date":"2026-05-05","title":"어린이날","category":"공휴일"},
    {"date":"2026-05-07","title":"전국연합학력평가(3학년)","category":"시험"},
    {"date":"2026-05-14","title":"현장체험학습(1,2학년), 체육한마당(3학년)","category":"학교행사"},
    {"date":"2026-05-15","title":"체육한마당(1,2학년), 현장체험학습(3학년)","category":"학교행사"},
    {"date":"2026-05-25","title":"대체공휴일(부처님 오신날)","category":"공휴일"},

    {"date":"2026-06-03","title":"지방선거","category":"학교행사"},
    {"date":"2026-06-04","title":"대학수학능력시험 모의평가(3학년), 전국연합학력평가(1,2학년)","category":"시험"},
    {"date":"2026-06-30","title":"1학기 2회 정기시험","category":"시험"},
    {"date":"2026-07-01","title":"1학기 2회 정기시험","category":"시험"},
    {"date":"2026-07-02","title":"1학기 2회 정기시험","category":"시험"},
    {"date":"2026-07-03","title":"1학기 2회 정기시험","category":"시험"},

    {"date":"2026-07-08","title":"전국연합학력평가(3학년)","category":"시험"},
    {"date":"2026-07-13","title":"최소성취수준 보장지도 기간","category":"학교행사"},
    {"date":"2026-07-14","title":"최소성취수준 보장지도 기간","category":"학교행사"},
    {"date":"2026-07-15","title":"최소성취수준 보장지도 기간","category":"학교행사"},
    {"date":"2026-07-16","title":"동아리 발표회","category":"학교행사"},
    {"date":"2026-07-17","title":"제헌절","category":"공휴일"},
    {"date":"2026-07-21","title":"방학식","category":"학교행사"},

    {"date":"2026-08-17","title":"대체공휴일(광복절)","category":"공휴일"},
    {"date":"2026-08-19","title":"개학식","category":"학교행사"},

    {"date":"2026-09-02","title":"대학수학능력시험 모의평가(3학년), 전국연합학력평가(1,2학년)","category":"시험"},
    {"date":"2026-09-24","title":"추석연휴","category":"공휴일"},
    {"date":"2026-09-25","title":"추석연휴","category":"공휴일"},

    {"date":"2026-10-03","title":"개천절","category":"공휴일"},
    {"date":"2026-10-05","title":"대체공휴일(개천절)","category":"공휴일"},
    {"date":"2026-10-06","title":"2학기 1회 정기시험","category":"시험"},
    {"date":"2026-10-07","title":"2학기 1회 정기시험","category":"시험"},
    {"date":"2026-10-08","title":"2학기 1회 정기시험","category":"시험"},
    {"date":"2026-10-09","title":"한글날","category":"공휴일"},
    {"date":"2026-10-20","title":"전국연합학력평가(1,2,3학년)","category":"시험"},
    {"date":"2026-10-27","title":"수학여행(2학년)","category":"학교행사"},
    {"date":"2026-10-28","title":"수학여행(2학년)","category":"학교행사"},
    {"date":"2026-10-29","title":"수학여행(2학년)","category":"학교행사"},
    {"date":"2026-10-30","title":"수학여행(2학년), 현장체험학습(1학년)","category":"학교행사"},

    {"date":"2026-11-19","title":"대학수학능력시험","category":"시험"},
    {"date":"2026-11-20","title":"재량휴업일(대학수학능력시험)","category":"공휴일"},

    {"date":"2026-12-04","title":"현장체험학습(3학년)","category":"학교행사"},
    {"date":"2026-12-15","title":"2학기 2회 정기시험","category":"시험"},
    {"date":"2026-12-16","title":"2학기 2회 정기시험","category":"시험"},
    {"date":"2026-12-17","title":"2학기 2회 정기시험","category":"시험"},
    {"date":"2026-12-18","title":"2학기 2회 정기시험","category":"시험"},
    {"date":"2026-12-28","title":"최소성취수준 보장 지도 기간","category":"학교행사"},
    {"date":"2026-12-29","title":"최소성취수준 보장 지도 기간","category":"학교행사"},
    {"date":"2026-12-30","title":"최소성취수준 보장 지도 기간","category":"학교행사"},
    {"date":"2026-12-31","title":"최소성취수준 보장 지도 기간","category":"학교행사"},

    {"date":"2027-01-01","title":"신정","category":"공휴일"},
    {"date":"2027-01-08","title":"종업식, 졸업식","category":"학교행사"}
]

def load_data():
    try:
        if os.path.exists(DATA_FILE):
            return pd.read_csv(DATA_FILE)

        df = pd.DataFrame(DEFAULT_EVENTS)
        df.to_csv(DATA_FILE, index=False)
        return df

    except:
        return pd.DataFrame(DEFAULT_EVENTS)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

if "df" not in st.session_state:
    st.session_state.df = load_data()

df = st.session_state.df

st.title("📚 천안오성고 학사일정 캘린더")

today = date.today()

future = df.copy()
future["date"] = pd.to_datetime(future["date"])

future = future[future["date"] >= pd.Timestamp(today)]

if len(future) > 0:
    next_event = future.sort_values("date").iloc[0]
    dday = (next_event["date"].date() - today).days

    st.info(
        f"📌 다음 일정 : {next_event['title']} (D-{dday})"
    )

with st.sidebar:
    st.header("일정 추가")

    new_date = st.date_input("날짜")
    new_title = st.text_input("일정명")

    new_category = st.selectbox(
        "종류",
        ["시험","학교행사","공휴일"]
    )

    if st.button("저장"):
        if new_title:
            new_row = pd.DataFrame([{
                "date": new_date.strftime("%Y-%m-%d"),
                "title": new_title,
                "category": new_category
            }])

            st.session_state.df = pd.concat(
                [st.session_state.df,new_row],
                ignore_index=True
            )

            save_data(st.session_state.df)
            st.rerun()

year = st.number_input(
    "연도",
    2026,
    2030,
    2026
)

month = st.selectbox(
    "월",
    list(range(1,13)),
    index=2
)

colors = {
    "시험":"#ffcccc",
    "학교행사":"#ccffcc",
    "공휴일":"#cce5ff"
}

weeks = calendar.monthcalendar(year, month)

for week in weeks:
    cols = st.columns(7)

    for i, day in enumerate(week):
        if day == 0:
            cols[i].write("")
            continue

        current = f"{year}-{month:02d}-{day:02d}"

        events = df[df["date"] == current]

        html = f"<b>{day}</b><br>"

        for _, row in events.iterrows():
            html += f'''
            <div style="
            background:{colors[row["category"]]};
            padding:4px;
            margin:2px;
            border-radius:5px;">
            {row["title"]}
            </div>
            '''

        cols[i].markdown(html, unsafe_allow_html=True)

st.divider()

st.subheader("전체 일정")

st.dataframe(
    df.sort_values("date"),
    use_container_width=True
)
```

