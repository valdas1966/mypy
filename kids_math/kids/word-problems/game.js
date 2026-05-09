// =========================================================================
//  Word Problems — Maya & Mika (Hebrew, +/-, drag balls between baskets)
// =========================================================================
document.addEventListener('DOMContentLoaded', () => {

    const REWARD_EVERY = 5;    // prize after every N successes
    const MAX_NUM      = 10;   // max value anywhere

    // -------------------------------------------------------------------
    //  Hebrew helpers — grammatical agreement for "ball" / "balls"
    // -------------------------------------------------------------------
    const _balls = (n) => (n === 1 ? 'כדור אחד' : `${n} כדורים`);
    const _had   = (n, who) =>
        n === 1 ? `ל${who} היה כדור אחד`
                : `ל${who} היו ${n} כדורים`;

    // -------------------------------------------------------------------
    //  Problem templates — each returns full problem record
    // -------------------------------------------------------------------
    const TEMPLATES = [
        // SUB — Maya gives Mika
        (a, b) => ({
            text:
                `${_had(a, 'מאיה')}. היא נתנה ${_balls(b)} למיקה. ` +
                `כמה כדורים נשארו למאיה?`,
            initialMaya: a, initialMika: 0, result: a - b,
        }),
        // SUB — Mika gives Maya
        (a, b) => ({
            text:
                `${_had(a, 'מיקה')}. היא נתנה ${_balls(b)} למאיה. ` +
                `כמה כדורים נשארו למיקה?`,
            initialMaya: 0, initialMika: a, result: a - b,
        }),
        // ADD — Mika gives Maya more
        (a, b) => ({
            text:
                `${_had(a, 'מאיה')}. מיקה נתנה לה עוד ${_balls(b)}. ` +
                `כמה כדורים יש למאיה עכשיו?`,
            initialMaya: a, initialMika: b, result: a + b,
        }),
        // ADD — Maya gives Mika more
        (a, b) => ({
            text:
                `${_had(a, 'מיקה')}. מאיה נתנה לה עוד ${_balls(b)}. ` +
                `כמה כדורים יש למיקה עכשיו?`,
            initialMaya: b, initialMika: a, result: a + b,
        }),
    ];

    const STATE = {
        problem: null,
        answering: true,
        successes: 0,
        batch: 0,         // successes since last reward
        lastSig: '',      // signature of last problem (avoid repeat)
    };

    const $maya     = document.getElementById('wp-basket-maya');
    const $mika     = document.getElementById('wp-basket-mika');
    const $question = document.getElementById('wp-question');
    const $answers  = document.getElementById('wp-answers');
    const $counter  = document.getElementById('wp-counter');
    const $mute     = document.getElementById('wp-mute');

    // -------------------------------------------------------------------
    //  Generate a fresh problem (random op, random operands ≤ 10)
    // -------------------------------------------------------------------
    function _genProblem() {
        for (let attempt = 0; attempt < 30; attempt++) {
            const op = Math.random() < 0.5 ? '-' : '+';
            let a, b, tmplIdx;
            if (op === '-') {
                a = 1 + Math.floor(Math.random() * MAX_NUM);     // 1..10
                b = 1 + Math.floor(Math.random() * a);           // 1..a
                tmplIdx = Math.floor(Math.random() * 2);         // 0 | 1
            } else {
                a = 1 + Math.floor(Math.random() * (MAX_NUM - 1));
                b = 1 + Math.floor(Math.random() * (MAX_NUM - a));
                tmplIdx = 2 + Math.floor(Math.random() * 2);     // 2 | 3
            }
            const sig = `${op}|${a}|${b}|${tmplIdx}`;
            if (sig === STATE.lastSig) continue;
            STATE.lastSig = sig;
            return TEMPLATES[tmplIdx](a, b);
        }
        // fallback (should never hit)
        return TEMPLATES[0](5, 2);
    }

    function _genWrongAnswer(correct) {
        const cands = [];
        for (const d of [-2, -1, 1, 2]) {
            const v = correct + d;
            if (v >= 0 && v <= MAX_NUM) cands.push(v);
        }
        return cands[Math.floor(Math.random() * cands.length)];
    }

    // -------------------------------------------------------------------
    //  Render baskets with given counts
    // -------------------------------------------------------------------
    function _setBaskets(mayaCount, mikaCount) {
        $maya.innerHTML = '';
        $mika.innerHTML = '';
        for (let i = 0; i < mayaCount; i++) _addBall($maya);
        for (let i = 0; i < mikaCount; i++) _addBall($mika);
    }

    function _addBall(basket) {
        const ball = document.createElement('div');
        ball.className = 'wp-ball';
        _attachDrag(ball);
        basket.appendChild(ball);
    }

    // -------------------------------------------------------------------
    //  Drag mechanics — pointer events, free 2-D drag, drop on basket
    // -------------------------------------------------------------------
    function _attachDrag(ball) {
        let dragging = false;
        let offX = 0, offY = 0;
        let originalParent = null;

        const onMove = (e) => {
            if (!dragging) return;
            ball.style.left = (e.clientX - offX) + 'px';
            ball.style.top  = (e.clientY - offY) + 'px';
            ball.style.display = 'none';
            const tgt = document.elementFromPoint(e.clientX, e.clientY);
            ball.style.display = '';
            const bk = tgt && tgt.closest('.wp-basket');
            document.querySelectorAll('.wp-basket').forEach(b =>
                b.classList.toggle('wp-drag-over', b === bk));
        };

        const onUp = (e) => {
            if (!dragging) return;
            dragging = false;
            document.removeEventListener('pointermove', onMove);
            document.removeEventListener('pointerup', onUp);
            document.removeEventListener('pointercancel', onUp);

            ball.style.display = 'none';
            const tgt = document.elementFromPoint(e.clientX, e.clientY);
            ball.style.display = '';
            const drop =
                (tgt && tgt.closest('.wp-basket')) || originalParent;

            ball.style.position = '';
            ball.style.left = '';
            ball.style.top = '';
            ball.style.pointerEvents = '';
            ball.classList.remove('wp-ball-drag');
            document.querySelectorAll('.wp-basket').forEach(b =>
                b.classList.remove('wp-drag-over'));

            drop.appendChild(ball);
            sfxPop();
        };

        ball.addEventListener('pointerdown', (e) => {
            initAudio();
            const rect = ball.getBoundingClientRect();
            offX = e.clientX - rect.left;
            offY = e.clientY - rect.top;
            originalParent = ball.parentElement;

            ball.classList.add('wp-ball-drag');
            ball.style.position = 'fixed';
            ball.style.left = rect.left + 'px';
            ball.style.top  = rect.top + 'px';
            ball.style.pointerEvents = 'none';
            document.body.appendChild(ball);

            dragging = true;
            ball.setPointerCapture && ball.setPointerCapture(e.pointerId);
            document.addEventListener('pointermove', onMove);
            document.addEventListener('pointerup', onUp);
            document.addEventListener('pointercancel', onUp);
            e.preventDefault();
        });
    }

    // -------------------------------------------------------------------
    //  Round flow
    // -------------------------------------------------------------------
    function _newRound() {
        STATE.problem = _genProblem();
        STATE.answering = true;

        $question.textContent = STATE.problem.text;
        _setBaskets(STATE.problem.initialMaya,
                    STATE.problem.initialMika);

        const correct = STATE.problem.result;
        const wrong   = _genWrongAnswer(correct);
        const order   = Math.random() < 0.5
            ? [correct, wrong] : [wrong, correct];

        $answers.innerHTML = '';
        order.forEach((num) => {
            const btn = document.createElement('button');
            btn.className = 'wp-ans';
            btn.textContent = num;
            btn.addEventListener('click', () => _onAnswer(num, btn));
            $answers.appendChild(btn);
        });
    }

    function _onAnswer(num, btn) {
        if (!STATE.answering) return;
        STATE.answering = false;
        initAudio();

        if (num === STATE.problem.result) {
            sfxCorrect();
            btn.classList.add('wp-correct');
            STATE.successes++;
            STATE.batch++;
            _renderCounter();
            flyingStar();
            showFeedback('כל הכבוד!', 'correct', 1200);

            if (STATE.batch >= REWARD_EVERY) {
                STATE.batch = 0;
                setTimeout(() => {
                    spawnConfetti(40);
                    PrizeManager.showRandom(() => {
                        _renderCounter();
                        _newRound();
                    });
                }, 1300);
            } else {
                setTimeout(_newRound, 1300);
            }
        } else {
            sfxWrong();
            btn.classList.add('wp-wrong');
            showFeedback('ננסה שוב!', 'wrong', 1000);
            setTimeout(() => {
                btn.classList.remove('wp-wrong');
                STATE.answering = true;
            }, 800);
        }
    }

    function _renderCounter() {
        $counter.textContent = `${STATE.batch}/${REWARD_EVERY}`;
    }

    // -------------------------------------------------------------------
    //  Mute toggle
    // -------------------------------------------------------------------
    $mute.addEventListener('click', () => {
        muted = !muted;
        $mute.innerHTML = muted ? '&#128263;' : '&#128264;';
    });

    // -------------------------------------------------------------------
    //  Boot
    // -------------------------------------------------------------------
    spawnClouds();
    _renderCounter();
    _newRound();
});
