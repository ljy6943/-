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
        st.warning("출결 현황이 모두 초기화되었습니다.")
        safe_rerun()

st.markdown("---")

# --- [선택] AI 사유 브리핑 기능 ---
st.header("🤖 AI 오늘의 출결 요약 브리핑")

if has_api_key:
    issue_df = df[df["출결 상태"].isin(["지각", "결석"])]
    
    if len(issue_df) > 0:
        if st.button("✨ AI 브리핑 생성하기"):
            with st.spinner("AI가 오늘의 특이사항을 분석 중입니다..."):
                try:
                    summary_text = ""
                    for _, row in issue_df.iterrows():
                        summary_text += f"- {row['이름']} ({row['출결 상태']}): {row['비고(사유)'] if row['비고(사유)'] else '사유 미기재'}\n"
                    
                    model = genai.GenerativeModel("gemini-2.5-flash-lite")
                    prompt = f"""
                    당신은 학급의 담임선생님을 돕는 AI 비서입니다. 
                    아래의 학생들의 지각 및 결석 명단을 바탕으로, 오늘 학급의 출결 특이사항을 담임선생님께 보고하듯 다정하고 깔끔하게 2~3문장으로 요약해 주세요.
                    
                    [명단]
                    {summary_text}
                    """
                    response = model.generate_content(prompt)
                    st.info(response.text)
                except Exception as e:
                    st.error(f"AI 요약 중 오류가 발생했습니다: {e}")
    else:
        st.write("모든 학생이 출석했거나 특이사항(지각/결석)이 없어 AI 브리핑이 필요하지 않습니다. 🎉")
else:
    st.warning("⚠️ AI 요약 기능을 사용하려면 Streamlit Cloud의 Secrets에 'GEMINI_API_KEY'를 등록해 주세요. (현재는 비활성화 상태이며 기본 출결 기능은 정상 작동합니다.)")
