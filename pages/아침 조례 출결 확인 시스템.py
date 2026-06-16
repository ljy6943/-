import streamlit as st
import pandas as pd
from datetime import datetime
import google.generativeai as genai

# ==========================================
# 1. 페이지 기본 설정 및 연한 노란색 테마 적용
# ==========================================
st.set_page_config(
    page_title="따뜻한 아침 조례 시스템",
    page_icon="☀️",
    layout="wide"
)

# 사용자 요청 반영: 전체 배경 연한 노란색(#FFFDE7) 지정 및 가독성을 위한 컴포넌트 스타일링
st.markdown("""
    <style>
    /* 전체 앱 배경색 */
    .stApp {
        background-color: #FFFDE7;
    }
    /* 입력 폼 및 컨테이너 배경을 흰색으로 하여 가독성 확보 */
    div[data-testid="stForm"], .stDataFrame {
        background-color: #FFFFFF !important;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    /* 제목 스타일 */
    h1, h2, h3 {
        color: #FBC02D !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 데이터 초기화 및 세션 상태 관리
# ==========================================
INITIAL_STUDENTS = ["강민준", "김서연", "박도현", "이이지아", "정우진", "최예은", "한지후", "홍길동"]

if "attendance_db" not in st.session_state:
    st.session_state.attendance_db = pd.DataFrame({
        "이름": INITIAL_STUDENTS,
        "출결 상태": ["미지정"] * len(INITIAL_STUDENTS),
        "확인 시간": ["-"] * len(INITIAL_STUDENTS),
        "비고(사유)": [""] * len(INITIAL_STUDENTS)
    })

# ==========================================
# 3. 안전한 내장 함수 (구버전 호환용 호환성 확보)
# ==========================================
def safe_rerun():
    """Streamlit 버전에 상관없이 안전하게 새로고침을 수행합니다."""
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

# ==========================================
# 4. 메인 대시보드 레이아웃
# ==========================================
st.title("☀️ 햇살 가득한 아침 조례 출결 시스템")
today_str = datetime.now().strftime("%Y년 %m월 %d일")
st.subheader(f"📅 오늘 날짜: {today_str}")
st.markdown("---")

# 실시간 데이터 집계
df = st.session_state.attendance_db
total_students = len(df)
attended = len(df[df["출결 상태"] == "출석"])
late = len(df[df["출결 상태"] == "지각"])
absent = len(df[df["출결 상태"] == "결석"])
attendance_rate = int((attended / total_students) * 100) if total_students > 0 else 0

# 통계 위젯 배치
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("학급 총원", f"{total_students}명")
col2.metric("출석 인원", f"{attended}명")
col3.metric("지각", f"{late}명")
col4.metric("결석", f"{absent}명")
col5.metric("현재 출석률", f"{attendance_rate}%")

st.markdown("---")

# ==========================================
# 5. 좌측 입력부 / 우측 출력부 분할
# ==========================================
left_col, right_col = st.columns([1, 2])

# [좌측] 출결 입력 폼
with left_col:
    st.header("📥 출결 기록하기")
    
    with st.form("attendance_form", clear_on_submit=False):
        selected_student = st.selectbox("학생 이름을 선택하세요", INITIAL_STUDENTS)
        status = st.radio("출결 상태 선택", ["출석", "지각", "결석"], horizontal=True)
        reason = st.text_input("비고 (지각/결석 사유)", placeholder="예: 늦잠, 병원 진료 등")
        
        submit_btn = st.form_submit_button("체크 완료", type="primary")
        
        if submit_btn:
            current_time = datetime.now().strftime("%H:%M:%S")
            idx = st.session_state.attendance_db[st.session_state.attendance_db["이름"] == selected_student].index[0]
            
            # 데이터프레임 안전 업데이트
            st.session_state.attendance_db.at[idx, "출결 상태"] = status
            st.session_state.attendance_db.at[idx, "확인 시간"] = current_time
            st.session_state.attendance_db.at[idx, "비고(사유)"] = reason if status != "출석" else ""
            
            st.success(f"✅ {selected_student} 학생 -> {status} 처리되었습니다.")
            safe_rerun()

# [우측] 실시간 현황 테이블
with right_col:
    st.header("📋 오늘자 출결 현황 명부")
    
    def color_status(val):
        """출결 상태에 따라 행 색상을 변경하는 안전한 함수"""
        if val == "출석": return 'background-color: #d4edda; color: #155724;' # 연두
        elif val == "지각": return 'background-color: #fff3cd; color: #856404;' # 연노랑
        elif val == "결석": return 'background-color: #f8d7da; color: #721c24;' # 연분홍
        return ''

    try:
        # 최신 Pandas와 구버전 Pandas 모두 호환되도록 스타일 지정
        if hasattr(df.style, "map"):
            styled_df = df.style.map(color_status, subset=["출결 상태"])
        else:
            styled_df = df.style.applymap(color_status, subset=["출결 상태"])
        
        st.dataframe(styled_df, use_container_width=True, height=280)
    except Exception:
        # 스타일링에서 에러가 날 경우 기본 테이블로 안전하게 우회 출력
        st.dataframe(df, use_container_width=True, height=280)
        
    # 데이터 전체 리셋 버튼
    if st.button("🔄 오늘 출결 전체 초기화", help="모든 데이터를 처음 상태로 되돌립니다."):
        st.session_state.attendance_db = pd.DataFrame({
            "이름": INITIAL_STUDENTS,
            "출결 상태": ["미정"] * len(INITIAL_STUDENTS),
            "확인 시간": ["-"] * len(INITIAL_STUDENTS),
            "비고(사유)": [""] * len(INITIAL_STUDENTS)
        })
        safe_rerun()

st.markdown("---")

# ==========================================
# 6. [AI 기능] 요약 브리핑 섹션 (요구사항 반영)
# ==========================================
st.header("🤖 AI 오늘의 조례 브리핑 요약")

# Secrets 키 존재 여부 안전 검사
has_api_key = False
try:
    if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"].strip() != "":
        has_api_key = True
except Exception:
    has_api_key = False

if has_api_key:
    # 특이사항 데이터 가공
    issue_df = df[df["출결 상태"].isin(["지각", "결석"])]
    
    if not issue_df.empty:
        if st.button("✨ AI 분석 보고서 생성", type="secondary"):
            with st.spinner("Gemini AI가 오늘의 등교 상태를 분석하고 있습니다..."):
                try:
                    # 데이터 텍스트 직렬화
                    summary_text = ""
                    for _, row in issue_df.iterrows():
                        summary_text += f"- {row['이름']} ({row['출결 상태']}): {row['비고(사유)'] if row['비고(사유)'] else '사유 미기재'}\n"
                    
                    # API 설정 및 호출 (지정된 gemini-2.5-flash-lite 모델 사용)
                    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                    model = genai.GenerativeModel("gemini-2.5-flash-lite")
                    
                    prompt = f"""
                    당신은 학급의 담임선생님을 돕는 유능한 AI 비서입니다. 
                    아래 제공된 아침 조례 출결 특이사항 명단을 확인하고, 오늘 학급 운영에 참고할 수 있도록 다정하고 깔끔하게 2~3문장으로 요약 및 격려의 한마디를 적어주세요.
                    
                    [특이사항 명단]
                    {summary_text}
                    """
                    response = model.generate_content(prompt)
                    st.info(response.text)
                    
                except Exception as e:
                    st.error(f"⚠️ AI 호출 중 오류가 발생했습니다. (자세한 에러: {e})")
    else:
        st.write("✅ 지각이나 결석 인원이 없습니다. 모두 즐거운 하루를 시작하세요!")
else:
    st.warning("⚠️ AI 요약 브리핑을 사용하려면 Streamlit Cloud [Settings] -> [Secrets]에 'GEMINI_API_KEY'를 등록해 주세요. (출결 입력 기능은 현재 상태로도 완벽히 작동합니다.)")
