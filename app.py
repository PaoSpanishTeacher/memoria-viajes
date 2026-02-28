import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Memoria - Viajes", layout="wide")

# Estilo para limpiar la interfaz de Streamlit
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    iframe { border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

html_viajes = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Dancing+Script:wght@700&family=Quicksand:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --azul-viaje: #00b4d8;
            --azul-oscuro: #0077b6;
            --naranja: #ffb703;
            --blanco: #ffffff;
        }

        * { box-sizing: border-box; }

        body {
            margin: 0;
            font-family: 'Quicksand', sans-serif;
            background: linear-gradient(rgba(255,255,255,0.2), rgba(255,255,255,0.2)), 
                        url('https://img.freepik.com/vector-gratis/fondo-dibujos-animados-aeropuerto-terminal-salon-salidas-interior-puerta-embarque_107791-4562.jpg');
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
            overflow-x: hidden;
        }

        header { text-align: center; margin-bottom: 20px; }
        
        h1 { 
            font-family: 'Montserrat', sans-serif; 
            color: var(--azul-oscuro); 
            font-size: 3rem; 
            margin: 0;
            text-shadow: 3px 3px 0px white;
        }

        .brand-name {
            font-family: 'Dancing Script', cursive;
            color: #d62828;
            font-size: 1.8rem;
            margin-top: -5px;
        }

        .game-container {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 15px;
            max-width: 900px;
            width: 100%;
            perspective: 1000px;
        }

        .card {
            aspect-ratio: 1/1;
            position: relative;
            cursor: pointer;
            transform-style: preserve-3d;
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .card:hover:not(.flipped) {
            transform: scale(1.05) translateY(-5px);
        }

        .card.flipped { transform: rotateY(180deg); }

        .card-face {
            position: absolute;
            width: 100%; height: 100%;
            backface-visibility: hidden;
            border-radius: 15px;
            display: flex;
            justify-content: center;
            align-items: center;
            border: 4px solid white;
            box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        }

        .card-front {
            background: var(--azul-viaje);
            background-image: radial-gradient(circle, #90e0ef 10%, transparent 11%);
            background-size: 20px 20px;
            z-index: 2;
        }

        .card-front::after {
            content: '✈️';
            font-size: 3rem;
            filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.2));
        }

        .card-back {
            background: var(--blanco);
            transform: rotateY(180deg);
            background-image: url('https://www.transparenttextures.com/patterns/clouds.png');
        }

        .card-image { font-size: 4rem; }
        .card-text { 
            font-size: 1.2rem; 
            font-weight: 700; 
            color: var(--azul-oscuro); 
            text-align: center;
            padding: 5px;
        }

        /* Mensaje animado Excelente */
        #msg-pop {
            position: fixed; top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            font-size: 4rem; font-weight: bold;
            color: #ffb703; text-shadow: 3px 3px 0 #000;
            display: none; z-index: 100;
            animation: bounceIn 0.5s ease;
        }

        @keyframes bounceIn {
            0% { transform: translate(-50%, -50%) scale(0); }
            70% { transform: translate(-50%, -50%) scale(1.2); }
            100% { transform: translate(-50%, -50%) scale(1); }
        }

        /* Pantalla Final */
        #final-screen {
            position: fixed; inset: 0;
            background: rgba(255, 255, 255, 0.95);
            display: none; flex-direction: column;
            justify-content: center; align-items: center;
            z-index: 200; text-align: center; padding: 20px;
        }

        .teacher-img {
            width: 200px;
            height: 200px;
            background: url('https://cdn-icons-png.flaticon.com/512/3429/3429433.png');
            background-size: contain;
            background-repeat: no-repeat;
            margin-bottom: 20px;
            animation: float 3s infinite ease-in-out;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }

        .btn-restart {
            padding: 20px 50px;
            background: #d62828;
            color: white;
            border: none;
            border-radius: 50px;
            font-size: 1.8rem;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 10px 0 #9d1d1d;
            transition: 0.2s;
        }

        .btn-restart:active {
            transform: translateY(5px);
            box-shadow: 0 5px 0 #9d1d1d;
        }

        .watermark {
            position: fixed; bottom: 10px; right: 10px;
            font-size: 0.8rem; color: rgba(0,0,0,0.3);
            font-style: italic; font-family: 'Dancing Script', cursive;
        }

        .balloon {
            position: absolute; bottom: -100px;
            width: 40px; height: 50px; border-radius: 50%;
            animation: fly 5s linear forwards;
        }

        @keyframes fly {
            to { transform: translateY(-120vh) translateX(50px); }
        }
    </style>
