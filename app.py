import random
import streamlit as st

st.set_page_config(page_title="لعبة الألغاز 🧩", layout="centered")

# إعداد حجم الشبكة
BOARD_SIZE = 3  # شبكة 3x3 لسهولة اللعب في المتصفح


def init_board():
    tiles = list(range(1, BOARD_SIZE * BOARD_SIZE)) + [None]
    random.shuffle(tiles)
    return [
        tiles[i : i + BOARD_SIZE] for i in range(0, len(tiles), BOARD_SIZE)
    ]


# تهيئة الحالة في Session State
if "board" not in st.session_state:
    st.session_state.board = init_board()
if "moves" not in st.session_state:
    st.session_state.moves = 0


def find_empty():
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if st.session_state.board[r][c] is None:
                return r, c


def move_tile(r, c):
    empty_r, empty_c = find_empty()
    # التحقق من أن المربع المحدد مجاور للمربع الفارغ
    if (abs(empty_r - r) == 1 and empty_c == c) or (
        abs(empty_c - c) == 1 and empty_r == r
    ):
        st.session_state.board[empty_r][empty_c] = st.session_state.board[r][c]
        st.session_state.board[r][c] = None
        st.session_state.moves += 1


st.title("🧩 لعبة ترتيب الأرقام (Slide Puzzle)")
st.write("اضغط على المربع المجاور للفراغ لنقله وترتيب الأرقام بالتسلسل.")

# عرض شبكة اللعبة باستخدام أزرار Streamlit
for r in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE)
    for c in range(BOARD_SIZE):
        val = st.session_state.board[r][c]
        label = str(val) if val is not None else " "
        cols[c].button(
            label,
            key=f"btn_{r}_{c}",
            on_click=move_tile,
            args=(r, c),
            use_container_width=True,
            type="primary" if val is not None else "secondary",
        )

st.write(f"**عدد المحاولات:** {st.session_state.moves}")

if st.button("إعادة بدء اللعبة 🔄"):
    st.session_state.board = init_board()
    st.session_state.moves = 0
    st.rerun()