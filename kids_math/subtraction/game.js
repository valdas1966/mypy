// =========================================================================
//  Subtraction Game — take away animals and count what's left
// =========================================================================
document.addEventListener('DOMContentLoaded', () => {

    let lastTotal = -1, lastSub = -1;

    GameEngine.init({

        title: 'Subtract the<br>Animals!',

        levels: [
            { minTotal: 2, maxTotal: 3, minSub: 1, maxSub: 2 },
            { minTotal: 3, maxTotal: 5, minSub: 1, maxSub: 3 },
            { minTotal: 4, maxTotal: 7, minSub: 1, maxSub: 5 },
            { minTotal: 5, maxTotal: 10, minSub: 1, maxSub: 7 },
        ],

        // Show animals, then some "walk away" (fade + red X)
        onNewRound(lv) {
            let total, sub;
            for (let t = 0; t < 20; t++) {
                total = lv.minTotal + Math.floor(
                    Math.random()
                    * (lv.maxTotal - lv.minTotal + 1));
                const maxS = Math.min(lv.maxSub, total);
                sub = lv.minSub + Math.floor(
                    Math.random()
                    * Math.max(maxS - lv.minSub + 1, 1));
                if (total !== lastTotal
                    || sub !== lastSub) break;
            }
            lastTotal = total; lastSub = sub;
            const result = total - sub;

            // Pick one animal type
            const animalIdx = Math.floor(
                Math.random() * animalFns.length
            );

            // Build layout
            const field = document.getElementById('animal-field');
            field.innerHTML = '';
            field.className = 'animal-field';

            // Create all animals wrapped in containers
            const wrappers = [];
            for (let i = 0; i < total; i++) {
                const wrapper = document.createElement('div');
                wrapper.className = 'sub-animal';
                wrapper.innerHTML = animalFns[animalIdx]();
                const svg = wrapper.firstElementChild;
                svg.style.animationDelay = (i * 0.1) + 's';
                field.appendChild(wrapper);
                wrappers.push(wrapper);
                setTimeout(() => sfxPop(), i * 120);
            }

            // After animals appear, mark some as "leaving"
            const indices = [...Array(total).keys()];
            for (let i = indices.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [indices[i], indices[j]] = [indices[j], indices[i]];
            }
            const leavingIndices = indices.slice(0, sub);

            const appearDelay = total * 120 + 500;
            setTimeout(() => {
                leavingIndices.forEach((idx, i) => {
                    setTimeout(() => {
                        wrappers[idx].classList.add('leaving');
                    }, i * 180);
                });
            }, appearDelay);

            // Question
            document.getElementById('question-text').innerHTML =
                `${total} &minus; ${sub} = <b>?</b>`;

            return result;
        },

        // Show buttons from 0 to max possible remaining
        getButtonRange(lv) {
            return {
                min: 0,
                max: Math.min(lv.maxTotal, 10),
            };
        },
    });
});
