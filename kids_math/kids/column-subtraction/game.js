// =========================================================================
//  Column Subtraction — step-by-step with automatic borrow animation
// =========================================================================
document.addEventListener('DOMContentLoaded', () => {

    let step = 'ones';
    let prob = null;
    let needTens = false;
    let pendingPrize = false;
    let showingResult = false;
    let lastProbA = -1, lastProbB = -1;

    GameEngine.init({

        title: '!חיסור<br>בטור',
        prizeMode: 'manual',

        levels: [
            { minA: 15, maxA: 30, minB: 10, maxB: 20,
              borrowMode: 'never'  },
            { minA: 20, maxA: 50, minB: 10, maxB: 30,
              borrowMode: 'never'  },
            { minA: 20, maxA: 50, minB: 10, maxB: 30,
              borrowMode: 'always' },
            { minA: 20, maxA: 70, minB: 10, maxB: 50,
              borrowMode: 'mixed'  },
        ],

        onNewRound(lv) {
            const field = document.getElementById('animal-field');
            field.classList.remove('happy');

            if (needTens) {
                needTens = false;
                step = 'tens';
                renderTensStep();
                return prob.tensDiff;
            }

            // --- New problem start ---

            // Show completed result for 3 seconds
            if (prob !== null && !showingResult &&
                !pendingPrize) {
                showingResult = true;
                GameEngine.state.answering = false;
                showCompletedResult();
                setTimeout(() => {
                    GameEngine.newRound();
                }, 3000);
                return -1;
            }

            if (showingResult) {
                showingResult = false;
            }
            if (pendingPrize) {
                pendingPrize = false;
            } else if (prob !== null) {
                if (PrizeManager.check(() => {
                    GameEngine.newRound();
                })) {
                    pendingPrize = true;
                    GameEngine.state.answering = false;
                    return -1;
                }
            }

            prob = generateProblem(lv);
            step = 'ones';
            needTens = true;
            renderOnesStep(field);
            return prob.onesDiff;
        },

        getButtonRange() {
            return { min: 0, max: 9 };
        },
    });

    // =================================================================
    //  Problem generation
    // =================================================================
    function generateProblem(lv) {
        let a, b;
        for (let i = 0; i < 200; i++) {
            a = lv.minA + Math.floor(
                Math.random()
                * (lv.maxA - lv.minA + 1));
            b = lv.minB + Math.floor(
                Math.random()
                * (lv.maxB - lv.minB + 1));
            if (b >= a) continue;
            const aO = a % 10, bO = b % 10;
            const needs = aO < bO;
            if (lv.borrowMode === 'never'
                && needs) continue;
            if (lv.borrowMode === 'always'
                && !needs) continue;
            if (a === lastProbA
                && b === lastProbB) continue;
            break;
        }
        lastProbA = a; lastProbB = b;
        const aOnes = a % 10, aTens = Math.floor(a / 10);
        const bOnes = b % 10, bTens = Math.floor(b / 10);
        const borrow = aOnes < bOnes ? 1 : 0;
        const adjAOnes = borrow ? aOnes + 10 : aOnes;
        const adjATens = aTens - borrow;
        const onesDiff = adjAOnes - bOnes;
        const tensDiff = adjATens - bTens;

        return {
            a, b, aOnes, aTens, bOnes, bTens,
            borrow, adjAOnes, adjATens,
            onesDiff, tensDiff,
        };
    }

    // =================================================================
    //  Render: ones step
    // =================================================================
    function renderOnesStep(field) {
        field.innerHTML = '';
        field.className = 'col-add-layout';

        field.innerHTML = `
            <div class="col-add">
                <div class="col-row col-carry-row">
                    <div class="col-op-space"></div>
                    <div class="col-carry-spacer"></div>
                    <div class="col-borrow-lbl"
                         id="borrow-label"></div>
                </div>
                <div class="col-row">
                    <div class="col-op-space"></div>
                    <div class="col-cell tens-bg"
                         id="a-tens">${prob.aTens}</div>
                    <div class="col-cell ones-bg active"
                         id="a-ones">${prob.aOnes}</div>
                </div>
                <div class="col-row">
                    <div class="col-op">&minus;</div>
                    <div class="col-cell tens-bg"
                         >${prob.bTens}</div>
                    <div class="col-cell ones-bg active"
                         >${prob.bOnes}</div>
                </div>
                <div class="col-line"></div>
                <div class="col-row">
                    <div class="col-op-space"></div>
                    <div class="col-cell tens-bg"
                         id="res-tens">?</div>
                    <div class="col-cell ones-bg active"
                         id="res-ones">?</div>
                </div>
                <div class="col-row col-labels">
                    <div class="col-op-space"></div>
                    <div class="col-lbl tens-color">
                        עשרות</div>
                    <div class="col-lbl ones-color">
                        אחדות</div>
                </div>
            </div>`;

        if (prob.borrow) {
            // --- Borrow animation ---
            GameEngine.state.answering = false;

            // Hide question & buttons during animation
            setTimeout(() => {
                document.getElementById('question-text')
                    .innerHTML = '';
                document.getElementById('number-grid')
                    .style.opacity = '0';
            }, 0);

            // Flash warning
            setTimeout(() => {
                showFeedback(
                    `!${prob.aOnes} קטן מ-${prob.bOnes}`,
                    'borrow-info', 1200);
            }, 600);

            // Tens shrinks
            setTimeout(() => {
                const el = document.getElementById('a-tens');
                el.textContent = prob.adjATens;
                el.classList.add('borrow-shrink');
            }, 2000);

            // "+10" pops above ones
            setTimeout(() => {
                const lbl =
                    document.getElementById('borrow-label');
                lbl.textContent = '+10';
                lbl.classList.add('show');
            }, 2200);

            // Ones grows
            setTimeout(() => {
                const el =
                    document.getElementById('a-ones');
                el.textContent = prob.adjAOnes;
                el.classList.add('borrow-grow');
                sfxPop();
            }, 2700);

            // Show question & buttons
            setTimeout(() => {
                document.getElementById('question-text')
                    .innerHTML =
                    `<span class="ones-color">`
                    + `${prob.adjAOnes} &minus; `
                    + `${prob.bOnes}</span> = <b>?</b>`;
                document.getElementById('number-grid')
                    .style.opacity = '1';
                GameEngine.state.answering = true;
            }, 3400);

        } else {
            document.getElementById('question-text')
                .innerHTML =
                `<span class="ones-color">`
                + `${prob.aOnes} &minus; `
                + `${prob.bOnes}</span> = <b>?</b>`;
        }
    }

    // =================================================================
    //  Render: tens step
    // =================================================================
    function renderTensStep() {
        const resOnes = document.getElementById('res-ones');
        resOnes.textContent = prob.onesDiff;
        resOnes.classList.remove('active');
        resOnes.classList.add('filled');

        document.querySelectorAll('.ones-bg.active')
            .forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.tens-bg')
            .forEach(el => el.classList.add('active'));

        // Hide borrow label
        const lbl = document.getElementById('borrow-label');
        if (lbl) lbl.style.opacity = '0';

        document.getElementById('question-text').innerHTML =
            `<span class="tens-color">`
            + `${prob.adjATens} &minus; ${prob.bTens}`
            + `</span> = <b>?</b>`;
    }

    // =================================================================
    //  Show completed result (3-second recap)
    // =================================================================
    function showCompletedResult() {
        const resTens = document.getElementById('res-tens');
        if (resTens) {
            resTens.textContent = prob.tensDiff;
            resTens.classList.remove('active');
            resTens.classList.add('filled', 'result-final');
        }
        const resOnes = document.getElementById('res-ones');
        if (resOnes) {
            resOnes.classList.add('result-final');
        }
        document.querySelectorAll('.tens-bg.active')
            .forEach(el => el.classList.remove('active'));

        const result = prob.a - prob.b;
        document.getElementById('question-text').innerHTML =
            `<span class="result-eq">`
            + `${prob.a} &minus; ${prob.b} = `
            + `<span class="result-ans">${result}`
            + `</span></span>`;
        document.getElementById('number-grid').innerHTML =
            '';
    }

    // Prizes use shared/prizes.js (random type + interval)
});
