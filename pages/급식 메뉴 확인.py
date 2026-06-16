import streamlit as st
import requests
from datetime import date

# ---------------------------
# 페이지 설정
# ---------------------------
st.set_page_config(
    page_title="Sunny Lunch Helper",
    page_icon="🍱",
    layout="centered"
)

# ---------------------------
# 연한 노란색 배경
# ---------------------------
st.markdown("""
<style>
.stApp {
    background-color: #FFF9DB;
}

.block-container {
    padding-top: 2rem;
}

.info-card {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    border: 2px solid #FFE066;
    margin-bottom: 15px;
}

.result-card {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    border: 2px solid #FFD43B;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# 학교 코드
# 예시 학교
# 필요시 변경 가능
# ---------------------------
ATPT_OFCDC_SC_CODE = "B10"
SD_SCHUL_CODE = "7010536"

# ---------------------------
# 알레르기 정보
# ---------------------------
ALLERGY_MAP = {
    "난류": "1.",
    "우유": "2.",
    "메밀": "3.",
    "땅콩": "4.",
    "대두": "5.",
    "밀": "6.",
    "고등어": "7.",
    "게": "8.",
    "새우": "9.",
    "돼지고기": "10.",
    "복숭아": "11.",
    "토마토": "12.",
    "아황산류": "13.",
    "호두": "14.",
    "닭고기": "15.",
    "쇠고기": "16.",
    "오징어": "17.",
    "조개류": "18."
}

# ---------------------------
# 급식 조회 함수
# ---------------------------
def get_meal_info(selected_date):
    url = (
        "https://open.neis.go.kr/hub/mealServiceDietInfo"
        f"?Type=json"
        f"&ATPT_OFCDC_SC_CODE={ATPT_OFCDC_SC_CODE}"
        f"&SD_SCHUL_CODE={SD_SCHUL_CODE}"
        f"&MLSV_YMD={selected_date.strftime('%Y%m%d')}"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if "mealServiceDietInfo" not in data:
            return None

        meal = data["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"]

        menu_list = [
            item.strip()
            for item in meal.replace("<br/>", "\n").split("\n")
            if item.strip()
        ]

        return menu_list

    except Exception:
        return None

# ---------------------------
# 알레르기 검사
# ---------------------------
def check_allergy(menu_list, allergies):

    warning_list = []

    for menu in menu_list:
        for allergy in allergies:

            code = ALLERGY_MAP[allergy]

            if code in menu:
                warning_list.append(
                    {
                        "menu": menu,
                        "allergy": allergy
                    }
                )

    return warning_list

# ---------------------------
# 제목
# ---------------------------
st.title("🍱 Sunny Lunch Helper")
st.subheader("학교 급식 & 알레르기 도우미")

st.write(
    "원하는 날짜의 급식을 조회하고 "
    "알레르기 위험 메뉴를 확인할 수 있습니다."
)

# ---------------------------
# 사용자 정보
# ---------------------------
st.markdown('<div class="info-card">', unsafe_allow_html=True)

name = st.text_input(
    "🙋 이름 입력",
    placeholder="이름을 입력하세요"
)

selected_allergies = st.multiselect(
    "⚠️ 알레르기 선택",
    list(ALLERGY_MAP.keys())
)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# 날짜 선택
# ---------------------------
selected_date = st.date_input(
    "📅 확인할 날짜",
    value=date.today()
)

# ---------------------------
# 조회 버튼
# ---------------------------
if st.button("🍽️ 급식 조회", use_container_width=True):

    if not name.strip():
        st.warning("이름을 입력해주세요.")
        st.stop()

    with st.spinner("급식 정보를 불러오는 중..."):

        menu_list = get_meal_info(selected_date)

    if not menu_list:
        st.error("해당 날짜의 급식 정보가 없습니다.")
        st.stop()

    st.markdown('<div class="result-card">', unsafe_allow_html=True)

    st.success(f"{name}님의 급식 결과")

    st.subheader("🍴 오늘의 메뉴")

    for menu in menu_list:
        st.write("•", menu)

    st.markdown("---")

    warnings = check_allergy(
        menu_list,
        selected_allergies
    )

    st.subheader("🚨 알레르기 확인")

    if warnings:

        st.error(
            f"{len(warnings)}개의 알레르기 주의 메뉴가 있습니다."
        )

        for item in warnings:
            st.write(
                f"⚠️ {item['allergy']} 포함 가능 → {item['menu']}"
            )

        st.progress(30)
        st.caption("급식 안전도 : 낮음")

    else:

        st.success(
            "선택한 알레르기 관련 위험 메뉴가 없습니다."
        )

        st.progress(100)
        st.caption("급식 안전도 : 높음")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# 하단 안내
# ---------------------------
st.markdown("---")

st.info(
    """
    현재 예시 학교 코드가 적용되어 있습니다.
    
    다른 학교로 사용하려면:
    
    - ATPT_OFCDC_SC_CODE
    - SD_SCHUL_CODE
    
    값을 원하는 학교 코드로 변경하세요.
    """
)
