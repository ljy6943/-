import json
import os
import html
import streamlit as st

# =========================
# 기본 설정
# =========================
st.set_page_config(
    page_title="반장의 정보 도우미",
    page_icon="📢",
    layout="wide"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "board_data.json")
PAGE_OPTIONS = ["홈", "오늘의 공지", "준비물", "반장 전용"]


def safe_rerun():
    """Streamlit 버전에 따라 안전하게 rerun."""
    try:
        st.rerun()
    except Exception:
        st.experimental_rerun()


def get_leader_password():
    """Secrets에 LEADER_PASSWORD가 있으면 사용하고, 없으면 기본값 사용."""
    try:
        return st.secrets["LEADER_PASSWORD"]
    except Exception:
        return "1234"


LEADER_PASSWORD = get_leader_password()


def default_board_data():
    return {
        "notice": "반장이 아직 공지를 작성하지 않았어요.\n반장 전용 메뉴에서 내용을 입력해 주세요.",
        "checklist": ["필통", "교과서", "공책", "숙제"]
    }


def load_board_data():
    data = default_board_data()
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded, dict):
                if "notice" in loaded and isinstance(loaded["notice"], str):
                    data["notice"] = loaded["notice"]
                if "checklist" in loaded and isinstance(loaded["checklist"], list):
                    items = [str(x).strip() for x in loaded["checklist"] if str(x).strip()]
                    if items:
                        data["checklist"] = items[:20]
        except Exception:
            pass
    return data


def save_board_data(data):
    try:
        tmp_file = DATA_FILE + ".tmp"
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_file, DATA_FILE)
        return True, ""
    except Exception as e:
        return False, str(e)


def init_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "name" not in st.session_state:
        st.session_state.name = ""
    if "page" not in st.session_state:
        st.session_state.page = "홈"
    if "leader_unlocked" not in st.session_state:
        st.session_state.leader_unlocked = False
    if "board_data" not in st.session_state:
        st.session_state.board_data = load_board_data()


def apply_style():
    st.markdown(
        """
        <style>
        .stApp {
            background: #FFF8C9;
        }

        .block-container {
            padding-top: 3.2rem;
            padding-bottom: 4.5rem;
            position: relative;
            z-index: 1;
        }

        .stApp::before,
        .stApp::after {
            content: "";
            position: fixed;
            left: 0;
            width: 100%;
            height: 52px;
            pointer-events: none;
            z-index: 0;
            background-repeat: repeat-x;
            background-size: 40px 52px;
            opacity: 0.98;
        }

        .stApp::before {
            top: 0;
            background-image:
                radial-gradient(circle at 20px 52px, #ffffff 18px, transparent 19px);
        }

        .stApp::after {
            bottom: 0;
            background-image:
                radial-gradient(circle at 20px 0px, #ffffff 18px, transparent 19px);
        }

        .main-title {
            text-align: center;
            font-size: 3rem;
            font-weight: 800;
            color: #333333;
            margin-top: 0.3rem;
            margin-bottom: 0.6rem;
            letter-spacing: -1px;
        }

        .subtitle {
            text-align: center;
            color: #555555;
            font-size: 1rem;
            margin-bottom: 1.2rem;
        }

        .card {
            background: #ffffff;
            border: 2px solid #fff0a8;
            border-radius: 24px;
            padding: 1.2rem 1.35rem;
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
            margin-bottom: 1rem;
        }

        .card-title {
            font-size: 1.05rem;
            font-weight: 800;
            margin-bottom: 0.6rem;
            color: #333333;
        }

        .notice-text {
            white-space: pre-wrap;
            line-height: 1.8;
            font-size: 1.05rem;
            color: #333333;
        }

        .pill {
            display: inline-block;
            background: #FFF0A8;
            color: #333333;
            font-weight: 700;
            border-radius: 999px;
            padding: 0.35rem 0.8rem;
            margin-bottom: 0.8rem;
        }

        .small-muted {
            color: #666666;
            font-size: 0.95rem;
        }

        .page-box {
            background: #ffffff;
            border-radius: 22px;
            padding: 1rem;
            border: 1px solid rgba(0,0,0,0.06);
            box-shadow: 0 6px 18px rgba(0,0,0,0.06);
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_title():
    st.markdown('<div class="main-title">안 보면 니 손해</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">반장의 말과 학급 정보를 보기 쉽게 모아둔 전자 게시판</div>',
        unsafe_allow_html=True
    )


def page_buttons():
    st.markdown("### 페이지 들어가기")
    c1, c2, c3, c4 = st.columns(4)

    buttons = [
        (c1, "홈"),
        (c2, "오늘의 공지"),
        (c3, "준비물"),
        (c4, "반장 전용"),
    ]

    for col, label in buttons:
        with col:
            if st.button(label, use_container_width=True):
                st.session_state.page = label
                safe_rerun()


def show_notice_board():
    notice = st.session_state.board_data.get("notice", default_board_data()["notice"])
    safe_notice = html.escape(notice).replace("\n", "<br>")

    st.markdown(
        f"""
        <div class="card">
            <div class="pill">반장이 말 적는 칸</div>
            <div class="notice-text">{safe_notice}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="small-muted">이 칸은 반장만 수정할 수 있어요.</div>',
        unsafe_allow_html=True
    )


