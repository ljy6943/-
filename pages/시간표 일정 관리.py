import streamlit as st
import pandas as pd
from datetime import datetime

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="우리반 시간표 정보 도우미",
    page_icon="📚",
    layout="wide"
)

# -----------------------------
# 배경색 설정
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-color: #FFF9D6;
}

h1, h2, h3 {
    color: #333333;
}

.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 제목
# -----------------------------
st.title("📚 우리반 시간표 정보 도우미")
st.write("우리 반의 시간표를 쉽고 빠르게 확인할 수 있습니다.")

# -----------------------------
# 새로고침 버튼
# -----------------------------
if st.button("🔄 시간표 새로고침"):
    st.cache_data.clear()
    st.success("최신 시간표를 다시 불러왔습니다.")

# -----------------------------
# 시간표 불러오기
# -----------------------------
@st.cache_data(ttl=60)
def load_timetable():
    return pd.read_csv("timetable.csv")

try:
    df = load_timetable()

    required_columns = [
        "교시",
        "월요일",
        "화요일",
        "수요일",
        "목요일",
        "금요일"
    ]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"{col} 열이 없습니다.")

    # -----------------------------
    # 오늘 시간표
    # -----------------------------
    weekday_map = {
        0: "월요일",
        1: "화요일",
        2: "수요일",
        3: "목요일",
        4: "금요일"
    }

    today_num = datetime.today().weekday()

    st.subheader("📅 오늘의 시간표")

    if today_num <= 4:
        today_col = weekday_map[today_num]

        today_df = pd.DataFrame({
            "교시": df["교시"],
            "과목": df[today_col]
        })

        st.dataframe(
            today_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("오늘은 주말입니다.")

    # -----------------------------
    # 전체 시간표
    # -----------------------------
    st.subheader("🗓️ 전체 시간표")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------
    # 과목 검색
    # -----------------------------
    st.subheader("🔍 과목 찾기")

    keyword = st.text_input(
        "과목명을 입력하세요"
    )

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
            st.success(f"{len(result)}개 찾았습니다.")
            st.dataframe(
                pd.DataFrame(result),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("검색 결과가 없습니다.")

except FileNotFoundError:
    st.error(
        "timetable.csv 파일을 찾을 수 없습니다. "
        "GitHub 저장소에 timetable.csv를 업로드하세요."
    )

except Exception as e:
    st.error(f"시간표를 불러오는 중 오류가 발생했습니다.\n\n{e}")
