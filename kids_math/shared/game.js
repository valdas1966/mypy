// =========================================================================
//  Game Engine — shared state, UI, and lifecycle for all games
// =========================================================================
const GameEngine = {

    // --- constants ---
    CANDIES_TO_WIN: 10,
    STARS_PER_CANDY: 3,
    STREAK_TO_LEVEL_UP: 3,

    praises: [
        'Great!', 'Awesome!', 'Super!',
        'Yay!', 'Wow!', 'Cool!', 'Nice!'
    ],
    encouragements: [
        'Try again!', 'Almost!',
        'One more try!', 'You can do it!'
    ],

    // --- state (reset on each start) ---
    state: {},

    // --- config (set by each game via init) ---
    //  {
    //    title:          string,
    //    levels:         array  — game-specific level configs,
    //    onNewRound:     fn(levelCfg) → correctAnswer,
    //    getButtonRange: fn(levelCfg) → { min, max },
    //  }
    config: null,

    // =====================================================================
    //  Initialisation — called once by the game-specific script
    // =====================================================================
    init(config) {
        this.config = config;

        // Welcome screen
        document.getElementById('welcome-title').innerHTML =
            config.title;
        populateAnimals('welcome-animals');
        populateAnimals('champion-animals');

        // Bind buttons
        document.getElementById('play-btn')
            .addEventListener('click', () => this.start());
        document.getElementById('play-again-btn')
            .addEventListener('click', () => this.start());
        document.getElementById('mute-btn')
            .addEventListener('click', () => {
                muted = !muted;
                document.getElementById('mute-btn').innerHTML =
                    muted ? '&#128263;' : '&#128264;';
            });

        spawnClouds();
    },

    // =====================================================================
    //  Start / restart a game session
    // =====================================================================
    start() {
        initAudio();
        this.state = {
            level: 0,
            stars: 0,
            candies: 0,
            streak: 0,
            correctAnswer: 0,
            answering: true,
        };
        this._updateBodyLevel();
        this._renderStars();
        this._renderLevel();
        this._renderCandyBar();
        this._showScreen('game-screen');
        spawnClouds();
        setTimeout(() => this.newRound(), 400);
    },

    // =====================================================================
    //  New round — delegate to game-specific onNewRound
    // =====================================================================
    newRound() {
        this.state.answering = true;
        const lvCfg = this.config.levels[this.state.level];
        this.state.correctAnswer = this.config.onNewRound(lvCfg);
        this._renderButtons(lvCfg);
    },

    // =====================================================================
    //  Handle answer
    // =====================================================================
    handleAnswer(num, btn) {
        if (!this.state.answering) return;
        this.state.answering = false;
        initAudio();

        if (num === this.state.correctAnswer) {
            this._onCorrect(btn);
        } else {
            this._onWrong(btn);
        }
    },

    // =====================================================================
    //  Correct answer flow
    // =====================================================================
    _onCorrect(btn) {
        const s = this.state;
        s.streak++;
        s.stars++;
        this._renderStars();
        sfxCorrect();
        btn.classList.add('correct-flash');

        const field = document.getElementById('animal-field');
        if (field) field.classList.add('happy');

        showFeedback(
            this.praises[Math.floor(Math.random() * this.praises.length)],
            'correct', 1200
        );
        flyingStar();

        // Candy check
        const prev = s.candies;
        s.candies = Math.floor(s.stars / this.STARS_PER_CANDY);
        if (s.candies > prev && s.candies <= this.CANDIES_TO_WIN) {
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
            s.level < this.config.levels.length - 1) {
            s.level++;
            s.streak = 0;
            this._updateBodyLevel();
            this._renderLevel();
            setTimeout(() => {
                sfxLevelUp();
                showFeedback('Level Up!', 'levelup', 2200);
                spawnConfetti(30);
            }, 800);
            setTimeout(() => this.newRound(), 3200);
        } else {
            setTimeout(() => this.newRound(), 1400);
        }
    },

    // =====================================================================
    //  Wrong answer flow
    // =====================================================================
    _onWrong(btn) {
        this.state.streak = 0;
        sfxWrong();
        btn.classList.add('shake');
        showFeedback(
            this.encouragements[
                Math.floor(Math.random() * this.encouragements.length)
            ],
            'wrong', 1000
        );
        setTimeout(() => {
            btn.classList.remove('shake');
            this.state.answering = true;
        }, 800);
    },

    // =====================================================================
    //  Champion screen
    // =====================================================================
    _showChampion() {
        sfxChampion();
        spawnConfetti(80);
        this._showScreen('champion-screen');
    },

    // =====================================================================
    //  UI helpers
    // =====================================================================
    _showScreen(id) {
        document.querySelectorAll('.screen')
            .forEach(s => s.classList.add('hidden'));
        document.getElementById(id).classList.remove('hidden');
    },

    _updateBodyLevel() {
        document.body.className = `level-${this.state.level + 1}`;
    },

    _renderStars() {
        document.getElementById('stars-display').innerHTML =
            `&#11088; ${this.state.stars}`;
    },

    _renderLevel() {
        document.getElementById('level-display').textContent =
            `Level ${this.state.level + 1}`;
    },

    _renderCandyBar() {
        const bar = document.getElementById('candy-bar');
        bar.innerHTML = '';
        for (let i = 0; i < this.CANDIES_TO_WIN; i++) {
            const slot = document.createElement('div');
            slot.className =
                'candy-slot' + (i < this.state.candies ? ' earned' : '');
            slot.textContent =
                i < this.state.candies ? '\u{1F36C}' : '';
            bar.appendChild(slot);
        }
    },

    _renderButtons(lvCfg) {
        const grid = document.getElementById('number-grid');
        grid.innerHTML = '';
        const range = this.config.getButtonRange(lvCfg);
        for (let i = range.min; i <= range.max; i++) {
            const btn = document.createElement('button');
            btn.className = 'num-btn';
            btn.textContent = i;
            const num = i;
            btn.addEventListener('click', () =>
                this.handleAnswer(num, btn));
            grid.appendChild(btn);
        }
    },
};
