import streamlit as st
import pandas as pd
from datetime import date
import calendar

st.set_page_config(page_title="학사일정 캘린더", page_icon="📚", layout="wide")

# 기본 일정

DEFAULT_EVENTS = [
["2026-03-01", "삼일절", "공휴일"],
["2026-03-03", "개학, 입학식", "학교행사"],
["2026-03-24", "전국연합학력평가(1,2,3학년)", "시험"],
["2026-04-22", "개교기념일", "학교행사"],
["2026-05-07", "전국연합학력평가(3학년)", "시험"],
["2026-07-21", "방학식", "학교행사"],
["2026-08-19", "개학식", "학교행사"],
["2026-10-20", "전국연합학력평가(1,2,3학년)", "시험"],
["2026-11-19", "대학수학능력시험", "시험"],
["2027-01-08", "종업식, 졸업식", "학교행사"],
]

if "events" not in st.session_state:
st.session_state.events = pd.DataFrame(
DEFAULT_EVENTS,
columns=["date", "title", "category"]
)

st.title("📚 학급 학사일정 캘린더")

with st.sidebar:
st.header("일정 추가")

```
new_date = st.date_input("날짜", value=date.today())
new_title = st.text_input("일정명")
new_category = st.selectbox(
    "종류",
    ["시험", "학교행사", "공휴일"]
)

if st.button("추가"):
    if new_title.strip():
        new_row = pd.DataFrame(
            [[new_date.strftime("%Y-%m-%d"), new_title, new_category]],
            columns=["date", "title", "category"]
        )

        st.session_state.events = pd.concat(
            [st.session_state.events, new_row],
            ignore_index=True
        )
        st.success("일정이 추가되었습니다.")
```

year = st.selectbox("연도", [2026, 2027])
month = st.selectbox("월", list(range(1, 13)), index=2)

colors = {
"시험": "#ffcccc",
"학교행사": "#ccffcc",
"공휴일": "#cce5ff"
}

weeks = calendar.monthcalendar(year, month)

for week in weeks:
cols = st.columns(7)

```
for i, day in enumerate(week):
    if day == 0:
        cols[i].write("")
        continue

    current_date = f"{year}-{month:02d}-{day:02d}"

    events = st.session_state.events[
        st.session_state.events["date"] == current_date
    ]

    html = f"<b>{day}</b><br>"

    for _, row in events.iterrows():
        html += (
            f"<div style='background:{colors[row['category']]};"
            f"padding:4px;margin:2px;border-radius:5px;'>"
            f"{row['title']}</div>"
        )

    cols[i].markdown(html, unsafe_allow_html=True)
```

st.subheader("전체 일정")

st.dataframe(
st.session_state.events.sort_values("date"),
use_container_width=True
)
