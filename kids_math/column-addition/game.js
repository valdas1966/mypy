// =========================================================================
//  Column Addition — step-by-step vertical addition (ones then tens)
// =========================================================================
document.addEventListener('DOMContentLoaded', () => {

    let step = 'ones';
    let prob = null;
    let needTens = false;
    let completed = 0;
    let pendingPrize = false;
    let showingResult = false;

    const ICE_CREAM_EVERY = 3;

    GameEngine.init({

        title: '!חיבור<br>בטור',

        levels: [
            { minNum: 11, maxNum: 29, carryMode: 'never'  },
            { minNum: 10, maxNum: 49, carryMode: 'never'  },
            { minNum: 10, maxNum: 49, carryMode: 'always' },
            { minNum: 10, maxNum: 60, carryMode: 'mixed'  },
        ],

        onNewRound(lv) {
            const field = document.getElementById('animal-field');
            field.classList.remove('happy');

            if (needTens) {
                needTens = false;
                step = 'tens';
                renderTensStep();
                return prob.tensSum;
            }

            // --- New problem start ---

            // Show completed result for 2 seconds
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

            // Returning from result display
            if (showingResult) {
                showingResult = false;
            }
            if (pendingPrize) {
                pendingPrize = false;
            } else if (prob !== null) {
                // Previous full problem completed
                completed++;
                if (completed % ICE_CREAM_EVERY === 0) {
                    pendingPrize = true;
                    GameEngine.state.answering = false;
                    showIceCreamPrize(() => {
                        GameEngine.newRound();
                    });
                    return -1;
                }
            }

            prob = generateProblem(lv);
            step = 'ones';
            needTens = true;
            renderOnesStep(field);
            return prob.onesSum;
        },

        getButtonRange(lv) {
            if (step === 'ones') {
                const hasCarry = lv.carryMode !== 'never';
                return { min: 0, max: hasCarry ? 18 : 9 };
            }
            return { min: 0, max: 9 };
        },
    });

    // =================================================================
    //  Problem generation
    // =================================================================
    function generateProblem(lv) {
        let a, b;
        for (let i = 0; i < 200; i++) {
            a = lv.minNum + Math.floor(
                Math.random() * (lv.maxNum - lv.minNum + 1)
            );
            b = lv.minNum + Math.floor(
                Math.random() * (lv.maxNum - lv.minNum + 1)
            );
            if (a + b > 99) continue;
            const aO = a % 10, bO = b % 10;
            const hasCarry = aO + bO >= 10;
            if (lv.carryMode === 'never' && hasCarry) continue;
            if (lv.carryMode === 'always' && !hasCarry) continue;
            break;
        }
        const aOnes = a % 10, aTens = Math.floor(a / 10);
        const bOnes = b % 10, bTens = Math.floor(b / 10);
        const onesSum = aOnes + bOnes;
        const carry = onesSum >= 10 ? 1 : 0;
        const onesDigit = onesSum % 10;
        const tensSum = aTens + bTens + carry;

        return {
            a, b, aOnes, aTens, bOnes, bTens,
            onesSum, tensSum, carry, onesDigit,
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
                    <div class="col-carry" id="col-carry"></div>
                    <div class="col-carry-spacer"></div>
                </div>
                <div class="col-row">
                    <div class="col-op-space"></div>
                    <div class="col-cell tens-bg">${prob.aTens}</div>
                    <div class="col-cell ones-bg active">${prob.aOnes}</div>
                </div>
                <div class="col-row">
                    <div class="col-op">+</div>
                    <div class="col-cell tens-bg">${prob.bTens}</div>
                    <div class="col-cell ones-bg active">${prob.bOnes}</div>
                </div>
                <div class="col-line"></div>
                <div class="col-row">
                    <div class="col-op-space"></div>
                    <div class="col-cell tens-bg" id="res-tens">?</div>
                    <div class="col-cell ones-bg active" id="res-ones">?</div>
                </div>
                <div class="col-row col-labels">
                    <div class="col-op-space"></div>
                    <div class="col-lbl tens-color">עשרות</div>
                    <div class="col-lbl ones-color">אחדות</div>
                </div>
            </div>`;

        document.getElementById('question-text').innerHTML =
            `<span class="ones-color">${prob.aOnes} + ${prob.bOnes}</span> = <b>?</b>`;
    }

    // =================================================================
    //  Render: tens step (update existing DOM)
    // =================================================================
    function renderTensStep() {
        const resOnes = document.getElementById('res-ones');
        resOnes.textContent = prob.onesDigit;
        resOnes.classList.remove('active');
        resOnes.classList.add('filled');

        document.querySelectorAll('.ones-bg.active').forEach(el =>
            el.classList.remove('active')
        );
        document.querySelectorAll('.tens-bg').forEach(el =>
            el.classList.add('active')
        );

        if (prob.carry) {
            const carryEl = document.getElementById('col-carry');
            carryEl.textContent = '1';
            carryEl.classList.add('show');
        }

        const parts = prob.carry
            ? `1 + ${prob.aTens} + ${prob.bTens}`
            : `${prob.aTens} + ${prob.bTens}`;
        document.getElementById('question-text').innerHTML =
            `<span class="tens-color">${parts}</span> = <b>?</b>`;
    }

    // =================================================================
    //  Show completed result (2-second recap)
    // =================================================================
    function showCompletedResult() {
        // Fill in tens digit
        const resTens = document.getElementById('res-tens');
        if (resTens) {
            resTens.textContent = prob.tensSum;
            resTens.classList.remove('active');
            resTens.classList.add('filled', 'result-final');
        }
        // Mark ones as final too
        const resOnes = document.getElementById('res-ones');
        if (resOnes) {
            resOnes.classList.add('result-final');
        }
        // Deactivate all column highlights
        document.querySelectorAll('.tens-bg.active').forEach(
            el => el.classList.remove('active')
        );
        // Hide carry
        const carry = document.getElementById('col-carry');
        if (carry) carry.style.opacity = '0';

        // Show full equation prominently
        const result = prob.a + prob.b;
        document.getElementById('question-text').innerHTML =
            `<span class="result-eq">${prob.a} + ${prob.b} = `
            + `<span class="result-ans">${result}</span></span>`;

        // Hide answer buttons during recap
        document.getElementById('number-grid').innerHTML = '';
    }

    // Ice cream prize uses shared/ice-cream.js
});
