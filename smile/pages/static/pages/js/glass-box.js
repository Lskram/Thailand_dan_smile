// ==============================================
// คลาสสำหรับสร้างกล่องใส (Glass Container)
// ============================================== 
class GlassBox {
    constructor(options = {}) {
        // ค่าเริ่มต้นของกล่อง
        this.config = {
            width: options.width || '300px',
            height: options.height || 'auto',
            position: options.position || 'relative',
            background: 'rgba(255, 255, 255, 0.1)',
            borderColor: 'rgba(255, 255, 255, 0.18)',
            blur: options.blur || 12,
            content: options.content || '',
            layout: options.layout || {}
        };

        this.element = null;
        this.shineElements = [];
        this.createBox();
    }

    createBox() {
        this.element = document.createElement('div');
        this.element.className = 'glass-box';
        
        // สไตล์พื้นฐาน
        const baseStyle = {
            ...this.config.layout,
            backdropFilter: `blur(${this.config.blur}px)`,
            backgroundColor: this.config.background,
            borderRadius: '15px',
            border: `1px solid ${this.config.borderColor}`,
            boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.15)',
            color: 'white',
            transition: 'all 0.3s ease',
            overflow: 'hidden'
        };

        Object.assign(this.element.style, baseStyle);

        if (this.config.content) {
            const contentDiv = document.createElement('div');
            contentDiv.className = 'glass-box-content';
            contentDiv.style.padding = '20px';
            contentDiv.innerHTML = this.config.content;
            this.element.appendChild(contentDiv);
        }

        this.addEffects();
    }

    addEffects() {
        this.addShineEffect();
        this.addHoverEffect();
    }

    addShineEffect() {
        // สร้างตัวรองรับแสง
        const shineContainer = document.createElement('div');
        shineContainer.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            pointer-events: none;
        `;
        this.element.appendChild(shineContainer);

        // สร้างแสง 3 ชุด
        for (let i = 0; i < 3; i++) {
            const shine = document.createElement('div');
            shine.style.cssText = `
                position: absolute;
                top: 0;
                left: 0;
                width: 250%;
                height: 100%;
                background: linear-gradient(
                    90deg,
                    rgba(255,255,255,0) 0%,
                    rgba(255,255,255,0.1) 45%,
                    rgba(255,255,255,0.15) 50%,
                    rgba(255,255,255,0.1) 55%,
                    rgba(255,255,255,0) 100%
                );
                transform: translateX(-100%);
                transition: transform 1.5s ease-in-out;
                mix-blend-mode: overlay;
                opacity: 0;
                pointer-events: none;
            `;
            shineContainer.appendChild(shine);
            this.shineElements.push(shine);
        }

        // เริ่มเล่น loop animation
        this.startShineLoop();
    }

    startShineLoop() {
        let index = 0;
        const animate = () => {
            const shine = this.shineElements[index];
            
            // รีเซ็ตทุกอัน
            this.shineElements.forEach(s => {
                s.style.opacity = '0';
                s.style.transform = 'translateX(-100%)';
            });

            // เล่นแสงปัจจุบัน
            requestAnimationFrame(() => {
                shine.style.opacity = '1';
                shine.style.transform = 'translateX(100%)';
                
                // เลื่อนไปตัวถัดไป
                index = (index + 1) % this.shineElements.length;
            });
        };

        // เริ่มเล่น loop
        const loop = () => {
            animate();
            setTimeout(loop, 3000); // เว้นระยะห่าง 3 วินาที
        };

        // เริ่มหลังจาก delay 1 วินาที
        setTimeout(loop, 1000);
    }

    addHoverEffect() {
        this.element.addEventListener('mouseenter', () => {
            this.element.style.transform = this.element.style.transform.includes('translate') 
                ? this.element.style.transform.replace('scale(1)', 'scale(1.02)')
                : 'scale(1.02)';
            this.element.style.filter = 'brightness(1.1)';
        });

        this.element.addEventListener('mouseleave', () => {
            this.element.style.transform = this.element.style.transform.includes('translate')
                ? this.element.style.transform.replace('scale(1.02)', 'scale(1)')
                : 'scale(1)';
            this.element.style.filter = 'brightness(1)';
        });
    }

    // เพิ่มกล่องลงในหน้าเว็บ
    addToPage(parent = document.body) {
        parent.appendChild(this.element);
        return this;
    }

    // อัพเดทค่าคอนฟิก
    updateConfig(newConfig) {
        this.config = { ...this.config, ...newConfig };
        const parent = this.element.parentNode;
        parent.removeChild(this.element);
        this.createBox();
        this.addToPage(parent);
        return this;
    }

    // เปลี่ยนเนื้อหา
    setContent(content) {
        const contentDiv = this.element.querySelector('.glass-box-content');
        if (contentDiv) {
            contentDiv.innerHTML = content;
        }
        return this;
    }
}

// สร้างและเพิ่มกล่องโปรไฟล์
function createProfileBox() {
    return new GlassBox({
        width: '400px',
        height: 'auto',
        blur: 12,
        layout: {
            position: 'absolute',
            left: '50%',
            top: '50%',
            transform: 'translate(-50%, -50%)',
            zIndex: 10
        },
        content: `
            <div style="text-align: center;">
                <img src="/static/images/profile.jpg" style="width: 100px; height: 100px; border-radius: 50%;">
                <h2>โหดมาก</h2>
                <p>旅行的意义在于发现自我。</p>
                <div style="margin-top: 20px;">
                    <a href="#" style="margin: 0 10px;"><i class="fab fa-spotify"></i></a>
                    <a href="#" style="margin: 0 10px;"><i class="fab fa-twitter"></i></a>
                    <a href="#" style="margin: 0 10px;"><i class="far fa-bookmark"></i></a>
                    <a href="#" style="margin: 0 10px;"><i class="fab fa-instagram"></i></a>
                </div>
                <div style="margin-top: 15px;">
                    <small>Views: 1128</small>
                </div>
            </div>
        `
    });
}

// สร้างและเพิ่มกล่องแชท
function createChatBox() {
    return new GlassBox({
        width: '350px',
        height: '75vh',
        blur: 8,
        layout: {
            position: 'absolute',
            left: '30px',
            top: '50%',
            transform: 'translateY(-50%)',
            zIndex: 5
        },
        content: `
            <div style="height: 100%; display: flex; flex-direction: column;">
                <h3>Live Chat</h3>
                <div style="flex-grow: 1; overflow-y: auto;"></div>
                <input type="text" placeholder="Type a message..." 
                    style="margin-top: 10px; padding: 10px; border-radius: 8px; 
                    background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); 
                    color: white;">
            </div>
        `
    });
}

// สร้างและเพิ่มกล่อง Stack ด้านขวา
function createRightStack() {
    const container = document.createElement('div');
    Object.assign(container.style, {
        position: 'absolute',
        right: '30px',
        bottom: '30px',
        display: 'flex',
        flexDirection: 'column',
        gap: '15px',
        width: '280px',
        zIndex: 15
    });

    [1, 2].forEach(i => {
        new GlassBox({
            height: '120px',
            blur: 8,
            content: `<h3>Box ${i}</h3>`
        }).addToPage(container);
    });

    return container;
}