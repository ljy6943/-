import streamlit as st
import pandas as pd
import calendar
from datetime import date

st.set_page_config(
    page_title="학급 학사일정",
    page_icon="📚",
    layout="wide"
)

# 연노랑 배경
st.markdown("""
<style>
.stApp {
    background-color: #FFF9C4;
}

.calendar-table {
    width:100%;
    border-collapse:collapse;
    text-align:center;
}

.calendar-table th {
    background:#FFD54F;
    padding:10px;
    border:1px solid #999;
}

.calendar-table td {
    height:110px;
    vertical-align:top;
    border:1px solid #999;
    background:white;
    padding:5px;
}

.day-number{
    font-weight:bold;
    color:#333;
}

.event{
    margin-top:5px;
    background:#FFF176;
    border-radius:5px;
    padding:3px;
    font-size:13px;
}
</style>
""", unsafe_allow_html=True)

st.title("📚 우리 반 학사일정 캘린더")

# 세션 상태
if "events" not in st.session_state:
    st.session_state.events = {}

# 일정 추가
with st.expander("➕ 일정 추가", expanded=True):
    col1, col2 = st.columns([1, 3])

    with col1:
        selected_date = st.date_input(
            "날짜 선택",
            value=date.today()
        )

    with col2:
        event_text = st.text_input("일정 내용")

    if st.button("일정 추가"):
        try:
            if event_text.strip():
                key = str(selected_date)

                if key not in st.session_state.events:
                    st.session_state.events[key] = []

                st.session_state.events[key].append(event_text)

                st.success("일정이 추가되었습니다.")
            else:
                st.warning("일정을 입력하세요.")
        except Exception as e:
            st.error(f"오류 발생: {e}")

# 월 선택
today = date.today()

year = st.selectbox(
    "연도",
    list(range(today.year - 1, today.year + 5)),
    index=1
)

month = st.selectbox(
    "월",
    list(range(1, 13)),
    index=today.month - 1
)

st.subheader(f"📅 {year}년 {month}월")

# 달력 생성
cal = calendar.monthcalendar(year, month)

html = """
<table class='calendar-table'>
<tr>
<th>월</th>
<th>화</th>
<th>수</th>
<th>목</th>
<th>금</th>
<th>토</th>
<th>일</th>
</tr>
"""

for week in cal:
    html += "<tr>"

    for day in week:
        if day == 0:
            html += "<td></td>"
        else:
            date_key = f"{year}-{month:02d}-{day:02d}"

            event_html = ""

            if date_key in st.session_state.events:
                for e in st.session_state.events[date_key]:
                    event_html += f"<div class='event'>{e}</div>"

            html += f"""
            <td>
            <div class='day-number'>{day}</div>
            {event_html}
            </td>
            """

    html += "</tr>"

html += "</table>"

st.markdown(html, unsafe_allow_html=True)

st.divider()

# 일정 목록
st.subheader("📝 등록된 일정")

if st.session_state.events:

    rows = []

    for d, events in st.session_state.events.items():
        for e in events:
            rows.append([d, e])

    df = pd.DataFrame(rows, columns=["날짜", "일정"])

    st.dataframe(
        df,
        use_container_width=True
    )

    delete_date = st.selectbox(
        "삭제할 날짜 선택",
        sorted(st.session_state.events.keys())
    )

    if st.button("해당 날짜 일정 삭제"):
        try:
            del st.session_state.events[delete_date]
            st.success("삭제 완료")
            st.rerun()
        except:
            st.error("삭제 실패")

    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        "📥 일정 CSV 다운로드",
        csv,
        file_name="학사일정.csv",
        mime="text/csv"
    )

else:
    st.info("등록된 일정이 없습니다.")
