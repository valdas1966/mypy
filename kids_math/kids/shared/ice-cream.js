// =========================================================================
//  Ice Cream Prize — build your own ice cream with maximum randomness
// =========================================================================

const IC_FLAVORS = [
    { name: 'וניל',      color: '#FFF5CC', hi: '#FFFDE8',
      dark: '#E8D5A3' },
    { name: 'שוקולד',    color: '#6B3E26', hi: '#8B5E46',
      dark: '#4A2B1A', light: true },
    { name: 'תות',       color: '#FF6B9D', hi: '#FF9DBF',
      dark: '#E0507A' },
    { name: 'מנטה',      color: '#7DCEA0', hi: '#A9DFBF',
      dark: '#52BE80' },
    { name: 'אוכמניות',  color: '#7B68EE', hi: '#9D8FFF',
      dark: '#5A48CC', light: true },
    { name: 'מנגו',      color: '#FFB347', hi: '#FFD08A',
      dark: '#E09030' },
    { name: 'קרמל',      color: '#DEB887', hi: '#F0DFC0',
      dark: '#B8945A' },
    { name: 'פיסטוק',    color: '#93C572', hi: '#B8E09A',
      dark: '#6FA34E' },
    { name: 'לימון',     color: '#FFF44F', hi: '#FFFF8A',
      dark: '#E0D530' },
    { name: 'סוכר ורוד', color: '#FFB6D9', hi: '#FFD6EB',
      dark: '#E8889F' },
    { name: 'מסטיק',     color: '#4FC3F7', hi: '#81D4FA',
      dark: '#0288D1' },
    { name: 'עוגיות',    color: '#D7CCC8', hi: '#EFEBE9',
      dark: '#8D6E63' },
    { name: 'גלקסיה',    color: '#311B92', hi: '#7C4DFF',
      dark: '#1A0A5C', light: true },
    { name: 'קשת',       color: '#FF69B4', hi: '#FFD700',
      dark: '#9B59B6', rainbow: true },
];

const IC_TOPPINGS = [
    { name: 'דובדבן',   emoji: '🍒' },
    { name: 'סוכריות',  emoji: '🌈' },
    { name: 'ופל',      emoji: '🥢' },
    { name: 'קצפת',     emoji: '☁️' },
    { name: 'ממתק',     emoji: '🍬' },
    { name: 'כוכבים',   emoji: '⭐' },
    { name: 'לבבות',    emoji: '💕' },
    { name: 'שוקולד',   emoji: '🍫' },
];

const IC_LAYOUTS = {
    1: [
        { cx: 100, cy: 155, r: 46 },
    ],
    2: [
        { cx: 100, cy: 162, r: 42 },
        { cx: 100, cy: 100, r: 39 },
    ],
    3: [
        { cx: 76,  cy: 165, r: 38 },
        { cx: 124, cy: 165, r: 38 },
        { cx: 100, cy: 108, r: 36 },
    ],
    4: [
        { cx: 76,  cy: 168, r: 36 },
        { cx: 124, cy: 168, r: 36 },
        { cx: 80,  cy: 112, r: 34 },
        { cx: 120, cy: 112, r: 34 },
    ],
    5: [
        { cx: 72,  cy: 172, r: 34 },
        { cx: 128, cy: 172, r: 34 },
        { cx: 74,  cy: 118, r: 32 },
        { cx: 126, cy: 118, r: 32 },
        { cx: 100, cy: 70,  r: 30 },
    ],
};

// Cone styles: waffle, sugar, chocolate-dipped
const IC_CONES = [
    { type: 'waffle',    body: '#E8A735', rim: '#C47A18',
      lines: '#C07818' },
    { type: 'sugar',     body: '#F5DEB3', rim: '#D2B48C',
      lines: '#D2B48C' },
    { type: 'chocolate', body: '#E8A735', rim: '#4A2B1A',
      lines: '#C07818' },
];

