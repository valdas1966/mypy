// =========================================================================
//  Princess Palace — decorate a royal palace with drag and drop.
//
//  Every 5 user changes (add / move / remove / flip) triggers a math
//  gate. The user picks a difficulty before the game; each gate question
//  uses one of four operations (+, -, x, /) with the answer in the
//  level's result range. Correct answer => +3 stars. 3 stars = 1 candy.
//  5 candies = Queen of the Palace.
//
//  Content reveals gradually based on lifetime total changes
//  (persisted). New categories and items unlock as the player keeps
//  decorating — they stay in the palace instead of being pulled into
//  side mini-games.
//
//  Palette categories: princesses, magic, decor, pets, royals,
//  furniture. Each princess drop triggers a signature magic effect.
// =========================================================================

const PrincessPalaceGame = {

    STORAGE_KEY: 'princess-palace-state-v2',
    OLD_STORAGE_KEY: 'princess-palace-state-v1',
    CHANGES_PER_MATH: 5,
    STARS_PER_MATH: 3,
    STARS_PER_CANDY: 3,
    CANDIES_TO_WIN: 5,

    // --- Difficulty levels (result range + optional op subset) ---
    // `ops` restricts which operations this level can use; when
    // absent, all four ops are in play.
    LEVEL_RANGES: {
        0: { min: 0,  max: 10, label: 'Ultra Easy',
             ops: ['+'] },
        1: { min: 0,  max: 10, label: 'Easy'   },
        2: { min: 10, max: 20, label: 'Medium' },
        3: { min: 20, max: 30, label: 'Hard'   },
    },

    OPS: ['+', '-', 'x', '/'],
    OP_DISPLAY: {
        '+': '+',
        '-': '\u2212',
        'x': '\u00D7',
        '/': '\u00F7',
    },

    // =================================================================
    //  Palette catalog — ~40 items across 6 tabs, each with `unlockAt`
    //  (lifetime total changes required to make the item appear).
    // =================================================================
    CATALOG: {
        princesses: [
            { id: 'elsa',       label: 'Elsa',
              emoji: '\uD83D\uDC78',
              c1: '#B3E5FC', c2: '#4FC3F7',
              border: '#0288D1',
              magic: 'snow', halo: true,
              unlockAt: 0 },
            { id: 'anna',       label: 'Anna',
              emoji: '\uD83D\uDC78',
              c1: '#FFCDD2', c2: '#E57373',
              border: '#C62828',
              magic: 'petals', halo: true,
              unlockAt: 0 },
            { id: 'belle',      label: 'Belle',
              emoji: '\uD83D\uDC78',
              c1: '#FFECB3', c2: '#FFD54F',
              border: '#F57F17',
              magic: 'golden', halo: true,
              unlockAt: 0 },
            { id: 'cinderella', label: 'Cinderella',
              emoji: '\uD83D\uDC78',
              c1: '#E1F5FE', c2: '#81D4FA',
              border: '#0277BD',
              magic: 'silver', halo: true,
              unlockAt: 4 },
            { id: 'rapunzel',   label: 'Rapunzel',
              emoji: '\uD83D\uDC78',
              c1: '#F3E5F5', c2: '#BA68C8',
              border: '#8E24AA',
              magic: 'blossom', halo: true,
              unlockAt: 8 },
            { id: 'ariel',      label: 'Ariel',
              emoji: '\uD83E\uDDDC\u200D\u2640\uFE0F',
              c1: '#B2DFDB', c2: '#4DB6AC',
              border: '#00695C',
              magic: 'bubbles', halo: true,
              unlockAt: 13 },
            { id: 'moana',      label: 'Moana',
              emoji: '\uD83D\uDC78',
              c1: '#C8E6C9', c2: '#81C784',
              border: '#2E7D32',
              magic: 'waves', halo: true,
              unlockAt: 13 },
        ],
        magic: [
            { id: 'star',      label: 'Star',
              emoji: '\u2B50',
              c1: '#FFF9C4', c2: '#FFD600',
              border: '#F57F17',
              unlockAt: 2 },
            { id: 'heart',     label: 'Heart',
              emoji: '\uD83D\uDC96',
              c1: '#FFCDD2', c2: '#F06292',
              border: '#C2185B',
              unlockAt: 6 },
            { id: 'sparkle',   label: 'Sparkle',
              emoji: '\u2728',
              c1: '#FFF9C4', c2: '#FFD700',
              border: '#F57F17',
              unlockAt: 10 },
            { id: 'rainbow',   label: 'Rainbow',
              emoji: '\uD83C\uDF08',
              c1: '#F8BBD0', c2: '#CE93D8',
              border: '#7B1FA2',
              size: 'big',
              unlockAt: 20 },
            { id: 'cloud',     label: 'Cloud',
              emoji: '\u2601\uFE0F',
              c1: '#ECEFF1', c2: '#B0BEC5',
              border: '#546E7A',
              unlockAt: 20 },
            { id: 'moon',      label: 'Moon',
              emoji: '\uD83C\uDF19',
              c1: '#E1F5FE', c2: '#90CAF9',
              border: '#1565C0',
              unlockAt: 30 },
            { id: 'sun',       label: 'Sun',
              emoji: '\u2600\uFE0F',
              c1: '#FFECB3', c2: '#FFC107',
              border: '#F57F17',
              unlockAt: 30 },
        ],
        decor: [
            { id: 'rose',      label: 'Rose',
              emoji: '\uD83C\uDF39',
              c1: '#FFCDD2', c2: '#EF5350',
              border: '#B71C1C',
              unlockAt: 5 },
            { id: 'tulip',     label: 'Tulip',
              emoji: '\uD83C\uDF37',
              c1: '#F8BBD0', c2: '#F06292',
              border: '#AD1457',
              unlockAt: 11 },
            { id: 'sunflower', label: 'Sunflower',
              emoji: '\uD83C\uDF3B',
              c1: '#FFF59D', c2: '#FDD835',
              border: '#F57F17',
              unlockAt: 11 },
            { id: 'lantern',   label: 'Lantern',
              emoji: '\uD83C\uDFEE',
              c1: '#FFCCBC', c2: '#FF8A65',
              border: '#BF360C',
              unlockAt: 17 },
            { id: 'candle',    label: 'Candle',
              emoji: '\uD83D\uDD6F\uFE0F',
              c1: '#FFF3E0', c2: '#FFB74D',
              border: '#E65100',
              unlockAt: 17 },
            { id: 'tree',      label: 'Tree',
              emoji: '\uD83C\uDF33',
              c1: '#C8E6C9', c2: '#66BB6A',
              border: '#2E7D32',
              size: 'big',
              unlockAt: 27 },
            { id: 'fountain',  label: 'Fountain',
              emoji: '\u26F2',
              c1: '#B3E5FC', c2: '#4FC3F7',
              border: '#0277BD',
              size: 'big',
              unlockAt: 27 },
        ],
        pets: [
            { id: 'cat',       label: 'Kitty',
              emoji: '\uD83D\uDC31',
              c1: '#FFF9C4', c2: '#FFEB3B',
              border: '#F9A825',
              unlockAt: 9 },
            { id: 'puppy',     label: 'Puppy',
              emoji: '\uD83D\uDC36',
              c1: '#FFE0B2', c2: '#FFB74D',
              border: '#EF6C00',
              unlockAt: 9 },
            { id: 'unicorn',   label: 'Unicorn',
              emoji: '\uD83E\uDD84',
              c1: '#F3E5F5', c2: '#CE93D8',
              border: '#6A1B9A',
              magic: 'rainbow', size: 'big',
              unlockAt: 15 },
            { id: 'pony',      label: 'Pony',
              emoji: '\uD83D\uDC0E',
              c1: '#EFEBE9', c2: '#BCAAA4',
              border: '#4E342E',
              unlockAt: 25 },
            { id: 'parrot',    label: 'Parrot',
              emoji: '\uD83E\uDD9C',
              c1: '#B2DFDB', c2: '#26A69A',
              border: '#004D40',
              unlockAt: 25 },
            { id: 'butterfly', label: 'Butterfly',
              emoji: '\uD83E\uDD8B',
              c1: '#BBDEFB', c2: '#64B5F6',
              border: '#1565C0',
              unlockAt: 25 },
        ],
        royals: [
            { id: 'fairy',   label: 'Fairy',
              emoji: '\uD83E\uDDDA',
              c1: '#F8BBD0', c2: '#F06292',
              border: '#AD1457',
              halo: true, magic: 'fairy-dust',
              unlockAt: 15 },
            { id: 'queen',   label: 'Queen',
              emoji: '\uD83D\uDC78',
              c1: '#FFE082', c2: '#FFB300',
              border: '#FF8F00',
              halo: true, size: 'big',
              unlockAt: 18 },
            { id: 'king',    label: 'King',
              emoji: '\uD83E\uDD34',
              c1: '#E1BEE7', c2: '#9575CD',
              border: '#5E35B1',
              halo: true, size: 'big',
              unlockAt: 26 },
            { id: 'prince',  label: 'Prince',
              emoji: '\uD83E\uDD34',
              c1: '#BBDEFB', c2: '#64B5F6',
              border: '#1976D2',
              halo: true,
              unlockAt: 26 },
            { id: 'baby',    label: 'Baby',
              emoji: '\uD83D\uDC76',
              c1: '#FFCDD2', c2: '#F48FB1',
              border: '#C2185B',
              halo: true,
              unlockAt: 26 },
        ],
        furniture: [
            { id: 'cake',      label: 'Cake',
              emoji: '\uD83C\uDF82',
              c1: '#FFF8E1', c2: '#FFE082',
              border: '#FF8F00',
              unlockAt: 21 },
            { id: 'crown',     label: 'Crown',
              emoji: '\uD83D\uDC51',
              c1: '#FFF9C4', c2: '#FFD600',
              border: '#F57F17',
              unlockAt: 21 },
            { id: 'gem',       label: 'Gem',
              emoji: '\uD83D\uDC8E',
              c1: '#E1F5FE', c2: '#81D4FA',
              border: '#0277BD',
              unlockAt: 21 },
            { id: 'throne',    label: 'Throne',
              emoji: '\uD83E\uDE91',
              c1: '#FFCDD2', c2: '#E57373',
              border: '#B71C1C',
              size: 'big',
              unlockAt: 30 },
            { id: 'bed',       label: 'Bed',
              emoji: '\uD83D\uDECF\uFE0F',
              c1: '#E1BEE7', c2: '#CE93D8',
              border: '#6A1B9A',
              size: 'big',
              unlockAt: 30 },
            { id: 'mirror',    label: 'Mirror',
              emoji: '\uD83E\uDE9E',
              c1: '#CFD8DC', c2: '#90A4AE',
              border: '#37474F',
              unlockAt: 30 },
            { id: 'wardrobe',  label: 'Wardrobe',
              emoji: '\uD83D\uDDC4\uFE0F',
              c1: '#D7CCC8', c2: '#A1887F',
              border: '#4E342E',
              size: 'big',
              unlockAt: 30 },
        ],
    },

    TAB_ORDER: ['princesses', 'magic', 'decor',
                'pets', 'royals', 'furniture'],

    TAB_LABELS: {
        princesses: 'Princesses',
        magic:      'Magic',
        decor:      'Decor',
        pets:       'Pets',
        royals:     'Royal Family',
        furniture:  'Furniture',
    },

    state: {},
    drag: null,
    lastTap: { time: 0, itemId: null },
    $scene: null,
    $sceneWrap: null,
    $trash: null,
    _boundMove: null,
    _boundUp: null,

    // =================================================================
    //  Init — wire UI, show welcome, continue-button if saved
    // =================================================================
    init() {
        this.$scene     = document.getElementById('pp-scene');
        this.$sceneWrap = document.getElementById('pp-scene-wrap');
        this.$trash     = document.getElementById('pp-trash');

        this._boundMove = e => this._onDragMove(e);
        this._boundUp   = e => this._onDragEnd(e);

        document.querySelectorAll('.pp-lvl-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const lvl = parseInt(btn.dataset.lvl, 10);
                this.start(lvl, false);
            });
        });

        document.getElementById('pp-continue-btn')
            .addEventListener('click', () => this.start(null, true));

        document.getElementById('play-again-btn')
            .addEventListener('click', () => {
                this.state.candies = 0;
                this.state.stars = 0;
                this._renderCandyBar();
                this._renderStars();
                this._save();
                this._showScreen('game-screen');
            });

        document.getElementById('mute-btn')
            .addEventListener('click', () => {
                muted = !muted;
                document.getElementById('mute-btn').innerHTML =
                    muted ? '&#128263;' : '&#128264;';
            });

        document.getElementById('pp-reset-btn')
            .addEventListener('click', () =>
                this._showConfirm());

        document.getElementById('pp-confirm-yes')
            .addEventListener('click', () => {
                this._hideConfirm();
                this._resetAll();
            });
        document.getElementById('pp-confirm-no')
            .addEventListener('click', () =>
                this._hideConfirm());

        document.querySelectorAll('.pp-tab').forEach(tab => {
            tab.addEventListener('click', () =>
                this._activateTab(tab.dataset.tab));
        });

        // Show continue button if saved state has items
        const saved = this._loadSaved();
        if (saved && saved.items && saved.items.length > 0) {
            document.getElementById('pp-continue-btn')
                .classList.remove('hidden');
        }

        spawnClouds();
    },

    // =================================================================
    //  Start — new game at level OR continue from saved state
    // =================================================================
    start(level, isContinue) {
        initAudio();
        const saved = this._loadSaved();

        const baseState = {
            stars:        saved ? (saved.stars || 0) : 0,
            candies:      saved ? (saved.candies || 0) : 0,
            items:        saved ? (saved.items || []) : [],
            nextItemId:   saved ? (saved.nextItemId || 1) : 1,
            totalChanges: saved ? (saved.totalChanges || 0) : 0,
            activeTab:    'princesses',
            mathActive:   false,
            currentQ:     null,
        };

        if (isContinue && saved) {
            this.state = {
                ...baseState,
                level:       saved.level || 1,
                changeCount: saved.changeCount || 0,
            };
        } else {
            this.state = {
                ...baseState,
                level:       level,
                changeCount: 0,
            };
        }

        // Force princesses tab on start so the first thing the user
        // sees is always the fully-unlocked princess catalog.
        this.state.activeTab = 'princesses';

        this._renderTabs();
        this._activateTab('princesses');
        this._renderScene();
        this._renderStars();
        this._renderCandyBar();
        this._renderCounter();
        this._renderLevel();
        this._showScreen('game-screen');
        this._save();
    },

    // =================================================================
    //  Screen switching
    // =================================================================
    _showScreen(id) {
        document.querySelectorAll('.screen').forEach(s =>
            s.classList.toggle('hidden', s.id !== id));
    },

    _showChampion() {
        sfxChampion();
        spawnConfetti(80);
        this._showScreen('champion-screen');
    },

    // =================================================================
    //  Unlock logic
    // =================================================================
    _isUnlocked(item) {
        return (this.state.totalChanges || 0)
            >= (item.unlockAt || 0);
    },

    _unlockedItems(tabName) {
        const items = this.CATALOG[tabName] || [];
        return items.filter(i => this._isUnlocked(i));
    },

    _visibleTabs() {
        return this.TAB_ORDER.filter(
            t => this._unlockedItems(t).length > 0);
    },

    // =================================================================
    //  Palette rendering
    // =================================================================
    _renderTabs() {
        const visible = new Set(this._visibleTabs());
        document.querySelectorAll('.pp-tab').forEach(t => {
            const ok = visible.has(t.dataset.tab);
            t.style.display = ok ? '' : 'none';
        });
    },

    _activateTab(tabName) {
        // Guard: if requested tab is not unlocked yet, fall back to
        // the first visible tab.
        const visible = this._visibleTabs();
        if (!visible.includes(tabName)) {
            if (visible.length === 0) return;
            tabName = visible[0];
        }
        this.state.activeTab = tabName;
        document.querySelectorAll('.pp-tab').forEach(t =>
            t.classList.toggle('active', t.dataset.tab === tabName));
        this._renderPaletteItems();
    },

    _renderPaletteItems() {
        const items = this._unlockedItems(this.state.activeTab);
        const container = document.getElementById('pp-items');
        container.innerHTML = '';
        items.forEach(item => {
            const el = document.createElement('div');
            el.className = 'pp-item';
            el.dataset.itemId = item.id;
            el.style.setProperty('--pp-c1', item.c1);
            el.style.setProperty('--pp-c2', item.c2);
            el.style.setProperty('--pp-border', item.border);
            el.innerHTML =
                `<span class="pp-item-emoji">${item.emoji}</span>` +
                `<span class="pp-item-label"` +
                ` style="color:${item.border}">` +
                `${item.label}</span>`;
            el.addEventListener('pointerdown', e =>
                this._startDragFromPalette(e, item));
            container.appendChild(el);
        });
    },

    // =================================================================
    //  Scene rendering
    // =================================================================
    _renderScene() {
        this.$scene.innerHTML = '';
        this.state.items.forEach(it => this._renderPlaced(it));
    },

    _renderPlaced(it) {
        const spec = this._findCatalog(it.type);
        if (!spec) return;
        const el = document.createElement('div');
        el.className = 'pp-placed';
        if (spec.size === 'big')  el.classList.add('pp-big');
        if (spec.size === 'huge') el.classList.add('pp-huge');
        if (it.flipped)           el.classList.add('pp-flipped');
        el.dataset.pid = it.id;
        el.textContent = spec.emoji;
        el.style.left = it.x + '%';
        el.style.top  = it.y + '%';
        if (spec.halo) {
            el.style.background =
                `radial-gradient(circle, ${spec.c1} 0%,` +
                ` ${spec.c2} 80%)`;
            el.style.border = `3px solid ${spec.border}`;
            el.style.borderRadius = '50%';
        }
        el.addEventListener('pointerdown', e =>
            this._startDragFromScene(e, it.id));
        this.$scene.appendChild(el);
    },

    _findCatalog(typeId) {
        for (const tab of this.TAB_ORDER) {
            const hit = this.CATALOG[tab].find(c => c.id === typeId);
            if (hit) return hit;
        }
        return null;
    },

    // =================================================================
    //  Drag helpers — ghost, trash, commit
    // =================================================================
    _createGhost(emoji, x, y) {
        const g = document.createElement('div');
        g.className = 'pp-ghost';
        g.textContent = emoji;
        g.style.left = x + 'px';
        g.style.top  = y + 'px';
        document.body.appendChild(g);
        if (this.drag) this.drag.ghost = g;
    },

    _showTrash() { this.$trash.classList.add('pp-show'); },
    _hideTrash() {
        this.$trash.classList.remove('pp-show');
        this.$trash.classList.remove('pp-hover');
    },

    // Palette drag: cross-axis detection — browser owns the scroll
    // axis (pan-y on landscape, pan-x on portrait via CSS), we own
    // the perpendicular axis for drag intent. This lets users swipe
    // the palette to scroll and still pull items out onto the scene.
    _startDragFromPalette(event, catalogItem) {
        if (this.state.mathActive) return;

        const startX = event.clientX;
        const startY = event.clientY;
        const portrait = window.matchMedia(
            '(max-aspect-ratio: 1/1)').matches;
        let committed = false;

        const onMove = (e) => {
            if (committed) return;
            const dx = e.clientX - startX;
            const dy = e.clientY - startY;
            const absX = Math.abs(dx);
            const absY = Math.abs(dy);
            if (Math.hypot(dx, dy) < 12) return;

            const primaryIsDragAxis = portrait
                ? absY > absX
                : absX > absY;
            committed = true;
            cleanup();
            if (primaryIsDragAxis) {
                this._commitDragFromPalette(
                    e, catalogItem, startX, startY);
            }
            // else: browser handles the pan; no drag.
        };
        const onEnd = () => {
            if (!committed) {
                committed = true;
                cleanup();
            }
        };
        const cleanup = () => {
            document.removeEventListener('pointermove', onMove);
            document.removeEventListener('pointerup', onEnd);
            document.removeEventListener('pointercancel', onEnd);
        };
        document.addEventListener('pointermove', onMove);
        document.addEventListener('pointerup', onEnd);
        document.addEventListener('pointercancel', onEnd);
    },

    _commitDragFromPalette(event, catalogItem, startX, startY) {
        this.drag = {
            mode: 'add',
            item: catalogItem,
            startX, startY,
            lastX: event.clientX,
            lastY: event.clientY,
            moved: true,
            ghost: null,
            overTrash: false,
        };
        this._createGhost(
            catalogItem.emoji, event.clientX, event.clientY);
        this._showTrash();
        document.addEventListener('pointermove', this._boundMove);
        document.addEventListener('pointerup',   this._boundUp);
        document.addEventListener('pointercancel', this._boundUp);
    },

    // Scene items: immediate drag (scene has touch-action: none, so
    // there's no scroll to distinguish from drag).
    _startDragFromScene(event, pid) {
        if (this.state.mathActive) return;
        event.preventDefault();
        const placed = this.state.items.find(i => i.id === pid);
        if (!placed) return;
        const spec = this._findCatalog(placed.type);
        if (!spec) return;
        const el = this.$scene.querySelector(`[data-pid="${pid}"]`);
        if (el) el.classList.add('pp-dragging');
        this.drag = {
            mode: 'move',
            itemId: pid,
            item: spec,
            startX: event.clientX,
            startY: event.clientY,
            lastX:  event.clientX,
            lastY:  event.clientY,
            startTime: Date.now(),
            moved: false,
            ghost: null,
            overTrash: false,
        };
        this._createGhost(spec.emoji, event.clientX, event.clientY);
        this._showTrash();
        document.addEventListener('pointermove', this._boundMove);
        document.addEventListener('pointerup',   this._boundUp);
        document.addEventListener('pointercancel', this._boundUp);
    },

    _onDragMove(event) {
        if (!this.drag) return;
        const d = this.drag;
        const dx = event.clientX - d.startX;
        const dy = event.clientY - d.startY;
        if (!d.moved && Math.hypot(dx, dy) > 6) {
            d.moved = true;
        }
        if (d.ghost) {
            d.ghost.style.left = event.clientX + 'px';
            d.ghost.style.top  = event.clientY + 'px';
        }
        d.lastX = event.clientX;
        d.lastY = event.clientY;

        const tr = this.$trash.getBoundingClientRect();
        const over = event.clientX >= tr.left
                  && event.clientX <= tr.right
                  && event.clientY >= tr.top
                  && event.clientY <= tr.bottom;
        d.overTrash = over;
        this.$trash.classList.toggle('pp-hover', over);
    },

    _onDragEnd(event) {
        if (!this.drag) return;
        const d = this.drag;
        this.drag = null;
        document.removeEventListener('pointermove', this._boundMove);
        document.removeEventListener('pointerup',   this._boundUp);
        document.removeEventListener('pointercancel', this._boundUp);
        if (d.ghost) d.ghost.remove();
        this._hideTrash();
        this.$scene.querySelectorAll('.pp-dragging')
            .forEach(el => el.classList.remove('pp-dragging'));

        // Drop on trash: REMOVE (only if moving)
        if (d.overTrash) {
            if (d.mode === 'move') {
                this._removeItem(d.itemId);
                sfxPop();
                this._registerChange();
            }
            return;
        }

        const rect = this.$sceneWrap.getBoundingClientRect();
        const x = d.lastX;
        const y = d.lastY;
        const inside = x >= rect.left && x <= rect.right
                    && y >= rect.top  && y <= rect.bottom;

        if (d.mode === 'add') {
            if (!inside) return;
            const rx = ((x - rect.left) / rect.width)  * 100;
            const ry = ((y - rect.top)  / rect.height) * 100;
            this._addItem(d.item.id, rx, ry);
            this._registerChange();
            return;
        }

        // MOVE branch — tap = flip on double-tap; hold = no-op.
        if (!d.moved) {
            const now = Date.now();
            if (this.lastTap.itemId === d.itemId
                && (now - this.lastTap.time) < 380) {
                this._flipItem(d.itemId);
                this.lastTap = { time: 0, itemId: null };
                sfxPop();
                this._registerChange();
            } else {
                this.lastTap = { time: now, itemId: d.itemId };
                sfxPop();
            }
            return;
        }
        if (!inside) return;
        const rx = ((x - rect.left) / rect.width)  * 100;
        const ry = ((y - rect.top)  / rect.height) * 100;
        this._moveItem(d.itemId, rx, ry);
        this._registerChange();
    },

    // =================================================================
    //  Mutations
    // =================================================================
    _addItem(typeId, x, y) {
        const spec = this._findCatalog(typeId);
        if (!spec) return;
        x = Math.max(3, Math.min(97, x));
        y = Math.max(5, Math.min(95, y));
        const it = {
            id: this.state.nextItemId++,
            type: typeId,
            x, y,
            flipped: false,
        };
        this.state.items.push(it);
        this._renderPlaced(it);
        sfxPop();
        if (spec.magic) {
            this._runMagicEffect(spec.magic, x, y);
        } else {
            this._plainSparkle(x, y);
        }
    },

    _moveItem(pid, x, y) {
        const it = this.state.items.find(i => i.id === pid);
        if (!it) return;
        it.x = Math.max(3, Math.min(97, x));
        it.y = Math.max(5, Math.min(95, y));
        const el = this.$scene.querySelector(`[data-pid="${pid}"]`);
        if (el) {
            el.style.left = it.x + '%';
            el.style.top  = it.y + '%';
        }
        sfxPop();
    },

    _removeItem(pid) {
        const idx = this.state.items.findIndex(i => i.id === pid);
        if (idx < 0) return;
        this.state.items.splice(idx, 1);
        const el = this.$scene.querySelector(`[data-pid="${pid}"]`);
        if (el) el.remove();
    },

    _flipItem(pid) {
        const it = this.state.items.find(i => i.id === pid);
        if (!it) return;
        it.flipped = !it.flipped;
        const el = this.$scene.querySelector(`[data-pid="${pid}"]`);
        if (el) el.classList.toggle('pp-flipped', it.flipped);
    },

    // =================================================================
    //  Magic sparkle effects
    // =================================================================
    _runMagicEffect(kind, xPct, yPct) {
        const kinds = {
            snow:        { emoji: '\u2744\uFE0F', count: 12, drift: 50 },
            petals:      { emoji: '\uD83C\uDF39', count:  8, drift: 40 },
            golden:      { emoji: '\u2728',       count: 12, drift: 45 },
            silver:      { emoji: '\uD83D\uDCAB', count: 10, drift: 45 },
            blossom:     { emoji: '\uD83C\uDF38', count:  9, drift: 40 },
            bubbles:     { emoji: '\uD83D\uDCA7', count: 12, drift: 35 },
            waves:       { emoji: '\uD83C\uDF38', count:  8, drift: 40 },
            rainbow:     { emoji: '\uD83C\uDF08', count:  6, drift: 55 },
            'fairy-dust':{ emoji: '\u2728',       count: 14, drift: 55 },
        };
        const eff = kinds[kind];
        if (!eff) return this._plainSparkle(xPct, yPct);
        this._spawnParticles(xPct, yPct, eff.emoji, eff.count,
                             eff.drift);
    },

    _plainSparkle(xPct, yPct) {
        this._spawnParticles(xPct, yPct, '\u2728', 6, 30);
    },

    _spawnParticles(xPct, yPct, emoji, count, drift) {
        const rect = this.$sceneWrap.getBoundingClientRect();
        const absX = rect.left + (xPct / 100) * rect.width;
        const absY = rect.top  + (yPct / 100) * rect.height;
        for (let i = 0; i < count; i++) {
            const s = document.createElement('div');
            s.className = 'pp-sparkle';
            s.textContent = emoji;
            s.style.left = absX + 'px';
            s.style.top  = absY + 'px';
            s.style.setProperty('--sx',
                ((Math.random() - 0.5) * drift * 2) + 'px');
            s.style.setProperty('--sy',
                ((Math.random() - 0.5) * drift * 2) + 'px');
            s.style.animationDelay =
                (Math.random() * 0.25) + 's';
            document.body.appendChild(s);
            setTimeout(() => s.remove(), 1500);
        }
    },

    // =================================================================
    //  Change counter, unlocks, math gate trigger
    // =================================================================
    _registerChange() {
        const oldTotal = this.state.totalChanges || 0;
        const newTotal = oldTotal + 1;
        this.state.totalChanges = newTotal;
        this.state.changeCount++;
        this._renderCounter();
        this._checkUnlocks(oldTotal, newTotal);
        this._save();
        if (this.state.changeCount >= this.CHANGES_PER_MATH
            && !this.state.mathActive) {
            // Freeze input immediately so a fast extra tap in the
            // 400ms fade-in window does not slip through.
            this.state.mathActive = true;
            setTimeout(() => this._openMathGate(), 400);
        }
    },

    _checkUnlocks(oldTotal, newTotal) {
        const newTabs = [];
        const newItems = [];
        for (const tabName of this.TAB_ORDER) {
            const items = this.CATALOG[tabName];
            let wasAnyVisible = false;
            let isAnyVisible  = false;
            for (const item of items) {
                const u = item.unlockAt || 0;
                if (u <= oldTotal) wasAnyVisible = true;
                if (u <= newTotal) isAnyVisible  = true;
                if (u > oldTotal && u <= newTotal) {
                    newItems.push({ item, tabName });
                }
            }
            if (!wasAnyVisible && isAnyVisible) {
                newTabs.push(tabName);
            }
        }

        if (newTabs.length === 0 && newItems.length === 0) return;

        // Re-render tabs (new tab may have appeared).
        this._renderTabs();
        // Re-render palette (new item in active tab may have appeared).
        this._renderPaletteItems();

        if (newTabs.length > 0) {
            const label = this.TAB_LABELS[newTabs[0]] || newTabs[0];
            showFeedback('New: ' + label + '!', 'levelup', 2000);
            sfxLevelUp();
            spawnConfetti(24);
        } else {
            // Only an item unlocked (no new tab). Lighter feedback.
            const first = newItems[0].item;
            showFeedback(
                'New: ' + first.label + '!', 'correct', 1400);
            sfxStar();
        }
    },

    _renderCounter() {
        const el = document.getElementById('pp-counter');
        el.textContent =
            this.state.changeCount + '/' + this.CHANGES_PER_MATH;
        el.classList.remove('pp-flash');
        void el.offsetWidth;
        el.classList.add('pp-flash');
    },

    // =================================================================
    //  Math gate
    // =================================================================
    _genQuestion() {
        const range = this.LEVEL_RANGES[this.state.level]
                   || this.LEVEL_RANGES[1];
        const ops = range.ops || this.OPS;
        for (let tries = 0; tries < 30; tries++) {
            const op = ops[
                Math.floor(Math.random() * ops.length)];
            const result = range.min + Math.floor(
                Math.random() * (range.max - range.min + 1));
            const q = this._buildQ(op, result);
            if (q) return q;
        }
        // Fallback — use the level's first op (always '+' for
        // Ultra Easy) which always has a valid build.
        const result = range.min + Math.floor(
            Math.random() * (range.max - range.min + 1));
        return this._buildQ(ops[0], result);
    },

    _buildQ(op, result) {
        if (op === '+') {
            const max = Math.min(result, 15);
            const a = Math.floor(Math.random() * (max + 1));
            const b = result - a;
            if (b < 0 || b > 20) return null;
            return { a, b, op, result };
        }
        if (op === '-') {
            // a - b = result; a in [result, result+12], b in [0, 12]
            const b = Math.floor(Math.random() * 13);
            const a = result + b;
            if (a > 40) return null;
            return { a, b, op, result };
        }
        if (op === 'x') {
            if (result === 0) {
                const b = 2 + Math.floor(Math.random() * 9);
                return { a: 0, b, op, result: 0 };
            }
            if (result === 1) return { a: 1, b: 1, op, result: 1 };
            const pairs = [];
            for (let a = 2; a <= 12; a++) {
                if (result % a === 0) {
                    const b = result / a;
                    if (b >= 2 && b <= 12) pairs.push([a, b]);
                }
            }
            if (pairs.length === 0) return null;
            const [a, b] = pairs[
                Math.floor(Math.random() * pairs.length)];
            return { a, b, op, result };
        }
        if (op === '/') {
            if (result === 0) {
                const b = 2 + Math.floor(Math.random() * 9);
                return { a: 0, b, op, result: 0 };
            }
            const cap = result <= 10 ? 30
                      : result <= 20 ? 60 : 90;
            const pairs = [];
            for (let b = 2; b <= 10; b++) {
                const a = result * b;
                if (a <= cap) pairs.push([a, b]);
            }
            if (pairs.length === 0) return null;
            const [a, b] = pairs[
                Math.floor(Math.random() * pairs.length)];
            return { a, b, op, result };
        }
        return null;
    },

    _genChoices(correct) {
        const set = new Set([correct]);
        let tries = 0;
        while (set.size < 4 && tries++ < 60) {
            const off = (Math.random() < 0.5 ? -1 : 1)
                      * (1 + Math.floor(Math.random() * 4));
            const d = correct + off;
            if (d >= 0 && d <= 40) set.add(d);
        }
        while (set.size < 4) {
            set.add(Math.floor(Math.random() * 40));
        }
        const arr = [...set];
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    },

    _openMathGate() {
        if (this.state.currentQ !== null) return;
        this.state.mathActive = true;
        const q = this._genQuestion();
        this.state.currentQ = q;

        const opSym = this.OP_DISPLAY[q.op] || q.op;
        document.getElementById('pp-math-prompt').textContent =
            'Help me, princess!';
        document.getElementById('pp-math-q').textContent =
            q.a + ' ' + opSym + ' ' + q.b + ' = ?';
        const container =
            document.getElementById('pp-math-choices');
        const choices = this._genChoices(q.result);
        container.innerHTML = '';
        choices.forEach(c => {
            const btn = document.createElement('button');
            btn.className = 'pp-choice';
            btn.textContent = c;
            btn.dataset.val = c;
            btn.addEventListener('click', () =>
                this._onChoice(btn, c, q.result));
            container.appendChild(btn);
        });
        document.getElementById('pp-math-overlay')
            .classList.add('pp-show');
        sfxPop();
    },

    _onChoice(btn, value, correct) {
        if (!this.state.mathActive) return;
        if (value === correct) {
            btn.classList.add('pp-correct');
            sfxCorrect();
            spawnConfetti(50);
            for (let i = 0; i < 3; i++) {
                setTimeout(() => flyingStar(), i * 180);
            }
            this._awardStars(this.STARS_PER_MATH);
            setTimeout(() => this._closeMathGate(), 1500);
        } else {
            btn.classList.add('pp-shake');
            sfxWrong();
            document.getElementById('pp-math-prompt')
                .textContent = 'Try again, sweetie!';
            setTimeout(() =>
                btn.classList.remove('pp-shake'), 500);
        }
    },

    _closeMathGate() {
        this.state.mathActive = false;
        this.state.currentQ = null;
        this.state.changeCount = 0;
        document.getElementById('pp-math-overlay')
            .classList.remove('pp-show');
        this._renderCounter();
        this._save();

        if (this.state.stars >= this.STARS_PER_CANDY) {
            setTimeout(() => this._handleCandyEarned(), 350);
        }
    },

    // =================================================================
    //  Rewards — no prize time-break; candies and champion only.
    // =================================================================
    _awardStars(n) {
        this.state.stars += n;
        this._renderStars();
        this._save();
    },

    _renderStars() {
        document.getElementById('stars-display').innerHTML =
            '&#11088; ' + this.state.stars;
    },

    _renderLevel() {
        const r = this.LEVEL_RANGES[this.state.level];
        document.getElementById('level-display').textContent =
            r ? r.label : 'Easy';
    },

    _renderCandyBar() {
        const bar = document.getElementById('candy-bar');
        bar.innerHTML = '';
        for (let i = 0; i < this.CANDIES_TO_WIN; i++) {
            const s = document.createElement('div');
            s.className = 'candy-slot';
            if (i < this.state.candies) {
                s.classList.add('earned');
                s.textContent = '\uD83C\uDF6C';
            }
            bar.appendChild(s);
        }
    },

    _handleCandyEarned() {
        while (this.state.stars >= this.STARS_PER_CANDY) {
            this.state.stars -= this.STARS_PER_CANDY;
            this.state.candies++;
        }
        this._renderStars();
        this._renderCandyBar();
        sfxCandy();
        this._save();

        if (this.state.candies >= this.CANDIES_TO_WIN) {
            setTimeout(() => this._showChampion(), 700);
        }
    },

    // =================================================================
    //  Reset confirm modal
    // =================================================================
    _showConfirm() {
        document.getElementById('pp-confirm-overlay')
            .classList.add('pp-show');
    },
    _hideConfirm() {
        document.getElementById('pp-confirm-overlay')
            .classList.remove('pp-show');
    },

    // Reset clears the palace + current session progress, but KEEPS
    // lifetime unlocks (totalChanges) so the player doesn't lose
    // content they already earned.
    _resetAll() {
        this.state.items = [];
        this.state.stars = 0;
        this.state.candies = 0;
        this.state.changeCount = 0;
        this.state.nextItemId = 1;
        this._renderScene();
        this._renderStars();
        this._renderCandyBar();
        this._renderCounter();
        this._renderTabs();
        this._activateTab(this.state.activeTab);
        this._save();
        sfxPop();
    },

    // =================================================================
    //  Persistence (v2 — includes totalChanges)
    // =================================================================
    _save() {
        try {
            const { level, stars, candies, changeCount,
                    items, nextItemId, totalChanges } = this.state;
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify({
                v: 2, level, stars, candies, changeCount,
                items, nextItemId,
                totalChanges: totalChanges || 0,
            }));
        } catch (e) { /* ignore quota / privacy-mode errors */ }
    },

    _loadSaved() {
        try {
            const raw = localStorage.getItem(this.STORAGE_KEY);
            if (raw) {
                const obj = JSON.parse(raw);
                if (obj && obj.v === 2) return obj;
            }
            // Fall-back: migrate from v1 (no totalChanges, old sum
            // ranges). Treat prior items as baseline progress.
            const oldRaw = localStorage.getItem(this.OLD_STORAGE_KEY);
            if (oldRaw) {
                const o = JSON.parse(oldRaw);
                if (o && o.v === 1) {
                    return {
                        v: 2,
                        level:        1,
                        stars:        o.stars        || 0,
                        candies:      o.candies      || 0,
                        changeCount:  0,
                        items:        o.items        || [],
                        nextItemId:   o.nextItemId   || 1,
                        totalChanges: (o.items
                            ? o.items.length : 0),
                    };
                }
            }
            return null;
        } catch (e) {
            return null;
        }
    },
};

document.addEventListener('DOMContentLoaded', () => {
    PrincessPalaceGame.init();
});
