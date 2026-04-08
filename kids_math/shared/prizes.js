// =========================================================================
//  Prize Manager — random interval, random prize type
// =========================================================================
const PrizeManager = {

    _counter: 0,
    _nextAt: 0,

    init() {
        this._counter = 0;
        this._rollNext();
    },

    _rollNext() {
        this._nextAt = 1 + Math.floor(Math.random() * 5);
    },

    // Increment counter. If threshold reached, show a random
    // prize and call onDone when finished. Returns true if
    // prize was triggered.
    check(onDone) {
        this._counter++;
        if (this._counter >= this._nextAt) {
            this._counter = 0;
            this._rollNext();
            this.showRandom(onDone);
            return true;
        }
        return false;
    },

    showRandom(onDone) {
        if (Math.random() < 0.5) {
            showIceCreamPrize(onDone);
        } else {
            showDressUpPrize(onDone);
        }
    },
};
