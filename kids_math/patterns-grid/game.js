// =========================================================================
//  Magic Grid — 2D Pattern Recognition (Raven's-style)
// =========================================================================

const GridGame = {

    // --- Constants ---
    CANDIES_TO_WIN: 10,
    STARS_PER_CANDY: 3,
    STREAK_TO_LEVEL_UP: 3,

    // --- Colors ---
    COLORS: [
        { name: 'red',    fill: '#EF5350', stroke: '#C62828' },
        { name: 'blue',   fill: '#42A5F5', stroke: '#1565C0' },
        { name: 'green',  fill: '#66BB6A', stroke: '#2E7D32' },
        { name: 'yellow', fill: '#FFEE58', stroke: '#F9A825' },
        { name: 'purple', fill: '#AB47BC', stroke: '#6A1B9A' },
        { name: 'orange', fill: '#FF7043', stroke: '#D84315' },
        { name: 'pink',   fill: '#EC407A', stroke: '#AD1457' },
    ],

    // --- Shapes ---
    SHAPES: [
        'circle', 'triangle', 'square',
        'star', 'heart', 'diamond',
    ],

    // --- Levels ---
    LEVELS: [
        // L1: 2x2, same color per row
        { size: 2, vary: 'color', fixShape: 'circle',
          rule: 'row-match', choices: 2 },
        // L2: 2x2, same color per column
        { size: 2, vary: 'color', fixShape: 'circle',
          rule: 'col-match', choices: 2 },
        // L3: 2x2 Latin square colors
        { size: 2, vary: 'color', fixShape: 'heart',
          rule: 'latin', choices: 2 },
        // L4: 2x2 Latin square shapes
        { size: 2, vary: 'shape',
          rule: 'latin', choices: 3 },
        // L5: 3x3 Latin square colors
        { size: 3, vary: 'color', fixShape: 'circle',
          rule: 'latin', choices: 3 },
        // L6: 3x3 Latin square shapes
        { size: 3, vary: 'shape',
          rule: 'latin', choices: 4 },
        // L7: 3x3 Latin square colors (stars)
        { size: 3, vary: 'color', fixShape: 'star',
          rule: 'latin', choices: 4 },
        // L8: 3x3 Latin square color+shape
        { size: 3, vary: 'both',
          rule: 'latin', choices: 5 },
    ],

    // --- State ---
    state: {},
    currentRound: null,
    prevAnswerKey: null,

    praises: [
        'Great!', 'Awesome!', 'Super!',
        'Yay!', 'Wow!', 'Cool!', 'Nice!',
    ],
    encouragements: [
        'Try again!', 'Almost!',
        'One more try!', 'You can do it!',
    ],

    // =================================================================
    //  SVG shape generators
    // =================================================================
    shapeSVG(shape, color, size) {
        const s = size || 60;
        const h = s / 2;
        let inner;
        switch (shape) {
            case 'circle':
                inner = '<circle cx="' + h + '" cy="' +
                    h + '" r="' + (h * 0.75) +
                    '" fill="' + color.fill +
                    '" stroke="' + color.stroke +
                    '" stroke-width="3"/>';
                break;
            case 'triangle':
                inner = '<polygon points="' +
                    h + ',' + (s * 0.1) + ' ' +
                    (s * 0.9) + ',' + (s * 0.85) + ' ' +
                    (s * 0.1) + ',' + (s * 0.85) +
                    '" fill="' + color.fill +
                    '" stroke="' + color.stroke +
                    '" stroke-width="3"' +
                    ' stroke-linejoin="round"/>';
                break;
            case 'square':
                inner = '<rect x="' + (s * 0.12) +
                    '" y="' + (s * 0.12) +
                    '" width="' + (s * 0.76) +
                    '" height="' + (s * 0.76) +
                    '" rx="5"' +
                    ' fill="' + color.fill +
                    '" stroke="' + color.stroke +
                    '" stroke-width="3"/>';
                break;
            case 'star': {
                const pts = [];
                for (let i = 0; i < 10; i++) {
                    const r = i % 2 === 0
                        ? h * 0.78 : h * 0.35;
                    const a = (Math.PI * i) / 5 -
                              Math.PI / 2;
                    pts.push(
                        (h + r * Math.cos(a)).toFixed(1) +
                        ',' +
                        (h + r * Math.sin(a)).toFixed(1)
                    );
                }
                inner = '<polygon points="' +
                    pts.join(' ') +
                    '" fill="' + color.fill +
                    '" stroke="' + color.stroke +
                    '" stroke-width="2.5"' +
                    ' stroke-linejoin="round"/>';
                break;
            }
            case 'heart':
                inner = '<path d="M ' + h + ' ' +
                    (s * 0.82) +
                    ' C ' + (s * 0.08) + ' ' +
                    (s * 0.55) + ', ' +
                    (s * 0.08) + ' ' + (s * 0.18) +
                    ', ' + h + ' ' + (s * 0.35) +
                    ' C ' + (s * 0.92) + ' ' +
                    (s * 0.18) + ', ' +
                    (s * 0.92) + ' ' + (s * 0.55) +
                    ', ' + h + ' ' + (s * 0.82) +
                    ' Z" fill="' + color.fill +
                    '" stroke="' + color.stroke +
                    '" stroke-width="2.5"/>';
                break;
            case 'diamond':
                inner = '<polygon points="' +
                    h + ',' + (s * 0.08) + ' ' +
                    (s * 0.88) + ',' + h + ' ' +
                    h + ',' + (s * 0.92) + ' ' +
                    (s * 0.12) + ',' + h +
                    '" fill="' + color.fill +
                    '" stroke="' + color.stroke +
                    '" stroke-width="3"' +
                    ' stroke-linejoin="round"/>';
                break;
        }
        return '<svg width="' + s + '" height="' + s +
               '" viewBox="0 0 ' + s + ' ' + s + '">' +
               inner + '</svg>';
    },

    // =================================================================
    //  Helpers
    // =================================================================
    itemKey(item) {
        return item.shape + '_' + item.color.name;
    },

    sameItem(a, b) {
        return a.shape === b.shape &&
               a.color.name === b.color.name;
    },

    shuffle(arr) {
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    },

    pickN(arr, n) {
        const copy = [...arr];
        this.shuffle(copy);
        return copy.slice(0, n);
    },

    // =================================================================
    //  Generate items for a level
    // =================================================================
    generateItems(lvl) {
        const n = lvl.size;
        const items = [];

        if (lvl.vary === 'color') {
            const colors = this.pickN(this.COLORS, n);
            const shape = lvl.fixShape || 'circle';
            for (let i = 0; i < n; i++) {
                items.push({ shape, color: colors[i] });
            }
        } else if (lvl.vary === 'shape') {
            const shapes = this.pickN(this.SHAPES, n);
            const color = this.COLORS[
                Math.floor(
                    Math.random() * this.COLORS.length
                )
            ];
            for (let i = 0; i < n; i++) {
                items.push({ shape: shapes[i], color });
            }
        } else {
            // 'both' — unique shape+color pairs
            const colors = this.pickN(this.COLORS, n);
            const shapes = this.pickN(this.SHAPES, n);
            for (let i = 0; i < n; i++) {
                items.push({
                    shape: shapes[i], color: colors[i],
                });
            }
        }
        return items;
    },

    // =================================================================
    //  Grid generators
    // =================================================================
    genRowMatch(items) {
        // 2x2: each row has the same item
        return [
            [items[0], items[0]],
            [items[1], items[1]],
        ];
    },

    genColMatch(items) {
        // 2x2: each column has the same item
        return [
            [items[0], items[1]],
            [items[0], items[1]],
        ];
    },

    genLatinSquare(size, items) {
        if (size === 2) {
            // Two arrangements — pick one
            const flip = Math.random() < 0.5;
            return flip
                ? [[items[0], items[1]],
                   [items[1], items[0]]]
                : [[items[1], items[0]],
                   [items[0], items[1]]];
        }
        // 3x3: cyclic construction
        const grid = [];
        for (let r = 0; r < 3; r++) {
            const row = [];
            for (let c = 0; c < 3; c++) {
                row.push(items[(r + c) % 3]);
            }
            grid.push(row);
        }
        // Shuffle rows
        this.shuffle(grid);
        // Shuffle columns
        const colOrder = [0, 1, 2];
        this.shuffle(colOrder);
        return grid.map(
            row => colOrder.map(c => row[c])
        );
    },

    // =================================================================
    //  Generate a full round
    // =================================================================
    generateRound(lvl) {
        const items = this.generateItems(lvl);
        let grid;

        switch (lvl.rule) {
            case 'row-match':
                grid = this.genRowMatch(items);
                break;
            case 'col-match':
                grid = this.genColMatch(items);
                break;
            case 'latin':
                grid = this.genLatinSquare(
                    lvl.size, items
                );
                break;
        }

        // Pick random cell to hide
        const mr = Math.floor(
            Math.random() * lvl.size
        );
        const mc = Math.floor(
            Math.random() * lvl.size
        );
        const answer = grid[mr][mc];
        grid[mr][mc] = null;

        // Generate choices
        const choices = [answer];
        for (const it of items) {
            if (choices.length >= lvl.choices) break;
            if (!this.sameItem(it, answer)) {
                choices.push(it);
            }
        }
        // Extra distractors if needed
        if (choices.length < lvl.choices) {
            const used = new Set(
                items.map(it => this.itemKey(it))
            );
            const pool = [];
            if (lvl.vary === 'color' ||
                lvl.vary === 'both') {
                const sh = lvl.fixShape || items[0].shape;
                for (const c of this.COLORS) {
                    if (!used.has(sh + '_' + c.name)) {
                        pool.push({ shape: sh, color: c });
                    }
                }
            }
            if (lvl.vary === 'shape' ||
                lvl.vary === 'both') {
                const cl = items[0].color;
                for (const sh of this.SHAPES) {
                    if (!used.has(sh + '_' + cl.name)) {
                        pool.push({ shape: sh, color: cl });
                    }
                }
            }
            this.shuffle(pool);
            for (const it of pool) {
                if (choices.length >= lvl.choices) break;
                choices.push(it);
            }
        }
        this.shuffle(choices);

        return { grid, answer, choices, mr, mc };
    },

    // =================================================================
    //  Init
    // =================================================================
    init() {
        populateAnimals('welcome-animals');
        populateAnimals('champion-animals');

        document.getElementById('play-btn')
            .addEventListener('click',
                () => this.start());
        document.getElementById('play-again-btn')
            .addEventListener('click',
                () => this.start());
        document.getElementById('mute-btn')
            .addEventListener('click', () => {
                muted = !muted;
                document.getElementById('mute-btn')
                    .innerHTML = muted
                        ? '&#128263;' : '&#128264;';
            });

        spawnClouds();
    },

    // =================================================================
    //  Start / restart
    // =================================================================
    start() {
        initAudio();
        this.state = {
            level: 0,
            stars: 0,
            candies: 0,
            streak: 0,
            answering: true,
        };
        this.prevAnswerKey = null;
        if (typeof PrizeManager !== 'undefined') {
            PrizeManager.init();
        }
        this._updateBodyLevel();
        this._renderStars();
        this._renderLevel();
        this._renderCandyBar();
        this._showScreen('game-screen');
        spawnClouds();
        setTimeout(() => this.newRound(), 400);
    },

    // =================================================================
    //  New round
    // =================================================================
    newRound() {
        this.state.answering = true;
        const lvl = this.LEVELS[this.state.level];

        // No-repeat check
        let round;
        let tries = 0;
        do {
            round = this.generateRound(lvl);
            tries++;
        } while (
            this.prevAnswerKey &&
            this.itemKey(round.answer) ===
                this.prevAnswerKey &&
            tries < 5
        );

        this.currentRound = round;
        this.prevAnswerKey = this.itemKey(round.answer);

        this._renderGrid(round, lvl);
        this._renderChoices(round);
    },

    // =================================================================
    //  Render grid
    // =================================================================
    _renderGrid(round, lvl) {
        const el = document.getElementById('grid-container');
        el.innerHTML = '';
        el.className = 'grid-container grid-' +
            lvl.size + 'x' + lvl.size;

        const sz = lvl.size === 2
            ? (window.innerWidth < 400 ? 60 : 80)
            : (window.innerWidth < 400 ? 50 : 68);

        let idx = 0;
        for (let r = 0; r < lvl.size; r++) {
            for (let c = 0; c < lvl.size; c++) {
                const cell = document.createElement('div');
                const item = round.grid[r][c];

                if (item === null) {
                    // Mystery cell
                    cell.className =
                        'grid-cell grid-mystery';
                    cell.textContent = '?';
                } else {
                    cell.className = 'grid-cell';
                    cell.innerHTML = this.shapeSVG(
                        item.shape, item.color, sz
                    );
                }
                cell.style.animationDelay =
                    (idx * 0.08) + 's';
                el.appendChild(cell);
                idx++;
            }
        }
    },

    // =================================================================
    //  Render choices
    // =================================================================
    _renderChoices(round) {
        const el = document.getElementById(
            'grid-choices'
        );
        el.innerHTML = '';

        const sz = window.innerWidth < 400 ? 56 : 68;

        for (const item of round.choices) {
            const btn = document.createElement('button');
            btn.className = 'grid-choice-btn';
            btn.innerHTML = this.shapeSVG(
                item.shape, item.color, sz
            );
            btn.addEventListener('click', () =>
                this.handleAnswer(item, btn)
            );
            el.appendChild(btn);
        }
    },

    // =================================================================
    //  Handle answer
    // =================================================================
    handleAnswer(item, btn) {
        if (!this.state.answering) return;
        this.state.answering = false;
        initAudio();

        if (this.sameItem(
                item, this.currentRound.answer)) {
            this._onCorrect(btn);
        } else {
            this._onWrong(btn);
        }
    },

    // =================================================================
    //  Correct
    // =================================================================
    _onCorrect(btn) {
        const s = this.state;
        s.streak++;
        s.stars++;
        this._renderStars();
        sfxCorrect();
        btn.classList.add('correct-flash');

        // Reveal answer in grid
        const mystery =
            document.querySelector('.grid-mystery');
        if (mystery) {
            const lvl = this.LEVELS[s.level];
            const sz = lvl.size === 2
                ? (window.innerWidth < 400 ? 60 : 80)
                : (window.innerWidth < 400 ? 50 : 68);
            mystery.textContent = '';
            mystery.classList.remove('grid-mystery');
            mystery.classList.add('grid-reveal');
            mystery.innerHTML = this.shapeSVG(
                this.currentRound.answer.shape,
                this.currentRound.answer.color, sz
            );
        }

        showFeedback(
            this.praises[
                Math.floor(
                    Math.random() * this.praises.length
                )
            ],
            'correct', 1200
        );
        flyingStar();

        // Candy check
        const prev = s.candies;
        s.candies = Math.floor(
            s.stars / this.STARS_PER_CANDY
        );
        if (s.candies > prev &&
            s.candies <= this.CANDIES_TO_WIN) {
            setTimeout(() => {
                this._renderCandyBar();
                sfxCandy();
            }, 600);
        }

        // Champion
        if (s.candies >= this.CANDIES_TO_WIN) {
            setTimeout(
                () => this._showChampion(), 1500
            );
            return;
        }

        // Level-up
        if (s.streak >= this.STREAK_TO_LEVEL_UP &&
            s.level < this.LEVELS.length - 1) {
            s.level++;
            s.streak = 0;
            this._updateBodyLevel();
            this._renderLevel();
            setTimeout(() => {
                sfxLevelUp();
                showFeedback(
                    'Level Up!', 'levelup', 2200
                );
                spawnConfetti(30);
            }, 800);
            setTimeout(
                () => this._maybeShowPrize(), 3200
            );
        } else {
            setTimeout(
                () => this._maybeShowPrize(), 1400
            );
        }
    },

    // =================================================================
    //  Wrong
    // =================================================================
    _onWrong(btn) {
        this.state.streak = 0;
        sfxWrong();
        btn.classList.add('shake');
        showFeedback(
            this.encouragements[
                Math.floor(
                    Math.random() *
                    this.encouragements.length
                )
            ],
            'wrong', 1000
        );
        setTimeout(() => {
            btn.classList.remove('shake');
            this.state.answering = true;
        }, 800);
    },

    // =================================================================
    //  Prize
    // =================================================================
    _maybeShowPrize() {
        if (typeof PrizeManager !== 'undefined' &&
            PrizeManager.check(
                () => this.newRound()
            )) {
            return;
        }
        this.newRound();
    },

    // =================================================================
    //  Champion
    // =================================================================
    _showChampion() {
        sfxChampion();
        spawnConfetti(80);
        this._showScreen('champion-screen');
    },

    // =================================================================
    //  UI helpers
    // =================================================================
    _showScreen(id) {
        document.querySelectorAll('.screen')
            .forEach(s => s.classList.add('hidden'));
        document.getElementById(id)
            .classList.remove('hidden');
    },

    _updateBodyLevel() {
        document.body.className =
            'level-' + (this.state.level + 1);
    },

    _renderStars() {
        document.getElementById('stars-display')
            .innerHTML = '&#11088; ' + this.state.stars;
    },

    _renderLevel() {
        document.getElementById('level-display')
            .textContent =
                'Level ' + (this.state.level + 1);
    },

    _renderCandyBar() {
        const bar = document.getElementById('candy-bar');
        bar.innerHTML = '';
        for (let i = 0; i < this.CANDIES_TO_WIN; i++) {
            const slot = document.createElement('div');
            slot.className = 'candy-slot' +
                (i < this.state.candies
                    ? ' earned' : '');
            slot.textContent =
                i < this.state.candies
                    ? '\u{1F36C}' : '';
            bar.appendChild(slot);
        }
    },
};

// === Bootstrap ===
document.addEventListener('DOMContentLoaded', () => {
    GridGame.init();
});
