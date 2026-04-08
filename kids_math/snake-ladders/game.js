// =========================================================================
//  Snakes & Ladders — Player vs Computer
// =========================================================================
document.addEventListener('DOMContentLoaded', () => {

    // --- Constants ---
    const COLS = 8, ROWS = 5, TOTAL = 40;
    const STREAK_NEEDED = 3;
    const LADDERS = { 4:14, 9:22, 20:29, 28:36 };
    const SNAKES  = { 17:7, 26:12, 31:19, 38:24 };
    const ANIMALS = ['🐱','🐰','🦊','🐻','🐸',
                     '🦄','🐶','🐼'];

    // ---- State ---
    let playerAnimal = '', computerAnimal = '';
    let playerPos = 0, computerPos = 0;
    let turn = 'player'; // 'player' | 'computer'
    let streak = 0;
    let answering = false;
    let currentProblem = null;

    // --- DOM refs ---
    const boardEl     = document.getElementById('sl-board');
    const boardWrap   = document.getElementById('sl-board-wrap');
    const pTokenEl    = document.getElementById('sl-token-player');
    const cTokenEl    = document.getElementById('sl-token-computer');
    const diceEl      = document.getElementById('sl-dice');
    const qText       = document.getElementById('question-text');
    const numGrid     = document.getElementById('number-grid');
    const linesEl     = document.getElementById('sl-lines');
    const turnEl      = document.getElementById('sl-turn');
    const streakWrap  = document.getElementById('sl-streak');
    const streakDots  = [
        document.getElementById('sd-1'),
        document.getElementById('sd-2'),
        document.getElementById('sd-3'),
    ];

    // =================================================================
    //  Screen management
    // =================================================================
    populateAnimals('welcome-animals');
    populateAnimals('champion-animals');
    populateAnimals('lose-animals');

    document.getElementById('play-btn')
        .addEventListener('click', showSelectScreen);
    document.getElementById('play-again-btn')
        .addEventListener('click', showSelectScreen);
    document.getElementById('retry-btn')
        .addEventListener('click', showSelectScreen);
    document.getElementById('sl-mute')
        .addEventListener('click', () => {
            muted = !muted;
            document.getElementById('sl-mute').innerHTML =
                muted ? '&#128263;' : '&#128264;';
        });

    function showScreen(id) {
        document.querySelectorAll('.screen')
            .forEach(s => s.classList.add('hidden'));
        document.getElementById(id)
            .classList.remove('hidden');
    }

    // =================================================================
    //  Animal selection screen
    // =================================================================
    function showSelectScreen() {
        initAudio();
        showScreen('select-screen');
        document.body.className = 'level-1';
        spawnClouds();

        const grid = document.getElementById(
            'sl-animal-grid');
        const vsLabel = document.getElementById(
            'sl-vs-label');
        const compPreview = document.getElementById(
            'sl-computer-preview');
        const startBtn = document.getElementById(
            'start-btn');

        grid.innerHTML = '';
        vsLabel.textContent = '';
        compPreview.textContent = '';
        startBtn.classList.add('hidden');
        playerAnimal = '';
        computerAnimal = '';

        ANIMALS.forEach(a => {
            const btn = document.createElement('button');
            btn.className = 'sl-animal-btn';
            btn.textContent = a;
            btn.addEventListener('click', () => {
                // Deselect all
                grid.querySelectorAll('.sl-animal-btn')
                    .forEach(b =>
                        b.classList.remove('selected'));
                btn.classList.add('selected');
                playerAnimal = a;
                sfxPop();

                // Pick different animal for computer
                const others = ANIMALS.filter(
                    x => x !== a);
                computerAnimal = others[
                    Math.floor(Math.random()
                        * others.length)];

                vsLabel.textContent = 'VS';
                compPreview.textContent = computerAnimal;
                startBtn.classList.remove('hidden');
            });
            grid.appendChild(btn);
        });

        startBtn.onclick = () => {
            if (playerAnimal) startGame();
        };
    }

    // =================================================================
    //  Start game
    // =================================================================
    function startGame() {
        playerPos = 0;
        computerPos = 0;
        streak = 0;
        answering = false;
        turn = 'player';

        pTokenEl.textContent = playerAnimal;
        cTokenEl.textContent = computerAnimal;
        pTokenEl.style.display = 'none';
        cTokenEl.style.display = 'none';

        document.getElementById('sp-emoji')
            .textContent = playerAnimal;
        document.getElementById('sc-emoji')
            .textContent = computerAnimal;

        buildBoard();
        showScreen('game-screen');
        document.body.className = 'level-1';
        spawnClouds();
        diceEl.textContent = '';
        updateScoreboard();
        renderStreak();

        setTimeout(() => startPlayerTurn(), 500);
    }

    // =================================================================
    //  Turn management
    // =================================================================
    function startPlayerTurn() {
        turn = 'player';
        streak = 0;
        renderStreak();
        streakWrap.style.display = 'flex';
        updateTurnDisplay();
        newRound();
    }

    function startComputerTurn() {
        turn = 'computer';
        answering = false;
        streakWrap.style.display = 'none';
        qText.textContent = '';
        numGrid.innerHTML = '';
        updateTurnDisplay();

        // Computer "thinks", then rolls
        setTimeout(() => {
            const roll = 1 + Math.floor(
                Math.random() * 3);
            diceEl.className = 'sl-dice computer-dice';
            showDice(roll, () => {
                diceEl.className = 'sl-dice';
                moveToken('computer', roll, () => {
                    if (computerPos >= TOTAL) {
                        computerWins();
                    } else {
                        setTimeout(() =>
                            startPlayerTurn(), 600);
                    }
                });
            });
        }, 1200);
    }

    function updateTurnDisplay() {
        const isP = turn === 'player';
        turnEl.className = 'sl-turn-banner '
            + (isP ? 'player-turn' : 'computer-turn');
        turnEl.textContent = isP
            ? `Your turn! ${playerAnimal}`
            : `Computer... ${computerAnimal}`;

        const sp = document.getElementById('score-player');
        const sc = document.getElementById('score-computer');
        sp.className = 'sl-score-item'
            + (isP ? ' active-player' : '');
        sc.className = 'sl-score-item'
            + (!isP ? ' active-computer' : '');
    }

    function updateScoreboard() {
        document.getElementById('sp-sq').textContent =
            playerPos;
        document.getElementById('sc-sq').textContent =
            computerPos;
        // Background by leader
        const best = Math.max(playerPos, computerPos);
        const pct = best / TOTAL;
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

    // =================================================================
    //  Streak display
    // =================================================================
    function renderStreak() {
        for (let i = 0; i < STREAK_NEEDED; i++) {
            if (i < streak) {
                streakDots[i].classList.add('filled');
            } else {
                streakDots[i].classList.remove('filled');
            }
        }
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
        // Re-position both tokens after layout change
        requestAnimationFrame(() => positionTokens());
        answering = true;
    }

    function generateProblem() {
        const pos = playerPos;
        let minA, maxA, maxSum;
        if (pos <= 10) {
            minA = 0; maxA = 5; maxSum = 10;
        } else if (pos <= 20) {
            minA = 1; maxA = 7; maxSum = 14;
        } else if (pos <= 30) {
            minA = 2; maxA = 9; maxSum = 18;
        } else {
            minA = 3; maxA = 10; maxSum = 20;
        }
        const a = minA + Math.floor(
            Math.random() * (maxA - minA + 1));
        const bMax = Math.min(maxA, maxSum - a);
        const b = minA + Math.floor(
            Math.random()
            * Math.max(bMax - minA + 1, 1));
        return { a, b, sum: a + b };
    }

    function renderButtons(correct) {
        numGrid.innerHTML = '';
        const lo = Math.max(0, correct - 5);
        const hi = Math.min(20,
            Math.max(correct + 5, lo + 9));
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
        if (!answering || turn !== 'player') return;
        answering = false;
        initAudio();
        if (num === currentProblem.sum) {
            onCorrect(btn);
        } else {
            onWrong(btn);
        }
    }

    function onCorrect(btn) {
        streak++;
        renderStreak();
        sfxCorrect();
        btn.classList.add('correct-flash');

        if (streak < STREAK_NEEDED) {
            showFeedback(
                `${streak} / ${STREAK_NEEDED} ⭐`,
                'correct', 1000);
            setTimeout(() => newRound(), 1200);
        } else {
            // 3 in a row — roll!
            streak = 0;
            renderStreak();
            showFeedback('Move!', 'levelup', 1400);
            sfxLevelUp();
            setTimeout(() => {
                const roll = 1 + Math.floor(
                    Math.random() * 3);
                showDice(roll, () => {
                    moveToken('player', roll, () => {
                        if (playerPos >= TOTAL) {
                            playerWins();
                        } else {
                            setTimeout(() =>
                                startComputerTurn(), 800);
                        }
                    });
                });
            }, 1000);
        }
    }

    function onWrong(btn) {
        sfxWrong();
        btn.classList.add('shake');
        const hadStreak = streak > 0;
        streak = 0;
        renderStreak();
        showFeedback(
            hadStreak ? 'Oops! Start over!'
                      : 'Try again!',
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
        void diceEl.offsetWidth;
        diceEl.classList.add('sl-roll');
        sfxPop();
        requestAnimationFrame(() => positionTokens());
        setTimeout(cb, 900);
    }

    // =================================================================
    //  Move token step by step
    // =================================================================
    function moveToken(who, steps, cb) {
        diceEl.textContent = '';
        const tokenEl = who === 'player'
            ? pTokenEl : cTokenEl;
        const curPos = who === 'player'
            ? playerPos : computerPos;

        if (curPos === 0) {
            // First appearance
            tokenEl.style.transition = 'none';
            setPos(who, 1);
            positionTokens();
            tokenEl.style.display = 'flex';
            updateScoreboard();
            sfxPop();
            requestAnimationFrame(() => {
                requestAnimationFrame(() => {
                    tokenEl.style.transition = '';
                    if (steps > 1) {
                        moveStep(who, steps - 1, cb);
                    } else {
                        checkSquare(who, cb);
                    }
                });
            });
            return;
        }
        moveStep(who, steps, cb);
    }

    function moveStep(who, remaining, cb) {
        if (remaining <= 0) {
            checkSquare(who, cb);
            return;
        }
        const cur = who === 'player'
            ? playerPos : computerPos;
        setPos(who, Math.min(cur + 1, TOTAL));
        updateScoreboard();
        positionTokens();
        sfxPop();

        const pos = who === 'player'
            ? playerPos : computerPos;
        if (pos >= TOTAL) {
            setTimeout(() => cb(), 400);
            return;
        }
        setTimeout(() =>
            moveStep(who, remaining - 1, cb), 350);
    }

    function setPos(who, val) {
        if (who === 'player') playerPos = val;
        else computerPos = val;
    }

    function getPos(who) {
        return who === 'player'
            ? playerPos : computerPos;
    }

    // =================================================================
    //  Check for snake / ladder
    // =================================================================
    function checkSquare(who, cb) {
        const pos = getPos(who);
        const tokenEl = who === 'player'
            ? pTokenEl : cTokenEl;
        const emoji = who === 'player'
            ? playerAnimal : computerAnimal;

        if (LADDERS[pos]) {
            const dest = LADDERS[pos];
            showEvent(
                `${emoji} 🪜 → ${dest}`,
                'sl-ladder-event');
            if (who === 'player') sfxLevelUp();
            else sfxPop();
            spawnConfetti(15);
            tokenEl.classList.add('sl-slide');
            setTimeout(() => {
                setPos(who, dest);
                updateScoreboard();
                positionTokens();
                setTimeout(() => {
                    tokenEl.classList.remove('sl-slide');
                    cb();
                }, 900);
            }, 600);
        } else if (SNAKES[pos]) {
            const dest = SNAKES[pos];
            showEvent(
                `${emoji} 🐍 → ${dest}`,
                'sl-snake-event');
            sfxWrong();
            tokenEl.classList.add('sl-slide');
            setTimeout(() => {
                setPos(who, dest);
                updateScoreboard();
                positionTokens();
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
    //  Win / Lose
    // =================================================================
    function playerWins() {
        sfxChampion();
        spawnConfetti(80);
        showScreen('champion-screen');
    }

    function computerWins() {
        document.getElementById('lose-emoji')
            .textContent = computerAnimal;
        sfxWrong();
        showScreen('lose-screen');
    }

    // =================================================================
    //  Position BOTH tokens (offset when same square)
    // =================================================================
    function positionTokens() {
        const same = playerPos === computerPos
            && playerPos > 0;
        if (playerPos > 0) {
            positionSingle(pTokenEl, playerPos,
                same ? -0.22 : 0);
        }
        if (computerPos > 0) {
            positionSingle(cTokenEl, computerPos,
                same ? 0.22 : 0);
        }
    }

    function positionSingle(el, sq, offsetFrac) {
        const cell = document.getElementById(
            'sl-cell-' + sq);
        if (!cell || !boardWrap) return;
        const bR = boardWrap.getBoundingClientRect();
        const cR = cell.getBoundingClientRect();
        const tW = el.offsetWidth, tH = el.offsetHeight;
        const ox = cR.width * offsetFrac;
        el.style.left = (cR.left - bR.left
            + cR.width / 2 - tW / 2 + ox) + 'px';
        el.style.top = (cR.top - bR.top
            + cR.height / 2 - tH / 2) + 'px';
    }

    // =================================================================
    //  Board rendering
    // =================================================================
    function buildBoard() {
        boardEl.innerHTML = '';
        for (let vr = 0; vr < ROWS; vr++) {
            for (let vc = 0; vc < COLS; vc++) {
                const sq = gridToSquare(vr, vc);
                const cell = document.createElement('div');
                cell.className = 'sl-cell sl-row-' + vr;
                cell.id = 'sl-cell-' + sq;
                let icon = '', cls = '';
                if (LADDERS[sq]) {
                    icon = '🪜'; cls = ' sl-ladder';
                } else if (SNAKES[sq]) {
                    icon = '🐍'; cls = ' sl-snake';
                }
                if (sq === TOTAL) cls += ' sl-finish';
                cell.className += cls;
                cell.innerHTML =
                    `<span class="sl-cell-num">${sq}</span>`
                    + (icon ? `<span class="sl-cell-icon">`
                        + `${icon}</span>` : '');
                boardEl.appendChild(cell);
            }
        }
        drawLines();
    }

    function drawLines() {
        let svg = '';
        for (const [from, to] of
            Object.entries(LADDERS)) {
            const p1 = sqToCenter(+from);
            const p2 = sqToCenter(+to);
            svg += `<line x1="${p1.x}" y1="${p1.y}"
                x2="${p2.x}" y2="${p2.y}"
                stroke="#FFD700" stroke-width="6"
                stroke-dasharray="12,6"
                stroke-linecap="round" opacity="0.7"/>`;
            const dx = p2.x-p1.x, dy = p2.y-p1.y;
            const len = Math.sqrt(dx*dx + dy*dy);
            const nx = -dy/len*12, ny = dx/len*12;
            const n = Math.max(2,
                Math.round(len / 40));
            for (let i = 1; i < n; i++) {
                const t = i / n;
                const mx = p1.x+dx*t, my = p1.y+dy*t;
                svg += `<line x1="${mx-nx}" y1="${my-ny}"
                    x2="${mx+nx}" y2="${my+ny}"
                    stroke="#FFC107" stroke-width="3"
                    stroke-linecap="round"
                    opacity="0.5"/>`;
            }
        }
        for (const [from, to] of
            Object.entries(SNAKES)) {
            const p1 = sqToCenter(+from);
            const p2 = sqToCenter(+to);
            const mx = (p1.x+p2.x)/2
                + (Math.random()-0.5)*60;
            const my = (p1.y+p2.y)/2;
            svg += `<path d="M${p1.x},${p1.y}
                Q${mx},${my} ${p2.x},${p2.y}"
                stroke="#EF5350" stroke-width="6"
                fill="none" stroke-linecap="round"
                opacity="0.65"/>`;
            svg += `<circle cx="${p1.x}" cy="${p1.y}"
                r="6" fill="#D32F2F" opacity="0.7"/>`;
        }
        linesEl.innerHTML = svg;
    }

    function gridToSquare(vr, vc) {
        const row = ROWS - 1 - vr;
        const ltr = row % 2 === 0;
        const col = ltr ? vc : COLS - 1 - vc;
        return row * COLS + col + 1;
    }

    function sqToCenter(sq) {
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

    function showEvent(text, cls) {
        const el = document.createElement('div');
        el.className = 'sl-event ' + cls;
        el.textContent = text;
        document.body.appendChild(el);
        setTimeout(() => el.remove(), 2000);
    }

    // =================================================================
    //  Resize handler
    // =================================================================
    window.addEventListener('resize', () => {
        if (playerPos > 0 || computerPos > 0) {
            pTokenEl.style.transition = 'none';
            cTokenEl.style.transition = 'none';
            positionTokens();
            requestAnimationFrame(() => {
                pTokenEl.style.transition = '';
                cTokenEl.style.transition = '';
            });
        }
    });
});
