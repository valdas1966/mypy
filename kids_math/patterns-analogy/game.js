// =========================================================================
//  Pattern Detective -- Analogy Puzzles  A : B  ::  C : ?
// =========================================================================

const AnalogyGame = {

    // --- Constants ---
    CANDIES_TO_WIN: 10,
    STARS_PER_CANDY: 3,
    STREAK_TO_LEVEL_UP: 3,

    // --- Colors (ordered by rainbow feel) ---
    COLORS: [
        { name: 'red',    fill: '#EF5350', stroke: '#C62828' },
        { name: 'orange', fill: '#FF7043', stroke: '#D84315' },
        { name: 'yellow', fill: '#FFEE58', stroke: '#F9A825' },
        { name: 'green',  fill: '#66BB6A', stroke: '#2E7D32' },
        { name: 'blue',   fill: '#42A5F5', stroke: '#1565C0' },
        { name: 'purple', fill: '#AB47BC', stroke: '#6A1B9A' },
        { name: 'pink',   fill: '#EC407A', stroke: '#AD1457' },
    ],

    // --- Shapes ---
    SHAPES: [
        'circle', 'triangle', 'square',
        'star', 'heart', 'diamond',
    ],

    // Rotation-visible shapes (for L4/L8 rotation-bearing rounds).
    DIR_SHAPES: ['triangle', 'arrow', 'heart'],

    SIZES: ['small', 'medium', 'large'],
    SIZE_SCALE: { small: 0.62, medium: 0.88, large: 1.15 },
    ROTATIONS: [0, 90, 180, 270],

    ALL_AXES: ['color', 'shape', 'size', 'rotation'],

    // --- Levels ---
    // cycling:  which properties change (A -> B)
    // fixes:    which non-cycling properties are locked to a value
    //           (missing = "free", randomly picked per round)
    // shapePool / colorPool: restrict the pool for cycling
    LEVELS: [
        // L1: Color only.  Shape free (C varies from A in shape).
        { cycling: ['color'],
          fixes: { size: 'medium', rotation: 0 },
          choices: 3 },

        // L2: Shape only.  Color free (C varies in color).
        { cycling: ['shape'],
          fixes: { size: 'medium', rotation: 0 },
          choices: 3 },

        // L3: Size only.  Shape + color free.
        { cycling: ['size'],
          fixes: { rotation: 0 },
          choices: 3 },

        // L4: Rotation only (arrow).  Color free.
        { cycling: ['rotation'],
          fixes: { shape: 'arrow', size: 'medium' },
          choices: 4 },

        // L5: Color + Shape.  Size free.
        { cycling: ['color', 'shape'],
          fixes: { rotation: 0 },
          choices: 4 },

        // L6: Color + Size.  Shape free.
        { cycling: ['color', 'size'],
          fixes: { rotation: 0 },
          choices: 4 },

        // L7: Shape + Size.  Color free.
        { cycling: ['shape', 'size'],
          fixes: { rotation: 0 },
          choices: 4 },

        // L8: Color + Shape + Rotation (three-way).
        //     Size is the free / perturbable axis.
        //     Shapes restricted to directional set so rotation
        //     is visibly different.
        { cycling: ['color', 'shape', 'rotation'],
          shapePool: ['triangle', 'arrow', 'heart'],
          choices: 5 },
    ],

    // --- State ---
    state: {},
    currentRound: null,
    prevAnswerKey: null,

    praises: [
        'Brilliant!', 'Sharp eye!', 'Super!',
        'Yes!', 'Amazing!', 'Nice!', 'Cool!',
    ],
    encouragements: [
        'Try again!', 'Look again!',
        'Almost!', 'You can do it!',
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

    pickOne(arr) {
        return arr[Math.floor(Math.random() * arr.length)];
    },

    propEq(prop, a, b) {
        if (a == null || b == null) return a === b;
        if (prop === 'color') return a.name === b.name;
        return a === b;
    },

    sameItem(a, b) {
        return this.propEq('color',  a.color,    b.color) &&
               this.propEq('shape',  a.shape,    b.shape) &&
               this.propEq('size',   a.size,     b.size) &&
               this.propEq('rotation', a.rotation, b.rotation);
    },

    itemKey(item) {
        return item.shape + '_' + item.color.name +
               '_' + item.size + '_' + item.rotation;
    },

    // --- Pool for a given axis under a given level ---
    axisPool(prop, lvl) {
        const fixes = lvl.fixes || {};
        if (prop in fixes) {
            return [fixes[prop]];
        }
        if (prop === 'color') {
            return lvl.colorPool
                ? this.COLORS.filter(
                      c => lvl.colorPool.includes(c.name))
                : this.COLORS;
        }
        if (prop === 'shape') {
            return lvl.shapePool || this.SHAPES;
        }
        if (prop === 'size') {
            return this.SIZES;
        }
        if (prop === 'rotation') {
            return this.ROTATIONS;
        }
        return [];
    },

    // =================================================================
    //  Item rendering (scaled, rotated div)
    // =================================================================
    renderItemHTML(item, baseSz) {
        const svg = this.shapeSVG(
            item.shape, item.color, baseSz);
        const sc = this.SIZE_SCALE[item.size] || 0.88;
        const rot = item.rotation || 0;
        const style = 'transform:scale(' + sc +
            ')rotate(' + rot + 'deg)';
        return '<div class="analogy-inner" style="' +
               style + '">' + svg + '</div>';
    },

    // =================================================================
    //  Round generation
    // =================================================================
    generateRound(lvl) {
        const cyclingSet = new Set(lvl.cycling);
        const nonCycling = this.ALL_AXES.filter(
            a => !cyclingSet.has(a));

        // 1. Pick src / tgt for each cycling property.
        const src = {};
        const tgt = {};
        for (const prop of lvl.cycling) {
            const pool = this.axisPool(prop, lvl);
            const [s, t] = this.pickN(pool, 2);
            src[prop] = s;
            tgt[prop] = t;
        }

        // 2. Build A.  Cycling props = src, non-cycling = random
        //    from the axis pool.
        const A = {};
        for (const prop of lvl.cycling) A[prop] = src[prop];
        for (const prop of nonCycling) {
            A[prop] = this.pickOne(this.axisPool(prop, lvl));
        }

        // 3. Build B = A with cycling props replaced by tgt.
        const B = { ...A };
        for (const prop of lvl.cycling) B[prop] = tgt[prop];

        // 4. Build C = A, then perturb in at least one
        //    non-cycling axis that has a multi-value pool.
        const C = { ...A };
        const perturbable = nonCycling.filter(prop => {
            const pool = this.axisPool(prop, lvl);
            return pool.length > 1;
        });
        if (perturbable.length > 0) {
            const axis = this.pickOne(perturbable);
            const pool = this.axisPool(axis, lvl);
            const alt = pool.filter(
                v => !this.propEq(axis, v, A[axis]));
            if (alt.length > 0) {
                C[axis] = this.pickOne(alt);
            }
        }

        // 5. Answer = C with cycling replaced by tgt.
        const answer = { ...C };
        for (const prop of lvl.cycling) {
            answer[prop] = tgt[prop];
        }

        // 6. Distractors.
        const choices = this._buildChoices(
            A, B, C, answer, src, tgt, lvl);

        return { A, B, C, answer, choices, src, tgt };
    },

    _buildChoices(A, B, C, answer, src, tgt, lvl) {
        const choices = [answer];
        const that = this;
        const tryAdd = (item) => {
            if (choices.length >= lvl.choices) return false;
            if (!item) return false;
            if (choices.some(
                    c => that.sameItem(c, item))) {
                return false;
            }
            choices.push(item);
            return true;
        };

        // D1: "No change" -- just C itself.  Tests whether
        //     the user actually applied the rule.
        tryAdd({ ...C });

        // D2: Partial -- apply only ONE of the cycling
        //     changes when rule involves 2+ axes.
        if (lvl.cycling.length >= 2) {
            for (const keep of lvl.cycling) {
                if (choices.length >= lvl.choices) break;
                const partial = { ...C };
                partial[keep] = tgt[keep];
                tryAdd(partial);
            }
        }

        // D3: Right axes, wrong target -- change one
        //     cycling prop to a value that is NOT the
        //     correct target.
        for (const prop of lvl.cycling) {
            if (choices.length >= lvl.choices) break;
            const pool = this.axisPool(prop, lvl);
            const wrong = pool.filter(v =>
                !this.propEq(prop, v, tgt[prop]) &&
                !this.propEq(prop, v, src[prop]));
            if (wrong.length > 0) {
                const alt = { ...answer };
                alt[prop] = this.pickOne(wrong);
                tryAdd(alt);
            }
        }

        // D4: Over-apply -- also change a non-cycling axis.
        const nonCy = this.ALL_AXES.filter(
            a => !lvl.cycling.includes(a));
        for (const prop of nonCy) {
            if (choices.length >= lvl.choices) break;
            const pool = this.axisPool(prop, lvl);
            if (pool.length <= 1) continue;
            const alt = pool.filter(
                v => !this.propEq(prop, v, answer[prop]));
            if (alt.length > 0) {
                const extra = { ...answer };
                extra[prop] = this.pickOne(alt);
                tryAdd(extra);
            }
        }

        // Fallback: random mutations of C.
        let safety = 30;
        while (choices.length < lvl.choices && safety-- > 0) {
            const axis = this.pickOne(this.ALL_AXES);
            const pool = this.axisPool(axis, lvl);
            if (pool.length <= 1) continue;
            const alt = pool.filter(
                v => !this.propEq(axis, v, C[axis]));
            if (alt.length > 0) {
                const cand = { ...C };
                cand[axis] = this.pickOne(alt);
                tryAdd(cand);
            }
        }

        this.shuffle(choices);
        return choices;
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
        this.prevAnswerKey = this.itemKey(round.answer);

        this._renderRound(round);
        this._renderChoices(round);
    },

    // =================================================================
    //  Render the example (A -> B) and puzzle (C -> ?)
    // =================================================================
    _renderRound(round) {
        const baseSz = window.innerWidth < 400 ? 50 : 58;

        const exEl = document.getElementById(
            'analogy-example');
        exEl.innerHTML = '';
        exEl.appendChild(
            this._makeItem(round.A, baseSz, 0));
        exEl.appendChild(this._makeArrow());
        exEl.appendChild(
            this._makeItem(round.B, baseSz, 1));

        const pzEl = document.getElementById(
            'analogy-puzzle');
        pzEl.innerHTML = '';
        pzEl.appendChild(
            this._makeItem(round.C, baseSz, 2));
        pzEl.appendChild(this._makeArrow());
        pzEl.appendChild(this._makeMystery(baseSz, 3));
    },

    _makeItem(item, baseSz, idx) {
        const div = document.createElement('div');
        div.className = 'analogy-item';
        div.innerHTML = this.renderItemHTML(item, baseSz);
        div.style.animationDelay = (idx * 0.12) + 's';
        return div;
    },

    _makeArrow() {
        const el = document.createElement('div');
        el.className = 'analogy-arrow';
        el.innerHTML = '&#10132;';
        return el;
    },

    _makeMystery(baseSz, idx) {
        const m = document.createElement('div');
        m.className = 'analogy-item analogy-mystery';
        m.textContent = '?';
        m.style.animationDelay = (idx * 0.12) + 's';
        return m;
    },

    // =================================================================
    //  Render choices
    // =================================================================
    _renderChoices(round) {
        const el = document.getElementById(
            'analogy-choices');
        el.innerHTML = '';

        const baseSz = window.innerWidth < 400 ? 52 : 62;

        for (const item of round.choices) {
            const btn = document.createElement('button');
            btn.className = 'analogy-choice-btn';
            btn.innerHTML = this.renderItemHTML(
                item, baseSz);
            btn.addEventListener('click',
                () => this.handleAnswer(item, btn));
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

        // Reveal answer in the puzzle's mystery slot.
        const mystery = document.querySelector(
            '.analogy-mystery');
        if (mystery) {
            const baseSz = window.innerWidth < 400
                ? 50 : 58;
            mystery.textContent = '';
            mystery.classList.remove('analogy-mystery');
            mystery.classList.add('analogy-reveal');
            mystery.innerHTML = this.renderItemHTML(
                this.currentRound.answer, baseSz);
        }

        showFeedback(
            this.praises[
                Math.floor(Math.random() *
                           this.praises.length)],
            'correct', 1200);
        flyingStar();

        const prev = s.candies;
        s.candies = Math.floor(
            s.stars / this.STARS_PER_CANDY);
        if (s.candies > prev &&
            s.candies <= this.CANDIES_TO_WIN) {
            setTimeout(() => {
                this._renderCandyBar();
                sfxCandy();
            }, 600);
        }

        if (s.candies >= this.CANDIES_TO_WIN) {
            setTimeout(
                () => this._showChampion(), 1500);
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
                    'Level Up!', 'levelup', 2200);
                spawnConfetti(30);
            }, 800);
            setTimeout(
                () => this._maybeShowPrize(), 3200);
        } else {
            setTimeout(
                () => this._maybeShowPrize(), 1400);
        }
    },

    _onWrong(btn) {
        this.state.streak = 0;
        sfxWrong();
        btn.classList.add('shake');
        showFeedback(
            this.encouragements[
                Math.floor(Math.random() *
                           this.encouragements.length)],
            'wrong', 1000);
        setTimeout(() => {
            btn.classList.remove('shake');
            this.state.answering = true;
        }, 800);
    },

    _maybeShowPrize() {
        if (typeof PrizeManager !== 'undefined' &&
            PrizeManager.check(
                () => this.newRound())) {
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
                (i < this.state.candies ? ' earned' : '');
            slot.textContent =
                i < this.state.candies
                    ? '\u{1F36C}' : '';
            bar.appendChild(slot);
        }
    },
};

// === Bootstrap ===
document.addEventListener('DOMContentLoaded', () => {
    AnalogyGame.init();
});
