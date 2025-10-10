// ==============================================
// Rain Effect with Configuration
// ==============================================

// คอนฟิกสำหรับเอฟเฟกต์ฝน
const RAIN_CONFIG = {
    // ความหนาแน่นของฝน
    density: 0.00010,

    // ขนาดหยดน้ำ
    size: {
        min: 10,
        max: 30
    },

    // ความเร็ว
    speed: {
        base: 15,
        variation: 0.3  // ± 30%
    },

    // สีของฝน
    colors: [
        '255, 255, 255',   // ขาว
        '45, 49, 146',     // น้ำเงิน
        '179, 25, 66',     // แดง
        '230, 230, 230',   // สีขาวนวล
        '70, 75, 180'      // สีน้ำเงินสว่าง
    ],

    // เอฟเฟกต์ลม
    wind: {
        max: 80,       // ความแรงลมสูงสุด
        gain: 0.1,     // ความไวต่อเมาส์
        decay: 0.86,   // อัตราการลดลง
        lerp: 0.28,    // ความนุ่มนวลของการเปลี่ยนทิศทาง
        jitter: 1.0    // ความสุ่มของการส่าย
    },

    // ทิศทาง
    direction: 'down'  // 'up' หรือ 'down'
};

// โค้ดส่วน Raindrop และ RainEffect classes (คงเดิม)
class Raindrop {
    constructor(canvas, opts) {
        this.canvas = canvas;
        this.opts = opts;
        this.reset(true);
    }

    reset(randomY = false) {
        const { sizeMin, sizeMax, baseSpeed, direction, colors } = this.opts;
        this.x = Math.random() * this.canvas.width;
        this.y = randomY ? Math.random() * this.canvas.height : -20;

        this.length = sizeMin + Math.random() * (sizeMax - sizeMin);
        const sizeFactor = this.length / ((sizeMin + sizeMax) / 2);
        const speed = baseSpeed * (0.85 + Math.random() * 0.3) * (0.9 + sizeFactor * 0.2);

        this.vy = direction === 'up' ? -speed : speed;
        this.vx = 0;

        if (colors && colors.length > 0) {
            const colorIndex = Math.floor(Math.random() * colors.length);
            const color = colors[colorIndex];
            if (color.startsWith('#')) {
                const r = parseInt(color.slice(1, 3), 16);
                const g = parseInt(color.slice(3, 5), 16);
                const b = parseInt(color.slice(5, 7), 16);
                this.color = `${r}, ${g}, ${b}`;
            } else {
                this.color = color;
            }
        } else {
            this.color = '174, 194, 224';
        }

        this.opacity = 0.12 + Math.random() * 0.2;
        this.localDrift = (Math.random() - 0.5) * 0.6;
    }

    update(globalWind) {
        const { windFollow, windJitter, direction } = this.opts;
        this.vx += (globalWind + this.localDrift * windJitter - this.vx) * windFollow;
        this.x += this.vx;
        this.y += this.vy;

        if (direction === 'down') {
            if (this.y > this.canvas.height + 40 || this.x < -40 || this.x > this.canvas.width + 40) this.reset(false);
        } else {
            if (this.y < -40 || this.x < -40 || this.x > this.canvas.width + 40) this.reset(false);
        }
    }

    draw(ctx) {
        ctx.beginPath();
        ctx.strokeStyle = `rgba(${this.color}, ${this.opacity})`;
        ctx.lineWidth = 1;

        const angle = Math.atan2(this.vy, this.vx);
        const endX = this.x - Math.cos(angle) * this.length;
        const endY = this.y - Math.sin(angle) * this.length;

        ctx.moveTo(this.x, this.y);
        ctx.lineTo(endX, endY);
        ctx.stroke();
    }
}

class RainEffect {
    constructor(canvasId, options = {}) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');

        // รวม default config กับ options ที่ส่งมา
        this.opts = Object.assign({
            density: RAIN_CONFIG.density,
            sizeMin: RAIN_CONFIG.size.min,
            sizeMax: RAIN_CONFIG.size.max,
            baseSpeed: RAIN_CONFIG.speed.base,
            direction: RAIN_CONFIG.direction,
            windMax: RAIN_CONFIG.wind.max,
            windGain: RAIN_CONFIG.wind.gain,
            windDecay: RAIN_CONFIG.wind.decay,
            windLerp: RAIN_CONFIG.wind.lerp,
            windFollow: 0.12,
            windJitter: RAIN_CONFIG.wind.jitter,
            colors: RAIN_CONFIG.colors
        }, options);

        this.raindrops = [];
        this.globalWind = 0;
        this.windTarget = 0;
        this.lastMouseX = null;

        this.initCanvas();
        this.initPointerImpulse();
        this.createRaindrops();
        this.animate();
    }

    initCanvas() {
        const resize = () => {
            const dpr = Math.max(1, window.devicePixelRatio || 1);
            const w = Math.floor(window.innerWidth);
            const h = Math.floor(window.innerHeight);

            this.canvas.style.width = `${w}px`;
            this.canvas.style.height = `${h}px`;
            this.canvas.width = Math.floor(w * dpr);
            this.canvas.height = Math.floor(h * dpr);
            this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

            const area = w * h;
            const desired = Math.max(10, Math.floor(area * this.opts.density));
            const diff = desired - this.raindrops.length;
            if (diff > 0) for (let i = 0; i < diff; i++) this.raindrops.push(new Raindrop(this.canvas, this.opts));
            else if (diff < 0) this.raindrops.splice(desired);
        };
        resize();
        window.addEventListener('resize', resize);
    }

    initPointerImpulse() {
        const nudge = (dx) => {
            this.windTarget = dx * this.opts.windGain;
            if (this.windTarget > this.opts.windMax) this.windTarget = this.opts.windMax;
            if (this.windTarget < -this.opts.windMax) this.windTarget = -this.opts.windMax;
        };

        this.canvas.addEventListener('mousemove', (e) => {
            let dx = (typeof e.movementX === 'number') ? e.movementX : 0;
            if (!dx && this.lastMouseX != null) dx = e.clientX - this.lastMouseX;
            this.lastMouseX = e.clientX;
            nudge(dx);
        });
        this.canvas.addEventListener('mouseleave', () => { this.lastMouseX = null; });

        this.canvas.addEventListener('touchmove', (e) => {
            if (!e.touches || !e.touches[0]) return;
            const t = e.touches[0];
            if (this.lastMouseX != null) {
                const dx = t.clientX - this.lastMouseX;
                nudge(dx);
            }
            this.lastMouseX = t.clientX;
        }, { passive: true });
        this.canvas.addEventListener('touchend', () => { this.lastMouseX = null; });
    }

    createRaindrops() {
        const w = parseInt(this.canvas.style.width) || window.innerWidth;
        const h = parseInt(this.canvas.style.height) || window.innerHeight;
        const desired = Math.max(10, Math.floor(w * h * this.opts.density));
        for (let i = 0; i < desired; i++) {
            const d = new Raindrop(this.canvas, this.opts);
            d.reset(true);
            this.raindrops.push(d);
        }
    }

    animate() {
        this.windTarget *= this.opts.windDecay;
        this.globalWind += (this.windTarget - this.globalWind) * this.opts.windLerp;

        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        for (const drop of this.raindrops) {
            drop.update(this.globalWind);
            drop.draw(this.ctx);
        }

        requestAnimationFrame(() => this.animate());
    }
}

// API
function startRainEffect(canvasId, options) {
    return new RainEffect(canvasId, options);
}