</head>
<body>

    <header>
        <h1>Memoria - Viajes</h1>
        <div class="brand-name">PaoSpanishTeacher</div>
    </header>

    <main class="game-container" id="board"></main>

    <div id="msg-pop">⭐ ¡Excelente! ⭐</div>

    <div id="final-screen">
        <div class="teacher-img"></div>
        <h2 style="font-size: 2.5rem; color: var(--azul-oscuro);">¡Felicidades!</h2>
        <p style="font-size: 1.5rem;">Has completado la memoria de viajes.</p>
        <p style="font-style: italic; color: #666;">Juego creado por PaoSpanishTeacher</p>
        <button class="btn-restart" onclick="resetGame()">Jugar otra vez</button>
    </div>

    <div class="watermark">PaoSpanishTeacher</div>

    <audio id="snd-match" src="https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3"></audio>
    <audio id="snd-error" src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3"></audio>
    <audio id="snd-win" loop src="https://assets.mixkit.co/active_storage/sfx/123/123-preview.mp3"></audio>

    <script>
        const DATA = [
            { n: "Aeropuerto", i: "🏢" }, { n: "Avión", i: "✈️" },
            { n: "Maleta", i: "🧳" }, { n: "Pasaporte", i: "🛂" },
            { n: "Hotel", i: "🏨" }, { n: "Mapa", i: "🗺️" },
            { n: "Playa", i: "🏖️" }, { n: "Tren", i: "🚂" },
            { n: "Autobús", i: "🚌" }, { n: "Turista", i: "📸" }
        ];

        let flipped = [];
        let matches = 0;
        let lock = false;

        function shuffle(array) {
            for (let i = array.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [array[i], array[j]] = [array[j], array[i]];
            }
            return array;
        }

        function init() {
            const board = document.getElementById('board');
            board.innerHTML = '';
            let deck = [];
            DATA.forEach(item => {
                deck.push({ t: 'text', v: item.n, id: item.n });
                deck.push({ t: 'img', v: item.i, id: item.n });
            });
            shuffle(deck);

            deck.forEach(item => {
                const card = document.createElement('div');
                card.className = 'card';
                card.dataset.id = item.id;
                card.innerHTML = `
                    <div class="card-face card-front"></div>
                    <div class="card-face card-back">
                        ${item.t === 'text' ? `<span class="card-text">${item.v}</span>` : `<span class="card-image">${item.v}</span>`}
                    </div>`;
                card.onclick = () => flip(card);
                board.appendChild(card);
            });
        }

        function flip(card) {
            if (lock || card.classList.contains('flipped')) return;
            
            // Wake up audio context on first click
            document.getElementById('snd-match').play().then(() => {
                document.getElementById('snd-match').pause();
                document.getElementById('snd-match').currentTime = 0;
            }).catch(() => {});

            card.classList.add('flipped');
            flipped.push(card);

            if (flipped.length === 2) check();
        }

        function check() {
            lock = true;
            const [c1, c2] = flipped;
            if (c1.dataset.id === c2.dataset.id) {
                matches++;
                document.getElementById('snd-match').play();
                showPop();
                flipped = [];
                lock = false;
                if (matches === DATA.length) win();
            } else {
                document.getElementById('snd-error').play();
                setTimeout(() => {
                    c1.classList.remove('flipped');
                    c2.classList.remove('flipped');
                    flipped = [];
                    lock = false;
                }, 1200);
            }
        }

        function showPop() {
            const p = document.getElementById('msg-pop');
            p.style.display = 'block';
            confetti({ particleCount: 40, spread: 50, origin: { y: 0.7 } });
            setTimeout(() => p.style.display = 'none', 800);
        }

        function win() {
            document.getElementById('snd-win').play();
            confetti({ particleCount: 200, spread: 90, origin: { y: 0.6 } });
            
            // Globos
            for(let i=0; i<15; i++) {
                setTimeout(() => {
                    const b = document.createElement('div');
                    b.className = 'balloon';
                    b.style.left = Math.random() * 90 + 'vw';
                    b.style.background = `hsl(${Math.random() * 360}, 70%, 60%)`;
                    document.body.appendChild(b);
                    setTimeout(() => b.remove(), 5000);
                }, i * 300);
            }

            setTimeout(() => {
                document.getElementById('final-screen').style.display = 'flex';
                speak();
            }, 1000);
        }

        function speak() {
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance("Te felicito, sigue avanzando en tu español.");
                utterance.lang = 'es-ES';
                utterance.rate = 0.9;
                window.speechSynthesis.speak(utterance);
            }
        }

        function resetGame() {
            matches = 0;
            flipped = [];
            lock = false;
            document.getElementById('snd-win').pause();
            document.getElementById('snd-win').currentTime = 0;
            document.getElementById('final-screen').style.display = 'none';
            init();
        }

        init();
    </script>
</body>
</html>
"""

components.html(html_viajes, height=900, scrolling=False)
