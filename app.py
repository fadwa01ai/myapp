import random
import streamlit as st

st.set_page_config(
    page_title="لعبة الألغاز التفاعلية 🧩", layout="centered"
)

BOARD_SIZE = 3  # شبكة 3x3
SOLVED_BOARD = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, None],
]


def init_board():
    tiles = list(range(1, BOARD_SIZE * BOARD_SIZE)) + [None]
    random.shuffle(tiles)
    return [
        tiles[i : i + BOARD_SIZE] for i in range(0, len(tiles), BOARD_SIZE)
    ]


# تهيئة متغيّرات الجلسة (Session State)
if "board" not in st.session_state:
    st.session_state.board = init_board()
if "moves" not in st.session_state:
    st.session_state.moves = 0
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []
if "hint_msg" not in st.session_state:
    st.session_state.hint_msg = ""


def find_empty(board):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] is None:
                return r, c


def move_tile(r, c):
    st.session_state.hint_msg = ""
    empty_r, empty_c = find_empty(st.session_state.board)
    if (abs(empty_r - r) == 1 and empty_c == c) or (
        abs(empty_c - c) == 1 and empty_r == r
    ):
        st.session_state.board[empty_r][empty_c] = st.session_state.board[r][c]
        st.session_state.board[r][c] = None
        st.session_state.moves += 1


def give_hint():
    empty_r, empty_c = find_empty(st.session_state.board)
    candidates = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = empty_r + dr, empty_c + dc
        if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
            val = st.session_state.board[nr][nc]
            # معرفة الموقع الصحيح للرقم
            correct_r, correct_c = (val - 1) // BOARD_SIZE, (
                val - 1
            ) % BOARD_SIZE
            if nr != correct_r or nc != correct_c:
                candidates.append(val)

    if candidates:
        st.session_state.hint_msg = (
            f"💡 تلميح: جرب تحريك المربع الذي يحمل الرقم **{candidates[0]}**"
        )
    else:
        st.session_state.hint_msg = (
            "💡 أنت قريب جداً من الحل! حرك المربعات المجاورة للفراغ."
        )


# الواجهة الرئيسية
st.title("🧩 لعبة ترتيب الأرقام")

# إدخال اسم اللاعب
player_name = st.text_input("أدخل اسمك للبدء:", placeholder="اسم اللاعب")

if player_name:
    st.write(f"مرحباً بك **{player_name}**! رتب الأرقام بالتسلسل من 1 إلى 8.")

    # عرض شبكة اللعبة
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

    # زر التلميح والإعادة
    col_hint, col_reset = st.columns(2)
    with col_hint:
        if st.button("💡 الحصول على تلميح (Hint)"):
            give_hint()
    with col_reset:
        if st.button("🔄 إعادة بدء اللعبة"):
            st.session_state.board = init_board()
            st.session_state.moves = 0
            st.session_state.hint_msg = ""
            st.rerun()

    if st.session_state.hint_msg:
        st.info(st.session_state.hint_msg)

    # التحقق من الفوز
    if st.session_state.board == SOLVED_BOARD:
        st.balloons()
        st.success(
            f"🎉 مبروك يا {player_name}! لقد فزت في {st.session_state.moves} حركة!"
        )

        # حفظ النتيجة
        if not any(
            item["player"] == player_name
            and item["moves"] == st.session_state.moves
            for item in st.session_state.leaderboard
        ):
            st.session_state.leaderboard.append(
                {"player": player_name, "moves": st.session_state.moves}
            )

    # لوحة الصدارة (Leaderboard)
    if st.session_state.leaderboard:
        st.markdown("---")
        st.subheader("🏆 لوحة الصدارة (Best Scores)")
        sorted_scores = sorted(
            st.session_state.leaderboard, key=lambda x: x["moves"]
        )
        st.table(sorted_scores)

else:
    st.warning("يرجى إدخال اسمك أولاً لبدء اللعب.")