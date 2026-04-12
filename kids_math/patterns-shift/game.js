// =========================================================================
//  Shape Shift — Transformation Pattern Recognition
// =========================================================================

const ShiftGame = {

    // --- Constants ---
    CANDIES_TO_WIN: 10,
    STARS_PER_CANDY: 3,
    STREAK_TO_LEVEL_UP: 3,

    COLORS: [
        { name: 'red',    fill: '#EF5350', stroke: '#C62828' },
        { name: 'blue',   fill: '#42A5F5', stroke: '#1565C0' },
        { name: 'green',  fill: '#66BB6A', stroke: '#2E7D32' },
        { name: 'yellow', fill: '#FFEE58', stroke: '#F9A825' },
        { name: 'purple', fill: '#AB47BC', stroke: '#6A1B9A' },
        { name: 'orange', fill: '#FF7043', stroke: '#D84315' },
        { name: 'pink',   fill: '#EC407A', stroke: '#AD1457' },
    ],

    SHAPES: [
        'circle', 'triangle', 'square',
        'star', 'heart', 'diamond',
    ],

    SIZES: ['small', 'medium', 'large'],
    ROTATIONS: [0, 90, 180, 270],
    SIZE_SCALE: { small: 0.6, medium: 0.85, large: 1.15 },

    // --- Levels ---
    // cycling: which properties transform each step
    LEVELS: [
        // L1: Color cycles (3 colors), circles
        { cycling: ['color'], nColors: 3,
          fixShape: 'circle', fixSize: 'medium',
          seqLen: 3, choices: 3 },
        // L2: Size cycles (S→M→L), circles
        { cycling: ['size'],
          fixShape: 'circle', fixSize: null,
          seqLen: 3, choices: 3 },
        // L3: Shape cycles (3 shapes)
        { cycling: ['shape'], nShapes: 3,
          fixShape: null, fixSize: 'medium',
          seqLen: 3, choices: 3 },
        // L4: Color cycles (4 colors), hearts
        { cycling: ['color'], nColors: 4,
          fixShape: 'heart', fixSize: 'medium',
          seqLen: 4, choices: 4 },
        // L5: Rotation (4 steps), arrows
        { cycling: ['rotation'],
          fixShape: 'arrow', fixSize: 'medium',
          seqLen: 4, choices: 4 },
        // L6: Color + size together
        { cycling: ['color', 'size'], nColors: 3,
          fixShape: 'star', fixSize: null,
          seqLen: 3, choices: 4 },
        // L7: Shape + color together
        { cycling: ['shape', 'color'],
          nShapes: 3, nColors: 3,
          fixShape: null, fixSize: 'medium',
          seqLen: 3, choices: 4 },
        // L8: Shape + color + size
        { cycling: ['shape', 'color', 'size'],
          nShapes: 3, nColors: 3,
          fixShape: null, fixSize: null,
          seqLen: 3, choices: 5 },
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
        const s = size || 56;
        const h = s / 2;
        let inner;
        switch (shape) {
            case 'circle':
                inner = '<circle cx="' + h +
                    '" cy="' + h +
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
                    '" rx="5" fill="' + color.fill +
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
            case 'arrow':
                inner = '<polygon points="' +
                    h + ',' + (s * 0.08) + ' ' +
                    (s * 0.87) + ',' + (s * 0.43) + ' ' +
                    (s * 0.63) + ',' + (s * 0.43) + ' ' +
                    (s * 0.63) + ',' + (s * 0.92) + ' ' +
                    (s * 0.37) + ',' + (s * 0.92) + ' ' +
                    (s * 0.37) + ',' + (s * 0.43) + ' ' +
                    (s * 0.13) + ',' + (s * 0.43) +
                    '" fill="' + color.fill +
                    '" stroke="' + color.stroke +
                    '" stroke-width="2.5"' +
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
    sameItem(a, b) {
        return a.color.name === b.color.name &&
               a.shape === b.shape &&
               a.size === b.size &&
               a.rotation === b.rotation;
    },

    itemKey(item) {
        return item.shape + '_' + item.color.name +
               '_' + item.size + '_' + item.rotation;
    },

    shuffle(arr) {
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(
                Math.random() * (i + 1)
            );
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    },

    pickN(arr, n) {
        const copy = [...arr];
        this.shuffle(copy);
        return copy.slice(0, n);
    },

    isCycling(lvl, prop) {
        return lvl.cycling.includes(prop);
    },

    // =================================================================
    //  Render a single item as HTML
    // =================================================================
    renderItemHTML(item, baseSz) {
        const svg = this.shapeSVG(
            item.shape, item.color, baseSz
        );
        const sc = this.SIZE_SCALE[item.size] || 0.85;
        const rot = item.rotation || 0;
        const style = 'transform:scale(' + sc +
            ')rotate(' + rot + 'deg)';
        return '<div class="shift-inner" style="' +
               style + '">' + svg + '</div>';
    },

    // =================================================================
    //  Generate a round
    // =================================================================
    generateRound(lvl) {
        // Pick pools for cycling properties
        const colorPool = this.isCycling(lvl, 'color')
            ? this.pickN(
                  this.COLORS, lvl.nColors || 3
              )
            : null;
        const shapePool = this.isCycling(lvl, 'shape')
            ? this.pickN(
                  this.SHAPES, lvl.nShapes || 3
              )
            : null;

        // Fixed values for non-cycling properties
        const fixColor = colorPool ? null
            : this.COLORS[
                  Math.floor(
                      Math.random() * this.COLORS.length
                  )
              ];
        const fixShape = lvl.fixShape
            || (shapePool ? null
                : this.SHAPES[
                      Math.floor(
                          Math.random() *
                          this.SHAPES.length
                      )
                  ]);
        const fixSize = lvl.fixSize !== null
            ? (lvl.fixSize || 'medium')
            : null;
        const fixRot = this.isCycling(lvl, 'rotation')
            ? null : 0;

        // Generate sequence + answer
        const total = lvl.seqLen + 1;
        const items = [];
        for (let i = 0; i < total; i++) {
            items.push({
                color: colorPool
                    ? colorPool[i % colorPool.length]
                    : fixColor,
                shape: shapePool
                    ? shapePool[i % shapePool.length]
                    : fixShape,
                size: this.isCycling(lvl, 'size')
                    ? this.SIZES[i % this.SIZES.length]
                    : (fixSize || 'medium'),
                rotation:
                    this.isCycling(lvl, 'rotation')
                    ? this.ROTATIONS[
                          i % this.ROTATIONS.length
                      ]
                    : (fixRot || 0),
            });
        }

        const sequence = items.slice(0, lvl.seqLen);
        const answer = items[lvl.seqLen];

        // Build choices — smart distractors
        const choices = [answer];
        const that = this;

        function addDistractor(prop, values) {
            for (const val of values) {
                if (choices.length >= lvl.choices) return;
                const d = Object.assign({}, answer);
                d[prop] = val;
                if (prop === 'color' &&
                    val.name === answer.color.name) {
                    continue;
                }
                if (prop !== 'color' &&
                    val === answer[prop]) {
                    continue;
                }
                if (!choices.some(
                        c => that.sameItem(c, d))) {
                    choices.push(d);
                }
            }
        }

        // Distractors from cycling properties first
        if (colorPool) {
            addDistractor('color', colorPool);
        }
        if (this.isCycling(lvl, 'size')) {
            addDistractor('size', this.SIZES);
        }
        if (shapePool) {
            addDistractor('shape', shapePool);
        }
        if (this.isCycling(lvl, 'rotation')) {
            addDistractor('rotation', this.ROTATIONS);
        }

        // Extra distractors from non-cycling pools
        if (choices.length < lvl.choices && colorPool) {
            const extra = this.COLORS.filter(
                c => !colorPool.some(
                    p => p.name === c.name
                )
            );
            addDistractor('color', extra);
        }
        if (choices.length < lvl.choices && shapePool) {
            const extra = this.SHAPES.filter(
                s => !shapePool.includes(s)
            );
            addDistractor('shape', extra);
        }

        this.shuffle(choices);
        return {
            sequence, answer, choices,
            colorPool, shapePool,
        };
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
    //  Start
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
        this.prevAnswerKey =
            this.itemKey(round.answer);

        this._renderSequence(round);
        this._renderChoices(round);
    },

    // =================================================================
    //  Render sequence with arrows
    // =================================================================
    _renderSequence(round) {
        const el = document.getElementById(
            'shift-sequence'
        );
        el.innerHTML = '';

        const baseSz = window.innerWidth < 400
            ? 48 : 56;

        for (let i = 0; i < round.sequence.length; i++)
        {
            // Arrow between items
            if (i > 0) {
                const arrow = document.createElement(
                    'div'
                );
                arrow.className = 'shift-arrow';
                arrow.innerHTML = '&#10132;';
                el.appendChild(arrow);
            }

            const div = document.createElement('div');
            div.className = 'shift-item';
            div.innerHTML = this.renderItemHTML(
                round.sequence[i], baseSz
            );
            div.style.animationDelay =
                (i * 0.15) + 's';
            el.appendChild(div);
        }

        // Arrow before mystery
        const arrow = document.createElement('div');
        arrow.className = 'shift-arrow';
        arrow.innerHTML = '&#10132;';
        el.appendChild(arrow);

        // Mystery
        const m = document.createElement('div');
        m.className = 'shift-item shift-mystery';
        m.textContent = '?';
        m.style.animationDelay =
            (round.sequence.length * 0.15) + 's';
        el.appendChild(m);
    },

    // =================================================================
    //  Render choices
    // =================================================================
    _renderChoices(round) {
        const el = document.getElementById(
            'shift-choices'
        );
        el.innerHTML = '';

        const baseSz = window.innerWidth < 400
            ? 52 : 64;

        for (const item of round.choices) {
            const btn = document.createElement('button');
            btn.className = 'shift-choice-btn';
            btn.innerHTML = this.renderItemHTML(
                item, baseSz
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

    _onCorrect(btn) {
        const s = this.state;
        s.streak++;
        s.stars++;
        this._renderStars();
        sfxCorrect();
        btn.classList.add('correct-flash');

        // Reveal answer
        const mystery = document.querySelector(
            '.shift-mystery'
        );
        if (mystery) {
            const baseSz = window.innerWidth < 400
                ? 48 : 56;
            mystery.textContent = '';
            mystery.classList.remove('shift-mystery');
            mystery.classList.add('shift-reveal');
            mystery.innerHTML = this.renderItemHTML(
                this.currentRound.answer, baseSz
            );
        }

        showFeedback(
            this.praises[
                Math.floor(
                    Math.random() *
                    this.praises.length
                )
            ],
            'correct', 1200
        );
        flyingStar();

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

        if (s.candies >= this.CANDIES_TO_WIN) {
            setTimeout(
                () => this._showChampion(), 1500
            );
            return;
        }

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

    _maybeShowPrize() {
        if (typeof PrizeManager !== 'undefined' &&
            PrizeManager.check(
                () => this.newRound()
            )) {
            return;
        }
        this.newRound();
    },

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
            .innerHTML =
                '&#11088; ' + this.state.stars;
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
    ShiftGame.init();
});
