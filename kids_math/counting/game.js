// =========================================================================
//  Counting Game — count the animals on screen
// =========================================================================
document.addEventListener('DOMContentLoaded', () => {

    GameEngine.init({

        title: 'Count the<br>Animals!',

        levels: [
            { min: 1, max: 3 },
            { min: 1, max: 5 },
            { min: 2, max: 7 },
            { min: 3, max: 10 },
        ],

        // Render animals and return the correct count
        onNewRound(lv) {
            const count =
                lv.min + Math.floor(Math.random() * (lv.max - lv.min + 1));
            const field = document.getElementById('animal-field');
            field.innerHTML = '';
            field.classList.remove('happy');
            for (let i = 0; i < count; i++) {
                const fn =
                    animalFns[Math.floor(Math.random() * animalFns.length)];
                const wrap = document.createElement('div');
                wrap.innerHTML = fn();
                field.appendChild(wrap.firstElementChild);
                setTimeout(() => sfxPop(), i * 120);
            }
            document.getElementById('question-text').textContent =
                'How many animals?';
            return count;
        },

        // Show buttons from 0 to max+2 (capped at 10)
        getButtonRange(lv) {
            return { min: 0, max: Math.min(lv.max + 2, 10) };
        },
    });
});
