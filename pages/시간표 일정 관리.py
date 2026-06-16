import streamlit as st
import pandas as pd
from datetime import datetime
from io import StringIO

st.set_page_config(
    page_title="우리반 시간표 정보 도우미",
    page_icon="📚",
    layout="wide"
)

# 배경색
st.markdown("""
<style>
.stApp {
    background-color: #FFF9D6;
}
</style>
""", unsafe_allow_html=True)

st.title("📚 우리반 시간표 정보 도우미")

# --------------------------------
# 시간표 양식
# --------------------------------
template_csv = """교시,월요일,화요일,수요일,목요일,금요일
1,국어,수학,영어,과학,국어
2,수학,영어,국어,사회,수학
3,영어,과학,수학,국어,체육
4,과학,국어,사회,영어,미술
5,체육,사회,체육,수학,음악
6,음악,체육,미술,창체,창체
7,창체,창체,창체,체육,동아리
"""

# --------------------------------
# 양식 다운로드
# --------------------------------
st.sidebar.header("⚙️ 시간표 관리")

st.sidebar.download_button(
    label="📥 시간표 양식 다운로드",
    data=template_csv,
    file_name="timetable_template.csv",
    mime="text/csv"
)

# --------------------------------
# 업로드
# --------------------------------
uploaded_file = st.sidebar.file_uploader(
    "📤 시간표 업로드",
    type=["csv"]
)

required_columns = [
    "교시",
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일"
]

# --------------------------------
# 업로드 파일 사용
# --------------------------------
if uploaded_file is not None:

    try:
        df = pd.read_csv(uploaded_file)

        for col in required_columns:
            if col not in df.columns:
                raise ValueError(
                    f"'{col}' 열이 없습니다."
                )

        st.success("✅ 시간표가 성공적으로 적용되었습니다.")

    except Exception as e:
        st.error(f"파일 형식 오류: {e}")
        st.stop()

# --------------------------------
# 기본 시간표 사용
# --------------------------------
else:

    default_data = {
        "교시":[1,2,3,4,5,6,7],
        "월요일":["국어","수학","영어","과학","체육","음악","창체"],
        "화요일":["수학","영어","과학","국어","사회","체육","창체"],
        "수요일":["영어","국어","수학","사회","체육","미술","창체"],
        "목요일":["과학","사회","국어","영어","수학","창체","체육"],
        "금요일":["국어","수학","체육","미술","음악","창체","동아리"]
    }

    df = pd.DataFrame(default_data)

# --------------------------------
# 오늘 시간표
# --------------------------------
st.subheader("📅 오늘의 시간표")

weekday_map = {
    0: "월요일",
    1: "화요일",
    2: "수요일",
    3: "목요일",
    4: "금요일"
}

today = datetime.today().weekday()

if today <= 4:

    day = weekday_map[today]

    today_df = pd.DataFrame({
        "교시": df["교시"],
        "과목": df[day]
    })

    st.dataframe(
        today_df,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("오늘은 주말입니다.")

# --------------------------------
# 전체 시간표
# --------------------------------
st.subheader("🗓️ 전체 시간표")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# --------------------------------
# 과목 검색
# --------------------------------
st.subheader("🔍 과목 찾기")

keyword = st.text_input("과목명 입력")

if keyword:

    result = []

    for day in required_columns[1:]:

        for idx, subject in enumerate(df[day]):

            if keyword.lower() in str(subject).lower():

                result.append({
                    "요일": day,
                    "교시": df.iloc[idx]["교시"],
                    "과목": subject
                })

    if result:
        st.dataframe(
            pd.DataFrame(result),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("검색 결과가 없습니다.")
