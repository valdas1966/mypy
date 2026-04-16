// =========================================================================
//  Tic Tac Toe — kid-friendly, 3 difficulty levels
//
//  Pieces: player = cat, computer = dog.
//  Player always goes first.
//
//  Scoring per game:
//    win  -> +3 stars
//    draw -> +1 star
//    loss -> +0 stars
//  Every 3 stars = 1 candy. 6 candies = Champion.
//
//  Difficulty:
//    easy   -> AI picks a random empty cell.
//    medium -> AI takes an immediate win, blocks an immediate
//              threat, otherwise random.
//    hard   -> AI plays minimax (perfect tic-tac-toe). With
//              probability HARD_RANDOM_PROB it picks randomly,
//              giving the child a small chance to win.
// =========================================================================

const TicTacToeGame = {

    // --- Constants ---
    CANDIES_TO_WIN: 6,
    STARS_PER_CANDY: 3,
    STARS_WIN: 3,
    STARS_DRAW: 1,
    HARD_RANDOM_PROB: 0.15,

    // --- Win lines (8 total: 3 rows, 3 cols, 2 diagonals) ---
    LINES: [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6],
    ],

    // --- Pieces ---
    PIECE_PLAYER: '\u{1F431}',   // cat
    PIECE_AI:     '\u{1F436}',   // dog

    // --- Difficulty meta ---
    DIFFICULTY_NAMES: {
        easy: 'Easy', medium: 'Medium', hard: 'Hard',
    },
    DIFFICULTY_LEVEL: {
        easy: 1, medium: 2, hard: 3,
    },

    // --- State ---
    state: {},

    praises: [
        'Great!', 'Awesome!', 'Super!',
        'Yay!', 'Wow!', 'Nice!',
    ],
    encouragements: [
        'Try again!', 'Almost!',
        'One more try!', 'You can do it!',
    ],

    // =================================================================
    //  Init — wire up welcome / game / champion buttons
    // =================================================================
    init() {
        populateAnimals('welcome-animals');
        populateAnimals('champion-animals');

        document.querySelectorAll('.ttt-diff-btn')
            .forEach(btn => btn.addEventListener('click',
                () => this.start(btn.dataset.diff)));

        document.getElementById('play-again-btn')
            .addEventListener('click',
                () => this.start(this.state.diff || 'easy'));

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
    //  Start / restart at a given difficulty
    // =================================================================
    start(difficulty) {
        initAudio();
        this.state = {
            diff: difficulty,
            stars: 0,
            candies: 0,
            board: Array(9).fill(null),
            playerTurn: true,
            gameOver: false,
            firstStart: true,
        };
        if (typeof PrizeManager !== 'undefined') {
            PrizeManager.init();
        }
        this._updateBodyLevel();
        this._renderStars();
        this._renderLevel();
        this._renderCandyBar();
        this._showScreen('game-screen');
        spawnClouds();
        this._renderBoard();
        this._setStatus('Your turn!');
    },

    // =================================================================
    //  Start a new game (same difficulty)
    // =================================================================
    newGame() {
        this.state.board = Array(9).fill(null);
        this.state.playerTurn = true;
        this.state.gameOver = false;
        this._renderBoard();
        this._setStatus('Your turn!');
    },

    // =================================================================
    //  Player clicked a cell
    // =================================================================
    handleCellClick(idx) {
        const s = this.state;
        if (s.gameOver || !s.playerTurn) return;
        if (s.board[idx] !== null) return;
        initAudio();

        s.board[idx] = 'P';
        s.playerTurn = false;
        sfxPop();
        this._renderBoard();

        if (this._endIfFinished()) return;

        this._setStatus("Computer's turn\u2026");
        setTimeout(() => this.aiMove(), 550);
    },

    // =================================================================
    //  AI plays one move
    // =================================================================
    aiMove() {
        if (this.state.gameOver) return;
        const move = this._pickAiMove();
        if (move >= 0) {
            this.state.board[move] = 'A';
            sfxPop();
            this._renderBoard();
        }
        if (this._endIfFinished()) return;
        this.state.playerTurn = true;
        this._setStatus('Your turn!');
    },

    // =================================================================
    //  AI strategy by difficulty
    // =================================================================
    _pickAiMove() {
        const board = this.state.board;
        const empties = this._emptyCells(board);
        if (empties.length === 0) return -1;

        if (this.state.diff === 'easy') {
            return this._randomFrom(empties);
        }

        if (this.state.diff === 'medium') {
            const win = this._findThreat(board, 'A');
            if (win >= 0) return win;
            const block = this._findThreat(board, 'P');
            if (block >= 0) return block;
            return this._randomFrom(empties);
        }

        // hard: mostly minimax, occasional random for fairness
        if (Math.random() < this.HARD_RANDOM_PROB) {
            return this._randomFrom(empties);
        }
        return this._minimax(board.slice(), 'A').move;
    },

    // =================================================================
    //  Find a cell that completes a line for `who` (immediate
    //  win or block). Returns -1 if none.
    // =================================================================
    _findThreat(board, who) {
        for (const line of this.LINES) {
            const vals = line.map(i => board[i]);
            const owned = vals.filter(v => v === who).length;
            const empty = vals.filter(v => v === null).length;
            if (owned === 2 && empty === 1) {
                const idx = vals.indexOf(null);
                return line[idx];
            }
        }
        return -1;
    },

    // =================================================================
    //  Minimax with depth-aware scoring (prefer faster wins,
    //  slower losses). Returns { score, move }.
    // =================================================================
    _minimax(board, turn, depth = 0) {
        const w = this._winnerOf(board);
        if (w === 'A')    return { score: 10 - depth };
        if (w === 'P')    return { score: depth - 10 };
        if (w === 'draw') return { score: 0 };

        const isMax = (turn === 'A');
        let best = {
            score: isMax ? -Infinity : Infinity,
            move: -1,
        };
        for (let i = 0; i < 9; i++) {
            if (board[i] !== null) continue;
            board[i] = turn;
            const res = this._minimax(
                board, turn === 'A' ? 'P' : 'A', depth + 1
            );
            board[i] = null;
            if (isMax) {
                if (res.score > best.score) {
                    best = { score: res.score, move: i };
                }
            } else {
                if (res.score < best.score) {
                    best = { score: res.score, move: i };
                }
            }
        }
        return best;
    },

    // =================================================================
    //  Game-state helpers
    // =================================================================
    _emptyCells(board) {
        const out = [];
        for (let i = 0; i < 9; i++) {
            if (board[i] === null) out.push(i);
        }
        return out;
    },

    _randomFrom(arr) {
        return arr[Math.floor(Math.random() * arr.length)];
    },

    _winnerOf(board) {
        for (const [a, b, c] of this.LINES) {
            if (board[a] &&
                board[a] === board[b] &&
                board[a] === board[c]) {
                return board[a];
            }
        }
        if (board.every(v => v !== null)) return 'draw';
        return null;
    },

    _winningLine(board) {
        for (const line of this.LINES) {
            const [a, b, c] = line;
            if (board[a] &&
                board[a] === board[b] &&
                board[a] === board[c]) {
                return line;
            }
        }
        return null;
    },

    // =================================================================
    //  Check end-of-game; trigger win/loss/draw flow.
    //  Returns true if the game ended.
    // =================================================================
    _endIfFinished() {
        const w = this._winnerOf(this.state.board);
        if (w === null) return false;
        this.state.gameOver = true;
        const line = this._winningLine(this.state.board);
        if (line) {
            const cls = (w === 'P') ? 'win' : 'lose';
            this._highlightLine(line, cls);
        }
        if (w === 'P')      this._onWin();
        else if (w === 'A') this._onLoss();
        else                this._onDraw();
        return true;
    },

    _highlightLine(line, cls) {
        const cells = document.querySelectorAll('.ttt-cell');
        line.forEach(i => cells[i].classList.add(cls));
    },

    // =================================================================
    //  Outcome handlers
    // =================================================================
    _onWin() {
        sfxCorrect();
        this.state.stars += this.STARS_WIN;
        this._renderStars();
        for (let i = 0; i < this.STARS_WIN; i++) {
            setTimeout(() => flyingStar(), i * 120);
        }
        showFeedback(
            this._pick(this.praises),
            'correct', 1400
        );
        this._setStatus('You won! \u{1F389}');
        this._afterGame();
    },

    _onLoss() {
        sfxWrong();
        showFeedback(
            this._pick(this.encouragements),
            'wrong', 1400
        );
        this._setStatus('Computer won.');
        this._afterGame();
    },

    _onDraw() {
        sfxPop();
        this.state.stars += this.STARS_DRAW;
        this._renderStars();
        flyingStar();
        showFeedback("It's a tie!", 'correct', 1400);
        this._setStatus('Tie game! +1 star');
        this._afterGame();
    },

    _pick(arr) {
        return arr[Math.floor(Math.random() * arr.length)];
    },

    // =================================================================
    //  Post-game: update candies, maybe show prize, then new game
    // =================================================================
    _afterGame() {
        const s = this.state;
        const prev = s.candies;
        s.candies = Math.min(
            Math.floor(s.stars / this.STARS_PER_CANDY),
            this.CANDIES_TO_WIN
        );
        if (s.candies > prev) {
            setTimeout(() => {
                this._renderCandyBar();
                sfxCandy();
            }, 600);
        }
        if (s.candies >= this.CANDIES_TO_WIN) {
            setTimeout(() => this._showChampion(), 2000);
            return;
        }
        setTimeout(() => {
            if (typeof PrizeManager !== 'undefined' &&
                PrizeManager.check(() => this.newGame())) {
                return;
            }
            this.newGame();
        }, 1800);
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
    //  Rendering
    // =================================================================
    _renderBoard() {
        const el = document.getElementById('ttt-board');
        el.innerHTML = '';
        for (let i = 0; i < 9; i++) {
            const cell = document.createElement('button');
            cell.className = 'ttt-cell';
            cell.type = 'button';
            const v = this.state.board[i];
            if (v) {
                cell.classList.add('played');
                const span = document.createElement('span');
                span.className = 'ttt-piece';
                span.textContent = (v === 'P')
                    ? this.PIECE_PLAYER
                    : this.PIECE_AI;
                cell.appendChild(span);
            } else if (!this.state.gameOver) {
                cell.addEventListener('click',
                    () => this.handleCellClick(i));
            }
            el.appendChild(cell);
        }
    },

    _setStatus(text) {
        document.getElementById('ttt-status').textContent = text;
    },

    _showScreen(id) {
        document.querySelectorAll('.screen')
            .forEach(s => s.classList.add('hidden'));
        document.getElementById(id).classList.remove('hidden');
    },

    _updateBodyLevel() {
        document.body.className =
            'level-' + this.DIFFICULTY_LEVEL[this.state.diff];
    },

    _renderStars() {
        document.getElementById('stars-display').innerHTML =
            '&#11088; ' + this.state.stars;
    },

    _renderLevel() {
        document.getElementById('level-display').textContent =
            this.DIFFICULTY_NAMES[this.state.diff];
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
    TicTacToeGame.init();
});
