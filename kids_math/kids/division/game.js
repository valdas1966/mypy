// =========================================================================
//  Division Game — dividend between 0 and 30, exact division
// =========================================================================
document.addEventListener('DOMContentLoaded', () => {

    let prevQ = '';

    GameEngine.init({

        title: '&#247; Divide!',

        levels: [
            // L1: ÷2 — quotients 1–5
            { divisors: [2], maxDividend: 10,
              btnMax: 5 },
            // L2: ÷2, ÷3 — quotients 1–7
            { divisors: [2, 3], maxDividend: 21,
              btnMax: 10 },
            // L3: ÷2–5 — quotients 1–10
            { divisors: [2, 3, 4, 5], maxDividend: 30,
              btnMax: 15 },
            // L4: ÷2–10 — quotients 1–15
            { divisors: [2, 3, 4, 5, 6, 7, 8, 9, 10],
              maxDividend: 30, btnMax: 15 },
        ],

        onNewRound(lv) {
            // Build all valid (quotient, divisor) pairs
            const pairs = [];
            for (const d of lv.divisors) {
                const maxQ = Math.floor(
                    lv.maxDividend / d
                );
                for (let q = 1; q <= maxQ; q++) {
                    pairs.push({
                        divisor: d,
                        quotient: q,
                        dividend: q * d,
                    });
                }
            }

            // Group by quotient for uniform answer
            const byQ = {};
            for (const p of pairs) {
                if (!byQ[p.quotient]) {
                    byQ[p.quotient] = [];
                }
                byQ[p.quotient].push(p);
            }
            const quotients = Object.keys(byQ)
                .map(Number);

            // Pick random quotient, then random pair
            let pair;
            let tries = 0;
            do {
                const q = quotients[
                    Math.floor(
                        Math.random() *
                        quotients.length
                    )
                ];
                const opts = byQ[q];
                pair = opts[
                    Math.floor(
                        Math.random() * opts.length
                    )
                ];
                tries++;
            } while (
                pair.dividend + '/' + pair.divisor ===
                    prevQ &&
                tries < 10
            );

            prevQ = pair.dividend + '/' + pair.divisor;

            document.getElementById('question-text')
                .innerHTML =
                    pair.dividend + ' &divide; ' +
                    pair.divisor + ' = <b>?</b>';

            return pair.quotient;
        },

        getButtonRange(lv) {
            return { min: 0, max: lv.btnMax };
        },
    });
});
