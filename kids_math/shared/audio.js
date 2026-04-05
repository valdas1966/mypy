// =========================================================================
//  Sound Engine (Web Audio API — no external files needed)
// =========================================================================
let audioCtx = null;
let muted = false;

function initAudio() {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (audioCtx.state === 'suspended') audioCtx.resume();
}

function playTone(freq, dur, type = 'sine', vol = 0.25, delay = 0) {
    if (muted || !audioCtx) return;
    const t = audioCtx.currentTime + delay;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, t);
    gain.gain.setValueAtTime(vol, t);
    gain.gain.exponentialRampToValueAtTime(0.001, t + dur);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start(t);
    osc.stop(t + dur);
}

function sfxPop() {
    playTone(600, 0.1, 'sine', 0.15);
    playTone(900, 0.08, 'sine', 0.1, 0.03);
}

function sfxCorrect() {
    playTone(523, 0.15, 'triangle', 0.2);
    playTone(659, 0.15, 'triangle', 0.2, 0.12);
    playTone(784, 0.25, 'triangle', 0.25, 0.24);
}

function sfxWrong() {
    playTone(330, 0.2, 'square', 0.1);
    playTone(262, 0.3, 'square', 0.08, 0.15);
}

function sfxLevelUp() {
    playTone(523, 0.12, 'triangle', 0.2);
    playTone(659, 0.12, 'triangle', 0.2, 0.1);
    playTone(784, 0.12, 'triangle', 0.2, 0.2);
    playTone(1047, 0.4, 'triangle', 0.3, 0.3);
    playTone(784, 0.15, 'sine', 0.15, 0.5);
    playTone(1047, 0.5, 'sine', 0.25, 0.6);
}

function sfxCandy() {
    playTone(880, 0.1, 'sine', 0.2);
    playTone(1100, 0.1, 'sine', 0.2, 0.08);
    playTone(1320, 0.2, 'sine', 0.25, 0.16);
}

function sfxChampion() {
    const notes = [523, 659, 784, 1047, 784, 1047, 1319, 1047, 1319, 1568];
    notes.forEach((n, i) => {
        playTone(n, 0.2, 'triangle', 0.2, i * 0.12);
        playTone(n * 0.5, 0.25, 'sine', 0.1, i * 0.12);
    });
}

function sfxStar() {
    playTone(1200, 0.08, 'sine', 0.15);
    playTone(1600, 0.12, 'sine', 0.12, 0.06);
}
