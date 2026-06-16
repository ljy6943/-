import streamlit as st
import pandas as pd
import google.generativeai as genai
from datetime import datetime

# 1. 페이지 설정 및 배경색 테마 적용 (연한 노란색)
st.set_page_config(page_title="Sunny Schedule", page_icon="☀️", layout="wide")

# CSS를 이용한 배경색 변경 및 UI 스타일링
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFDE7;
    }
    .main {
        background-color: #FFFDE7;
    }
    h1, h2, h3 {
        color: #FBC02D;
    }
    .stButton>button {
        background-color: #FBC02D;
        color: white;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_stdio=True)

# 2. 세션 상태 초기화 (데이터 보존)
if 'timetable' not in st.session_state:
    # 기본 시간표 데이터 생성
    hours = [f"{h:02d}:00" for h in range(9, 19)]
    days = ["월요일", "화요일", "수요일", "목요일", "금요일"]
    st.session_state.timetable = pd.DataFrame("", index=hours, columns=days)

if 'todo_list' not in st.session_state:
    st.session_state.todo_list = []

# 3. 사이드바 - AI 학습 멘토 기능
with st.sidebar:
    st.header("🤖 AI 학습 멘토")
    if "GEMINI_API_KEY" in st.secrets:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-2.5-flash-lite')
            
            if st.button("AI 스케줄 분석받기"):
                with st.spinner("AI가 일정을 분석 중입니다..."):
                    # 데이터 요약
                    sched_data = st.session_state.timetable.to_string()
                    todo_data = ", ".join([t['task'] for t in st.session_state.todo_list])
                    
                    prompt = f"""
                    다음은 학생의 주간 시간표와 할 일 목록이야.
                    시간표: {sched_data}
                    할 일: {todo_data}
                    
                    이 일정을 보고 1. 가장 바쁜 날 분석 2. 효율적인 공부 시간 추천 3. 짧은 응원 메시지를 한국어로 친절하게 말해줘.
                    """
                    response = model.generate_content(prompt)
                    st.success("분석 완료!")
                    st.info(response.text)
        except Exception as e:
            st.error(f"AI 호출 중 오류가 발생했습니다: {e}")
    else:
        st.warning("Secrets에 GEMINI_API_KEY를 설정해주세요.")

# 4. 메인 화면 구성
st.title("☀️ Sunny Schedule")
st.subheader("나만의 스마트 시간표 & 일정 관리")

tab1, tab2 = st.tabs(["📅 주간 시간표", "📝 할 일 목록"])

with tab1:
    st.write("💡 아래 표를 클릭하여 직접 과목명을 입력하세요. (자동 저장됩니다)")
    # Data Editor를 활용한 시간표 관리
    edited_df = st.data_editor(
        st.session_state.timetable,
        use_container_width=True,
        num_rows="fixed"
    )
    st.session_state.timetable = edited_df
    
    if st.button("시간표 초기화"):
        st.session_state.timetable = pd.DataFrame("", index=[f"{h:02d}:00" for h in range(9, 19)], columns=["월요일", "화요일", "수요일", "목요일", "금요일"])
        st.rerun()

with tab2:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("### 일정 추가")
        new_task = st.text_input("무엇을 해야 하나요?", placeholder="예: 수학 과제 제출")
        task_date = st.date_input("마감일")
        if st.button("추가하기"):
            if new_task:
                st.session_state.todo_list.append({"task": new_task, "date": task_date, "done": False})
                st.rerun()
            else:
                st.warning("내용을 입력해주세요.")
                
    with col2:
        st.write("### To-do List")
        if not st.session_state.todo_list:
            st.write("등록된 일정이 없습니다. 사이드바의 AI 멘토에게 도움을 요청해보세요!")
        else:
            for i, item in enumerate(st.session_state.todo_list):
                cols = st.columns([0.1, 0.6, 0.3])
                # 체크박스로 완료 처리
                is_done = cols[0].checkbox("", value=item['done'], key=f"check_{i}")
                st.session_state.todo_list[i]['done'] = is_done
                
                # 가로선이나 취소선 대신 텍스트로 표시
                task_text = f"~~{item['task']}~~" if is_done else item['task']
                cols[1].markdown(f"{task_text} ({item['date']})")
                
                if cols[2].button("삭제", key=f"del_{i}"):
                    st.session_state.todo_list.pop(i)
                    st.rerun()

# 하단 정보
st.divider()
st.caption(f"현재 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Sunny Schedule v1.0")
