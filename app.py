import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Snake Cosmic Maze HD 🐍", page_icon="🐍", layout="centered"
)

# CSS للتنسيق العام
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
        font-size: 2.5rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 0.2rem;
        text-shadow: 0 0 20px rgba(0, 242, 254, 0.3);
    }
    
    .hd-subtitle {
        text-align: center;
        color: #8b949e;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hd-title">SNAKE COSMIC MAZE HD</div>', unsafe_allow_html=True
)
st.markdown(
    '<div class="hd-subtitle">تحكم مباشر ورسومي عبر أسهم لوحة المفاتيح ⌨️</div>',
    unsafe_allow_html=True,
)

# لعبة الأفعى كاملة بالـ Canvas و JavaScript لضمان التحكم بالأسهم 100%
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            background-color: transparent;
            color: white;
            font-family: 'Tajawal', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0;
            overflow: hidden;
        }
        #gameCanvas {
            background: #0f172a;
            border: 2px solid #00f2fe;
            border-radius: 16px;
            box-shadow: 0 0 20px rgba(0, 242, 254, 0.3);
            outline: none;
        }
        .stats {
            display: flex;
            justify-content: space-between;
            width: 400px;
            margin-top: 15px;
            font-size: 1.1rem;
            font-weight: bold;
        }
        .controls-hint {
            color: #8b949e;
            font-size: 0.9rem;
            margin-top: 10px;
        }
        button {
            background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
            border: none;
            color: #000;
            padding: 8px 16px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }
        button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 10px #00f2fe;
        }
    </style>
</head>
<body>

    <canvas id="gameCanvas" width="400" height="400" tabindex="1"></canvas>
    
    <div class="stats">
        <div>💎 النقاط: <span id="score">0</span></div>
        <button onclick="resetGame()">🔄 إعادة اللعب</button>
    </div>
    
    <div class="controls-hint">🎮 **طريقة التحكم:** اضغطي على الأسهم مباشرة (⬆️ ⬇️ ⬅️ ➡️) من لوحة المفاتيح!</div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        const gridSize = 10;
        const cellSize = canvas.width / gridSize;

        const MAZE = [
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [1, 1, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 1, 0],
            [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 1, 1, 0, 1],
            [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 0, 0]
        ];

        let snake = [{r: 0, c: 0}];
        let direction = {dr: 0, dc: 0};
        let food = generateFood();
        let score = 0;
        let gameOver = false;

        function generateFood() {
            while (true) {
                let r = Math.floor(Math.random() * gridSize);
                let c = Math.floor(Math.random() * gridSize);
                if (MAZE[r][c] === 0 && !snake.some(s => s.r === r && s.c === c)) {
                    return {r, c};
                }
            }
        }

        window.addEventListener("keydown", function(e) {
            if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].indexOf(e.code) > -1) {
                e.preventDefault();
            }

            if (e.key === "ArrowUp" && direction.dr !== 1) {
                direction = {dr: -1, dc: 0};
            } else if (e.key === "ArrowDown" && direction.dr !== -1) {
                direction = {dr: 1, dc: 0};
            } else if (e.key === "ArrowLeft" && direction.dc !== 1) {
                direction = {dr: 0, dc: -1};
            } else if (e.key === "ArrowRight" && direction.dc !== -1) {
                direction = {dr: 0, dc: 1};
            }
        });

        function gameLoop() {
            if (!gameOver) {
                moveSnake();
                draw();
            }
        }

        function moveSnake() {
            if (direction.dr === 0 && direction.dc === 0) return;

            let head = {r: snake[0].r + direction.dr, c: snake[0].c + direction.dc};

            if (head.r < 0 || head.r >= gridSize || head.c < 0 || head.c >= gridSize) {
                gameOver = true;
                alert("💥 انتهت اللعبة! الاصطدام بحدود المتاهة.");
                return;
            }

            if (MAZE[head.r][head.c] === 1 || snake.some(s => s.r === head.r && s.c === head.c)) {
                gameOver = true;
                alert("💥 انتهت اللعبة! الاصطدام بالجدار النيون أو بجسم الأفعى.");
                return;
            }

            snake.unshift(head);

            if (head.r === food.r && head.c === food.c) {
                score += 10;
                document.getElementById("score").innerText = score;
                food = generateFood();
            } else {
                snake.pop();
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            for (let r = 0; r < gridSize; r++) {
                for (let c = 0; c < gridSize; c++) {
                    if (MAZE[r][c] === 1) {
                        ctx.fillStyle = "#a855f7";
                        ctx.shadowColor = "#d8b4fe";
                        ctx.shadowBlur = 10;
                        ctx.fillRect(c * cellSize + 2, r * cellSize + 2, cellSize - 4, cellSize - 4);
                        ctx.shadowBlur = 0;
                    } else {
                        ctx.fillStyle = "rgba(255, 255, 255, 0.03)";
                        ctx.fillRect(c * cellSize + 2, r * cellSize + 2, cellSize - 4, cellSize - 4);
                    }
                }
            }

            ctx.fillStyle = "#ff0844";
            ctx.shadowColor = "#ff0844";
            ctx.shadowBlur = 15;
            ctx.beginPath();
            ctx.arc(food.c * cellSize + cellSize / 2, food.r * cellSize + cellSize / 2, cellSize / 3, 0, Math.PI * 2);
            ctx.fill();
            ctx.shadowBlur = 0;

            snake.forEach((segment, index) => {
                if (index === 0) {
                    ctx.fillStyle = "#00f2fe";
                    ctx.font = "24px Arial";
                    ctx.textAlign = "center";
                    ctx.textBaseline = "middle";
                    ctx.fillText("🐍", segment.c * cellSize + cellSize / 2, segment.r * cellSize + cellSize / 2);
                } else {
                    ctx.fillStyle = "#22c55e";
                    ctx.shadowColor = "#22c55e";
                    ctx.shadowBlur = 8;
                    ctx.fillRect(segment.c * cellSize + 3, segment.r * cellSize + 3, cellSize - 6, cellSize - 6);
                    ctx.shadowBlur = 0;
                }
            });
        }

        function resetGame() {
            snake = [{r: 0, c: 0}];
            direction = {dr: 0, dc: 0};
            food = generateFood();
            score = 0;
            gameOver = false;
            document.getElementById("score").innerText = score;
            draw();
            canvas.focus();
        }

        canvas.focus();
        setInterval(gameLoop, 200);
        draw();
    </script>
</body>
</html>
"""

components.html(game_html, height=520)