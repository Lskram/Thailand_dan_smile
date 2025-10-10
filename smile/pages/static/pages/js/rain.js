// ==============================================
// Rain Effect (Canvas) — 0.3s mouse impulse, no locking
// ==============================================
class Raindrop {
  constructor(canvas, opts) {
    this.canvas = canvas;
    this.opts = opts;
    this.reset(true);
  }

  reset(randomY = false) {
    const { sizeMin, sizeMax, baseSpeed, direction } = this.opts;
    this.x = Math.random() * this.canvas.width;
    this.y = randomY ? Math.random() * this.canvas.height : -20;

    // ความยาวสัมพันธ์กับความเร็ว (คงฟีลเดิมช้า ๆ)
    this.length = sizeMin + Math.random() * (sizeMax - sizeMin); // 10..30
    const sizeFactor = this.length / ((sizeMin + sizeMax) / 2);
    const speed = baseSpeed * (0.85 + Math.random() * 0.3) * (0.9 + sizeFactor * 0.2);

    this.vy = direction === 'up' ? -speed : speed; // ปกติลงล่าง
    this.vx = 0;

    this.opacity = 0.12 + Math.random() * 0.2;
    this.localDrift = (Math.random() - 0.5) * 0.6; // ส่ายยิบๆ เบาๆ
  }

  update(globalWind) {
    const { windFollow, windJitter, direction } = this.opts;

    // หยดไล่ตาม global wind แบบนุ่ม ๆ
    this.vx += (globalWind + this.localDrift * windJitter - this.vx) * windFollow;

    this.x += this.vx;
    this.y += this.vy;

    // ออกจอแล้วรีเซ็ต
    if (direction === 'down') {
      if (this.y > this.canvas.height + 40 || this.x < -40 || this.x > this.canvas.width + 40) this.reset(false);
    } else {
      if (this.y < -40 || this.x < -40 || this.x > this.canvas.width + 40) this.reset(false);
    }
  }

  draw(ctx) {
    ctx.beginPath();
    ctx.strokeStyle = `rgba(174, 194, 224, ${this.opacity})`;
    ctx.lineWidth = 1;

    // หางย้อนทิศทางการเคลื่อนที่จริง
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

    // ค่าตั้งต้น: ฝนช้า, เอียงสั้น 0.3 วิ, ไม่ล็อคทาง
    this.opts = Object.assign({
      density: 0.00010,
      sizeMin: 10,
      sizeMax: 30,
      baseSpeed: 15,       // ≈ 15–30 (แบบที่คุณชอบ)
      direction: 'down',

      // ลมสั้นแบบ impulse (ตามความเร็วเมาส์)
      windMax: 80,         // จำกัดแรงเอียงรวม
      windGain: 0.1,       // ความไวต่อ movementX ของเมาส์
      windDecay: 0.86,     // สลายตัวต่อเฟรม (~0.3 วินาทีที่ 60fps)  // ~18 เฟรม
      windLerp: 0.28,      // ลมจริงไล่หาเป้าหมาย (ไม่หน่วงมาก)
      windFollow: 0.12,    // หยดไล่ตามลม (นุ่ม)
      windJitter: 1.0      // ส่ายยิบ ๆ ต่อหยด
    }, options);

    this.raindrops = [];
    this.globalWind = 0;
    this.windTarget = 0;   // เป้าหมายลมปัจจุบัน (สั้น ๆ)
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

  // ใช้ “ความเร็วเมาส์” เป็นลมสั้น ๆ (~0.3s) ไม่สะสม, ไม่ล็อค
  initPointerImpulse() {
    const nudge = (dx) => {
      // ไม่บวกสะสมยาว — ตั้งเป้าหมายจากการส่ายล่าสุดทันที
      this.windTarget = dx * this.opts.windGain;
      // จำกัด
      if (this.windTarget >  this.opts.windMax) this.windTarget =  this.opts.windMax;
      if (this.windTarget < -this.opts.windMax) this.windTarget = -this.opts.windMax;
    };

    // mouse
    this.canvas.addEventListener('mousemove', (e) => {
      let dx = (typeof e.movementX === 'number') ? e.movementX : 0;
      if (!dx && this.lastMouseX != null) dx = e.clientX - this.lastMouseX; // fallback
      this.lastMouseX = e.clientX;
      nudge(dx);
    });
    this.canvas.addEventListener('mouseleave', () => { this.lastMouseX = null; /* ปล่อย decay ต่อเอง */ });

    // touch
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
    // 1) สลาย windTarget เร็ว ๆ (~0.3s) เพื่อ “เอียงสั้น ๆ แล้วกลับ”
    this.windTarget *= this.opts.windDecay;

    // 2) globalWind ไล่หาเป้าหมายแบบนุ่ม (ไม่ล็อคทาง)
    this.globalWind += (this.windTarget - this.globalWind) * this.opts.windLerp;

    // 3) วาด
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    for (const drop of this.raindrops) {
      drop.update(this.globalWind);
      drop.draw(this.ctx);
    }

    requestAnimationFrame(() => this.animate());
  }
}

// ==============================================
// API
// ==============================================
function startRainEffect(canvasId, options) {
  return new RainEffect(canvasId, options);
}
