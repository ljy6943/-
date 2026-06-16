import streamlit as st
import pandas as pd
import calendar
from datetime import date, datetime

# 1. 페이지 설정 및 테마 적용
st.set_page_config(
    page_title="우리반 알림판 - 학사일정",
    page_icon="📅",
    layout="wide"
)

# CSS를 활용한 연노랑 배경 및 달력 스타일링
st.markdown("""
<style>
.stApp {
    background-color: #FFFDE7;
}
.calendar-table {
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
}
.calendar-table th {
    background-color: #FFF59D;
    color: #424242;
    padding: 12px;
    border: 1px solid #E0E0E0;
    font-weight: bold;
    text-align: center;
}
.calendar-table td {
    height: 120px;
    vertical-align: top;
    border: 1px solid #E0E0E0;
    background-color: #FFFFFF;
    padding: 8px;
}
.day-number {
    font-weight: bold;
    font-size: 14px;
    margin-bottom: 6px;
}
.event-item {
    background-color: #FFF9C4;
    border-left: 4px solid #FBC02D;
    padding: 4px 6px;
    margin-bottom: 4px;
    border-radius: 3px;
    font-size: 12px;
    color: #212121;
    word-break: break-all;
}
</style>
""", unsafe_allow_html=True)

# 2. 세션 상태(데이터 저장소) 초기화
if "events" not in st.session_state:
    # 기본 샘플 데이터 제공
    st.session_state.events = [
        {"날짜": str(date(2026, 3, 2)), "일정": "1학기 개학식 🌸"},
        {"날짜": str(date(2026, 5, 1)), "일정": "교내 체육대회 🏃‍♂️"},
        {"날짜": str(date(2026, 7, 17)), "일정": "여름방학식 ☀️"}
    ]

# 3. 타이틀 및 D-Day 섹션
st.title("💛 우리반 학사일정 알림판")
st.caption("우리 반의 중요한 일정을 한눈에 확인하고 관리하는 공간입니다.")

# D-Day 계산 및 표시
today_str = str(date.today())
future_events = [e for e in st.session_state.events if e["날짜"] >= today_str]
if future_events:
    future_events.sort(key=lambda x: x["날짜"])
    next_event = future_events[0]
    d_day = (datetime.strptime(next_event["날짜"], "%Y-%m-%d").date() - date.today()).days
    
    if d_day == 0:
        st.info(f"🚨 **오늘의 주요 일정**: {next_event['일정']} (D-Day)")
    else:
        st.warning(f"📌 **다가오는 가장 빠른 일정**: {next_event['일정']} ({next_event['날짜']}) 까지 **D-{d_day}** 남았습니다!")

st.divider()

# 4. 사이드바: 일정 입력 및 데이터 관리
with st.sidebar:
    st.header("⚙️ 일정 관리 메뉴")
    
    # 일정 추가 서브메뉴
    with st.expander("➕ 새 일정 등록", expanded=True):
        input_date = st.date_input("날짜 선택", value=date.today())
        input_text = st.text_input("일정 내용 입력")
        
        if st.button("추가하기", use_container_width=True):
            if input_text.strip():
                st.session_state.events.append({
                    "날짜": str(input_date),
                    "일정": input_text.strip()
                })
                st.success("일정이 추가되었습니다!")
                st.rerun()
            else:
                st.error("일정 내용을 입력해주세요.")
                
    # 데이터 백업 및 복구
    with st.expander("💾 데이터 백업/복구"):
        df_all = pd.DataFrame(st.session_state.events)
        
        # 다운로드
        csv = df_all.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="CSV로 일정 백업(다운로드)",
            data=csv,
            file_name="class_schedule.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # 업로드
        uploaded_file = st.file_uploader("백업된 CSV 파일 불러오기", type=["csv"])
        if uploaded_file is not None:
            try:
                uploaded_df = pd.read_csv(uploaded_file)
                if list(uploaded_df.columns) == ["날짜", "일정"]:
                    st.session_state.events = uploaded_df.to_dict(orient="records")
                    st.success("데이터를 성공적으로 복구했습니다!")
                    st.rerun()
                else:
                    st.error("올바른 형식의 CSV 파일이 아닙니다.")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

# 5. 메인 화면: 연월 선택 및 캘린더 출력
col1, col2 = st.columns([1, 2])
with col1:
    current_year = st.selectbox("연도 선택", list(range(2025, 2031)), index=1) # 2026년 기본 선택
with col2:
    current_month = st.selectbox("월 선택", list(range(1, 13)), index=date.today().month - 1)

# 달력 데이터 생성
cal = calendar.monthcalendar(current_year, current_month)

# HTML 달력 렌더링 시작
html_code = """
<table class='calendar-table'>
<thead>
    <tr>
        <th style='color: #D32F2F;'>일</th>
        <th>월</th>
        <th>화</th>
        <th>수</th>
        <th>목</th>
        <th>금</th>
        <th style='color: #1976D2;'>토</th>
    </tr>
</thead>
<tbody>
"""

# 파이썬 달력은 월요일 시작(0)이 기본이므로, 일요일 시작(6)으로 정렬 맞추기
calendar.setfirstweekday(6)
cal = calendar.monthcalendar(current_year, current_month)

for week in cal:
    html_code += "<tr>"
    for i, day in enumerate(week):
        if day == 0:
            html_code += "<td></td>"
        else:
            # 날짜 스트링 포맷팅 (YYYY-MM-DD)
            target_date_str = f"{current_year}-{current_month:02d}-{day:02d}"
            
            # 요일별 숫자 색상 처리 (일: 빨강, 토: 파랑)
            if i == 0:
                day_style = "color: #D32F2F;"
            elif i == 6:
                day_style = "color: #1976D2;"
            else:
                day_style = "color: #212121;"
                
            html_code += f"<td><div class='day-number' style='{day_style}'>{day}</div>"
            
            # 해당 날짜의 일정 필터링 후 HTML 주입
            day_events = [e for e in st.session_state.events if e["날짜"] == target_date_str]
            for event in day_events:
                html_code += f"<div class='event-item'>{event['일정']}</div>"
                
            html_code += "</td>"
    html_code += "</tr>"

html_code += "</tbody></table>"

# 달력 출력
st.markdown(html_code, unsafe_allow_html=True)

st.divider()

# 6. 하단 전체 일정 표 및 삭제 기능
st.subheader("📋 전체 일정 리스트")
if st.session_state.events:
    df_display = pd.DataFrame(st.session_state.events)
    df_display = df_display.sort_values(by="날짜").reset_index(drop=True)
    
    # 데이터프레임 보여주기
    st.dataframe(df_display, use_container_width=True)
    
    # 일정 개별 삭제 기능
    delete_options = [f"[{item['날짜']}] {item['일정']}" for item in st.session_state.events]
    selected_delete = st.selectbox("❌ 삭제할 일정을 선택하세요", delete_options)
    
    if st.button("선택한 일정 삭제", type="primary"):
        idx = delete_options.index(selected_delete)
        deleted_item = st.session_state.events.pop(idx)
        st.success(f"'{deleted_item['일정']}' 일정이 삭제되었습니다.")
        st.rerun()
else:
    st.info("등록된 학사일정이 없습니다. 사이드바에서 새 일정을 등록해 보세요!")