// =================================================================
//  Main prize function
// =================================================================
function showIceCreamPrize(onDone) {
    const picked = [];
    const numScoops = 1 + Math.floor(Math.random() * 5);
    const layout = IC_LAYOUTS[numScoops];
    const numShow = 4 + Math.floor(Math.random() * 4);
    const shuffled = [...IC_FLAVORS]
        .sort(() => Math.random() - 0.5)
        .slice(0, Math.min(numShow, IC_FLAVORS.length));
    const toppingChance = 0.3 + Math.random() * 0.5;
    const offerTopping = Math.random() < toppingChance;
    const numToppingRounds = offerTopping
        ? (Math.random() < 0.25 ? 2 : 1) : 0;
    const addFace = Math.random() < 0.3;
    const cone = IC_CONES[
        Math.floor(Math.random() * IC_CONES.length)];

    const overlay = document.createElement('div');
    overlay.className = 'ic-overlay';

    // --- Cone SVG varies by type ---
    let coneSvg = _icCone(cone);

    overlay.innerHTML = `
        <div class="ic-title">!בנו גלידה</div>
        <div class="ic-cone-area">
            <svg class="ic-svg" viewBox="0 0 200 350">
                <defs>
                    <filter id="ic-shadow">
                        <feDropShadow dx="0" dy="3"
                            stdDeviation="3"
                            flood-opacity="0.2"/>
                    </filter>
                    <linearGradient id="ic-rainbow"
                        x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#FF69B4"/>
                        <stop offset="33%" stop-color="#FFD700"/>
                        <stop offset="66%" stop-color="#7DCEA0"/>
                        <stop offset="100%" stop-color="#9B59B6"/>
                    </linearGradient>
                </defs>
                ${coneSvg}
                <g id="ic-scoops"
                   filter="url(#ic-shadow)"></g>
                <g id="ic-face"></g>
                <g id="ic-toppings"></g>
            </svg>
        </div>
        <div class="ic-prompt">
            ${numScoops === 1
                ? 'בחרו טעם אחד'
                : `בחרו ${numScoops} טעמים`}
        </div>
        <div class="ic-flavors" id="ic-buttons">
            ${shuffled.map((f, i) => `
                <button class="ic-flav-btn"
                        data-idx="${i}"
                        style="background:
                            linear-gradient(135deg,
                                ${f.hi}, ${f.color});
                            border: 3px solid ${f.dark};
                            color: ${f.light
                                ? '#FFF' : '#333'}">
                    ${f.name}
                </button>
            `).join('')}
        </div>
        <div class="ic-count" id="ic-count">
            0 / ${numScoops}
        </div>
    `;

    document.body.appendChild(overlay);
    requestAnimationFrame(() => overlay.classList.add('show'));

    const scoopsG = overlay.querySelector('#ic-scoops');
    const faceG = overlay.querySelector('#ic-face');
    const toppingsG = overlay.querySelector('#ic-toppings');
    const countEl = overlay.querySelector('#ic-count');
    const promptEl = overlay.querySelector('.ic-prompt');
    const btnsEl = overlay.querySelector('#ic-buttons');

    btnsEl.querySelectorAll('.ic-flav-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            if (picked.length >= numScoops) return;
            const idx = parseInt(btn.dataset.idx);
            const flav = shuffled[idx];
            picked.push(flav);
            sfxPop();

            const pos = layout[picked.length - 1];
            icAddScoop(scoopsG, flav, pos);
            countEl.textContent =
                `${picked.length} / ${numScoops}`;

            if (picked.length === numScoops) {
                onAllDone();
            }
        });
    });

    let toppingRound = 0;

    function onAllDone() {
        btnsEl.querySelectorAll('.ic-flav-btn')
            .forEach(b => b.disabled = true);

        // Add cute face on top scoop
        if (addFace) {
            const top = layout[layout.length - 1];
            icAddFace(faceG, top);
        }

        if (numToppingRounds > 0) {
            setTimeout(() => showTops(), 600);
        } else {
            celebrate();
        }
    }

    function showTops() {
        toppingRound++;
        promptEl.textContent = toppingRound === 1
            ? '!הוסיפו תוספת' : '!עוד תוספת';
        countEl.textContent = '';
        const tops = [...IC_TOPPINGS]
            .sort(() => Math.random() - 0.5)
            .slice(0, 3 + Math.floor(Math.random() * 2));

        btnsEl.innerHTML = tops.map((t, i) => `
            <button class="ic-flav-btn ic-top-btn"
                    data-tidx="${i}">
                <span class="ic-top-emoji">
                    ${t.emoji}</span>
                ${t.name}
            </button>
        `).join('');

        btnsEl.querySelectorAll('.ic-top-btn')
            .forEach(btn => {
            btn.addEventListener('click', () => {
                const ti = parseInt(btn.dataset.tidx);
                sfxPop();
                icAddTopping(toppingsG, tops[ti], layout);
                btnsEl.querySelectorAll('.ic-top-btn')
                    .forEach(b => b.disabled = true);
                if (toppingRound < numToppingRounds) {
                    setTimeout(() => showTops(), 500);
                } else {
                    setTimeout(() => celebrate(), 500);
                }
            });
        });
    }

    function celebrate() {
        promptEl.textContent = '!יופי';
        countEl.textContent = '';
        btnsEl.innerHTML = '';
        sfxCorrect();
        spawnConfetti(50);
        setTimeout(() => {
            overlay.classList.remove('show');
            setTimeout(() => {
                overlay.remove();
                onDone();
            }, 500);
        }, 2000);
    }
}

