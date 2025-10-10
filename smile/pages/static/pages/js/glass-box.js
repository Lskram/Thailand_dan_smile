// ==============================================
// คลาสสำหรับสร้างกล่องใส (Glass Container)
// ============================================== 
class GlassBox {
    constructor(options = {}) {
        // ค่าเริ่มต้นของกล่อง
        this.config = {
            width: options.width || 300,           // ความกว้าง (px)
            height: options.height || 200,         // ความสูง (px)
            background: options.background || 'rgba(255, 255, 255, 0.1)',  // สีพื้นหลัง
            borderColor: options.borderColor || 'rgba(255, 255, 255, 0.2)', // สีขอบ
            blur: options.blur || 10,              // ความเบลอ (px)
            borderRadius: options.borderRadius || 15, // ความโค้งของมุม (px)
            borderWidth: options.borderWidth || 1,  // ความหนาของขอบ (px)
            x: options.x || 50,                    // ตำแหน่ง X จากขอบซ้าย (px)
            y: options.y || 50,                    // ตำแหน่ง Y จากขอบบน (px)
            shadowColor: options.shadowColor || 'rgba(0, 0, 0, 0.2)', // สีเงา
            shadowBlur: options.shadowBlur || 15,   // ความเบลอของเงา (px)
            content: options.content || '',         // เนื้อหาภายในกล่อง (HTML)
            gradient: options.gradient || false,    // เปิด/ปิดการไล่ระดับสี
            glareEffect: options.glareEffect || false // เปิด/ปิดเอฟเฟกต์แสงสะท้อน
        };

        this.element = null;
        this.createBox();
    }

    // สร้างกล่อง
    createBox() {
        // สร้าง element
        this.element = document.createElement('div');
        this.element.className = 'glass-box';
        
        // กำหนดสไตล์พื้นฐาน
        const baseStyle = {
            position: 'absolute',
            width: this.config.width + 'px',
            height: this.config.height + 'px',
            left: this.config.x + 'px',
            top: this.config.y + 'px',
            background: this.config.background,
            borderRadius: this.config.borderRadius + 'px',
            border: `${this.config.borderWidth}px solid ${this.config.borderColor}`,
            backdropFilter: `blur(${this.config.blur}px)`,
            boxShadow: `0 0 ${this.config.shadowBlur}px ${this.config.shadowColor}`,
            transition: 'all 0.3s ease',
            overflow: 'hidden'
        };

        // ใส่สไตล์ให้กล่อง
        Object.assign(this.element.style, baseStyle);

        // เพิ่มการไล่ระดับสีถ้าเปิดใช้งาน
        if (this.config.gradient) {
            this.element.style.background = `
                linear-gradient(
                    135deg,
                    rgba(255, 255, 255, 0.2) 0%,
                    rgba(255, 255, 255, 0.1) 100%
                )
            `;
        }

        // เพิ่มเอฟเฟกต์แสงสะท้อนถ้าเปิดใช้งาน
        if (this.config.glareEffect) {
            const glare = document.createElement('div');
            glare.style.cssText = `
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: linear-gradient(
                    45deg,
                    rgba(255, 255, 255, 0.2) 0%,
                    rgba(255, 255, 255, 0) 60%
                );
                transform: rotate(35deg);
                pointer-events: none;
            `;
            this.element.appendChild(glare);
        }

        // ใส่เนื้อหา
        if (this.config.content) {
            const contentDiv = document.createElement('div');
            contentDiv.className = 'glass-box-content';
            contentDiv.style.cssText = `
                position: relative;
                z-index: 1;
                padding: 20px;
                color: white;
            `;
            contentDiv.innerHTML = this.config.content;
            this.element.appendChild(contentDiv);
        }

        // เพิ่มเอฟเฟกต์ hover
        this.addHoverEffect();
    }

    // เพิ่มเอฟเฟกต์เมื่อ hover
    addHoverEffect() {
        this.element.addEventListener('mouseenter', () => {
            this.element.style.transform = 'scale(1.02)';
            this.element.style.boxShadow = `
                0 0 ${this.config.shadowBlur * 1.5}px ${this.config.shadowColor}
            `;
        });

        this.element.addEventListener('mouseleave', () => {
            this.element.style.transform = 'scale(1)';
            this.element.style.boxShadow = `
                0 0 ${this.config.shadowBlur}px ${this.config.shadowColor}
            `;
        });
    }

    // เพิ่มกล่องลงในหน้าเว็บ
    addToPage() {
        document.body.appendChild(this.element);
        return this;
    }

    // อัพเดทค่าคอนฟิก
    updateConfig(newConfig) {
        this.config = { ...this.config, ...newConfig };
        document.body.removeChild(this.element);
        this.createBox();
        this.addToPage();
        return this;
    }

    // ย้ายตำแหน่ง
    moveTo(x, y) {
        this.element.style.left = x + 'px';
        this.element.style.top = y + 'px';
        return this;
    }

    // เปลี่ยนขนาด
    resize(width, height) {
        this.element.style.width = width + 'px';
        this.element.style.height = height + 'px';
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

// ตัวอย่างการใช้งาน:
/*
const glassBox = new GlassBox({
    width: 400,
    height: 300,
    content: '<h2>Glass Box</h2><p>This is a glass effect box</p>',
    gradient: true,
    glareEffect: true
}).addToPage();

// ปรับแต่งหลังจากสร้าง
glassBox.moveTo(100, 100);
glassBox.resize(500, 400);
glassBox.setContent('New content');
glassBox.updateConfig({ blur: 20, borderRadius: 30 });
*/