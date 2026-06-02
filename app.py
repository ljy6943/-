import streamlit as st
from google import genai
from google.genai import types

# 페이지 설정
st.set_page_config(
    page_title="전자칠판 반장 알림봇",
    page_icon="🖥️",
    layout="wide"
)

st.title("🖥️ 전자칠판 반장 알림봇")
st.caption("반장의 말을 텍스트로 정리하여 전하는 전자칠판")

# API KEY 불러오기
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)

except Exception:
    st.error("❌ API 키를 불러오지 못했습니다. Secrets 설정을 확인하세요.")
    st.stop()

# 채팅 기록 유지
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 입력창
user_input = st.chat_input("반장의 전달 내용을 입력하세요...")

if user_input:

    # 사용자 메시지 저장
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    try:

        # 시스템 프롬프트
        system_prompt = """
너는 학교 전자칠판 AI이다.

목표:
반장의 말을 명확하고 보기 쉽게 텍스트 공지로 바꾼다.

규칙:
- 핵심 내용을 정리한다.
- 공지사항 형식으로 작성한다.
- 중요 일정, 준비물, 과제는 강조한다.
- 학생들이 쉽게 이해하도록 친절하게 작성한다.
"""

        # Gemini 호출
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",

            contents=[
                types.Content(
                    role="user",
                    parts=[types.Part(text=f"{system_prompt}\n\n반장 말:\n{user_input}")]
                )
            ]
        )

        bot_reply = response.text

    except Exception as e:
        bot_reply = f"""
⚠️ 오류가 발생했습니다.

오류 내용:
`{str(e)}`

잠시 후 다시 시도해주세요.
"""

    # 응답 저장
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    with st.chat_message("assistant"):
        st.markdown(bot_reply)
