// =========================================================================
//  Memory Game — Hebrew Letters
//  Start with 4 cards, expand +2 each level
// =========================================================================
document.addEventListener('DOMContentLoaded', () => {

    // --- Hebrew alphabet ---
    const LETTERS = [
        { char: 'א', name: 'אָלֶף' },
        { char: 'ב', name: 'בֵּית' },
        { char: 'ג', name: 'גִּימֶל' },
        { char: 'ד', name: 'דָּלֶת' },
        { char: 'ה', name: 'הֵא' },
        { char: 'ו', name: 'וָו' },
        { char: 'ז', name: 'זַיִן' },
        { char: 'ח', name: 'חֵית' },
        { char: 'ט', name: 'טֵית' },
        { char: 'י', name: 'יוֹד' },
        { char: 'כ', name: 'כָּף' },
        { char: 'ל', name: 'לָמֶד' },
        { char: 'מ', name: 'מֵם' },
        { char: 'נ', name: 'נוּן' },
        { char: 'ס', name: 'סָמֶך' },
        { char: 'ע', name: 'עַיִן' },
        { char: 'פ', name: 'פֵּא' },
        { char: 'צ', name: 'צָדִי' },
        { char: 'ק', name: 'קוֹף' },
        { char: 'ר', name: 'רֵישׁ' },
        { char: 'ש', name: 'שִׁין' },
        { char: 'ת', name: 'תָּו' },
    ];

    const PAIR_COLORS = [
        '#FF6B9D', '#7B68EE', '#FFB347', '#7DCEA0',
        '#FF6F00', '#5DADE2', '#F06292', '#AED581',
        '#FFD54F', '#CE93D8', '#4DB6AC',
    ];

    const START_CARDS = 4;
    const MAX_CARDS = 16;
    const CARDS_INC = 2;

    // --- State ---
    let level = 1;
    let numCards = START_CARDS;
    let cards = [];       // { char, name, color, pairId }
    let flipped = [];     // indices of currently flipped
    let matched = new Set(); // matched pairIds
    let locked = false;
    let moves = 0;

    // --- DOM refs ---
    const gridEl    = document.getElementById('mem-grid');
    const levelEl   = document.getElementById('mem-level');
    const movesEl   = document.getElementById('mem-moves');
    const peekEl    = document.getElementById('mem-peek');
    const pairsEl   = document.getElementById('mem-pairs-left');

    // =================================================================
    //  Screens
    // =================================================================
    populateAnimals('welcome-animals');
    populateAnimals('champion-animals');
    document.getElementById('play-btn')
        .addEventListener('click', startGame);
    document.getElementById('play-again-btn')
        .addEventListener('click', startGame);
    document.getElementById('mem-mute')
        .addEventListener('click', () => {
            muted = !muted;
            document.getElementById('mem-mute')
                .innerHTML =
                muted ? '&#128263;' : '&#128264;';
        });

    function showScreen(id) {
        document.querySelectorAll('.screen')
            .forEach(s => s.classList.add('hidden'));
        document.getElementById(id)
            .classList.remove('hidden');
    }

    // =================================================================
    //  Start game
    // =================================================================
    function startGame() {
        initAudio();
        level = 1;
        numCards = START_CARDS;
        showScreen('game-screen');
        document.body.className = 'level-1';
        spawnClouds();
        startLevel();
    }

    // =================================================================
    //  Start a level
    // =================================================================
    function startLevel() {
        const numPairs = numCards / 2;

        // Pick random letters for this level
        const picked = shuffle([...LETTERS])
            .slice(0, numPairs);

        // Create card pairs
        cards = [];
        picked.forEach((letter, i) => {
            const color =
                PAIR_COLORS[i % PAIR_COLORS.length];
            cards.push({
                char: letter.char, name: letter.name,
                color, pairId: i,
            });
            cards.push({
                char: letter.char, name: letter.name,
                color, pairId: i,
            });
        });
        shuffle(cards);

        flipped = [];
        matched = new Set();
        locked = true;
        moves = 0;

        updateDisplay();
        renderBoard();

        // --- Peek phase: show all, then hide ---
        const peekMs = 1500 + (numCards - 4) * 150;
        peekEl.textContent = '!זִכְרוּ';

        setTimeout(() => flipAll(true), 400);
        setTimeout(() => {
            flipAll(false);
            peekEl.textContent = '';
            locked = false;
        }, 400 + peekMs);
    }

    // =================================================================
    //  Render the card grid
    // =================================================================
    function renderBoard() {
        const cols = getCols(numCards);
        gridEl.style.setProperty('--mem-cols', cols);
        gridEl.innerHTML = '';

        cards.forEach((card, idx) => {
            const el = document.createElement('div');
            el.className = 'mem-card';
            el.dataset.idx = idx;
            el.innerHTML = `
                <div class="mem-card-inner">
                    <div class="mem-card-back"></div>
                    <div class="mem-card-front"
                         style="background:
                            linear-gradient(135deg,
                                ${lighten(card.color)},
                                ${card.color})">
                        <span class="mem-char">
                            ${card.char}</span>
                        <span class="mem-name">
                            ${card.name}</span>
                    </div>
                </div>`;
            el.addEventListener('click',
                () => onCardClick(idx, el));
            gridEl.appendChild(el);
        });
    }

    // =================================================================
    //  Card click handler
    // =================================================================
    function onCardClick(idx, el) {
        if (locked) return;
        if (flipped.includes(idx)) return;
        if (matched.has(cards[idx].pairId)) return;

        // Flip this card
        el.classList.add('flipped');
        flipped.push(idx);
        sfxPop();

        if (flipped.length === 2) {
            moves++;
            updateDisplay();
            locked = true;

            const [a, b] = flipped;
            const cardA = cards[a], cardB = cards[b];

            if (cardA.pairId === cardB.pairId) {
                // --- Match! ---
                matched.add(cardA.pairId);
                sfxCorrect();
                flyingStar();
                setTimeout(() => {
                    getCardEl(a).classList.add('matched');
                    getCardEl(b).classList.add('matched');
                    flipped = [];
                    locked = false;
                    updatePairsLeft();

                    if (matched.size === numCards / 2) {
                        onLevelComplete();
                    }
                }, 500);

            } else {
                // --- No match ---
                sfxWrong();
                setTimeout(() => {
                    getCardEl(a).classList.add('no-match');
                    getCardEl(b).classList.add('no-match');
                }, 400);
                setTimeout(() => {
                    getCardEl(a).classList.remove(
                        'flipped', 'no-match');
                    getCardEl(b).classList.remove(
                        'flipped', 'no-match');
                    flipped = [];
                    locked = false;
                }, 1100);
            }
        }
    }

    // =================================================================
    //  Level complete
    // =================================================================
    function onLevelComplete() {
        locked = true;
        spawnConfetti(40);
        sfxLevelUp();

        // Bounce all matched cards
        document.querySelectorAll('.mem-card.matched')
            .forEach((c, i) => {
                setTimeout(() =>
                    c.classList.add('bounce'), i * 80);
            });

        showFeedback('!כָּל הַכָּבוֹד', 'levelup', 2200);

        numCards += CARDS_INC;
        level++;

        // Update background with progress
        const pct = level / 7;
        if (pct > 0.75) {
            document.body.className = 'level-4';
        } else if (pct > 0.5) {
            document.body.className = 'level-3';
        } else if (pct > 0.25) {
            document.body.className = 'level-2';
        }

        if (numCards > MAX_CARDS) {
            // Champion!
            setTimeout(() => {
                sfxChampion();
                spawnConfetti(80);
                showScreen('champion-screen');
            }, 2800);
        } else {
            setTimeout(() => startLevel(), 3000);
        }
    }

    // =================================================================
    //  Helpers
    // =================================================================
    function getCardEl(idx) {
        return gridEl.children[idx];
    }

    function flipAll(show) {
        gridEl.querySelectorAll('.mem-card')
            .forEach(c => {
                if (show) c.classList.add('flipped');
                else c.classList.remove('flipped');
            });
    }

    function updateDisplay() {
        levelEl.textContent = `שלב ${level}`;
        movesEl.textContent = `${moves} מהלכים`;
        updatePairsLeft();
    }

    function updatePairsLeft() {
        const left = numCards / 2 - matched.size;
        if (left > 0) {
            pairsEl.textContent =
                `${left} זוגות נותרו`;
        } else {
            pairsEl.textContent = '';
        }
    }

    function getCols(n) {
        if (n <= 4) return 2;
        if (n <= 6) return 3;
        return 4;
    }

    function shuffle(arr) {
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(
                Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    }

    function lighten(hex) {
        const r = parseInt(hex.slice(1, 3), 16);
        const g = parseInt(hex.slice(3, 5), 16);
        const b = parseInt(hex.slice(5, 7), 16);
        const lr = Math.min(255,
            r + Math.round((255 - r) * 0.4));
        const lg = Math.min(255,
            g + Math.round((255 - g) * 0.4));
        const lb = Math.min(255,
            b + Math.round((255 - b) * 0.4));
        return `#${lr.toString(16).padStart(2, '0')}`
             + `${lg.toString(16).padStart(2, '0')}`
             + `${lb.toString(16).padStart(2, '0')}`;
    }
});
