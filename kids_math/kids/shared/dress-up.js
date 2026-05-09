// =========================================================================
//  Dress-Up Prize — princess outfit builder mini-game
// =========================================================================

const DU_SKINS = [
    '#FFE0BD', '#FFCD94', '#F5C68E', '#E8B68F', '#D4A373'
];

const DU_HAIRS = [
    { name: 'בלונדינית', color: '#FFD700', hi: '#FFF176' },
    { name: 'חומה',      color: '#8B4513', hi: '#A0522D' },
    { name: 'שחורה',     color: '#2C1810', hi: '#4A3728' },
    { name: 'אדומה',     color: '#CC3300', hi: '#E85D3A' },
    { name: 'ורודה',     color: '#FF69B4', hi: '#FFB6D9' },
    { name: 'סגולה',     color: '#9B59B6', hi: '#BB8FCE' },
];

const DU_DRESSES = [
    { name: 'ורוד',  main: '#FF69B4', accent: '#FF1493',
      sparkle: '#FFB6D9' },
    { name: 'סגול',  main: '#9B59B6', accent: '#7D3C98',
      sparkle: '#D7BDE2' },
    { name: 'תכלת',  main: '#5DADE2', accent: '#2E86C1',
      sparkle: '#AED6F1' },
    { name: 'ירוק',  main: '#58D68D', accent: '#27AE60',
      sparkle: '#ABEBC6' },
    { name: 'אדום',  main: '#E74C3C', accent: '#C0392B',
      sparkle: '#F5B7B1' },
    { name: 'זהב',   main: '#F4D03F', accent: '#D4AC0D',
      sparkle: '#F9E79F' },
    { name: 'קשת',   main: '#FF69B4', accent: '#9B59B6',
      sparkle: '#FFD700', rainbow: true },
    { name: 'לבן',   main: '#FFFFFF', accent: '#E0E0E0',
      sparkle: '#F5F5F5' },
];

const DU_CROWNS = [
    { name: 'כתר זהב',      color: '#FFD700',
      gems: '#FF1744' },
    { name: 'כתר כסף',      color: '#C0C0C0',
      gems: '#2196F3' },
    { name: 'עטרת פרחים',   color: '#FF69B4',
      gems: '#4CAF50', floral: true },
    { name: 'פפיון',        color: '#FF4081',
      gems: '#E91E63', bow: true },
    { name: 'כתר יהלומים',  color: '#E1BEE7',
      gems: '#CE93D8' },
];

const DU_ACCESSORIES = [
    { name: 'שרביט',  emoji: '✨', type: 'wand' },
    { name: 'כנפיים', emoji: '🦋', type: 'wings' },
    { name: 'שרשרת',  emoji: '💎', type: 'necklace' },
    { name: 'תיק',    emoji: '👛', type: 'purse' },
    { name: 'פרח',    emoji: '🌸', type: 'flower' },
    { name: 'לב',     emoji: '💖', type: 'heart' },
    { name: 'משקפיים',emoji: '🕶️', type: 'glasses' },
    { name: 'צמיד',   emoji: '💍', type: 'bracelet' },
];

