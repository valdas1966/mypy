// =========================================================================
//  Snakes & Ladders — Player vs Computer, configurable operations
// =========================================================================
document.addEventListener('DOMContentLoaded', () => {

    // --- Constants ---
    const COLS = 8, ROWS = 5, TOTAL = 40;
    const STREAK_NEEDED = 3;
    const LADDERS = { 4:14, 9:22, 20:29, 28:36 };
    const SNAKES  = { 17:7, 26:12, 31:19, 38:24 };
    const ANIMALS = ['🐱','🐰','🦊','🐻','🐸',
                     '🦄','🐶','🐼'];

    // =================================================================
    //  Operation definitions
    // =================================================================
    // ---------------------------------------------------------
    //  Generators use "pick answer first" for uniform
    //  distribution. Each gen(max) takes an effective max
    //  that scales with board position (easy → hard).
    // ---------------------------------------------------------
    const OPS = [
        { id: 'add2_10',  icon: '+', cls: 'op-add',
          label: 'a + b = ?',   range: 'result 0 – 10',
          maxAns: 10,
          gen(m) {
              const s = rand(0, m);
              const a = rand(0, s);
              return { display: `${a} + ${s - a}`,
                       answer: s };
          }},
        { id: 'add3_10',  icon: '+', cls: 'op-add',
          label: 'a + b + c = ?', range: 'result 0 – 10',
          maxAns: 10,
          gen(m) {
              const s = rand(0, m);
              const a = rand(0, s);
              const b = rand(0, s - a);
              return { display: `${a} + ${b} + ${s-a-b}`,
                       answer: s };
          }},
        { id: 'add2_20',  icon: '+', cls: 'op-add',
          label: 'a + b = ?',   range: 'result 0 – 20',
          maxAns: 20,
          gen(m) {
              const s = rand(0, m);
              const a = rand(0, s);
              return { display: `${a} + ${s - a}`,
                       answer: s };
          }},
        { id: 'add3_20',  icon: '+', cls: 'op-add',
          label: 'a + b + c = ?', range: 'result 0 – 20',
          maxAns: 20,
          gen(m) {
              const s = rand(0, m);
              const a = rand(0, s);
              const b = rand(0, s - a);
              return { display: `${a} + ${b} + ${s-a-b}`,
                       answer: s };
          }},
        { id: 'add2_30',  icon: '+', cls: 'op-add',
          label: 'a + b = ?',   range: 'result 0 – 30',
          maxAns: 30,
          gen(m) {
              const s = rand(0, m);
              const a = rand(0, s);
              return { display: `${a} + ${s - a}`,
                       answer: s };
          }},
        { id: 'mul2_10',  icon: '×', cls: 'op-mul',
          label: 'a × b = ?',  range: 'result 0 – 10',
          maxAns: 10,
          gen(m) { return genMul(m, 10); } },
        { id: 'mul2_20',  icon: '×', cls: 'op-mul',
          label: 'a × b = ?',  range: 'result 0 – 20',
          maxAns: 20,
          gen(m) { return genMul(m, 10); } },
        { id: 'mul2_30',  icon: '×', cls: 'op-mul',
          label: 'a × b = ?',  range: 'result 0 – 30',
          maxAns: 30,
          gen(m) { return genMul(m, 10); } },
        { id: 'sub_10',   icon: '−', cls: 'op-sub',
          label: 'a − b = ?',  range: 'numbers 0 – 10',
          maxAns: 10,
          gen(m) {
              const d = rand(0, m);
              const b = rand(0, m - d);
              return { display: `${d + b} − ${b}`,
                       answer: d };
          }},
        { id: 'sub_20',   icon: '−', cls: 'op-sub',
          label: 'a − b = ?',  range: 'numbers 0 – 20',
          maxAns: 20,
          gen(m) {
              const d = rand(0, m);
              const b = rand(0, m - d);
              return { display: `${d + b} − ${b}`,
                       answer: d };
          }},
        { id: 'div_10',   icon: '÷', cls: 'op-div',
          label: 'a ÷ b = ?',  range: 'numbers 0 – 10',
          maxAns: 10,
          gen(m) {
              const c = rand(0, m);
              if (c === 0) {
                  const b = rand(1, Math.max(1, m));
                  return { display: `0 ÷ ${b}`,
                           answer: 0 };
              }
              const bMax = Math.floor(m / c);
              if (bMax < 1)
                  return { display: '0 ÷ 1', answer: 0 };
              const b = rand(1, bMax);
              return { display: `${b * c} ÷ ${b}`,
                       answer: c };
          }},
    ];

    // Multiplication helper: pick product uniformly,
    // then find valid factor pair.
    function genMul(maxP, maxF) {
        for (let t = 0; t < 40; t++) {
            const p = rand(0, maxP);
            if (p === 0) {
                const a = rand(0, maxF);
                const b = a === 0 ? rand(1, maxF) : 0;
                return { display: `${a} × ${b}`,
                         answer: 0 };
            }
            const pairs = [];
            for (let a = 1; a <= maxF; a++) {
                if (p % a === 0) {
                    const b = p / a;
                    if (b >= 1 && b <= maxF)
                        pairs.push([a, b]);
                }
            }
            if (pairs.length > 0) {
                const [a, b] = pairs[
                    rand(0, pairs.length - 1)];
                return { display: `${a} × ${b}`,
                         answer: p };
            }
        }
        return { display: '1 × 1', answer: 1 };
    }

    // Compute effective max based on board position.
    // 4 tiers: ~30%, ~50%, ~80%, 100% of the op's max.
    function effectiveMax() {
        const zone = Math.min(3,
            Math.floor(playerPos / 10));
        const full = selectedOp.maxAns;
        const tiers = [
            Math.max(2, Math.round(full * 0.3)),
            Math.max(4, Math.round(full * 0.5)),
            Math.max(7, Math.round(full * 0.8)),
            full,
        ];
        return tiers[zone];
    }

    function rand(lo, hi) {
        return lo + Math.floor(
            Math.random() * (hi - lo + 1));
    }

    // --- State ---
    let playerAnimal = '', computerAnimal = '';
    let playerPos = 0, computerPos = 0;
    let turn = 'player';
    let streak = 0;
    let answering = false;
    let currentProblem = null;
    let lastDisplay = '';
    let selectedOp = null;

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
        const nextBtn = document.getElementById(
            'start-btn');

        grid.innerHTML = '';
        vsLabel.textContent = '';
        compPreview.textContent = '';
        nextBtn.classList.add('hidden');
        playerAnimal = '';

        ANIMALS.forEach(a => {
            const btn = document.createElement('button');
            btn.className = 'sl-animal-btn';
            btn.textContent = a;
            btn.addEventListener('click', () => {
                grid.querySelectorAll('.sl-animal-btn')
                    .forEach(b =>
                        b.classList.remove('selected'));
                btn.classList.add('selected');
                playerAnimal = a;
                sfxPop();
                const others = ANIMALS.filter(
                    x => x !== a);
                computerAnimal = others[
                    Math.floor(Math.random()
                        * others.length)];
                vsLabel.textContent = 'VS';
                compPreview.textContent = computerAnimal;
                nextBtn.classList.remove('hidden');
            });
            grid.appendChild(btn);
        });

        nextBtn.onclick = () => {
            if (playerAnimal) showOpsScreen();
        };
    }

    // =================================================================
    //  Operation selection screen
    // =================================================================
    function showOpsScreen() {
        showScreen('ops-screen');
        const grid = document.getElementById(
            'sl-ops-grid');
        const goBtn = document.getElementById(
            'ops-go-btn');
        grid.innerHTML = '';
        goBtn.classList.add('hidden');
        selectedOp = null;

        OPS.forEach(op => {
            const btn = document.createElement('button');
            btn.className = 'sl-op-btn';
            btn.innerHTML = `
                <div class="sl-op-icon ${op.cls}">
                    ${op.icon}</div>
                <div>
                    <div class="sl-op-label">
                        ${op.label}</div>
                    <div class="sl-op-range">
                        ${op.range}</div>
                </div>`;
            btn.addEventListener('click', () => {
                grid.querySelectorAll('.sl-op-btn')
                    .forEach(b =>
                        b.classList.remove('selected'));
                btn.classList.add('selected');
                selectedOp = op;
                sfxPop();
                goBtn.classList.remove('hidden');
            });
            grid.appendChild(btn);
        });

        goBtn.onclick = () => {
            if (selectedOp) startGame();
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
        lastDisplay = '';

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
        const best = Math.max(playerPos, computerPos);
        const pct = best / TOTAL;
        if (pct > 0.75)
            document.body.className = 'level-4';
        else if (pct > 0.5)
            document.body.className = 'level-3';
        else if (pct > 0.25)
            document.body.className = 'level-2';
        else
            document.body.className = 'level-1';
    }

    // =================================================================
    //  Streak display
    // =================================================================
    function renderStreak() {
        for (let i = 0; i < STREAK_NEEDED; i++) {
            streakDots[i].classList.toggle(
                'filled', i < streak);
        }
    }

    // =================================================================
    //  Problem generation — uses selected operation
    // =================================================================
    let curMax = 10; // current effective max for buttons

    function generateProblem() {
        curMax = effectiveMax();
        let prob;
        for (let t = 0; t < 30; t++) {
            prob = selectedOp.gen(curMax);
            if (prob.display !== lastDisplay) break;
        }
        lastDisplay = prob.display;
        return prob;
    }

    function newRound() {
        currentProblem = generateProblem();
        qText.innerHTML =
            `${currentProblem.display} = <b>?</b>`;
        renderButtons(currentProblem.answer);
        requestAnimationFrame(() => positionTokens());
        answering = true;
    }

    function renderButtons(correct) {
        numGrid.innerHTML = '';
        const max = curMax;
        const lo = Math.max(0, correct - 5);
        const hi = Math.min(max,
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
        if (num === currentProblem.answer) {
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

    // =================================================================
    //  Check for snake / ladder
    // =================================================================
    function checkSquare(who, cb) {
        const pos = who === 'player'
            ? playerPos : computerPos;
        const tokenEl = who === 'player'
            ? pTokenEl : cTokenEl;
        const emoji = who === 'player'
            ? playerAnimal : computerAnimal;

        if (LADDERS[pos]) {
            const dest = LADDERS[pos];
            showEvent(`${emoji} 🪜 → ${dest}`,
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
            showEvent(`${emoji} 🐍 → ${dest}`,
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
    //  Position BOTH tokens
    // =================================================================
    function positionTokens() {
        const same = playerPos === computerPos
            && playerPos > 0;
        if (playerPos > 0)
            positionSingle(pTokenEl, playerPos,
                same ? -0.22 : 0);
        if (computerPos > 0)
            positionSingle(cTokenEl, computerPos,
                same ? 0.22 : 0);
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
