// =========================================================================
//  Snakes & Ladders — addition board game
// =========================================================================
document.addEventListener('DOMContentLoaded', () => {

    // --- Constants ---
    const COLS = 8;
    const ROWS = 5;
    const TOTAL = COLS * ROWS; // 40

    const LADDERS = { 4: 14, 9: 22, 20: 29, 28: 36 };
    const SNAKES  = { 17: 7, 26: 12, 31: 19, 38: 24 };

    const ROW_COLORS = [
        '#E1BEE7', '#FFF9C4', '#F8BBD0',
        '#BBDEFB', '#C8E6C9',
    ];

    const TOKENS = ['🐱', '🐰', '🦊', '🐻', '🐸',
                    '🦄', '🐶', '🐼'];

    // --- State ---
    let position = 0;
    let answering = false;
    let currentProblem = null;
    let correctCount = 0;
    let tokenEmoji = '🐱';

    // --- DOM refs ---
    const boardEl   = document.getElementById('sl-board');
    const boardWrap = document.getElementById('sl-board-wrap');
    const tokenEl   = document.getElementById('sl-token');
    const diceEl    = document.getElementById('sl-dice');
    const posEl     = document.getElementById('sl-pos');
    const qText     = document.getElementById('question-text');
    const numGrid   = document.getElementById('number-grid');
    const linesEl   = document.getElementById('sl-lines');

    // =================================================================
    //  Welcome / Champion screens
    // =================================================================
    populateAnimals('welcome-animals');
    populateAnimals('champion-animals');
    document.getElementById('play-btn')
        .addEventListener('click', startGame);
    document.getElementById('play-again-btn')
        .addEventListener('click', startGame);
    document.getElementById('sl-mute')
        .addEventListener('click', () => {
            muted = !muted;
            document.getElementById('sl-mute').innerHTML =
                muted ? '&#128263;' : '&#128264;';
        });

    // =================================================================
    //  Build board (once)
    // =================================================================
    function buildBoard() {
        boardEl.innerHTML = '';
        for (let vr = 0; vr < ROWS; vr++) {
            for (let vc = 0; vc < COLS; vc++) {
                const sq = gridToSquare(vr, vc);
                const cell = document.createElement('div');
                cell.className = 'sl-cell sl-row-' + vr;
                cell.id = 'sl-cell-' + sq;

                let icon = '';
                let cls = '';
                if (LADDERS[sq]) {
                    icon = '🪜';
                    cls = ' sl-ladder';
                } else if (SNAKES[sq]) {
                    icon = '🐍';
                    cls = ' sl-snake';
                }
                if (sq === TOTAL) cls += ' sl-finish';

                cell.className += cls;
                cell.innerHTML =
                    `<span class="sl-cell-num">${sq}</span>`
                    + (icon
                        ? `<span class="sl-cell-icon">`
                          + `${icon}</span>`
                        : '');
                boardEl.appendChild(cell);
            }
        }
        drawLines();
    }

    // =================================================================
    //  Draw snake/ladder lines on SVG overlay
    // =================================================================
    function drawLines() {
        let svg = '';
        // Ladders — golden dashed
        for (const [from, to] of Object.entries(LADDERS)) {
            const p1 = squareToCenter(+from);
            const p2 = squareToCenter(+to);
            svg += `<line x1="${p1.x}" y1="${p1.y}"
                x2="${p2.x}" y2="${p2.y}"
                stroke="#FFD700" stroke-width="6"
                stroke-dasharray="12,6"
                stroke-linecap="round" opacity="0.7"/>`;
            // Rungs
            const dx = p2.x - p1.x, dy = p2.y - p1.y;
            const len = Math.sqrt(dx * dx + dy * dy);
            const nx = -dy / len * 12, ny = dx / len * 12;
            const steps = Math.max(2,
                Math.round(len / 40));
            for (let i = 1; i < steps; i++) {
                const t = i / steps;
                const mx = p1.x + dx * t;
                const my = p1.y + dy * t;
                svg += `<line
                    x1="${mx - nx}" y1="${my - ny}"
                    x2="${mx + nx}" y2="${my + ny}"
                    stroke="#FFC107" stroke-width="3"
                    stroke-linecap="round"
                    opacity="0.5"/>`;
            }
        }
        // Snakes — red wavy
        for (const [from, to] of Object.entries(SNAKES)) {
            const p1 = squareToCenter(+from);
            const p2 = squareToCenter(+to);
            const mx = (p1.x + p2.x) / 2
                + (Math.random() - 0.5) * 60;
            const my = (p1.y + p2.y) / 2;
            svg += `<path d="M${p1.x},${p1.y}
                Q${mx},${my} ${p2.x},${p2.y}"
                stroke="#EF5350" stroke-width="6"
                fill="none" stroke-linecap="round"
                opacity="0.65"/>`;
            // Snake head dot
            svg += `<circle cx="${p1.x}" cy="${p1.y}"
                r="6" fill="#D32F2F" opacity="0.7"/>`;
        }
        linesEl.innerHTML = svg;
    }

    // Map visual grid position to square number
    function gridToSquare(vr, vc) {
        const row = ROWS - 1 - vr; // bottom row = 0
        const ltr = row % 2 === 0;
        const col = ltr ? vc : COLS - 1 - vc;
        return row * COLS + col + 1;
    }

    // Map square number to SVG viewBox coordinates
    // (viewBox is 800 x 500)
    function squareToCenter(sq) {
        const row = Math.floor((sq - 1) / COLS);
        const col = (sq - 1) % COLS;
        const ltr = row % 2 === 0;
        const vc = ltr ? col : COLS - 1 - col;
        const vr = ROWS - 1 - row;
        return {
            x: (vc + 0.5) * (800 / COLS),
            y: (vr + 0.5) * (500 / ROWS),
        };
    }

    // =================================================================
    //  Start game
    // =================================================================
    function startGame() {
        initAudio();
        position = 0;
        correctCount = 0;
        answering = false;
        tokenEmoji = TOKENS[
            Math.floor(Math.random() * TOKENS.length)];
        PrizeManager.init();
        buildBoard();
        showScreen('game-screen');
        document.body.className = 'level-1';
        spawnClouds();
        tokenEl.textContent = tokenEmoji;
        tokenEl.style.display = 'none';
        diceEl.textContent = '';
        updatePosDisplay();
        setTimeout(() => newRound(), 500);
    }

    // =================================================================
    //  New round — generate addition problem
    // =================================================================
    function newRound() {
        currentProblem = generateProblem();
        qText.innerHTML =
            `${currentProblem.a} + ${currentProblem.b}`
            + ` = <b>?</b>`;
        renderButtons(currentProblem.sum);
        answering = true;
    }

    // =================================================================
    //  Problem generation — difficulty by position
    // =================================================================
    function generateProblem() {
        let minA, maxA, maxSum;
        if (position <= 10) {
            minA = 0; maxA = 5; maxSum = 10;
        } else if (position <= 20) {
            minA = 1; maxA = 7; maxSum = 14;
        } else if (position <= 30) {
            minA = 2; maxA = 9; maxSum = 18;
        } else {
            minA = 3; maxA = 10; maxSum = 20;
        }
        const a = minA + Math.floor(
            Math.random() * (maxA - minA + 1));
        const bMax = Math.min(maxA, maxSum - a);
        const b = minA + Math.floor(
            Math.random()
            * (Math.max(bMax - minA + 1, 1)));
        return { a, b, sum: a + b };
    }

    // =================================================================
    //  Render answer buttons
    // =================================================================
    function renderButtons(correct) {
        numGrid.innerHTML = '';
        const lo = Math.max(0, correct - 5);
        const hi = Math.min(20, Math.max(correct + 5,
            lo + 9));
        for (let i = lo; i <= hi; i++) {
            const btn = document.createElement('button');
            btn.className = 'num-btn';
            btn.textContent = i;
            const num = i;
            btn.addEventListener('click', () =>
                handleAnswer(num, btn));
            numGrid.appendChild(btn);
        }
    }

    // =================================================================
    //  Handle answer
    // =================================================================
    function handleAnswer(num, btn) {
        if (!answering) return;
        answering = false;
        initAudio();

        if (num === currentProblem.sum) {
            onCorrect(btn);
        } else {
            onWrong(btn);
        }
    }

    function onCorrect(btn) {
        correctCount++;
        sfxCorrect();
        btn.classList.add('correct-flash');
        showFeedback(
            ['Great!','Awesome!','Super!','Yay!','Wow!'][
                Math.floor(Math.random() * 5)],
            'correct', 1000);

        // Roll dice after short delay
        setTimeout(() => {
            const roll = 1 + Math.floor(
                Math.random() * 3);
            showDice(roll, () => {
                moveToken(roll, () => {
                    // Check prize
                    if (position < TOTAL &&
                        PrizeManager.check(
                            () => newRound())) {
                        return;
                    }
                    if (position < TOTAL) {
                        newRound();
                    }
                });
            });
        }, 800);
    }

    function onWrong(btn) {
        sfxWrong();
        btn.classList.add('shake');
        showFeedback(
            ['Try again!','Almost!','One more try!'][
                Math.floor(Math.random() * 3)],
            'wrong', 1000);
        setTimeout(() => {
            btn.classList.remove('shake');
            answering = true;
        }, 800);
    }

    // =================================================================
    //  Dice display
    // =================================================================
    function showDice(roll, cb) {
        qText.textContent = '';
        numGrid.innerHTML = '';
        diceEl.textContent = '🎲 ' + roll;
        diceEl.classList.remove('sl-roll');
        void diceEl.offsetWidth; // reflow
        diceEl.classList.add('sl-roll');
        sfxPop();
        setTimeout(cb, 900);
    }

    // =================================================================
    //  Move token step by step
    // =================================================================
    function moveToken(steps, cb) {
        diceEl.textContent = '';
        if (position === 0) {
            tokenEl.style.display = 'flex';
        }
        moveStep(steps, cb);
    }

    function moveStep(remaining, cb) {
        if (remaining <= 0) {
            // Check snake or ladder
            checkSquare(cb);
            return;
        }
        position = Math.min(position + 1, TOTAL);
        updatePosDisplay();
        positionToken(position);
        sfxPop();
        highlightCell(position);

        if (position >= TOTAL) {
            setTimeout(() => winGame(), 600);
            return;
        }

        setTimeout(() =>
            moveStep(remaining - 1, cb), 350);
    }

    // =================================================================
    //  Check for snake / ladder
    // =================================================================
    function checkSquare(cb) {
        if (LADDERS[position]) {
            const dest = LADDERS[position];
            showEvent('🪜 Ladder! → ' + dest,
                'sl-ladder-event');
            sfxLevelUp();
            spawnConfetti(20);
            tokenEl.classList.add('sl-slide');
            setTimeout(() => {
                position = dest;
                updatePosDisplay();
                positionToken(position);
                highlightCell(position);
                setTimeout(() => {
                    tokenEl.classList.remove('sl-slide');
                    cb();
                }, 900);
            }, 600);
        } else if (SNAKES[position]) {
            const dest = SNAKES[position];
            showEvent('🐍 Snake! → ' + dest,
                'sl-snake-event');
            sfxWrong();
            tokenEl.classList.add('sl-slide');
            setTimeout(() => {
                position = dest;
                updatePosDisplay();
                positionToken(position);
                highlightCell(position);
                setTimeout(() => {
                    tokenEl.classList.remove('sl-slide');
                    cb();
                }, 900);
            }, 600);
        } else {
            cb();
        }
    }

    // =================================================================
    //  Position token on a square
    // =================================================================
    function positionToken(sq) {
        const cell = document.getElementById(
            'sl-cell-' + sq);
        if (!cell || !boardWrap) return;
        const bRect = boardWrap.getBoundingClientRect();
        const cRect = cell.getBoundingClientRect();
        const tW = tokenEl.offsetWidth;
        const tH = tokenEl.offsetHeight;
        tokenEl.style.left =
            (cRect.left - bRect.left
             + cRect.width / 2 - tW / 2) + 'px';
        tokenEl.style.top =
            (cRect.top - bRect.top
             + cRect.height / 2 - tH / 2) + 'px';
    }

    // =================================================================
    //  Highlight current cell
    // =================================================================
    let prevHighlight = null;

    function highlightCell(sq) {
        // Clear previous highlight
        if (prevHighlight) {
            prevHighlight.style.boxShadow = '';
        }
        const cell = document.getElementById(
            'sl-cell-' + sq);
        if (cell && !cell.classList.contains('sl-ladder')
            && !cell.classList.contains('sl-snake')) {
            cell.style.boxShadow =
                'inset 0 0 0 3px #FF6F00,'
                + ' 0 0 10px rgba(255,111,0,0.4)';
            prevHighlight = cell;
        } else {
            prevHighlight = null;
        }
    }

    // =================================================================
    //  Event banner (ladder / snake)
    // =================================================================
    function showEvent(text, cls) {
        const el = document.createElement('div');
        el.className = 'sl-event ' + cls;
        el.textContent = text;
        document.body.appendChild(el);
        setTimeout(() => el.remove(), 2000);
    }

    // =================================================================
    //  Win
    // =================================================================
    function winGame() {
        sfxChampion();
        spawnConfetti(80);
        showScreen('champion-screen');
    }

    // =================================================================
    //  Helpers
    // =================================================================
    function updatePosDisplay() {
        posEl.textContent =
            `Square ${position} / ${TOTAL}`;
        // Update background based on progress
        const pct = position / TOTAL;
        if (pct > 0.75) {
            document.body.className = 'level-4';
        } else if (pct > 0.5) {
            document.body.className = 'level-3';
        } else if (pct > 0.25) {
            document.body.className = 'level-2';
        } else {
            document.body.className = 'level-1';
        }
    }

    function showScreen(id) {
        document.querySelectorAll('.screen')
            .forEach(s => s.classList.add('hidden'));
        document.getElementById(id)
            .classList.remove('hidden');
    }

    // Reposition token on window resize
    window.addEventListener('resize', () => {
        if (position > 0) {
            tokenEl.style.transition = 'none';
            positionToken(position);
            requestAnimationFrame(() => {
                tokenEl.style.transition = '';
            });
        }
    });
});
