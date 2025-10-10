// ==============================================
// Glass Box Component with Configuration
// ==============================================

// ฟังก์ชันช่วยเหลือ
const helpers = {
    // แปลงค่าสีเป็น rgba
    toRGBA: (color, opacity) => {
        if (color.startsWith('#')) {
            const r = parseInt(color.slice(1, 3), 16);
            const g = parseInt(color.slice(3, 5), 16);
            const b = parseInt(color.slice(5, 7), 16);
            return `rgba(${r}, ${g}, ${b}, ${opacity})`;
        }
        return color;
    },

    // สุ่มค่าในช่วง
    random: (min, max) => min + Math.random() * (max - min),

    // สุ่มค่าจาก array
    randomFrom: (array) => array[Math.floor(Math.random() * array.length)],

    // สร้าง CSS Transform
    transform: (...transforms) => transforms.join(' ')
};

// ธีมหลัก
const THEME = {
    colors: {
        primary: '#2D3192',    // น้ำเงินเข้ม
        secondary: '#B31942',  // แดง
        white: '#FFFFFF',
        overlay: 'rgba(255, 255, 255, 0.1)',
        border: 'rgba(255, 255, 255, 0.2)'
    },

    animation: {
        timing: {
            normal: 'cubic-bezier(0.4, 0, 0.2, 1)',
            smooth: 'cubic-bezier(0.4, 0, 0.6, 1)',
            bounce: 'cubic-bezier(0.34, 1.56, 0.64, 1)'
        },
        duration: {
            fast: 0.2,
            normal: 0.3,
            slow: 0.5
        }
    },

    content: {
        title: 'ยินดีต้อนรับสู่ประเทศไทย',
        subtitle: 'สัมผัสมนต์เสน่ห์แห่งดินแดนแห่งรอยยิ้ม',
        menu: ['ท่องเที่ยว', 'วัฒนธรรม', 'อาหาร']
    }
};

// คอนฟิกสำหรับกล่องแก้ว
const GLASS_CONFIG = {
    // สไตล์พื้นฐาน
    style: {
        blur: 15,
        opacity: 0.08,
        border: {
            width: 1.5,
            opacity: 0.22,
            color: 'rgba(255, 255, 255, 0.2)'
        },
        shadow: '0 8px 32px 0 rgba(0, 0, 0, 0.2)',
        radius: '18px'
    },

    // เอฟเฟกต์แสง
    shine: {
        enabled: true,
        opacity: 0.15,
        duration: 1.5,
        delay: 3,
        timing: 'cubic-bezier(0.4, 0, 0.2, 1)'
    },

    // เอฟเฟกต์ hover
    hover: {
        enabled: true,
        scale: 1.02,
        brightness: 1.1,
        duration: 0.3
    },

    // กล่องต่างๆ
    boxes: {
        profile: {
            width: '400px',
            height: 'auto',
            position: {
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)'
            },
            zIndex: 10
        },

        chat: {
            width: '350px',
            height: '75vh',
            position: {
                left: '30px',
                top: '50%',
                transform: 'translateY(-50%)'
            },
            zIndex: 5
        },

        stack: {
            container: {
                width: '280px',
                position: {
                    right: '30px',
                    bottom: '30px'
                },
                gap: '15px',
                zIndex: 15
            },
            items: [
                { height: '120px', title: 'Box 1' },
                { height: '120px', title: 'Box 2' }
            ]
        }
    }
};

// คลาสหลัก GlassBox
class GlassBox {
    constructor(options = {}) {
        // ผสาน options กับ default config
        this.config = {
            width: options.width || GLASS_CONFIG.boxes.profile.width,
            height: options.height || 'auto',
            position: options.position || 'relative',
            background: helpers.toRGBA(THEME.colors.white, GLASS_CONFIG.style.opacity),
            borderColor: GLASS_CONFIG.style.border.color,
            blur: options.blur || GLASS_CONFIG.style.blur,
            content: options.content || '',
            layout: options.layout || {},
            theme: options.theme || 'thai'
        };

        this.element = null;
        this.shineElements = [];
        this.createBox();
    }

    createBox() {
        this.element = document.createElement('div');
        this.element.className = 'glass-box';
        
        const baseStyle = {
            ...this.config.layout,
            backdropFilter: `blur(${this.config.blur}px)`,
            backgroundColor: this.config.background,
            borderRadius: GLASS_CONFIG.style.radius,
            border: `${GLASS_CONFIG.style.border.width}px solid ${this.config.borderColor}`,
            boxShadow: GLASS_CONFIG.style.shadow,
            color: THEME.colors.white,
            transition: `all ${THEME.animation.duration.normal}s ${THEME.animation.timing.normal}`,
            overflow: 'hidden'
        };
        
        if (this.config.theme === 'thai') {
            Object.assign(baseStyle, {
                backgroundImage: `
                    linear-gradient(135deg, 
                        rgba(255,255,255,0.03) 0%,
                        rgba(255,255,255,0.06) 100%
                    ),
                    radial-gradient(
                        circle at 50% 50%,
                        rgba(255,255,255,0.05) 0%,
                        rgba(255,255,255,0) 60%
                    )
                `,
                borderImage: `
                    linear-gradient(
                        45deg,
                        rgba(255,255,255,0.1),
                        rgba(255,255,255,0.3),
                        rgba(255,255,255,0.1)
                    ) 1
                `
            });
        }

        Object.assign(this.element.style, baseStyle);

        if (this.config.content) {
            const contentDiv = document.createElement('div');
            contentDiv.className = 'glass-box-content';
            contentDiv.style.padding = '20px';
            contentDiv.innerHTML = this.config.content;
            this.element.appendChild(contentDiv);
        }

        if (GLASS_CONFIG.shine.enabled) {
            this.addEffects();
        }
    }

