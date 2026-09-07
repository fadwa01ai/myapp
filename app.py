import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Snake Cosmic Maze HD 🐍", page_icon="🪐", layout="centered"
)

# CSS للتصميم الكوني الغامر
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at center, #111827 0%, #030712 100%);
        color: #f3f4f6;
    }

    .hd-title {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.6rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 0.2rem;
        text-shadow: 0 0 25px rgba(0, 242, 254, 0.4);
    }

    .hd-subtitle {
        text-align: center;
        color: #9ca3af;
        font-size: 1rem;
        margin-bottom: 1rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hd-title">SNAKE COSMIC MAZE HD 🪐</div>', unsafe_allow_html=True
)
st.markdown(
    '<div class="hd-subtitle">متاهة الأفعى الفضائية | أسهم لوحة المفاتيح أو أزرار اللمس 📱⌨️</div>',
    unsafe_allow_html=True,
)

# كود اللعبة بالكامل
game_html = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');

        body {
            background-color: transparent;
            color: #f3f4f6;
            font-family: 'Tajawal', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0;
            overflow: hidden;
            -webkit-user-select: none;
            user-select: none;
        }

        .canvas-wrapper {
            position: relative;
            border-radius: 20px;
            padding: 10px;
            background: rgba(17, 24, 39, 0.8);
            box-shadow: 0 0 35px rgba(0, 242, 254, 0.25), inset 0 0 15px rgba(168, 85, 247, 0.2);
            border: 2px solid rgba(0, 242, 254, 0.5);
        }

        #gameCanvas {
            background: #090d16;
            border-radius: 12px;
            outline: none;
            display: block;
            touch-action: none;
        }

        .dashboard {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 420px;
            margin-top: 15px;
            padding: 10px 15px;
            background: rgba(31, 41, 55, 0.7);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .stat-box {
            font-size: 1.1rem;
            font-weight: bold;
        }

        .stat-box span {
            color: #00f2fe;
            font-size: 1.3rem;
        }

        .btn-action {
            background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
            border: none;
            color: #000;
            padding: 8px 18px;
            font-weight: 900;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
            font-family: 'Tajawal', sans-serif;
        }

        .btn-action:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.6);
        }

        .leaderboard-card {
            width: 420px;
            margin-top: 15px;
            background: rgba(17, 24, 39, 0.85);
            border: 1px solid rgba(168, 85, 247, 0.4);
            border-radius: 12px;
            padding: 12px 18px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        }

        .leaderboard-title {
            text-align: center;
            font-size: 1.1rem;
            font-weight: bold;
            color: #d8b4fe;
            margin-bottom: 10px;
            text-shadow: 0 0 10px rgba(168, 85, 247, 0.5);
        }

        .leaderboard-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .leaderboard-item {
            display: flex;
            justify-content: space-between;
            padding: 6px 12px;
            margin-bottom: 6px;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.05);
            font-size: 0.95rem;
        }

        .rank-1 { border-right: 4px solid #ffd700; background: rgba(255, 215, 0, 0.1); }
        .rank-2 { border-right: 4px solid #c0c0c0; background: rgba(192, 192, 192, 0.1); }
        .rank-3 { border-right: 4px solid #cd7f32; background: rgba(205, 127, 50, 0.1); }

        .overlay {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(9, 13, 22, 0.92);
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 10;
            text-align: center;
            padding: 20px;
            box-sizing: border-box;
        }

        .overlay input {
            padding: 10px 15px;
            border-radius: 8px;
            border: 1px solid #00f2fe;
            background: #1e293b;
            color: white;
            font-family: 'Tajawal', sans-serif;
            font-size: 1rem;
            text-align: center;
            margin-bottom: 12px;
            outline: none;
        }

        .overlay h3 { color: #00f2fe; margin-bottom: 10px; }
        .overlay .score-final { color: #d8b4fe; font-size: 1.2rem; margin-bottom: 16px; }

        .touch-controls {
            display: none;
            margin-top: 14px;
            grid-template-columns: repeat(3, 56px);
            grid-template-rows: repeat(2, 56px);
            gap: 8px;
            justify-content: center;
        }

        .touch-btn {
            background: rgba(0, 242, 254, 0.15);
            border: 1px solid rgba(0, 242, 254, 0.5);
            color: #00f2fe;
            font-size: 1.4rem;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            user-select: none;
        }

        .touch-btn:active { background: rgba(0, 242, 254, 0.4); }

        @media (pointer: coarse) {
            .touch-controls { display: grid; }
        }
    </style>
</head>
<body>

    <div class="canvas-wrapper">
        <canvas id="gameCanvas" width="400" height="400" tabindex="1"></canvas>

        <div id="startOverlay" class="overlay">
            <h3>🌌 مرحباً بك في المتاهة</h3>
            <input type="text" id="playerNameInput" placeholder="أدخل اسمك للانطلاق..." maxlength="12">
            <button class="btn-action" onclick="startGame()">بدء اللعبة 🚀</button>
        </div>

        <div id="gameOverOverlay" class="overlay" style="display:none;">
            <h3>💥 انتهت اللعبة</h3>
            <div class="score-final" id="finalScoreText">مجموع نقاطك: 0</div>
            <button class="btn-action" onclick="resetGame()">🔄 العب مرة أخرى</button>
        </div>
    </div>

    <div class="touch-controls" id="touchControls">
        <div></div>
        <div class="touch-btn" data-dir="up">⬆️</div>
        <div></div>
        <div class="touch-btn" data-dir="left">⬅️</div>
        <div class="touch-btn" data-dir="down">⬇️</div>
        <div class="touch-btn" data-dir="right">➡️</div>
    </div>

    <div class="dashboard">
        <div class="stat-box">🎮 اللاعب: <span id="displayName">---</span></div>
        <div class="stat-box">💎 النقاط: <span id="score">0</span></div>
        <button class="btn-action" onclick="resetGame()">🔄 إعادة</button>
    </div>

    <div class="leaderboard-card">
        <div class="leaderboard-title">🏆 لوحة صدارة الأبطال (Top 3)</div>
        <ul id="leaderboardList" class="leaderboard-list">
            <li class="leaderboard-item"><span>1. ---</span><span>0 PTS</span></li>
            <li class="leaderboard-item"><span>2. ---</span><span>0 PTS</span></li>
            <li class="leaderboard-item"><span>3. ---</span><span>0 PTS</span></li>
        </ul>
    </div>

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
        let gameStarted = false;
        let playerName = "محارب المجرة";

        // localStorage قد يفشل في بعض المتصفحات (وضع التصفح الخاص، iframes مقيدة)
        // لذلك نحميه بـ try/catch حتى لا تتعطل اللعبة بالكامل.
        function loadLeaderboard() {
            try {
                return JSON.parse(localStorage.getItem("cosmic_snake_top3")) || [];
            } catch (e) {
                return [];
            }
        }

        function persistLeaderboard() {
            try {
                localStorage.setItem("cosmic_snake_top3", JSON.stringify(leaderboard));
            } catch (e) {
                // تجاهل بصمت إذا التخزين غير متاح
            }
        }

        let leaderboard = loadLeaderboard();

        function updateLeaderboardUI() {
            const list = document.getElementById("leaderboardList");
            list.innerHTML = "";

            for (let i = 0; i < 3; i++) {
                const item = leaderboard[i] || { name: "---", score: 0 };
                const li = document.createElement("li");
                li.className = `leaderboard-item rank-${i+1}`;

                let medal = i === 0 ? "🥇" : i === 1 ? "🥈" : "🥉";
                li.innerHTML = `<span>${medal} ${i+1}. ${item.name}</span><span>${item.score} PTS</span>`;
                list.appendChild(li);
            }
        }

        function saveScore(name, pts) {
            if (pts === 0) return;
            leaderboard.push({ name: name, score: pts });
            leaderboard.sort((a, b) => b.score - a.score);
            leaderboard = leaderboard.slice(0, 3);
            persistLeaderboard();
            updateLeaderboardUI();
        }

        function generateFood() {
            while (true) {
                let r = Math.floor(Math.random() * gridSize);
                let c = Math.floor(Math.random() * gridSize);
                if (MAZE[r][c] === 0 && !snake.some(s => s.r === r && s.c === c)) {
                    return {r, c};
                }
            }
        }

        function setDirection(dir) {
            if (!gameStarted || gameOver) return;
            if (dir === "up" && direction.dr !== 1) direction = {dr: -1, dc: 0};
            else if (dir === "down" && direction.dr !== -1) direction = {dr: 1, dc: 0};
            else if (dir === "left" && direction.dc !== 1) direction = {dr: 0, dc: -1};
            else if (dir === "right" && direction.dc !== -1) direction = {dr: 0, dc: 1};
        }

        window.addEventListener("keydown", function(e) {
            if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].indexOf(e.code) > -1) {
                e.preventDefault();
            }

            if (!gameStarted || gameOver) return;

            if (e.key === "ArrowUp" || e.key === "w" || e.key === "W") setDirection("up");
            else if (e.key === "ArrowDown" || e.key === "s" || e.key === "S") setDirection("down");
            else if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") setDirection("left");
            else if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") setDirection("right");
        });

        // أزرار اللمس للموبايل
        document.querySelectorAll(".touch-btn").forEach(btn => {
            btn.addEventListener("click", () => setDirection(btn.dataset.dir));
        });

        // دعم السحب (swipe) على الشاشة مباشرة
        let touchStartX = 0, touchStartY = 0;
        canvas.addEventListener("touchstart", (e) => {
            const t = e.touches[0];
            touchStartX = t.clientX;
            touchStartY = t.clientY;
        }, { passive: true });

        canvas.addEventListener("touchend", (e) => {
            const t = e.changedTouches[0];
            const dx = t.clientX - touchStartX;
            const dy = t.clientY - touchStartY;
            if (Math.abs(dx) < 20 && Math.abs(dy) < 20) return;
            if (Math.abs(dx) > Math.abs(dy)) {
                setDirection(dx > 0 ? "right" : "left");
            } else {
                setDirection(dy > 0 ? "down" : "up");
            }
        }, { passive: true });

        function startGame() {
            const input = document.getElementById("playerNameInput").value.trim();
            if (input !== "") playerName = input;
            document.getElementById("displayName").innerText = playerName;
            document.getElementById("startOverlay").style.display = "none";
            gameStarted = true;
            canvas.focus();
        }

        function gameLoop() {
            if (gameStarted && !gameOver) {
                moveSnake();
                draw();
            }
        }

        function moveSnake() {
            if (direction.dr === 0 && direction.dc === 0) return;

            let head = {r: snake[0].r + direction.dr, c: snake[0].c + direction.dc};

            if (head.r < 0 || head.r >= gridSize || head.c < 0 || head.c >= gridSize ||
                MAZE[head.r][head.c] === 1 || snake.some(s => s.r === head.r && s.c === head.c)) {
                gameOver = true;
                saveScore(playerName, score);
                document.getElementById("finalScoreText").innerText = `${playerName} — مجموع نقاطك: ${score}`;
                document.getElementById("gameOverOverlay").style.display = "flex";
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
                        ctx.shadowBlur = 12;
                        ctx.fillRect(c * cellSize + 2, r * cellSize + 2, cellSize - 4, cellSize - 4);
                        ctx.shadowBlur = 0;
                    } else {
                        ctx.fillStyle = "rgba(255, 255, 255, 0.02)";
                        ctx.fillRect(c * cellSize + 2, r * cellSize + 2, cellSize - 4, cellSize - 4);
                    }
                }
            }

            ctx.fillStyle = "#ff0844";
            ctx.shadowColor = "#ff0844";
            ctx.shadowBlur = 18;
            ctx.beginPath();
            ctx.arc(food.c * cellSize + cellSize / 2, food.r * cellSize + cellSize / 2, cellSize / 3.2, 0, Math.PI * 2);
            ctx.fill();
            ctx.shadowBlur = 0;

            snake.forEach((segment, index) => {
                if (index === 0) {
                    ctx.font = "24px Arial";
                    ctx.textAlign = "center";
                    ctx.textBaseline = "middle";
                    ctx.fillText("🐍", segment.c * cellSize + cellSize / 2, segment.r * cellSize + cellSize / 2);
                } else {
                    ctx.fillStyle = "#22c55e";
                    ctx.shadowColor = "#22c55e";
                    ctx.shadowBlur = 8;
                    ctx.fillRect(segment.c * cellSize + 4, segment.r * cellSize + 4, cellSize - 8, cellSize - 8);
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
            document.getElementById("gameOverOverlay").style.display = "none";
            document.getElementById("score").innerText = score;
            draw();
            canvas.focus();
        }

        updateLeaderboardUI();
        draw();

        // إبطاء السرعة إلى 450ms للحركة المريحة
        setInterval(gameLoop, 450);
    </script>
</body>
</html>
"""

components.html(game_html, height=760)
