// =========================================================================
//  Ice Cream Prize — shared mini-game for column math games
// =========================================================================

const IC_FLAVORS = [
    { name: 'וניל',     color: '#FFF5CC', hi: '#FFFDE8',
      dark: '#E8D5A3' },
    { name: 'שוקולד',   color: '#6B3E26', hi: '#8B5E46',
      dark: '#4A2B1A', light: true },
    { name: 'תות',      color: '#FF6B9D', hi: '#FF9DBF',
      dark: '#E0507A' },
    { name: 'מנטה',     color: '#7DCEA0', hi: '#A9DFBF',
      dark: '#52BE80' },
    { name: 'אוכמניות', color: '#7B68EE', hi: '#9D8FFF',
      dark: '#5A48CC', light: true },
    { name: 'מנגו',     color: '#FFB347', hi: '#FFD08A',
      dark: '#E09030' },
    { name: 'קרמל',     color: '#DEB887', hi: '#F0DFC0',
      dark: '#B8945A' },
    { name: 'פיסטוק',   color: '#93C572', hi: '#B8E09A',
      dark: '#6FA34E' },
    { name: 'לימון',    color: '#FFF44F', hi: '#FFFF8A',
      dark: '#E0D530' },
];

const IC_TOPPINGS = [
    { name: 'דובדבן',   emoji: '🍒' },
    { name: 'סוכריות',  emoji: '🌈' },
    { name: 'ופל',      emoji: '🥢' },
    { name: 'קצפת',     emoji: '☁️' },
    { name: 'ממתק',     emoji: '🍬' },
];

const IC_LAYOUTS = {
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
};

// =================================================================
//  Main prize function
// =================================================================
function showIceCreamPrize(onDone) {
    const picked = [];
    const numScoops = 2 + Math.floor(Math.random() * 3);
    const layout = IC_LAYOUTS[numScoops];
    const shuffled = [...IC_FLAVORS]
        .sort(() => Math.random() - 0.5)
        .slice(0, 6);
    const offerTopping = Math.random() < 0.5;

    const overlay = document.createElement('div');
    overlay.className = 'ic-overlay';

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
                </defs>
                <polygon points="58,192 142,192 100,340"
                         fill="#C47A18"/>
                <polygon points="62,192 138,192 100,335"
                         fill="#E8A735"/>
                <line x1="70" y1="202" x2="106" y2="318"
                      stroke="#C07818" stroke-width="1.5"
                      opacity="0.4"/>
                <line x1="82" y1="196" x2="112" y2="300"
                      stroke="#C07818" stroke-width="1.5"
                      opacity="0.4"/>
                <line x1="96" y1="194" x2="118" y2="278"
                      stroke="#C07818" stroke-width="1.5"
                      opacity="0.4"/>
                <line x1="112" y1="196" x2="124" y2="258"
                      stroke="#C07818" stroke-width="1.5"
                      opacity="0.4"/>
                <line x1="130" y1="202" x2="94" y2="318"
                      stroke="#C07818" stroke-width="1.5"
                      opacity="0.4"/>
                <line x1="118" y1="196" x2="88" y2="300"
                      stroke="#C07818" stroke-width="1.5"
                      opacity="0.4"/>
                <line x1="104" y1="194" x2="82" y2="278"
                      stroke="#C07818" stroke-width="1.5"
                      opacity="0.4"/>
                <line x1="88" y1="196" x2="76" y2="258"
                      stroke="#C07818" stroke-width="1.5"
                      opacity="0.4"/>
                <ellipse cx="100" cy="192" rx="42" ry="7"
                         fill="#E8A735"
                         stroke="#C47A18"
                         stroke-width="1"/>
                <g id="ic-scoops"
                   filter="url(#ic-shadow)"></g>
                <g id="ic-toppings"></g>
            </svg>
        </div>
        <div class="ic-prompt">
            ${numScoops} בחרו ${numScoops} טעמים
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

    function onAllDone() {
        btnsEl.querySelectorAll('.ic-flav-btn')
            .forEach(b => b.disabled = true);
        if (offerTopping) {
            setTimeout(() => showTops(), 600);
        } else {
            celebrate();
        }
    }

    function showTops() {
        promptEl.textContent = '!הוסיפו תוספת';
        countEl.textContent = '';
        const tops = [...IC_TOPPINGS]
            .sort(() => Math.random() - 0.5)
            .slice(0, 3);

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
                setTimeout(() => celebrate(), 500);
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
function icAddScoop(parent, flav, pos) {
    const g = document.createElementNS(
        'http://www.w3.org/2000/svg', 'g');
    g.classList.add('ic-scoop-anim');
    const { cx, cy, r } = pos;
    const drip = Math.random() < 0.4;
    const dripX = cx + (Math.random() - 0.5) * r * 0.8;
    g.innerHTML = `
        ${drip ? `<ellipse cx="${dripX}" cy="${cy + r + 6}"
            rx="5" ry="9" fill="${flav.color}"
            opacity="0.8"/>` : ''}
        <circle cx="${cx}" cy="${cy}" r="${r}"
                fill="${flav.color}"
                stroke="${flav.dark}"
                stroke-width="1.5"/>
        <circle cx="${cx - r * 0.28}"
                cy="${cy - r * 0.28}"
                r="${r * 0.25}"
                fill="${flav.hi}" opacity="0.55"/>
        <circle cx="${cx - r * 0.1}"
                cy="${cy - r * 0.42}"
                r="${r * 0.12}"
                fill="${flav.hi}" opacity="0.35"/>
    `;
    parent.appendChild(g);
}

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
                    Math.floor(Math.random() * layout.length)];
                const sx = s.cx + (Math.random() - 0.5)
                           * s.r * 1.4;
                const sy = s.cy + (Math.random() - 0.5)
                           * s.r * 1.2;
                const colors = ['#FF1744', '#FFD600',
                    '#00E676', '#2979FF', '#FF4081',
                    '#FF9100'];
                const sc = colors[
                    Math.floor(Math.random() * colors.length)];
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
                <ellipse cx="${hx - 6}" cy="${hy - hr - 10}"
                         rx="${hr * 0.4}" ry="${hr * 0.25}"
                         fill="white"/>
                <ellipse cx="${hx + 8}" cy="${hy - hr - 8}"
                         rx="${hr * 0.35}" ry="${hr * 0.22}"
                         fill="white"/>
                <ellipse cx="${hx}" cy="${hy - hr - 14}"
                         rx="${hr * 0.25}" ry="${hr * 0.18}"
                         fill="#FAFAFA"/>`;
            break;
        case 'ממתק':
            const cx1 = hx - 12, cy1 = hy - hr - 8;
            g.innerHTML = `
                <circle cx="${cx1}" cy="${cy1}"
                        r="8" fill="#FF4081"/>
                <circle cx="${cx1 - 2}" cy="${cy1 - 2}"
                        r="2.5" fill="#FF80AB" opacity="0.6"/>
                <circle cx="${hx + 14}" cy="${hy - hr - 12}"
                        r="7" fill="#FFD600"/>
                <circle cx="${hx + 12}" cy="${hy - hr - 14}"
                        r="2" fill="#FFF176" opacity="0.6"/>
                <circle cx="${hx + 2}" cy="${hy - hr - 16}"
                        r="6" fill="#00E676"/>
                <circle cx="${hx}" cy="${hy - hr - 18}"
                        r="2" fill="#69F0AE" opacity="0.6"/>`;
            break;
    }
    parent.appendChild(g);
}
