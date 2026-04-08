// =========================================================================
//  Addition Game — add two groups of animals (sum up to 10)
// =========================================================================
document.addEventListener('DOMContentLoaded', () => {

    let lastA = -1, lastB = -1;

    GameEngine.init({

        title: 'Add the<br>Animals!',

        levels: [
            { minNum: 1, maxNum: 2, maxSum: 4  },
            { minNum: 1, maxNum: 3, maxSum: 6  },
            { minNum: 1, maxNum: 4, maxSum: 8  },
            { minNum: 0, maxNum: 5, maxSum: 10 },
        ],

        // Render two groups of animals with + and return the sum
        onNewRound(lv) {
            let a, b;
            for (let t = 0; t < 20; t++) {
                a = lv.minNum + Math.floor(
                    Math.random()
                    * (lv.maxNum - lv.minNum + 1));
                const bMax = Math.min(
                    lv.maxNum, lv.maxSum - a);
                b = lv.minNum + Math.floor(
                    Math.random()
                    * Math.max(bMax - lv.minNum + 1, 1));
                if (a !== lastA || b !== lastB) break;
            }
            lastA = a; lastB = b;
            const sum = a + b;

            // Pick a different animal type for each group
            const idxA = Math.floor(Math.random() * animalFns.length);
            let idxB = Math.floor(Math.random() * (animalFns.length - 1));
            if (idxB >= idxA) idxB++;

            // Build layout
            const field = document.getElementById('animal-field');
            field.innerHTML = '';
            field.className = 'addition-layout';

            // Group A
            const groupA = document.createElement('div');
            groupA.className = 'addition-group';
            for (let i = 0; i < a; i++) {
                const w = document.createElement('div');
                w.innerHTML = animalFns[idxA]();
                const svg = w.firstElementChild;
                svg.style.animationDelay = (i * 0.1) + 's';
                groupA.appendChild(svg);
                setTimeout(() => sfxPop(), i * 120);
            }
            field.appendChild(groupA);

            // Plus sign
            const plus = document.createElement('div');
            plus.className = 'addition-operator';
            plus.textContent = '+';
            field.appendChild(plus);

            // Group B
            const groupB = document.createElement('div');
            groupB.className = 'addition-group';
            for (let i = 0; i < b; i++) {
                const w = document.createElement('div');
                w.innerHTML = animalFns[idxB]();
                const svg = w.firstElementChild;
                svg.style.animationDelay = ((a + i) * 0.1) + 's';
                groupB.appendChild(svg);
                setTimeout(() => sfxPop(), (a + i) * 120);
            }
            field.appendChild(groupB);

            // Question
            document.getElementById('question-text').innerHTML =
                `${a} + ${b} = <b>?</b>`;

            return sum;
        },

        // Show buttons covering plausible answers
        getButtonRange(lv) {
            return {
                min: Math.max(0, lv.minNum * 2 - 1),
                max: Math.min(lv.maxSum + 2, 12),
            };
        },
    });
});
