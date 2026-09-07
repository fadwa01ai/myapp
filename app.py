import random
import streamlit as st

st.set_page_config(page_title="لعبة الأفعى والمتاهة 🐍", layout="centered")

GRID_SIZE = 10  # شبكة 10x10

# تصميم المتاهة (1 = جدار، 0 = مسار متاح)
MAZE = [
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 0, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 1, 1, 1, 0, 1],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
]


def generate_food(snake):
    while True:
        r = random.randint(0, GRID_SIZE - 1)
        c = random.randint(0, GRID_SIZE - 1)
        if MAZE[r][c] == 0 and [r, c] not in snake:
            return [r, c]


def init_game():
    snake = [[0, 0]]
    food = generate_food(snake)
    return snake, food, 0, False, ""


if "snake" not in st.session_state:
    (
        st.session_state.snake,
        st.session_state.food,
        st.session_state.score,
        st.session_state.game_over,
        st.session_state.hint_msg,
    ) = init_game()

if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []


def move_snake(dr, dc):
    if st.session_state.game_over:
        return

    st.session_state.hint_msg = ""
    head = st.session_state.snake[0]
    new_r, new_c = head[0] + dr, head[1] + dc

    # الاصطدام بالحواف أو الجدران أو الجسم
    if not (0 <= new_r < GRID_SIZE and 0 <= new_c < GRID_SIZE):
        st.session_state.game_over = True
        return
    if MAZE[new_r][new_c] == 1 or [new_r, new_c] in st.session_state.snake:
        st.session_state.game_over = True
        return

    new_head = [new_r, new_c]
    st.session_state.snake.insert(0, new_head)

    # أكل النقطة
    if new_head == st.session_state.food:
        st.session_state.score += 10
        st.session_state.food = generate_food(st.session_state.snake)
    else:
        st.session_state.snake.pop()


def give_hint():
    head = st.session_state.snake[0]
    food = st.session_state.food
    dr, dc = food[0] - head[0], food[1] - head[1]

    directions = []
    if dr < 0:
        directions.append("لأعلى ⬆️")
    elif dr > 0:
        directions.append("لأسفل ⬇️")
    if dc < 0:
        directions.append("لليسار ⬅️")
    elif dc > 0:
        directions.append("لليمين ➡️")

    st.session_state.hint_msg = (
        f"💡 تلميح: النقطة تبعد باتجاه {' أو '.join(directions)}"
    )


# الواجهة
st.title("🐍 لعبة الأفعى والمتاهة")
player_name = st.text_input("أدخل اسمك للبدء:", placeholder="اسم اللاعب")

if player_name:
    st.write(
        f"مرحباً **{player_name}**! وجه الأفعى لالتهام النقاط وتجنب جدران المتاهة."
    )

    # أزرار الاتجاهات والتلميح
    st.markdown("### 🎮 أزرار التحكم")
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        st.button(
            "⬆️ أعلى",
            on_click=move_snake,
            args=(-1, 0),
            use_container_width=True,
        )

    c4, c5, c6 = st.columns([1, 1, 1])
    with c4:
        st.button(
            "⬅️ يسار",
            on_click=move_snake,
            args=(0, -1),
            use_container_width=True,
        )
    with c5:
        if st.button("💡 تلميح", use_container_width=True):
            give_hint()
    with c6:
        st.button(
            "➡️ يمين", on_click=move_snake, args=(0, 1), use_container_width=True
        )

    c7, c8, c9 = st.columns([1, 1, 1])
    with c8:
        st.button(
            "⬇️ أسفل",
            on_click=move_snake,
            args=(1, 0),
            use_container_width=True,
        )

    if st.session_state.hint_msg:
        st.info(st.session_state.hint_msg)

    # رسم شبكة المتاهة والأفعى
    st.markdown("---")
    for r in range(GRID_SIZE):
        cols = st.columns(GRID_SIZE)
        for c in range(GRID_SIZE):
            cell = [r, c]
            if cell == st.session_state.snake[0]:
                cols[c].markdown("🟢")
            elif cell in st.session_state.snake:
                cols[c].markdown("🟩")
            elif cell == st.session_state.food:
                cols[c].markdown("🍎")
            elif MAZE[r][c] == 1:
                cols[c].markdown("⬛")
            else:
                cols[c].markdown("⬜")

    st.write(f"**النقاط الحالية:** {st.session_state.score}")

    if st.session_state.game_over:
        st.error(
            f"❌ انتهت اللعبة يا {player_name}! اصطدمت بالجدار أو بمحيط اللعبة."
        )

        if st.session_state.score > 0:
            if not any(
                item["player"] == player_name
                and item["score"] == st.session_state.score
                for item in st.session_state.leaderboard
            ):
                st.session_state.leaderboard.append(
                    {"player": player_name, "score": st.session_state.score}
                )

        if st.button("🔄 إعادة بدء اللعبة"):
            (
                st.session_state.snake,
                st.session_state.food,
                st.session_state.score,
                st.session_state.game_over,
                st.session_state.hint_msg,
            ) = init_game()
            st.rerun()

    if st.session_state.score >= 50 and not st.session_state.game_over:
        st.balloons()
        st.success(
            f"🎉 مبروك يا {player_name}! وصلت إلى {st.session_state.score} نقطة بنجاح!"
        )

    if st.session_state.leaderboard:
        st.markdown("---")
        st.subheader("🏆 لوحة الصدارة (Best Scores)")
        sorted_scores = sorted(
            st.session_state.leaderboard,
            key=lambda x: x["score"],
            reverse=True,
        )
        st.table(sorted_scores)

else:
    st.warning("يرجى إدخال اسمك أولاً لبدء اللعب.")