// =================================================================
//  Cone rendering by type
// =================================================================
function _icCone(c) {
    let lines = '';
    const pairs = [
        [70,202,106,318], [82,196,112,300],
        [96,194,118,278], [112,196,124,258],
        [130,202,94,318],  [118,196,88,300],
        [104,194,82,278],  [88,196,76,258],
    ];
    pairs.forEach(([x1,y1,x2,y2]) => {
        lines += `<line x1="${x1}" y1="${y1}"
            x2="${x2}" y2="${y2}"
            stroke="${c.lines}" stroke-width="1.5"
            opacity="0.4"/>`;
    });
    let extra = '';
    if (c.type === 'chocolate') {
        extra = `<ellipse cx="100" cy="195" rx="44" ry="10"
            fill="#4A2B1A"/>
            <ellipse cx="90" cy="200" rx="6" ry="10"
                fill="#4A2B1A" opacity="0.7"/>
            <ellipse cx="115" cy="198" rx="5" ry="8"
                fill="#4A2B1A" opacity="0.7"/>`;
    }
    return `
        <polygon points="58,192 142,192 100,340"
                 fill="${c.body}"/>
        <polygon points="62,192 138,192 100,335"
                 fill="${c.type === 'sugar'
                     ? '#FFF8E1' : c.body}"/>
        ${lines}
        <ellipse cx="100" cy="192" rx="42" ry="7"
                 fill="${c.body}"
                 stroke="${c.rim}" stroke-width="1"/>
        ${extra}`;
}

// =================================================================
//  Scoop rendering
// =================================================================
function icAddScoop(parent, flav, pos) {
    const g = document.createElementNS(
        'http://www.w3.org/2000/svg', 'g');
    g.classList.add('ic-scoop-anim');
    const { cx, cy, r } = pos;
    const drip = Math.random() < 0.4;
    const dripX = cx + (Math.random() - 0.5) * r * 0.8;

    const fill = flav.rainbow
        ? 'url(#ic-rainbow)' : flav.color;
    const stroke = flav.rainbow
        ? flav.dark : flav.dark;

    // Random sparkle dots on scoop
    let sparkles = '';
    if (Math.random() < 0.35) {
        for (let i = 0; i < 5; i++) {
            const sx = cx + (Math.random() - 0.5) * r * 1.2;
            const sy = cy + (Math.random() - 0.5) * r * 1.0;
            sparkles += `<circle cx="${sx}" cy="${sy}"
                r="1.5" fill="white"
                opacity="${0.4 + Math.random() * 0.4}"/>`;
        }
    }

    // Random cookie bits for "cookies" flavor
    let bits = '';
    if (flav.name === 'עוגיות') {
        for (let i = 0; i < 6; i++) {
            const bx = cx + (Math.random() - 0.5) * r * 1.1;
            const by = cy + (Math.random() - 0.5) * r * 0.9;
            bits += `<rect x="${bx - 2}" y="${by - 1}"
                width="4" height="2.5" rx="1"
                fill="#5D4037" opacity="0.7"/>`;
        }
    }

    g.innerHTML = `
        ${drip ? `<ellipse cx="${dripX}" cy="${cy + r + 6}"
            rx="5" ry="9" fill="${flav.color}"
            opacity="0.8"/>` : ''}
        <circle cx="${cx}" cy="${cy}" r="${r}"
                fill="${fill}"
                stroke="${stroke}"
                stroke-width="1.5"/>
        <circle cx="${cx - r * 0.28}"
                cy="${cy - r * 0.28}"
                r="${r * 0.25}"
                fill="${flav.hi}" opacity="0.55"/>
        <circle cx="${cx - r * 0.1}"
                cy="${cy - r * 0.42}"
                r="${r * 0.12}"
                fill="${flav.hi}" opacity="0.35"/>
        ${sparkles}
        ${bits}
    `;
    parent.appendChild(g);
}

