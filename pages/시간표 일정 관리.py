import streamlit as st
import pandas as pd
from datetime import date

# 1. 페이지 설정
st.set_page_config(page_title="스마트 시간표 & 일정 관리", page_icon="📅", layout="wide")

# 2. 세션 상태(Session State) 초기화 (데이터 휘발 방지)
if "timetable" not in st.session_state:
    # 기본 빈 시간표 데이터프레임 생성 (1교시 ~ 8교시)
    days = ["월요일", "화요일", "수요일", "목요일", "금요일"]
    periods = [f"{i}교시" for i in range(1, 9)]
    st.session_state.timetable = pd.DataFrame("", index=periods, columns=days)

if "todos" not in st.session_state:
    st.session_state.todos = []

# 3. 앱 타이틀 및 설명
st.title("📅 스마트 시간표 & 일정 관리자")
st.markdown("나만의 주간 시간표를 짜고, 과목별 과제와 시험 일정을 스마트하게 관리해보세요!")
st.divider()

# 4. 레이아웃 분할 (왼쪽: 입력 사이드바 / 오른쪽: 메인 화면)
with st.sidebar:
    st.header("⚙️ 데이터 입력 및 수정")
    
    # 기능 1: 시간표 등록 관리
    with st.expander("🕒 시간표 과목 등록/수정", expanded=True):
        day_input = st.selectbox("요일 선택", ["월요일", "화요일", "수요일", "목요일", "금요일"])
        period_input = st.selectbox("교시 선택", [f"{i}교시" for i in range(1, 9)])
        subject_input = st.text_input("과목명 입력", placeholder="예: 컴퓨터공학개론")
        
        if st.button("시간표에 반영하기", use_container_width=True):
            if subject_input.strip():
                st.session_state.timetable.at[period_input, day_input] = subject_input.strip()
                st.success(f"[{day_input} {period_input}]에 '{subject_input}' 등록 완료!")
                st.rerun()
            else:
                st.warning("과목명을 입력해주세요.")
                
    # 기능 2: 일정(Todo) 등록 관리
    with st.expander("📝 과제 및 시험 일정 추가", expanded=True):
        # 시간표에 등록된 고유 과목 리스트 추출 (빈 값 제외)
        registered_subjects = sorted(list(set(st.session_state.timetable.values.flatten())))
        if "" in registered_subjects:
            registered_subjects.remove("")
            
        if not registered_subjects:
            st.info("💡 일정 등록을 위해 먼저 시간표에 과목을 하나 이상 등록해주세요.")
        else:
            todo_subject = st.selectbox("연동할 과목 선택", registered_subjects)
            todo_title = st.text_input("일정 내용", placeholder="예: 중간고사, 레포트 제출")
            todo_date = st.date_input("마감일 선택", min_value=date.today())
            
            if st.button("일정 추가하기", use_container_width=True):
                if todo_title.strip():
                    new_todo = {
                        "subject": todo_subject,
                        "title": todo_title.strip(),
                        "due_date": todo_date
                    }
                    st.session_state.todos.append(new_todo)
                    st.success("새로운 일정이 추가되었습니다!")
                    st.rerun()
                else:
                    st.warning("일정 내용을 입력해주세요.")

    # 초기화 버튼
    st.divider()
    if st.button("🔄 모든 데이터 초기화", type="secondary", use_container_width=True):
        st.session_state.timetable = pd.DataFrame("", index=[f"{i}교시" for i in range(1, 9)], columns=["월요일", "화요일", "수요일", "목요일", "금요일"])
        st.session_state.todos = []
        st.toast("데이터가 초기화되었습니다.")
        st.rerun()

# 5. 메인 화면 표시
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("🗓️ 이번 학기 주간 시간표")
