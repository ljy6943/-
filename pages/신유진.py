import streamlit as st
import pandas as pd
from datetime import datetime
import google.generativeai as genai

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="아침 조례 출결 시스템",
    page_icon="☀️",
    layout="wide"
)

# 2. 고정된 학생 명단 설정 (원하는 이름으로 변경 가능)
INITIAL_STUDENTS = ["강민준", "김서연", "박도현", "이이지아", "정우진", "최예은", "한지후", "홍길동"]

# 3. 세션 상태(Session State) 초기화 (앱이 새로고침되어도 데이터 유지)
if "attendance_db" not in st.session_state:
    # 초기 데이터셋 생성 (모든 학생 '미지정')
    st.session_state.attendance_db = pd.DataFrame({
        "이름": INITIAL_STUDENTS,
        "출결 상태": ["미지정"] * len(INITIAL_STUDENTS),
        "확인 시간": ["-"] * len(INITIAL_STUDENTS),
        "비고(사유)": [""] * len(INITIAL_STUDENTS)
    })

# 4. Gemini AI 설정 (Secrets에 키가 등록되어 있는 경우에만 활성화)
has_api_key = "GEMINI_API_KEY" in st.secrets
if has_api_key:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- 메인 화면 타이틀 ---
st.title("☀️ 아침 조례 출결 확인 시스템")
today_str = datetime.now().strftime("%Y년 %m월 %d일")
st.subheader(f"📅 오늘 날짜: {today_str}")
st.markdown("---")

# --- 통계 대시보드 ---
df = st.session_state.attendance_db
total_students = len(df)
attended = len(df[df["출결 상태"] == "출석"])
late = len(df[df["출결 상태"] == "지각"])
absent = len(df[df["출결 상태"] == "결석"])
undecided = len(df[df["출결 상태"] == "미지정"])

# 출석률 계산
attendance_rate = int((attended / total_students) * 100) if total_students > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("총원", f"{total_students}명")
col2.metric("출석", f"{attended}명", delta=f"+{attended}" if attended > 0 else None)
col3.metric("지각", f"{late}명", delta=f"-{late}" if late > 0 else None, delta_color="inverse")
col4.metric("결석", f"{absent}명", delta=f"-{absent}" if absent > 0 else None, delta_color="inverse")
col5.metric("출석률", f"{attendance_rate}%")

st.markdown("---")

# --- 화면 레이아웃 분할 ---
sidebar_col, main_col = st.columns