// =================================================================
//  Cute face on top scoop
// =================================================================
function icAddFace(parent, pos) {
    const g = document.createElementNS(
        'http://www.w3.org/2000/svg', 'g');
    g.classList.add('ic-scoop-anim');
    const { cx, cy } = pos;
    g.innerHTML = `
        <circle cx="${cx - 8}" cy="${cy - 3}" r="3"
            fill="#333"/>
        <circle cx="${cx + 8}" cy="${cy - 3}" r="3"
            fill="#333"/>
        <circle cx="${cx - 7}" cy="${cy - 4}" r="1.2"
            fill="white"/>
        <circle cx="${cx + 9}" cy="${cy - 4}" r="1.2"
            fill="white"/>
        <ellipse cx="${cx - 12}" cy="${cy + 4}" rx="5"
            ry="3" fill="#FFB6C1" opacity="0.4"/>
        <ellipse cx="${cx + 12}" cy="${cy + 4}" rx="5"
            ry="3" fill="#FFB6C1" opacity="0.4"/>
        <path d="M${cx - 5},${cy + 5}
            Q${cx},${cy + 11} ${cx + 5},${cy + 5}"
            stroke="#E91E63" stroke-width="1.5"
            fill="none" stroke-linecap="round"/>
    `;
    parent.appendChild(g);
}