def render_home():
    show_notice_board()
    page_buttons()

    st.markdown("### 오늘의 빠른 정보")
    cols = st.columns(3)
    with cols[0]:
        st.info("이름 입력 후 사용")
    with cols[1]:
        st.info("반장만 공지 수정")
    with cols[2]:
        st.info("준비물도 한눈에 확인")


def render_notice_page():
    st.markdown("### 오늘의 공지")
    show_notice_board()

    st.markdown(
        """
        <div class="page-box">
            <b>안내</b><br>
            공지는 반장 전용 페이지에서 수정할 수 있습니다.
        </div>
        """,
        unsafe_allow_html=True
    )


def render_checklist_page():
    st.markdown("### 준비물")
    checklist = st.session_state.board_data.get("checklist", default_board_data()["checklist"])

    st.markdown(
        """
        <div class="page-box">
            수업 전에 확인할 준비물입니다. 체크는 각자 편하게 사용하세요.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    for i, item in enumerate(checklist):
        st.checkbox(item, key=f"check_{i}")


def render_leader_page():
    st.markdown("### 반장 전용")

    if not st.session_state.leader_unlocked:
        st.markdown(
            """
            <div class="page-box">
                비밀번호를 입력해야 공지를 수정할 수 있어요.
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.form("leader_login_form"):
            pw = st.text_input("반장 확인 비밀번호", type="password")
            submitted = st.form_submit_button("잠금 해제")

        if submitted:
            if pw == LEADER_PASSWORD:
                st.session_state.leader_unlocked = True
                st.success("반장 확인 완료")
                safe_rerun()
            else:
                st.error("비밀번호가 맞지 않아요.")
        return

    st.success("반장 모드가 열렸어요.")

    current_notice = st.session_state.board_data.get("notice", "")
    current_checklist = st.session_state.board_data.get("checklist", [])

    with st.form("leader_edit_form"):
        new_notice = st.text_area(
            "반장이 말 적는 칸",
            value=current_notice,
            height=180
        )

        new_checklist = st.text_area(
            "준비물 목록(한 줄에 하나씩)",
            value="\n".join(current_checklist),
            height=160
        )

        save_button = st.form_submit_button("저장하기")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("잠금 다시 걸기", use_container_width=True):
            st.session_state.leader_unlocked = False
            safe_rerun()

    with col2:
        st.caption("저장하면 파일에 반영되어 다른 페이지에서도 바로 보입니다.")

    if save_button:
        clean_items = [line.strip() for line in new_checklist.splitlines() if line.strip()]
        if not clean_items:
            clean_items = default_board_data()["checklist"]

        updated = {
            "notice": new_notice.strip() if new_notice.strip() else default_board_data()["notice"],
            "checklist": clean_items
        }

        ok, err = save_board_data(updated)
        st.session_state.board_data = updated

        if ok:
            st.success("저장 완료")
            safe_rerun()
        else:
            st.warning(f"파일 저장은 실패했지만 현재 세션에는 반영됐어요. 오류: {err}")


def login_screen():
    st.markdown(
        """
        <div class="card">
            <div class="card-title">이름 입력</div>
            <div class="small-muted">입장 후 원하는 페이지를 볼 수 있어요.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.form("login_form"):
        name = st.text_input("이름")
        submitted = st.form_submit_button("입장하기")

    if submitted:
        if not name.strip():
            st.warning("이름을 입력해 주세요.")
            return
        st.session_state.logged_in = True
        st.session_state.name = name.strip()
        st.session_state.page = "홈"
        safe_rerun()


def sidebar_menu():
    st.sidebar.title("메뉴")
    st.sidebar.caption(f"{st.session_state.name}님")
    selected = st.sidebar.radio(
        "페이지 이동",
        PAGE_OPTIONS,
        index=PAGE_OPTIONS.index(st.session_state.page),
        key="sidebar_page"
    )
    st.session_state.page = selected

    st.sidebar.divider()

    if st.sidebar.button("로그아웃", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.name = ""
        st.session_state.page = "홈"
        st.session_state.leader_unlocked = False
        safe_rerun()


# =========================
# 실행
# =========================
init_state()
apply_style()
render_title()

if not st.session_state.logged_in:
    login_screen()
else:
    sidebar_menu()

    if st.session_state.page == "홈":
        render_home()
    elif st.session_state.page == "오늘의 공지":
        render_notice_page()
    elif st.session_state.page == "준비물":
        render_checklist_page()
    elif st.session_state.page == "반장 전용":
        render_leader_page()
    else:
        st.session_state.page = "홈"
        safe_rerun()
