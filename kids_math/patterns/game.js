// =========================================================================
//  Patterns Game — Color & Shape Pattern Recognition
// =========================================================================

const PatternsGame = {

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

    // --- Pattern templates ---
    TEMPLATES: {
        'AB':   [0, 1],
        'ABC':  [0, 1, 2],
        'AABB': [0, 0, 1, 1],
        'ABB':  [0, 1, 1],
    },

    // --- Levels ---
    LEVELS: [
        // L1: AB color, circles, short
        { pattern: 'AB', vary: 'color',
          fixShape: 'circle', seqLen: 4, choices: 2 },
        // L2: AB color, circles, longer
        { pattern: 'AB', vary: 'color',
          fixShape: 'circle', seqLen: 6, choices: 2 },
        // L3: ABC color, circles
        { pattern: 'ABC', vary: 'color',
          fixShape: 'circle', seqLen: 5, choices: 3 },
        // L4: AB shape, single color
        { pattern: 'AB', vary: 'shape',
          seqLen: 4, choices: 3 },
        // L5: ABC shape
        { pattern: 'ABC', vary: 'shape',
          seqLen: 5, choices: 4 },
        // L6: AB color + shape
        { pattern: 'AB', vary: 'both',
          seqLen: 4, choices: 3 },
        // L7: AABB color
        { pattern: 'AABB', vary: 'color',
          fixShape: 'heart', seqLen: 8, choices: 2 },
        // L8: ABC color + shape
        { pattern: 'ABC', vary: 'both',
          seqLen: 6, choices: 4 },
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
                inner = '<circle cx="' + h + '" cy="' + h +
                    '" r="' + (h * 0.75) +
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
        const tpl = this.TEMPLATES[lvl.pattern];
        const n = Math.max(...tpl) + 1;
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
                Math.floor(Math.random() * this.COLORS.length)
            ];
            for (let i = 0; i < n; i++) {
                items.push({ shape: shapes[i], color });
            }
        } else {
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
    //  Generate a full round (sequence + answer + choices)
    // =================================================================
    generateRound(lvl) {
        const tpl = this.TEMPLATES[lvl.pattern];
        const items = this.generateItems(lvl);

        // Build visible sequence
        const sequence = [];
        for (let i = 0; i < lvl.seqLen; i++) {
            sequence.push(items[tpl[i % tpl.length]]);
        }

        // Answer = next in pattern
        const answer = items[tpl[lvl.seqLen % tpl.length]];

        // Choices: answer + distractors
        const choices = [answer];

        // Other pattern items
        for (const it of items) {
            if (choices.length >= lvl.choices) break;
            if (!this.sameItem(it, answer)) {
                choices.push(it);
            }
        }

        // If still need more, pull from unused pool
        if (choices.length < lvl.choices) {
            const used = new Set(
                items.map(it => this.itemKey(it))
            );
            const pool = [];
            if (lvl.vary === 'color' || lvl.vary === 'both') {
                const shape = lvl.fixShape || items[0].shape;
                for (const c of this.COLORS) {
                    const k = shape + '_' + c.name;
                    if (!used.has(k)) {
                        pool.push({ shape, color: c });
                    }
                }
            }
            if (lvl.vary === 'shape' || lvl.vary === 'both') {
                const color = items[0].color;
                for (const sh of this.SHAPES) {
                    const k = sh + '_' + color.name;
                    if (!used.has(k)) {
                        pool.push({ shape: sh, color });
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
        return { sequence, answer, choices };
    },

    // =================================================================
    //  Init — called on DOMContentLoaded
    // =================================================================
    init() {
        populateAnimals('welcome-animals');
        populateAnimals('champion-animals');

        document.getElementById('play-btn')
            .addEventListener('click', () => this.start());
        document.getElementById('play-again-btn')
            .addEventListener('click', () => this.start());
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

        this._renderPattern(round);
        this._renderChoices(round);
    },

    // =================================================================
    //  Render pattern sequence
    // =================================================================
    _renderPattern(round) {
        const el = document.getElementById('pattern-sequence');
        el.innerHTML = '';

        const sz = window.innerWidth < 400 ? 48 : 60;

        for (let i = 0; i < round.sequence.length; i++) {
            const item = round.sequence[i];
            const div = document.createElement('div');
            div.className = 'pattern-item';
            div.innerHTML = this.shapeSVG(
                item.shape, item.color, sz
            );
            div.style.animationDelay = (i * 0.1) + 's';
            el.appendChild(div);
        }

        // Mystery placeholder
        const m = document.createElement('div');
        m.className = 'pattern-item pattern-mystery';
        m.textContent = '?';
        m.style.animationDelay =
            (round.sequence.length * 0.1) + 's';
        el.appendChild(m);
    },

    // =================================================================
    //  Render choice buttons
    // =================================================================
    _renderChoices(round) {
        const el = document.getElementById('pattern-choices');
        el.innerHTML = '';

        const sz = window.innerWidth < 400 ? 56 : 68;

        for (const item of round.choices) {
            const btn = document.createElement('button');
            btn.className = 'pattern-choice-btn';
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

        if (this.sameItem(item, this.currentRound.answer)) {
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

        // Reveal answer in sequence
        const mystery =
            document.querySelector('.pattern-mystery');
        if (mystery) {
            const sz = window.innerWidth < 400 ? 48 : 60;
            mystery.textContent = '';
            mystery.classList.remove('pattern-mystery');
            mystery.classList.add('pattern-reveal');
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

        // Champion check
        if (s.candies >= this.CANDIES_TO_WIN) {
            setTimeout(() => this._showChampion(), 1500);
            return;
        }

        // Level-up check
        if (s.streak >= this.STREAK_TO_LEVEL_UP &&
            s.level < this.LEVELS.length - 1) {
            s.level++;
            s.streak = 0;
            this._updateBodyLevel();
            this._renderLevel();
            setTimeout(() => {
                sfxLevelUp();
                showFeedback('Level Up!', 'levelup', 2200);
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
            PrizeManager.check(() => this.newRound())) {
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
                (i < this.state.candies ? ' earned' : '');
            slot.textContent =
                i < this.state.candies ? '\u{1F36C}' : '';
            bar.appendChild(slot);
        }
    },
};

// === Bootstrap ===
document.addEventListener('DOMContentLoaded', () => {
    PatternsGame.init();
});