// =================================================================
//  Topping rendering
// =================================================================
function icAddTopping(parent, top, layout) {
    const g = document.createElementNS(
        'http://www.w3.org/2000/svg', 'g');
    g.classList.add('ic-scoop-anim');
    const highest = layout.reduce((a, b) =>
        a.cy < b.cy ? a : b);
    const hx = highest.cx, hy = highest.cy,
          hr = highest.r;

    switch (top.name) {
        case 'דובדבן':
            g.innerHTML = `
                <circle cx="${hx}" cy="${hy - hr - 10}"
                        r="10" fill="#FF1744"/>
                <circle cx="${hx - 3}" cy="${hy - hr - 13}"
                        r="3" fill="#FF5252" opacity="0.6"/>
                <path d="M${hx},${hy - hr - 10}
                       Q${hx + 6},${hy - hr - 32}
                        ${hx + 14},${hy - hr - 36}"
                      stroke="#388E3C" stroke-width="2.5"
                      fill="none" stroke-linecap="round"/>
                <ellipse cx="${hx + 16}"
                         cy="${hy - hr - 38}"
                         rx="7" ry="4" fill="#4CAF50"
                         transform="rotate(-20 ${hx + 16}
                                    ${hy - hr - 38})"/>`;
            break;
        case 'סוכריות':
            let sp = '';
            for (let i = 0; i < 20; i++) {
                const s = layout[
                    Math.floor(Math.random()
                        * layout.length)];
                const sx = s.cx + (Math.random() - 0.5)
                           * s.r * 1.4;
                const sy = s.cy + (Math.random() - 0.5)
                           * s.r * 1.2;
                const colors = ['#FF1744', '#FFD600',
                    '#00E676', '#2979FF', '#FF4081',
                    '#FF9100'];
                const sc = colors[
                    Math.floor(Math.random()
                        * colors.length)];
                const angle = Math.random() * 180;
                sp += `<rect x="${sx - 3}" y="${sy - 1}"
                        width="6" height="2.5" rx="1"
                        fill="${sc}"
                        transform="rotate(${angle}
                            ${sx} ${sy})"/>`;
            }
            g.innerHTML = sp;
            break;
        case 'ופל':
            g.innerHTML = `
                <rect x="${hx + 5}" y="${hy - hr - 45}"
                      width="8" height="55" rx="2"
                      fill="#E8A735"
                      transform="rotate(15 ${hx + 9}
                                 ${hy - hr - 18})"/>
                <rect x="${hx + 6}" y="${hy - hr - 45}"
                      width="6" height="55" rx="2"
                      fill="#F0C060"
                      transform="rotate(15 ${hx + 9}
                                 ${hy - hr - 18})"
                      opacity="0.6"/>`;
            break;
        case 'קצפת':
            g.innerHTML = `
                <ellipse cx="${hx}" cy="${hy - hr - 4}"
                         rx="${hr * 0.7}" ry="${hr * 0.3}"
                         fill="white" stroke="#E0E0E0"
                         stroke-width="0.8"/>
                <ellipse cx="${hx - 6}"
                         cy="${hy - hr - 10}"
                         rx="${hr * 0.4}" ry="${hr * 0.25}"
                         fill="white"/>
                <ellipse cx="${hx + 8}"
                         cy="${hy - hr - 8}"
                         rx="${hr * 0.35}"
                         ry="${hr * 0.22}"
                         fill="white"/>
                <ellipse cx="${hx}"
                         cy="${hy - hr - 14}"
                         rx="${hr * 0.25}"
                         ry="${hr * 0.18}"
                         fill="#FAFAFA"/>`;
            break;
        case 'ממתק':
            const cx1 = hx - 12, cy1 = hy - hr - 8;
            g.innerHTML = `
                <circle cx="${cx1}" cy="${cy1}"
                        r="8" fill="#FF4081"/>
                <circle cx="${cx1 - 2}" cy="${cy1 - 2}"
                        r="2.5" fill="#FF80AB"
                        opacity="0.6"/>
                <circle cx="${hx + 14}"
                        cy="${hy - hr - 12}"
                        r="7" fill="#FFD600"/>
                <circle cx="${hx + 12}"
                        cy="${hy - hr - 14}"
                        r="2" fill="#FFF176"
                        opacity="0.6"/>
                <circle cx="${hx + 2}"
                        cy="${hy - hr - 16}"
                        r="6" fill="#00E676"/>
                <circle cx="${hx}"
                        cy="${hy - hr - 18}"
                        r="2" fill="#69F0AE"
                        opacity="0.6"/>`;
            break;
        case 'כוכבים': {
            let stars = '';
            for (let i = 0; i < 8; i++) {
                const s = layout[
                    Math.floor(Math.random()
                        * layout.length)];
                const sx = s.cx + (Math.random() - 0.5)
                           * s.r * 1.3;
                const sy = s.cy + (Math.random() - 0.5)
                           * s.r * 1.1;
                const sr = 2 + Math.random() * 3;
                stars += `<polygon
                    points="${_icStar(sx, sy, sr)}"
                    fill="#FFD700"
                    opacity="${0.6 + Math.random() * 0.4}"/>`;
            }
            g.innerHTML = stars;
            break;
        }
        case 'לבבות': {
            let hearts = '';
            for (let i = 0; i < 7; i++) {
                const s = layout[
                    Math.floor(Math.random()
                        * layout.length)];
                const hxx = s.cx + (Math.random() - 0.5)
                            * s.r * 1.3;
                const hyy = s.cy + (Math.random() - 0.5)
                            * s.r * 1.0;
                const hs = 3 + Math.random() * 3;
                const hc = ['#FF1744', '#FF4081',
                    '#E91E63', '#FF6090'][
                    Math.floor(Math.random() * 4)];
                hearts += `<path d="M${hxx},${hyy + hs * 0.4}
                    C${hxx},${hyy - hs * 0.2}
                     ${hxx + hs},${hyy - hs * 0.5}
                     ${hxx + hs},${hyy + hs * 0.1}
                    C${hxx + hs},${hyy + hs * 0.6}
                     ${hxx},${hyy + hs}
                     ${hxx},${hyy + hs}
                    C${hxx},${hyy + hs}
                     ${hxx - hs},${hyy + hs * 0.6}
                     ${hxx - hs},${hyy + hs * 0.1}
                    C${hxx - hs},${hyy - hs * 0.5}
                     ${hxx},${hyy - hs * 0.2}
                     ${hxx},${hyy + hs * 0.4}Z"
                    fill="${hc}"
                    opacity="${0.6 + Math.random() * 0.4}"/>`;
            }
            g.innerHTML = hearts;
            break;
        }
        case 'שוקולד':
            g.innerHTML = `
                <path d="M${hx - hr * 0.6},${hy - hr * 0.1}
                    Q${hx - hr * 0.3},${hy + hr * 0.3}
                     ${hx},${hy - hr * 0.05}
                    Q${hx + hr * 0.3},${hy + hr * 0.4}
                     ${hx + hr * 0.6},${hy - hr * 0.1}"
                    stroke="#4A2B1A" stroke-width="4"
                    fill="none" stroke-linecap="round"
                    opacity="0.8"/>
                <path d="M${hx - hr * 0.4},${hy + hr * 0.4}
                    Q${hx},${hy + hr * 0.7}
                     ${hx + hr * 0.4},${hy + hr * 0.35}"
                    stroke="#4A2B1A" stroke-width="3"
                    fill="none" stroke-linecap="round"
                    opacity="0.6"/>`;
            break;
    }
    parent.appendChild(g);
}

// =================================================================
//  Star polygon helper
// =================================================================
function _icStar(cx, cy, r) {
    const pts = [];
    for (let i = 0; i < 10; i++) {
        const a = Math.PI / 2 + i * Math.PI / 5;
        const rr = i % 2 === 0 ? r : r * 0.45;
        pts.push(`${cx + rr * Math.cos(a)},`
            + `${cy - rr * Math.sin(a)}`);
    }
    return pts.join(' ');
}
