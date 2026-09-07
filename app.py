import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Snake Cosmic Maze HD 🐍", page_icon="🪐", layout="centered"
)

# CSS لتعديل التصميم بالكامل وإعطائه طابع cosmic احترافي بتأثيرات HD
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #090d16 100%);
        color: #c9d1d9;
    }
    
    .hd-title {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 0.2rem;
        text-shadow: 0 0 20px rgba(0, 242, 254, 0.3);
    }
    
    .hd-subtitle {
        text-align: center;
        color: #8b949e;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    .game-container {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
    
    .maze-grid {
        display: grid;
        grid-template-columns: repeat(10, 38px);
        grid-template-rows: repeat(10, 38px);
        gap: 4px;
        background: rgba(22, 27, 34, 0.8);
        padding: 12px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 0 15px rgba(79, 172, 254, 0.15);
        border: 1px solid rgba(79, 172, 254, 0.3);
    }

    .cell {
        width: 38px;
        height: 38px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        transition: all 0.2s ease-in-out;
    }

    .path {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.02);
    }

    .wall {
        background: linear-gradient(135deg, #21262d 0%, #30363d 100%);
        border: 1px solid rgba(139, 148, 158, 0.2);
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.4);
    }

    .snake-head {
        background: linear-gradient(135deg, #00f2fe 0%, #00c6ff 100%);
        box-shadow: 0 0 12px #00f2fe;
        border-radius: 10px;
    }

    .snake-body {
        background: linear-gradient(135deg, #38ef7d 0%, #11998e 100%);
        box-shadow: 0 0 8px rgba(56, 239, 125, 0.5);
        border-radius: 8px;
    }

    .food {
        background: linear-gradient(135deg, #ff0844 0%, #ffb199 100%);
        box-shadow: 0 0 15px #ff0844;
        border-radius: 50%;
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(0.9); box-shadow: 0 0 10px #ff0844; }
        50% { transform: scale(1.05); box-shadow: 0 0 20px #ff0844; }
        100% { transform: scale(0.9); box-shadow: 0 0 10px #ff0844; }
    }
</style>
""",
    unsafe_allow_html=True,
)

GRID_SIZE = 10

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


def move_snake(direction):
    if st.session_state.game_over:
        return

    dr, dc = 0, 0
    if direction == "UP":
        dr = -1
    elif direction == "DOWN":
        dr = 1
    elif direction == "LEFT":
        dc = -1
    elif direction == "RIGHT":
        dc = 1
    else:
        return

    st.session_state.hint_msg = ""
    head = st.session_state.snake[0]
    new_r, new_c = head[0] + dr, head[1] + dc

    if not (0 <= new_r < GRID_SIZE and 0 <= new_c < GRID_SIZE):
        st.session_state.game_over = True
        return
    if MAZE[new_r][new_c] == 1 or [new_r, new_c] in st.session_state.snake:
        st.session_state.game_over = True
        return

    new_head = [new_r, new_c]
    st.session_state.snake.insert(0, new_head)

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
        f"⚡ تلميح كوني: الهدف يقع باتجاه {' أو '.join(directions)}"
    )


# الواجهة
st.markdown(
    '<div class="hd-title">SNAKE COSMIC MAZE</div>', unsafe_allow_html=True
)
st.markdown(
    '<div class="hd-subtitle">تحدي المتاهة عالية الدقة | التحكم بلوحة المفاتيح ⌨️</div>',
    unsafe_allow_html=True,
)

player_name = st.text_input("🎮 اسم المحارب:", placeholder="أدخل اسمك للانطلاق")

if player_name:
    # السكربت المسؤول عن ربط الكيبورد بالأزرار
    keyboard_component = """
    <script>
    const doc = window.parent.document;
    doc.addEventListener('keydown', function(e) {
        let key = "";
        if (e.key === "ArrowUp" || e.key === "w" || e.key === "W") key = "UP";
        else if (e.key === "ArrowDown" || e.key === "s" || e.key === "S") key = "DOWN";
        else if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") key = "LEFT";
        else if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") key = "RIGHT";
        
        if (key !== "") {
            const btn = doc.querySelector(`button[data-direction="${key}"]`);
            if (btn) btn.click();
        }
    });
    </script>
    """
    components.html(keyboard_component, height=0, width=0)

    # أزرار التحكم في الواجهة
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("⬆️", key="btn_up", use_container_width=True):
            move_snake("UP")
            st.rerun()

    c4, c5, c6 = st.columns([1, 1, 1])
    with c4:
        if st.button("⬅️", key="btn_left", use_container_width=True):
            move_snake("LEFT")
            st.rerun()
    with c5:
        if st.button("💡 تلميح", use_container_width=True):
            give_hint()
    with c6:
        if st.button("➡️", key="btn_right", use_container_width=True):
            move_snake("RIGHT")
            st.rerun()

    c7, c8, c9 = st.columns([1, 1, 1])
    with c8:
        if st.button("⬇️", key="btn_down", use_container_width=True):
            move_snake("DOWN")
            st.rerun()

    st.markdown(
        """
    <script>
        const parentDoc = window.parent.document;
        setTimeout(() => {
            const btns = parentDoc.querySelectorAll('button');
            btns.forEach(btn => {
                if (btn.innerText.includes('⬆️')) btn.setAttribute('data-direction', 'UP');
                if (btn.innerText.includes('⬇️')) btn.setAttribute('data-direction', 'DOWN');
                if (btn.innerText.includes('⬅️')) btn.setAttribute('data-direction', 'LEFT');
                if (btn.innerText.includes('➡️')) btn.setAttribute('data-direction', 'RIGHT');
            });
        }, 300);
    </script>
    """,
        unsafe_allow_html=True,
    )

    if st.session_state.hint_msg:
        st.info(st.session_state.hint_msg)

    # بناء شبكة المتاهة المخصصة
    grid_html = '<div class="game-container"><div class="maze-grid">'
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            cell = [r, c]
            if cell == st.session_state.snake[0]:
                grid_html += '<div class="cell snake-head">👁️</div>'
            elif cell in st.session_state.snake:
                grid_html += '<div class="cell snake-body"></div>'
            elif cell == st.session_state.food:
                grid_html += '<div class="cell food">💎</div>'
            elif MAZE[r][c] == 1:
                grid_html += '<div class="cell wall"></div>'
            else:
                grid_html += '<div class="cell path"></div>'
    grid_html += "</div></div>"

    st.markdown(grid_html, unsafe_allow_html=True)

    col_score, col_kb = st.columns(2)
    col_score.metric("💎 النتيجة الحالية", f"{st.session_state.score} PTS")
    col_kb.caption(
        "⌨️ **طريقة التحكم:** استخدم أسهم الكيبورد (⬆️ ⬇️ ⬅️ ➡️) أو أزرار W, A, S, D"
    )

    if st.session_state.game_over:
        st.error(
            f"💥 انتهت اللعبة يا {player_name}! اصطدمت بالجدار أو بمحيط المتاهة."
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

        if st.button("🔄 جولة جديدة"):
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
            f"🎉 أداء أسطوري يا {player_name}! حققت {st.session_state.score} نقطة!"
        )

    if st.session_state.leaderboard:
        st.markdown("---")
        st.subheader("🏆 قائمة الأبطال (Leaderboard HD)")
        sorted_scores = sorted(
            st.session_state.leaderboard,
            key=lambda x: x["score"],
            reverse=True,
        )
        st.table(sorted_scores)

else:
    st.warning("⚡ يرجى إدخال اسمك أولاً للانطلاق في المتاهة.")