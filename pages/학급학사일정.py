import streamlit as st
import pandas as pd
import calendar
from datetime import date

# 1. 페이지 설정
st.set_page_config(
    page_title="학급 학사일정",
    page_icon="📚",
    layout="wide"
)

# 2. 스타일 시트 (연노랑 테마)
st.markdown("""
<style>
.stApp {
    background-color: #FFF9C4;
}
.calendar-table {
    width: 100%;
    border-collapse: collapse;
    text-align: center;
    table-layout: fixed; /* 셀 너비를 균등하게 고정 */
}
.calendar-table th {
    background: #FFD54F;
    padding: 10px;
    border: 1px solid #999;
    font-weight: bold;
}
.calendar-table td {
    height: 110px;
    vertical-align: top;
    border: 1px solid #999;
    background: white;
    padding: 5px;
}
.day-number {
    font-weight: bold;
    color: #333;
    text-align: left;
    margin-bottom: 5px;
}
.event {
    margin-top: 5px;
    background: #FFF176;
    border-radius: 5px;
    padding: 3px;
    font-size: 13px;
    text-align: left;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
</style>
""", unsafe_allow_html=True)

st.title("📚 우리 반 학사일정 캘린더")

# 3. 세션 상태 초기화
if "events" not in st.session_state:
    st.session_state.events = {}

# 4. 일정 추가 섹션
with st.expander("➕ 일정 추가", expanded=False): # 기본적으로 접어두어 깔끔하게 유지
    col1, col2 = st.columns([1, 3])

    with col1:
        selected_date = st.date_input("날짜 선택", value=date.today())

    with col2:
        event_text = st.text_input("일정 내용", placeholder="예: 중간고사, 소풍")

    if st.button("일정 추가", use_container_width=True):
        if event_text.strip():
            key = str(selected_date)
            if key not in st.session_state.events:
                st.session_state.events[key] = []
            
            st.session_state.events[key].append(event_text.strip())
            st.success("일정이 추가되었습니다.")
            st.rerun() # 추가 즉시 달력 갱신
        else:
            st.warning("일정 내용을 입력해주세요.")

# 5. 조회 연월 선택
today = date.today()

col_yr, col_mo = st.columns(2)
with col_yr:
    year = st.selectbox(
        "연도",
        list(range(today.year - 1, today.year + 5)),
        index=1 # 기본적으로 올해 선택 (range 구성상 index=1이 올해가 됨)
    )
with col_mo:
    month = st.selectbox(
        "월",
        list(range(1, 13)),
        index=today.month - 1
    )

st.subheader(f"📅 {year}년 {month}월")

# 6. 달력 HTML 생성 (calendar.monthcalendar는 기본적으로 월요일 시작)
cal = calendar.monthcalendar(year, month)

html = """
<table class='calendar-table'>
<tr>
    <th style='color: #1976D2;'>월</th>
    <th>화</th>
    <th>수</th>
    <th>목</th>
    <th>금</th>
    <th style='color: #388E3C;'>토</th>
    <th style='color: #D32F2F;'>일</th>
</tr>
"""

for week in cal:
    html += "<tr>"
    for day in week:
        if day == 0:
            html += "<td></td>"
        else:
            # 딕셔너리 키 포맷 일치 (YYYY-MM-DD)
            date_key = f"{year}-{month:02d}-{day:02d}"
            event_html = ""

            if date_key in st.session_state.events:
                for e in st.session_state.events[date_key]:
                    event_html += f"<div class='event' title='{e}'>{e}</div>"

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

# 7. 등록된 일정 관리 및 다운로드
st.subheader("📝 등록된 일정 관리")

if st.session_state.events:
    rows = []
    for d, events in sorted(st.session_state.events.items()):
        for e in events:
            rows.append([d, e])

    if rows:
        df = pd.DataFrame(rows, columns=["날짜", "일정"])
        st.dataframe(df, use_container_width=True, hide_index=True)

        # 수정된 삭제 기능 (날짜별이 아닌 전체에서 선택하거나, 깔끔하게 키 삭제)
        col_del, col_btn = st.columns([3, 1])
        with col_del:
            delete_date = st.selectbox(
                "삭제할 날짜 선택",
                sorted(st.session_state.events.keys()),
                key="del_select"
            )
        with col_btn:
            st.write("") # 레이아웃 맞추기용 공백
            st.write("") 
            if st.button("해당 날짜 전체 삭제", use_container_width=True):
                if delete_date in st.session_state.events:
                    del st.session_state.events[delete_date]
                    st.success(f"{delete_date} 일정이 삭제되었습니다.")
                    st.rerun()

        # CSV 다운로드
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "📥 전체 일정 CSV 다운로드",
            csv,
            file_name=f"학사일정_{year}_{month}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("등록된 일정이 없습니다.")
else:
    st.info("등록된 일정이 없습니다.")
