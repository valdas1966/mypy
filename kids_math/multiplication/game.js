// =========================================================================
//  Multiplication Game — product between 0 and 30
// =========================================================================
document.addEventListener('DOMContentLoaded', () => {

    let prevQ = '';

    GameEngine.init({

        title: '&#10006; Multiply!',

        levels: [
            // L1: ×2, ×3 — products up to 15
            { factors: [2, 3], maxOther: 5,
              btnMax: 15 },
            // L2: ×2–5 — products up to 25
            { factors: [2, 3, 4, 5], maxOther: 5,
              btnMax: 25 },
            // L3: ×2–5 — products up to 30
            { factors: [2, 3, 4, 5], maxOther: 6,
              btnMax: 30 },
            // L4: ×2–10 — products up to 30
            { factors: [2, 3, 4, 5, 6, 7, 8, 9, 10],
              maxOther: 10, btnMax: 30 },
        ],

        onNewRound(lv) {
            // Build all valid (factor, other) pairs
            const pairs = [];
            for (const f of lv.factors) {
                for (let o = 1; o <= lv.maxOther; o++) {
                    if (f * o <= 30) {
                        pairs.push({
                            a: f, b: o,
                            product: f * o,
                        });
                    }
                }
            }

            // Group by product for uniform answer dist
            const byP = {};
            for (const p of pairs) {
                if (!byP[p.product]) byP[p.product] = [];
                byP[p.product].push(p);
            }
            const products = Object.keys(byP)
                .map(Number);

            // Pick random product, then random pair
            let pair;
            let tries = 0;
            do {
                const prod = products[
                    Math.floor(
                        Math.random() * products.length
                    )
                ];
                const opts = byP[prod];
                pair = opts[
                    Math.floor(
                        Math.random() * opts.length
                    )
                ];
                tries++;
            } while (
                pair.a + 'x' + pair.b === prevQ &&
                tries < 10
            );

            // Randomly swap operand order
            const swap = Math.random() < 0.5;
            const x = swap ? pair.b : pair.a;
            const y = swap ? pair.a : pair.b;
            prevQ = pair.a + 'x' + pair.b;

            document.getElementById('question-text')
                .innerHTML =
                    x + ' &times; ' + y +
                    ' = <b>?</b>';

            return pair.product;
        },

        getButtonRange(lv) {
            return { min: 0, max: lv.btnMax };
        },
    });
});
