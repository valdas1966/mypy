// =========================================================================
//  Visual Effects — confetti, flying stars, feedback text, clouds
// =========================================================================

function showFeedback(text, cls, dur = 1000) {
    const fb = document.getElementById('feedback');
    fb.innerHTML = `<div class="feedback-text ${cls}">${text}</div>`;
    setTimeout(() => fb.innerHTML = '', dur);
}

function spawnConfetti(count = 40) {
    const colors = [
        '#FF6F00', '#FF1744', '#D500F9',
        '#2979FF', '#00E676', '#FFD600', '#FF4081'
    ];
    for (let i = 0; i < count; i++) {
        const el = document.createElement('div');
        el.className = 'confetti-piece';
        el.style.background =
            colors[Math.floor(Math.random() * colors.length)];
        el.style.left = Math.random() * 100 + 'vw';
        el.style.top = '-20px';
        el.style.width = (6 + Math.random() * 8) + 'px';
        el.style.height = (6 + Math.random() * 8) + 'px';
        el.style.borderRadius = Math.random() > 0.5 ? '50%' : '2px';
        el.style.animationDuration = (1.5 + Math.random() * 2) + 's';
        el.style.animationDelay = Math.random() * 0.5 + 's';
        document.body.appendChild(el);
        setTimeout(() => el.remove(), 4000);
    }
}

function flyingStar() {
    const el = document.createElement('div');
    el.className = 'star-fly';
    el.textContent = '\u2B50';
    el.style.left = '50%';
    el.style.top = '50%';
    el.style.setProperty('--tx', '-40vw');
    el.style.setProperty('--ty', '-45vh');
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 1000);
    sfxStar();
}

function spawnClouds() {
    document.querySelectorAll('.cloud').forEach(c => c.remove());
    for (let i = 0; i < 4; i++) {
        const cloud = document.createElement('div');
        cloud.className = 'cloud';
        cloud.innerHTML = `<svg width="120" height="50" viewBox="0 0 120 50">
            <ellipse cx="60" cy="35" rx="50" ry="15"
                     fill="rgba(255,255,255,0.8)"/>
            <ellipse cx="40" cy="28" rx="25" ry="18"
                     fill="rgba(255,255,255,0.8)"/>
            <ellipse cx="75" cy="25" rx="30" ry="20"
                     fill="rgba(255,255,255,0.8)"/>
            <ellipse cx="55" cy="20" rx="20" ry="15"
                     fill="rgba(255,255,255,0.9)"/>
        </svg>`;
        cloud.style.top = (5 + Math.random() * 35) + '%';
        cloud.style.animationDuration = (20 + Math.random() * 30) + 's';
        cloud.style.animationDelay = (-Math.random() * 30) + 's';
        cloud.style.transform =
            `scale(${0.5 + Math.random() * 0.8})`;
        document.body.appendChild(cloud);
    }
}

// Helper: populate a container with all 4 animal SVGs
function populateAnimals(containerId) {
    const el = document.getElementById(containerId);
    if (!el) return;
    el.innerHTML = '';
    animalFns.forEach(fn => {
        const wrap = document.createElement('div');
        wrap.innerHTML = fn();
        el.appendChild(wrap.firstElementChild);
    });
}
