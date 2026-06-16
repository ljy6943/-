import streamlit as st
import requests
from datetime import date

st.set_page_config(
    page_title="학교 급식 & 알레르기 도우미",
    page_icon="🍱",
    layout="centered"
)

# ----------------------------
# 학교 설정
# 예시: 서울디지텍고등학교
# 필요하면 학교코드 변경 가능
# ----------------------------
ATPT_OFCDC_SC_CODE = "B10"
SD_SCHUL_CODE = "7010536"

# 알레르기 번호 매핑
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


def get_meal_info(selected_date):
    """
    NEIS 급식 조회
    """
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

        meal_row = data["mealServiceDietInfo"][1]["row"][0]

        menu = meal_row["DDISH_NM"]

        menu_list = [
            item.strip()
            for item in menu.replace("<br/>", "\n").split("\n")
            if item.strip()
        ]

        return menu_list

    except Exception:
        return None


def check_allergy(menu_list, user_allergies):
    warnings = []

    for menu in menu_list:
        for allergy_name in user_allergies:
            allergy_code = ALLERGY_MAP[allergy_name]

            if allergy_code in menu:
                warnings.append((menu, allergy_name))

    return warnings


st.title("🍱 학교 급식 & 알레르기 도우미")
st.caption("원하는 날짜의 급식을 확인하고 알레르기 위험 메뉴를 확인하세요.")

# ----------------------------
# 사용자 정보
# ----------------------------
with st.sidebar:
    st.header("🙋 사용자 정보")

    user_name = st.text_input(
        "이름",
        placeholder="이름을 입력하세요"
    )

    user_allergies = st.multiselect(
        "알레르기 선택",
        list(ALLERGY_MAP.keys())
    )

# ----------------------------
# 날짜 선택
# ----------------------------
selected_date = st.date_input(
    "📅 급식 조회 날짜",
    value=date.today()
)

# ----------------------------
# 조회 버튼
# ----------------------------
if st.button("급식 조회", use_container_width=True):

    if not user_name.strip():
        st.warning("이름을 입력해주세요.")
        st.stop()

    with st.spinner("급식 정보를 조회하는 중입니다..."):

        menu_list = get_meal_info(selected_date)

    if not menu_list:
        st.error("해당 날짜의 급식 정보가 없습니다.")
        st.stop()

    st.success(f"{user_name}님의 급식 정보")

    st.subheader("🍽️ 오늘의 메뉴")

    for menu in menu_list:
        st.write("•", menu)

    # 알레르기 검사
    warnings = check_allergy(menu_list, user_allergies)

    st.divider()

    st.subheader("⚠️ 알레르기 확인")

    if warnings:
        st.error("알레르기 주의가 필요한 메뉴가 있습니다.")

        for menu, allergy in warnings:
            st.write(f"🚨 {allergy} 포함 가능 → {menu}")

    else:
        st.success("선택한 알레르기와 관련된 메뉴가 발견되지 않았습니다.")

st.divider()

st.info(
    """
    학교 코드가 변경되면 상단의
    ATPT_OFCDC_SC_CODE,
    SD_SCHUL_CODE 값을 수정하면 됩니다.
    """
)
