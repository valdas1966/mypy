// =========================================================================
//  Triple Addition — add three groups of animals
// =========================================================================
document.addEventListener('DOMContentLoaded', () => {

    GameEngine.init({

        title: 'Add Three<br>Groups!',

        levels: [
            { minNum: 1, maxNum: 2, maxSum: 6  },
            { minNum: 1, maxNum: 3, maxSum: 9  },
            { minNum: 0, maxNum: 4, maxSum: 12 },
            { minNum: 0, maxNum: 6, maxSum: 18 },
        ],

        onNewRound(lv) {
            // Pick three numbers within range
            let a, b, c;
            do {
                a = randRange(lv.minNum, lv.maxNum);
                b = randRange(lv.minNum, lv.maxNum);
                c = randRange(lv.minNum, lv.maxNum);
            } while (a + b + c > lv.maxSum ||
                     a + b + c < 1);
            const sum = a + b + c;

            // Pick a different animal type per group
            const idxs = pickDistinct(3, animalFns.length);

            // Build layout
            const field = document.getElementById('animal-field');
            field.innerHTML = '';
            field.className = 'addition-layout';

            const counts = [a, b, c];
            let totalDelay = 0;

            for (let g = 0; g < 3; g++) {
                // Group
                const group = document.createElement('div');
                group.className = 'addition-group';
                for (let i = 0; i < counts[g]; i++) {
                    const w = document.createElement('div');
                    w.innerHTML = animalFns[idxs[g]]();
                    const svg = w.firstElementChild;
                    svg.style.animationDelay =
                        (totalDelay * 0.1) + 's';
                    group.appendChild(svg);
                    setTimeout(() => sfxPop(),
                        totalDelay * 120);
                    totalDelay++;
                }
                // Show "0" text for empty groups
                if (counts[g] === 0) {
                    const empty = document.createElement('div');
                    empty.className = 'triple-empty';
                    empty.textContent = '0';
                    group.appendChild(empty);
                }
                field.appendChild(group);

                // Plus sign (after first and second groups)
                if (g < 2) {
                    const plus = document.createElement('div');
                    plus.className = 'addition-operator';
                    plus.textContent = '+';
                    field.appendChild(plus);
                }
            }

            // Question
            document.getElementById('question-text').innerHTML =
                `${a} + ${b} + ${c} = <b>?</b>`;

            return sum;
        },

        getButtonRange(lv) {
            return {
                min: Math.max(0, lv.minNum * 3 - 1),
                max: Math.min(lv.maxSum + 2, 20),
            };
        },
    });

    function randRange(min, max) {
        return min + Math.floor(
            Math.random() * (max - min + 1)
        );
    }

    function pickDistinct(n, max) {
        const arr = [];
        while (arr.length < n) {
            const v = Math.floor(Math.random() * max);
            if (!arr.includes(v)) arr.push(v);
        }
        return arr;
    }
});
