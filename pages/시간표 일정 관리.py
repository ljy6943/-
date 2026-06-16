import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="1-7 정보 도우미", page_icon="🏫", layout="wide")

# 2. 연한 노란색 바탕 및 커스텀 스타일 지정을 위한 CSS 주입
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFDE7;
    }
    .main {
        background-color: #FFFDE7;
    }
    h1, h2, h3 {
        color: #F57F17; /* 진한 주황/노란색 계열 포인트 */
    }
    .stButton>button {
        background-color: #FBC02D;
        color: white;
        border-radius: 8px;
    }
    .css-1r6slb0 {
        background-color: #FFF9C4;
    }
    </style>
    """, unsafe_allow_stdio=True)

# 3. 세션 상태 데이터 초기화 (기본 시간표 및 변경 사항 저장)
if 'base_timetable' not in st.session_state:
    # 1학년 7반 표준 고정 시간표 예시 데이터
    periods = [f"{i}교시" for i in range(1, 8)]
    days = ["월요일", "화요일", "수요일", "목요일", "금요일"]
    data = {
        "월요일": ["국어", "수학", "영어", "과학", "체육", "미술", "미술"],
        "화요일": ["사회", "역사", "수학", "국어", "영어", "음악", "동아리"],
        "수요일": ["과학", "영어", "국어", "수학", "창체", "", ""],
        "목요일": ["수학", "과학", "사회", "영어", "기술가정", "기술가정", "진로"],
        "금요일": ["영어", "국어", "체육", "한문", "과학", "수학", "자치"]
    }
    st.session_state.base_timetable = pd.DataFrame(data, index=periods)

if 'changed_schedule' not in st.session_state:
    # 당일 변경된 시간표를 저장할 딕셔너리 (예: {"월요일": {"1교시": "자습 (대체)"}})
    st.session_state.changed_schedule = {}

if 'notices' not in st.session_state:
    st.session_state.notices = ["우유 급식 신청서 내일까지 제출", "내일 체육복 지참"]

# 4. 헤더 영역
st.title("🏫 1학년 7반 스마트 정보 도우미")
st.markdown(f"**현재 일시:** {datetime.now().strftime('%Y년 %m월 %d일')} | 우리 반의 실시간 시간표와 공지사항을 확인하세요.")
st.divider()

# 5. 메인 레이아웃 분할 (좌측: 시간표 및 변경 확인 / 우측: 알림 및 관리자 기능)
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📅 주간 기본 시간표")
    
    # 디스플레이용 데이터프레임 복사
    display_timetable = st.session_state.base_timetable.copy()
    
    # 변경된 시간표가 있다면 기존 시간표 위에 표시 및 강조 기호 추가
    has_changes = False
    if st.session_state.changed_schedule:
        for day, changes in st.session_state.changed_schedule.items():
            for period, new_subject in changes.items():
                if new_subject.strip():
                    display_timetable.at[period, day] = f"🔄 {new_subject}"
                    has_changes = True

    # 시간표 렌더링
    st.dataframe(display_timetable, use_container_width=True, height=290)
    
    # 변경 사항 알림 배너
    if has_changes:
