import streamlit as st
import pandas as pd
from datetime import datetime
import google.generativeai as genai

# 1. 페이지 설정 및 배경색(연한 노란색) 적용
st.set_page_config(page_title="햇살 학급 출결 시스템", page_icon="☀️", layout="wide")

# CSS를 이용한 배경색 및 스타일 설정
st.markdown(f"""
    <style>
    .stApp {{
        background-color: #FFFDE7;
    }}
    .main-title {{
        color: #FBC02D;
        text-align: center;
        font-family: 'Nanum Gothic', sans-serif;
    }}
    </style>
    """, unsafe_allow_html=True)

# 2. 세션 상태 초기화 (데이터 유지)
if 'student_data' not in st.session_state:
    # 샘플 학생 명단
    initial_students = ["강민준", "김서연", "박도현", "이이지아", "정우진", "최예은", "한지후", "홍길동"]
    st.session_state.student_data = pd.DataFrame({
        "이름": initial_students,
        "상태": ["미지정"] * len(initial_students),
        "시간": ["-"] * len(initial_students),
        "사유": [""] * len(initial_students)
    })

# 3. AI 설정 (Gemini)
def get_ai_summary(df):
    try:
        if "GEMINI_API_KEY" not in st.secrets:
            return "API 키가 설정되지 않았습니다. Secrets 설정을 확인해주세요."
        
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-1.5-flash") # 최신 안정 버전 사용
        
        # 특이사항(지각, 결석)만 추출
        issues = df[df["상태"].isin(["지각", "결석"])]
        if issues.empty:
            return "오늘 모든 학생이 출석했거나 특이사항이 없습니다. 좋은 아침입니다!"
            
        context = issues.to_string(index=False)
        prompt = f"다음은 오늘 아침 학급 출결 현황이야. 지각이나 결석 사유를 요약해서 선생님께 드릴 짧은 학급 브리핑을 작성해줘:\n{context}"
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI 분석 중 오류가 발생했습니다: {str(e)}"

# --- 메인 화면 구성 ---
st.markdown("<h1 class='main-title'>☀️ 햇살 학급 아침 조례 시스템</h1>", unsafe_allow_html=True)
today = datetime.now().strftime("%Y년 %m월 %d일")
st.write(f"<p style='text-align:center;'><b>{today}</b></p>", unsafe_allow_html=True)

# 4. 통계 섹션
data = st.session_state.student_data
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("총원", len(data))
with col2: st.metric("출석", len(data[data["상태"] == "출석"]))
with col3: st.metric("지각", len(data[data["상태"] == "지각"]), delta_color="inverse")
with col4: st.metric("결석", len(data[data["상태"] == "결석"]), delta_color="inverse")

st.divider()

# 5. 입력 및 테이블 섹션
left_col, right_col = st.columns([1, 2])

with left_col:
    st.subheader("📥 출결 기록")
    with st.form("attendance_form", clear_on_submit=True):
        name = st.selectbox("학생 선택", data["이름"])
        status = st.radio("상태", ["출석
