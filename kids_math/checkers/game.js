// =========================================================================
//  Checkers — kid-friendly handicap match
//
//  Player always has 4 cat warriors. Computer has 1-4 dog warriors,
//  chosen on the welcome screen.
//
//  Board: 8x8, dark squares only used. Player at row 7 (cols
//  0,2,4,6); computer at row 0 (center-out columns).
//
//  Rules (simplified for a 5-year-old):
//    * Pieces move one square diagonally forward.
//    * Capture by jumping diagonally over an opponent to the
//      empty square beyond.
//    * No multi-jumps. No mandatory captures (player free to
//      choose any legal move).
//    * Reach the opposite back row -> piece becomes a king (crown)
//      and may move/capture in all 4 diagonals.
//    * You win when the computer has no legal moves (captured or
//      stuck). You lose when you have no legal moves.
//
//  Scoring per match: win = +3 stars. Every 3 stars = 1 candy.
//  5 candies = Champion.
//
//  Computer AI: greedy. Always takes a capture if available;
//  otherwise advances toward the player with mild randomness.
// =========================================================================

const CheckersGame = {

    SIZE: 8,
    CANDIES_TO_WIN: 5,
    STARS_PER_CANDY: 3,
    STARS_WIN: 3,

    // PC starting columns on row 0 (center-out) by count.
    PC_COLS: {
        1: [3],
        2: [3, 5],
        3: [1, 3, 5],
        4: [1, 3, 5, 7],
    },
    PLAYER_COLS: [0, 2, 4, 6],

    // --- State ---
    state: {},

    // =================================================================
    //  Init — wire welcome buttons, play-again, mute
    // =================================================================
    init() {
        populateAnimals('welcome-animals');
        populateAnimals('champion-animals');

        document.querySelectorAll('.ck-pc-btn')
            .forEach(btn => btn.addEventListener('click',
                () => this.start(
                    parseInt(btn.dataset.pc, 10)
                )));

        document.getElementById('play-again-btn')
            .addEventListener('click',
                () => this.start(this.state.pcCount || 4));

        document.getElementById('mute-btn')
            .addEventListener('click', () => {
                muted = !muted;
                document.getElementById('mute-btn').innerHTML =
                    muted ? '&#128263;' : '&#128264;';
            });

        spawnClouds();
    },

    // =================================================================
    //  Start a fresh session at the chosen PC count
    // =================================================================
    start(pcCount) {
        initAudio();
        this.state = {
            pcCount: pcCount,
            stars: 0,
            candies: 0,
            board: this._initialBoard(pcCount),
            turn: 'P',
            selected: null,
            validTargets: [],
            gameOver: false,
            playerWon: false,
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
        this._renderTally();
        this._setStatus('Your turn!');
    },

    // =================================================================
    //  Build the initial board for the given PC count
    // =================================================================
    _initialBoard(pcCount) {
        const board = Array(this.SIZE * this.SIZE).fill(null);
        for (const c of this.PLAYER_COLS) {
            board[this._idx(7, c)] =
                { side: 'P', king: false };
        }
        for (const c of this.PC_COLS[pcCount]) {
            board[this._idx(0, c)] =
                { side: 'A', king: false };
        }
        return board;
    },

    // =================================================================
    //  Restart the same handicap (after a finished match)
    // =================================================================
    _restart() {
        this.state.board =
            this._initialBoard(this.state.pcCount);
        this.state.turn = 'P';
        this.state.selected = null;
        this.state.validTargets = [];
        this.state.gameOver = false;
        this.state.playerWon = false;
        this._renderBoard();
        this._renderTally();
        this._setStatus('Your turn!');
    },

    // =================================================================
    //  Board helpers
    // =================================================================
    _idx(r, c)    { return r * this.SIZE + c; },
    _at(r, c)     { return this.state.board[this._idx(r, c)]; },
    _set(r, c, v) { this.state.board[this._idx(r, c)] = v; },
    _inBounds(r, c) {
        return r >= 0 && r < this.SIZE &&
               c >= 0 && c < this.SIZE;
    },
    _isDark(r, c) { return ((r + c) % 2) === 1; },

    _moveDirs(piece) {
        if (piece.king) {
            return [[-1,-1], [-1,1], [1,-1], [1,1]];
        }
        // Player moves up (row -); computer moves down (row +).
        return piece.side === 'P'
            ? [[-1,-1], [-1,1]]
            : [[1,-1], [1,1]];
    },

    // =================================================================
    //  Valid moves for a single piece (simple moves + captures)
    // =================================================================
    _validMoves(r, c) {
        const piece = this._at(r, c);
        if (!piece) return [];
        const out = [];
        for (const [dr, dc] of this._moveDirs(piece)) {
            const r1 = r + dr, c1 = c + dc;
            if (!this._inBounds(r1, c1)) continue;

            const mid = this._at(r1, c1);
            if (mid === null) {
                out.push({ toR: r1, toC: c1, capture: null });
                continue;
            }
            if (mid.side === piece.side) continue;

            // Opponent: try to jump
            const r2 = r + 2 * dr, c2 = c + 2 * dc;
            if (this._inBounds(r2, c2) && this._at(r2, c2) === null) {
                out.push({
                    toR: r2, toC: c2,
                    capture: { r: r1, c: c1 },
                });
            }
        }
        return out;
    },

    // =================================================================
    //  All legal moves for a side
    // =================================================================
    _allMovesFor(side) {
        const all = [];
        for (let r = 0; r < this.SIZE; r++) {
            for (let c = 0; c < this.SIZE; c++) {
                const p = this._at(r, c);
                if (!p || p.side !== side) continue;
                for (const m of this._validMoves(r, c)) {
                    all.push({
                        fromR: r, fromC: c,
                        toR: m.toR, toC: m.toC,
                        capture: m.capture,
                    });
                }
            }
        }
        return all;
    },

    // =================================================================
    //  Player click handler
    // =================================================================
    handleCellClick(r, c) {
        const s = this.state;
        if (s.gameOver || s.turn !== 'P') return;

        const piece = this._at(r, c);
        const sel = s.selected;

        if (sel) {
            const tgt = s.validTargets.find(
                m => m.toR === r && m.toC === c
            );
            if (tgt) {
                this._executeMove(sel.r, sel.c, tgt);
                return;
            }
            // Switch selection to another own piece with moves
            if (piece && piece.side === 'P') {
                const moves = this._validMoves(r, c);
                if (moves.length > 0) {
                    this._select(r, c, moves);
                    return;
                }
            }
            // Otherwise: deselect
            s.selected = null;
            s.validTargets = [];
            this._renderBoard();
            return;
        }

        // No prior selection
        if (piece && piece.side === 'P') {
            const moves = this._validMoves(r, c);
            if (moves.length > 0) {
                this._select(r, c, moves);
            }
        }
    },

    _select(r, c, moves) {
        initAudio();
        sfxPop();
        this.state.selected = { r, c };
        this.state.validTargets = moves;
        this._renderBoard();
    },

    // =================================================================
    //  Execute a move (used by both player and AI)
    // =================================================================
    _executeMove(fromR, fromC, move) {
        const s = this.state;
        const piece = this._at(fromR, fromC);

        // Move piece
        this._set(fromR, fromC, null);
        this._set(move.toR, move.toC, piece);

        // Capture
        if (move.capture) {
            this._set(move.capture.r, move.capture.c, null);
            sfxCorrect();
        } else {
            sfxPop();
        }

        // King promotion (regular pieces only — kings stay kings)
        let crowned = false;
        if (!piece.king) {
            if (piece.side === 'P' && move.toR === 0) {
                piece.king = true; crowned = true;
            } else if (piece.side === 'A' &&
                       move.toR === this.SIZE - 1) {
                piece.king = true; crowned = true;
            }
        }
        if (crowned) sfxLevelUp();

        // Reset selection / targets
        s.selected = null;
        s.validTargets = [];
        this._renderBoard();
        this._renderTally();

        // End-of-match check (opponent has no moves -> we win)
        if (this._checkGameOver(piece.side)) return;

        // Switch turn
        s.turn = piece.side === 'P' ? 'A' : 'P';
        if (s.turn === 'A') {
            this._setStatus("Computer's turn\u2026");
            setTimeout(() => this._aiMove(), 700);
        } else {
            this._setStatus('Your turn!');
        }
    },

    _checkGameOver(justMovedSide) {
        const opponent = justMovedSide === 'P' ? 'A' : 'P';
        const opponentMoves = this._allMovesFor(opponent);
        if (opponentMoves.length === 0) {
            this.state.gameOver = true;
            this.state.playerWon = (justMovedSide === 'P');
            setTimeout(() => this._showOutcome(), 700);
            return true;
        }
        return false;
    },

    // =================================================================
    //  AI: pick and play a move
    // =================================================================
    _aiMove() {
        if (this.state.gameOver) return;
        const moves = this._allMovesFor('A');
        if (moves.length === 0) return;

        // Captures first
        const captures = moves.filter(m => m.capture);
        let chosen;
        if (captures.length > 0) {
            chosen = captures[
                Math.floor(Math.random() * captures.length)
            ];
        } else {
            // Score by advancement (PC moves down, prefer higher row)
            // plus a tiny random tiebreak
            const scored = moves.map(m => ({
                m,
                score: m.toR + Math.random() * 0.5,
            }));
            scored.sort((a, b) => b.score - a.score);
            chosen = scored[0].m;
        }
        this._executeMove(chosen.fromR, chosen.fromC, chosen);
    },

    // =================================================================
    //  Outcome
    // =================================================================
    _showOutcome() {
        if (this.state.playerWon) this._onWin();
        else                      this._onLoss();
    },

    _onWin() {
        sfxCorrect();
        this.state.stars += this.STARS_WIN;
        this._renderStars();
        for (let i = 0; i < this.STARS_WIN; i++) {
            setTimeout(() => flyingStar(), i * 120);
        }
        showFeedback('You Won!', 'correct', 1600);
        this._setStatus('You won! \u{1F389}');
        spawnConfetti(40);
        this._afterGame();
    },

    _onLoss() {
        sfxWrong();
        showFeedback('Try again!', 'wrong', 1600);
        this._setStatus('Computer won. Try again!');
        this._afterGame();
    },

    // =================================================================
    //  After-game flow: candies, prize, restart or champion
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
            setTimeout(() => this._showChampion(), 2200);
            return;
        }
        setTimeout(() => {
            if (typeof PrizeManager !== 'undefined' &&
                PrizeManager.check(() => this._restart())) {
                return;
            }
            this._restart();
        }, 2400);
    },

    _showChampion() {
        sfxChampion();
        spawnConfetti(80);
        this._showScreen('champion-screen');
    },

    // =================================================================
    //  Rendering
    // =================================================================
    _renderBoard() {
        const el = document.getElementById('ck-board');
        el.innerHTML = '';
        const s = this.state;

        for (let r = 0; r < this.SIZE; r++) {
            for (let c = 0; c < this.SIZE; c++) {
                const cell = document.createElement('div');
                cell.className = 'ck-cell ' +
                    (this._isDark(r, c) ? 'dark' : 'light');

                if (s.selected &&
                    s.selected.r === r && s.selected.c === c) {
                    cell.classList.add('selected');
                }
                const tgt = s.validTargets.find(
                    m => m.toR === r && m.toC === c
                );
                if (tgt) {
                    cell.classList.add(
                        tgt.capture
                            ? 'capture-target'
                            : 'move-target'
                    );
                }

                const piece = this._at(r, c);
                if (piece) {
                    const p = document.createElement('div');
                    p.className = 'ck-piece ' +
                        (piece.side === 'P' ? 'player' : 'ai');
                    if (piece.king) {
                        const crown = document.createElement(
                            'span'
                        );
                        crown.className = 'ck-crown';
                        crown.innerHTML = '&#128081;';
                        p.appendChild(crown);
                    }
                    cell.appendChild(p);
                }

                // handleCellClick guards turn + gameOver,
                // so attach unconditionally.
                if (this._isDark(r, c)) {
                    cell.addEventListener('click',
                        () => this.handleCellClick(r, c));
                }

                el.appendChild(cell);
            }
        }
    },

    _renderTally() {
        let p = 0, a = 0;
        for (const piece of this.state.board) {
            if (!piece) continue;
            if (piece.side === 'P') p++; else a++;
        }
        document.getElementById('ck-tally-p').textContent = p;
        document.getElementById('ck-tally-a').textContent = a;
    },

    _setStatus(text) {
        document.getElementById('ck-status').textContent = text;
    },

    _showScreen(id) {
        document.querySelectorAll('.screen')
            .forEach(s => s.classList.add('hidden'));
        document.getElementById(id).classList.remove('hidden');
    },

    _updateBodyLevel() {
        document.body.className =
            'level-' + this.state.pcCount;
    },

    _renderStars() {
        document.getElementById('stars-display').innerHTML =
            '&#11088; ' + this.state.stars;
    },

    _renderLevel() {
        document.getElementById('level-display').textContent =
            'PC: ' + this.state.pcCount;
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
    CheckersGame.init();
});