// =================================================================
//  Main prize function
// =================================================================
function showDressUpPrize(onDone) {
    const skin = DU_SKINS[
        Math.floor(Math.random() * DU_SKINS.length)];
    const hair = DU_HAIRS[
        Math.floor(Math.random() * DU_HAIRS.length)];

    const dressOpts = _duShuffle([...DU_DRESSES]).slice(0, 5);
    const crownOpts = _duShuffle([...DU_CROWNS]).slice(0, 4);
    const accOpts   = _duShuffle([...DU_ACCESSORIES]).slice(0,4);
    const hasAcc    = Math.random() < 0.65;

    const steps = ['dress', 'crown'];
    if (hasAcc) steps.push('accessory');
    let curStep = 0;

    // --- Build overlay ---
    const overlay = document.createElement('div');
    overlay.className = 'ic-overlay';
    overlay.innerHTML = `
        <div class="ic-title">!הלבישו את הנסיכה</div>
        <div class="ic-cone-area">
            <svg class="ic-svg" viewBox="0 0 200 350">
                <defs>
                    <linearGradient id="du-rainbow"
                        x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#FF69B4"/>
                        <stop offset="25%" stop-color="#FFD700"/>
                        <stop offset="50%" stop-color="#7DCEA0"/>
                        <stop offset="75%" stop-color="#5DADE2"/>
                        <stop offset="100%" stop-color="#9B59B6"/>
                    </linearGradient>
                    <filter id="du-shadow">
                        <feDropShadow dx="0" dy="2"
                            stdDeviation="2"
                            flood-opacity="0.15"/>
                    </filter>
                </defs>

                <!-- Hair back -->
                <ellipse cx="100" cy="95" rx="52" ry="65"
                         fill="${hair.color}"/>
                <ellipse cx="58" cy="140" rx="18" ry="48"
                         fill="${hair.color}"/>
                <ellipse cx="142" cy="140" rx="18" ry="48"
                         fill="${hair.color}"/>

                <!-- Body / legs (behind dress) -->
                <g id="du-body-base">
                    <rect x="85" y="125" width="30" height="35"
                          rx="6" fill="${skin}"/>
                    <line x1="90" y1="160" x2="82" y2="232"
                          stroke="${skin}" stroke-width="14"
                          stroke-linecap="round"/>
                    <line x1="110" y1="160" x2="118" y2="232"
                          stroke="${skin}" stroke-width="14"
                          stroke-linecap="round"/>
                </g>

                <!-- Dress layer -->
                <g id="du-dress" filter="url(#du-shadow)"></g>

                <!-- Arms -->
                <line x1="84" y1="132" x2="50" y2="178"
                      stroke="${skin}" stroke-width="11"
                      stroke-linecap="round"/>
                <line x1="116" y1="132" x2="150" y2="178"
                      stroke="${skin}" stroke-width="11"
                      stroke-linecap="round"/>
                <!-- Hands -->
                <circle cx="48" cy="180" r="7" fill="${skin}"/>
                <circle cx="152" cy="180" r="7" fill="${skin}"/>

                <!-- Shoes -->
                <ellipse cx="80" cy="237" rx="13" ry="6"
                         fill="#333"/>
                <ellipse cx="120" cy="237" rx="13" ry="6"
                         fill="#333"/>

                <!-- Head -->
                <circle cx="100" cy="80" r="42" fill="${skin}"/>

                <!-- Hair front / bangs -->
                <path d="M58,68 Q72,28 100,25 Q128,28 142,68
                         Q140,50 128,42 Q118,34 100,32
                         Q82,34 72,42 Q60,50 58,68"
                      fill="${hair.color}"/>
                <!-- Shine on hair -->
                <path d="M78,38 Q90,30 100,29"
                      stroke="${hair.hi}"
                      stroke-width="3" fill="none"
                      opacity="0.5"
                      stroke-linecap="round"/>

                <!-- Face -->
                <ellipse cx="84" cy="78" rx="6.5" ry="7.5"
                         fill="white"/>
                <ellipse cx="116" cy="78" rx="6.5" ry="7.5"
                         fill="white"/>
                <circle cx="85" cy="80" r="4.5" fill="#333"/>
                <circle cx="117" cy="80" r="4.5" fill="#333"/>
                <circle cx="86.5" cy="78" r="2" fill="white"/>
                <circle cx="118.5" cy="78" r="2"
                        fill="white"/>
                <!-- Eyelashes -->
                <line x1="78" y1="73" x2="80" y2="70"
                      stroke="#333" stroke-width="1.2"/>
                <line x1="90" y1="73" x2="88" y2="70"
                      stroke="#333" stroke-width="1.2"/>
                <line x1="110" y1="73" x2="112" y2="70"
                      stroke="#333" stroke-width="1.2"/>
                <line x1="122" y1="73" x2="120" y2="70"
                      stroke="#333" stroke-width="1.2"/>
                <!-- Blush -->
                <ellipse cx="80" cy="93" rx="10" ry="5"
                         fill="#FFB6C1" opacity="0.35"/>
                <ellipse cx="120" cy="93" rx="10" ry="5"
                         fill="#FFB6C1" opacity="0.35"/>
                <!-- Smile -->
                <path d="M91,97 Q100,107 109,97"
                      stroke="#E91E63" stroke-width="2.2"
                      fill="none" stroke-linecap="round"/>

                <!-- Crown layer (above head) -->
                <g id="du-crown"></g>
                <!-- Wings layer (behind body, drawn last
                     for simplicity) -->
                <g id="du-wings"></g>
                <!-- Accessory layer -->
                <g id="du-accessory"></g>
            </svg>
        </div>
        <div class="ic-prompt" id="du-prompt"></div>
        <div class="ic-flavors" id="du-buttons"></div>
        <div class="ic-count" id="du-count"></div>
    `;

    document.body.appendChild(overlay);
    requestAnimationFrame(() => overlay.classList.add('show'));

    setTimeout(() => _duShowStep(0), 300);

    // =============================================================
    function _duShowStep(idx) {
        curStep = idx;
        const btns   = overlay.querySelector('#du-buttons');
        const prompt = overlay.querySelector('#du-prompt');
        const count  = overlay.querySelector('#du-count');
        count.textContent = `${idx + 1} / ${steps.length}`;

        if (steps[idx] === 'dress') {
            prompt.textContent = '!בחרו שמלה';
            btns.innerHTML = dressOpts.map((d, i) => `
                <button class="ic-flav-btn" data-idx="${i}"
                    style="background:linear-gradient(135deg,
                        ${d.sparkle},${d.main});
                        border:3px solid ${d.accent};
                        color:${_duDark(d.main)
                            ? '#FFF' : '#333'}">
                    ${d.name}
                </button>`).join('');
            _duBind(btns, i => {
                _duRenderDress(dressOpts[i]);
                _duNext();
            });

        } else if (steps[idx] === 'crown') {
            prompt.textContent = '!בחרו כתר';
            btns.innerHTML = crownOpts.map((c, i) => `
                <button class="ic-flav-btn" data-idx="${i}"
                    style="background:linear-gradient(135deg,
                        ${c.gems},${c.color});
                        border:3px solid ${c.color};
                        color:#FFF">
                    ${c.name}
                </button>`).join('');
            _duBind(btns, i => {
                _duRenderCrown(crownOpts[i]);
                _duNext();
            });

        } else if (steps[idx] === 'accessory') {
            prompt.textContent = '!בחרו אביזר';
            btns.innerHTML = accOpts.map((a, i) => `
                <button class="ic-flav-btn ic-top-btn"
                        data-idx="${i}">
                    <span class="ic-top-emoji">${a.emoji}
                    </span> ${a.name}
                </button>`).join('');
            _duBind(btns, i => {
                _duRenderAcc(accOpts[i]);
                _duNext();
            });
        }
    }

    function _duBind(btns, cb) {
        btns.querySelectorAll('.ic-flav-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const i = parseInt(btn.dataset.idx);
                sfxPop();
                cb(i);
            });
        });
    }

    function _duNext() {
        if (curStep + 1 < steps.length) {
            setTimeout(() => _duShowStep(curStep + 1), 500);
        } else {
            _duCelebrate();
        }
    }

    // =============================================================
    //  Render dress on character
    // =============================================================
    function _duRenderDress(d) {
        const g = overlay.querySelector('#du-dress');
        const fill = d.rainbow
            ? 'url(#du-rainbow)' : d.main;
        // Sparkle dots
        let dots = '';
        if (Math.random() < 0.6) {
            for (let i = 0; i < 8; i++) {
                const dx = 72 + Math.random() * 56;
                const dy = 135 + Math.random() * 80;
                dots += `<circle cx="${dx}" cy="${dy}"
                    r="1.8" fill="${d.sparkle}"
                    opacity="${0.4 + Math.random() * 0.4}"/>`;
            }
        }
        g.innerHTML = `
            <g class="ic-scoop-anim">
                <path d="M83,125 L62,225 L138,225 L117,125 Z"
                      fill="${fill}"/>
                <path d="M83,125 L62,225 L100,225 L100,125 Z"
                      fill="${d.accent}" opacity="0.12"/>
                <ellipse cx="100" cy="225" rx="40" ry="6"
                         fill="${d.accent}" opacity="0.25"/>
                <circle cx="100" cy="130" r="4"
                        fill="${d.sparkle}"/>
                ${dots}
            </g>`;
    }

    // =============================================================
    //  Render crown / headpiece
    // =============================================================
    function _duRenderCrown(c) {
        const g = overlay.querySelector('#du-crown');
        if (c.floral) {
            const pts = [
                [70,44],[82,36],[100,32],[118,36],[130,44]
            ];
            const cols = ['#FF69B4','#FF4081','#FFD700',
                '#E91E63','#FF6F00'];
            let f = '';
            pts.forEach(([x, y], i) => {
                f += `<circle cx="${x}" cy="${y}" r="6.5"
                        fill="${cols[i]}"
                        class="ic-scoop-anim"/>
                      <circle cx="${x}" cy="${y}" r="2.5"
                        fill="#FFD700"
                        class="ic-scoop-anim"/>`;
            });
            g.innerHTML = f + `
                <path d="M66,50 Q100,24 134,50"
                      fill="none" stroke="#4CAF50"
                      stroke-width="3"
                      class="ic-scoop-anim"/>`;
        } else if (c.bow) {
            g.innerHTML = `<g class="ic-scoop-anim">
                <ellipse cx="86" cy="40" rx="16" ry="11"
                    fill="${c.color}"
                    transform="rotate(-15 86 40)"/>
                <ellipse cx="114" cy="40" rx="16" ry="11"
                    fill="${c.color}"
                    transform="rotate(15 114 40)"/>
                <circle cx="100" cy="40" r="5.5"
                    fill="${c.gems}"/>
            </g>`;
        } else {
            g.innerHTML = `<g class="ic-scoop-anim">
                <polygon points="70,50 74,28 84,42
                    92,22 100,38 108,22 116,42
                    126,28 130,50"
                    fill="${c.color}"
                    stroke="${c.color}"
                    stroke-width="1"/>
                <circle cx="92" cy="36" r="3.2"
                    fill="${c.gems}"/>
                <circle cx="100" cy="28" r="3.8"
                    fill="${c.gems}"/>
                <circle cx="108" cy="36" r="3.2"
                    fill="${c.gems}"/>
                <rect x="70" y="47" width="60" height="6"
                    rx="2" fill="${c.color}"/>
            </g>`;
        }
    }

    // =============================================================
    //  Render accessory
    // =============================================================
    function _duRenderAcc(a) {
        const g = overlay.querySelector('#du-accessory');
        const svg = {
            wand: `
                <line x1="156" y1="175" x2="172" y2="102"
                    stroke="#FFD700" stroke-width="4"
                    stroke-linecap="round"/>
                <polygon points="172,102 165,84 172,72 179,84"
                    fill="#FFD700"/>
                <circle cx="172" cy="84" r="6"
                    fill="#FFF" opacity="0.6"/>
                <circle cx="172" cy="72" r="3"
                    fill="#FFD700"/>`,
            wings: `
                <g opacity="0.65">
                <ellipse cx="46" cy="148" rx="32" ry="22"
                    fill="#E1BEE7" stroke="#CE93D8"
                    stroke-width="1"/>
                <ellipse cx="46" cy="130" rx="22" ry="16"
                    fill="#F3E5F5" stroke="#CE93D8"
                    stroke-width="1"/>
                <ellipse cx="154" cy="148" rx="32" ry="22"
                    fill="#E1BEE7" stroke="#CE93D8"
                    stroke-width="1"/>
                <ellipse cx="154" cy="130" rx="22" ry="16"
                    fill="#F3E5F5" stroke="#CE93D8"
                    stroke-width="1"/>
                </g>`,
            necklace: `
                <path d="M84,118 Q100,142 116,118"
                    fill="none" stroke="#FFD700"
                    stroke-width="2.5"/>
                <circle cx="100" cy="139" r="7"
                    fill="#FF1744"/>
                <circle cx="100" cy="139" r="3.5"
                    fill="#FF5252" opacity="0.6"/>`,
            purse: `
                <rect x="148" y="173" width="24" height="20"
                    rx="5" fill="#FF4081"/>
                <path d="M152,173 Q160,162 168,173"
                    fill="none" stroke="#FF4081"
                    stroke-width="2.5"/>
                <circle cx="160" cy="182" r="3.5"
                    fill="#FFD700"/>`,
            flower: `
                <circle cx="156" cy="158" r="9"
                    fill="#FF69B4"/>
                <circle cx="156" cy="158" r="4"
                    fill="#FFD700"/>
                <circle cx="148" cy="153" r="5.5"
                    fill="#FF69B4" opacity="0.7"/>
                <circle cx="164" cy="153" r="5.5"
                    fill="#FF69B4" opacity="0.7"/>
                <circle cx="148" cy="163" r="5.5"
                    fill="#FF69B4" opacity="0.7"/>
                <circle cx="164" cy="163" r="5.5"
                    fill="#FF69B4" opacity="0.7"/>
                <line x1="156" y1="167" x2="156" y2="192"
                    stroke="#4CAF50" stroke-width="2.5"/>
                <ellipse cx="151" cy="185" rx="6" ry="3"
                    fill="#4CAF50"
                    transform="rotate(-30 151 185)"/>`,
            heart: `
                <path d="M150,163
                    C150,155 160,150 160,158
                    C160,150 170,155 170,163
                    C170,173 160,180 160,180
                    C160,180 150,173 150,163Z"
                    fill="#FF1744"/>`,
            glasses: `
                <circle cx="82" cy="78" r="14"
                    fill="none" stroke="#333"
                    stroke-width="2.5"/>
                <circle cx="118" cy="78" r="14"
                    fill="none" stroke="#333"
                    stroke-width="2.5"/>
                <line x1="96" y1="78" x2="104" y2="78"
                    stroke="#333" stroke-width="2"/>
                <line x1="68" y1="78" x2="58" y2="75"
                    stroke="#333" stroke-width="2"/>
                <line x1="132" y1="78" x2="142" y2="75"
                    stroke="#333" stroke-width="2"/>
                <circle cx="82" cy="78" r="12"
                    fill="#9C27B0" opacity="0.15"/>
                <circle cx="118" cy="78" r="12"
                    fill="#9C27B0" opacity="0.15"/>`,
            bracelet: `
                <ellipse cx="48" cy="178" rx="10" ry="6"
                    fill="none" stroke="#FFD700"
                    stroke-width="3"/>
                <circle cx="44" cy="174" r="2.5"
                    fill="#FF1744"/>
                <circle cx="52" cy="174" r="2.5"
                    fill="#2196F3"/>
                <circle cx="48" cy="182" r="2.5"
                    fill="#4CAF50"/>`,
        };
        g.innerHTML = `<g class="ic-scoop-anim">
            ${svg[a.type] || ''}</g>`;
    }

    // =============================================================
    //  Celebration
    // =============================================================
    function _duCelebrate() {
        const prompt = overlay.querySelector('#du-prompt');
        const btns   = overlay.querySelector('#du-buttons');
        const count  = overlay.querySelector('#du-count');
        prompt.textContent = '!יופי';
        count.textContent = '';
        btns.innerHTML = '';
        sfxCorrect();
        spawnConfetti(60);
        setTimeout(() => {
            overlay.classList.remove('show');
            setTimeout(() => {
                overlay.remove();
                onDone();
            }, 500);
        }, 2500);
    }
}

// =================================================================
//  Helpers
// =================================================================
function _duShuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
}

function _duDark(hex) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return (r * 0.299 + g * 0.587 + b * 0.114) < 150;
}
