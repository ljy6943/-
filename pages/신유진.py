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

# 2. 고정된 학생 명단 설정
INITIAL_STUDENTS = ["강민준", "김서연", "박도현", "이이지아", "정우진", "최예은", "한지후", "홍길동"]

# 3. 세션 상태(Session State) 초기화
if "attendance_db" not in st.session_state:
    st.session_state.attendance_db = pd.DataFrame({
        "이름": INITIAL_STUDENTS,
        "출결 상태": ["미지정"] * len(INITIAL_STUDENTS),
        "확인 시간": ["-"] * len(INITIAL_STUDENTS),
        "비고(사유)": [""] * len(INITIAL_STUDENTS)
    })

# 4. Gemini AI 설정 (Secrets 안전 검사 및 예외 처리)
has_api_key = False
try:
    if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        has_api_key = True
except Exception:
    # Secrets 파일이 아예 없는 로컬 환경 등에서도 에러 없이 통과하게 만듭니다.
    has_api_key = False

# --- 안전한 화면 새로고침 함수 정의 ---
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

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

attendance_rate = int((attended / total_students) * 100) if total_students > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("총원", f"{total_students}명")
col2.metric("출석", f"{attended}명")
col3.metric("지각", f"{late}명")
col4.metric("결석", f"{absent}명")
col5.metric("출석률", f"{attendance_rate}%")

st.markdown("---")

# --- 화면 레이아웃 분할 ---
sidebar_col, main_col = st.columns([1, 2])

# [좌측 영역] 출결 입력 및 수정
with sidebar_col:
    st.header("📥 출결 입력")
    
    selected_student = st.selectbox("학생 이름을 선택하세요", INITIAL_STUDENTS)
    status = st.radio("출결 상태", ["출석", "지각", "결석"])
    reason = st.text_input("비고 (지각/결석 사유 입력)", placeholder="예: 늦잠, 병원 진료 등")
    
    submit_btn = st.button("출결 저장하기", type="primary")
    
    if submit_btn:
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # 데이터프레임 업데이트
        idx = st.session_state.attendance_db[st.session_state.attendance_db["이름"] == selected_student].index[0]
        st.session_state.attendance_db.at[idx, "출결 상태"] = status
        st.session_state.attendance_db.at[idx, "확인 시간"] = current_time
        st.session_state.attendance_db.at[idx, "비고(사유)"] = reason if status != "출석" else ""
        
        st.success(f"✅ {selected_student} 학생: {status} 처리 완료!")
        safe_rerun()

# [우측 영역] 실시간 출결 현황 표
with main_col:
    st.header("📋 오늘자 출결 현황 명부")
    
    def color_status(val):
        if val == "출석": color = "#d4edda"
        elif val == "지각": color = "#fff3cd"
        elif val == "결석": color = "#f8d7da"
        else: color = "#ffffff"
        return f'background-color: {color}'
    
    # [수정 포인트] 최신 pandas 버전에 맞춰 applymap 대신 map 사용구조로 변경
    styled_df = st.session_state.attendance_db.style.map(color_status, subset=["출결 상태"])
    st.dataframe(styled_df, use_container_width=True, height=320)
    
    if st.button("🔄 오늘 출결 전체 초기화"):
        st.session_state.attendance_db = pd.DataFrame({
            "이름": INITIAL_STUDENTS,
            "출결 상태": ["미지정"] * len(INITIAL_STUDENTS),
            "확인 시간": ["-"] * len(INITIAL_STUDENTS),
            "비고(사유)": [""] * len(INITIAL_STUDENTS)
        })
        st.warning("출결