    addEffects() {
        this.addShineEffect();
        if (GLASS_CONFIG.hover.enabled) {
            this.addHoverEffect();
        }
    }

    addShineEffect() {
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
                    rgba(255,255,255,${GLASS_CONFIG.shine.opacity}) 45%,
                    rgba(255,255,255,${GLASS_CONFIG.shine.opacity * 1.5}) 50%,
                    rgba(255,255,255,${GLASS_CONFIG.shine.opacity}) 55%,
                    rgba(255,255,255,0) 100%
                );
                transform: translateX(-100%);
                transition: transform ${GLASS_CONFIG.shine.duration}s ${GLASS_CONFIG.shine.timing};
                mix-blend-mode: overlay;
                opacity: 0;
                pointer-events: none;
            `;
            shineContainer.appendChild(shine);
            this.shineElements.push(shine);
        }

        this.startShineLoop();
    }

    startShineLoop() {
        let index = 0;
        const animate = () => {
            const shine = this.shineElements[index];
            
            this.shineElements.forEach(s => {
                s.style.opacity = '0';
                s.style.transform = 'translateX(-100%)';
            });

            requestAnimationFrame(() => {
                shine.style.opacity = '1';
                shine.style.transform = 'translateX(100%)';
                index = (index + 1) % this.shineElements.length;
            });
        };

        const loop = () => {
            animate();
            setTimeout(loop, GLASS_CONFIG.shine.delay * 1000);
        };

        setTimeout(loop, 1000);
    }

    addHoverEffect() {
        this.element.addEventListener('mouseenter', () => {
            this.element.style.transform = this.element.style.transform.includes('translate') 
                ? this.element.style.transform.replace('scale(1)', `scale(${GLASS_CONFIG.hover.scale})`)
                : `scale(${GLASS_CONFIG.hover.scale})`;
            this.element.style.filter = `brightness(${GLASS_CONFIG.hover.brightness})`;
        });

        this.element.addEventListener('mouseleave', () => {
            this.element.style.transform = this.element.style.transform.includes('translate')
                ? this.element.style.transform.replace(`scale(${GLASS_CONFIG.hover.scale})`, 'scale(1)')
                : 'scale(1)';
            this.element.style.filter = 'brightness(1)';
        });
    }

    addToPage(parent = document.body) {
        parent.appendChild(this.element);
        return this;
    }

    updateConfig(newConfig) {
        this.config = { ...this.config, ...newConfig };
        const parent = this.element.parentNode;
        parent.removeChild(this.element);
        this.createBox();
        this.addToPage(parent);
        return this;
    }

    setContent(content) {
        const contentDiv = this.element.querySelector('.glass-box-content');
        if (contentDiv) {
            contentDiv.innerHTML = content;
        }
        return this;
    }
}

// ฟังก์ชันสำหรับสร้างกล่องต่างๆ
function createProfileBox() {
    const config = GLASS_CONFIG.boxes.profile;
    return new GlassBox({
        width: config.width,
        height: config.height,
        blur: GLASS_CONFIG.style.blur,
        theme: 'thai',
        layout: {
            position: 'absolute',
            ...config.position,
            zIndex: config.zIndex
        },
        content: `
            <div style="text-align: center;">
                <img src="/static/images/profile.jpg" style="
                    width: 120px; 
                    height: 120px; 
                    border-radius: 50%;
                    border: 3px solid rgba(255,255,255,0.2);
                    box-shadow: 0 0 20px rgba(0,0,0,0.2);
                ">
                <h2 style="
                    margin-top: 20px;
                    font-family: 'Noto Sans Thai', sans-serif;
                    font-weight: 300;
                    letter-spacing: 1px;
                ">${THEME.content.title}</h2>
                <p style="
                    font-family: 'Noto Sans Thai', sans-serif;
                    color: rgba(255,255,255,0.8);
                ">${THEME.content.subtitle}</p>
                <div style="
                    margin-top: 25px;
                    display: flex;
                    justify-content: center;
                    gap: 20px;
                ">
                    ${THEME.content.menu.map(item => `
                        <a href="#" style="
                            color: white;
                            text-decoration: none;
                            padding: 8px 15px;
                            border: 1px solid rgba(255,255,255,0.2);
                            border-radius: 20px;
                            font-size: 14px;
                            transition: all 0.3s ease;
                        ">${item}</a>
                    `).join('')}
                </div>
                <div style="margin-top: 20px;">
                    <span style="
                        font-size: 14px;
                        color: rgba(255,255,255,0.6);
                    ">ผู้เยี่ยมชม: 1,128</span>
                </div>
            </div>
        `
    });
}

function createChatBox() {
    const config = GLASS_CONFIG.boxes.chat;
    return new GlassBox({
        width: config.width,
        height: config.height,
        blur: GLASS_CONFIG.style.blur,
        layout: {
            position: 'absolute',
            ...config.position,
            zIndex: config.zIndex
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

function createRightStack() {
    const config = GLASS_CONFIG.boxes.stack;
    const container = document.createElement('div');
    Object.assign(container.style, {
        position: 'absolute',
        ...config.container.position,
        display: 'flex',
        flexDirection: 'column',
        gap: config.container.gap,
        width: config.container.width,
        zIndex: config.container.zIndex
    });

    config.items.forEach(item => {
        new GlassBox({
            height: item.height,
            blur: GLASS_CONFIG.style.blur,
            content: `<h3>${item.title}</h3>`
        }).addToPage(container);
    });

    return container;
}