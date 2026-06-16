import streamlit as st

# --------------------
# 페이지 설정
# --------------------
st.set_page_config(
    page_title="반장의 정보 도우미",
    page_icon="📢",
    layout="wide"
)

# --------------------
# 스타일
# --------------------
st.markdown("""
<style>
.stApp{
    background-color:#FFF176;
}

.title{
    text-align:center;
    font-size:45px;
    font-weight:bold;
    color:black;
    margin-bottom:10px;
}

.notice-box{
    background:white;
    padding:15px;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# --------------------
# 기본 데이터
# --------------------
if "notice" not in st.session_state:
    st.session_state.notice = """
📢 오늘의 공지

- 숙제 제출하기
- 준비물 챙기기
- 내일 체육복 입기
"""

if "login" not in st.session_state:
    st.session_state.login = False

if "name" not in st.session_state:
    st.session_state.name = ""

# --------------------
# 제목
# --------------------
st.markdown(
    "<div class='title'>안 보면 니 손해</div>",
    unsafe_allow_html=True
)

# --------------------
# 로그인
# --------------------
if not st.session_state.login:

    st.subheader("이름 입력")

    name = st.text_input("이름")

    if st.button("입장하기"):

        if name.strip() == "":
            st.warning("이름을 입력하세요.")
        else:
            st.session_state.login = True
            st.session_state.name = name
            st.rerun()

# --------------------
# 메인
# --------------------
else:

    st.success(f"{st.session_state.name}님 환영합니다!")

    page = st.sidebar.radio(
        "페이지 선택",
        [
            "오늘의 공지",
            "준비물 확인",
            "학생 정보",
            "반장 전용"
        ]
    )

    # ----------------
    # 공지
    # ----------------
    if page == "오늘의 공지":

        st.header("📢 오늘의 공지")

        st.markdown(
            f"""
            <div class="notice-box">
            {st.session_state.notice}
            </div>
            """,
            unsafe_allow_html=True
        )

    # ----------------
    # 준비물
    # ----------------
    elif page == "준비물 확인":

        st.header("🎒 준비물")

        st.write("✔ 필통")
        st.write("✔ 교과서")
        st.write("✔ 공책")
        st.write("✔ 숙제")

    # ----------------
    # 학생 정보
    # ----------------
    elif page == "학생 정보":

        st.header("🙋 학생 정보")

        st.write(f"이름 : {st.session_state.name}")

    # ----------------
    # 반장 전용
    # ----------------
    elif page == "반장 전용":

        st.header("👑 반장 전용")

        password = st.text_input(
            "비밀번호 입력",
            type="password"
        )

        if password == "classleader123":

            st.success("반장 인증 완료")

            new_notice = st.text_area(
                "공지 작성",
                value=st.session_state.notice,
                height=250
            )

            if st.button("공지 저장"):

                st.session_state.notice = new_notice

                st.success("공지 저장 완료!")

        elif password != "":
            st.error("비밀번호가 틀렸습니다.")

    st.sidebar.divider()

    if st.sidebar.button("로그아웃"):

        st.session_state.login = False
        st.session_state.name = ""

        st.rerun()
