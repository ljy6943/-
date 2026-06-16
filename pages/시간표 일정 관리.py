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
        color: #F57F17;
    }
    .stButton>button {
        background-color: #FBC02D;
        color: white;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_stdio=True)

# 3. 세션 상태 데이터 초기화
if 'base_timetable' not in st.session_state:
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
    st.session_state.changed_schedule = {}

if 'notices' not in st.session_state:
    st.session_state.notices = ["우유 급식 신청서 내일까지 제출", "내일 체육복 지참"]

# 4. 헤더 영역
st.title("🏫 1학년 7반 스마트 정보 도우미")
st.markdown(f"**현재 일시:** {datetime.now().strftime('%Y년 %m월 %d일')} | 우리 반의 실시간 시간표와 공지사항을 확인하세요.")
st.divider()

# 5. 메인 레이아웃 분할
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📅 주간 기본 시간표")
    
    # 디스플레이용 데이터프레임 복사 및 변경 사항 반영
    display_timetable = st.session_state.base_timetable.copy()
    has_changes = False
    
    if st.session_state.changed_schedule:
        for day, changes in st.session_state.changed_schedule.items():
            for period, new_subject in changes.items():
                if new_subject.strip():
                    display_timetable.at[period, day] = f"🔄 {new_subject}"
                    has_changes = True

    # 시간표 출력
    st.dataframe(display_timetable, use_container_width=True, height=290)
    
    # 변경 사항 알림 배너
    if has_changes:
        st.error("⚠️ [알림] 오늘 또는 이번 주 변경된 시간표가 반영되어 있습니다 (🔄 표시 확인).")
    else:
        st.success("✅ 현재 변경 사항 없는 정상 시간표입니다.")

with col2:
    st.subheader("📢 오늘의 학급 전달사항")
    if st.session_state.notices:
        for note in st.session_state.notices:
            st.info(f"📌 {note}")
    else:
        st.write("공지사항이 없습니다.")
        
    st.divider()
    
    # 관리자 기능 (텍스트 들여쓰기 정밀 정렬)
    with st.expander("🛠️ 정보 도우미/관리자 전용 설정"):
        st.write("당일 변동된 시간표나 공지사항을 등록할 수 있습니다.")
        tab_time, tab_note = st.tabs(["시간표 변경", "공지 추가"])
        
        with tab_time:
            c_day = st.selectbox("변경 요일", ["월요일", "화요일", "수요일", "목요일", "금요일"])
            c_period = st.selectbox("변경 교시", [f"{i}교시" for i in range(1, 8)])
            c_subject = st.text_input("변경될 과목명", placeholder="예: 자습, 수학(대체)")
            
            if st.button("변경 사항 저장", use_container_width=True):
                if c_day not in st.session_state.changed_schedule:
                    st.session_state.changed_schedule[c_day] = {}
                st.session_state.changed_schedule[c_day][c_period] = c_subject
                st.toast("시간표 변경 사항이 반영되었습니다.")
                st.rerun()
                
            if st.button("🔄 변경 기록 모두 초기화", type="secondary", use_container_width=True):
                st.session_state.changed_schedule = {}
                st.toast("모든 변경 사항이 초기화되었습니다.")
                st.rerun()
                
        with tab_note:
            new_note = st.text_input("새로운 공지사항 입력")
            if st.button("공지 추가", use_container_width=True):
                if new_note.strip():
                    st.session_state.notices.append(new_note.strip())
                    st.rerun()
            if st.button("❌ 공지사항 전체 삭제", type="secondary", use_container_width=True):
                st.session_state.notices = []
                st.rerun()
