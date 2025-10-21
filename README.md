📋 black.html ประกอบด้วย:

1️⃣ HEAD Section - โหลด CSS และ Config
html<head>
    <!-- Meta Tags -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Profile</title>

    <!-- CSS Files -->
    ├── layout-config.css           (โครงสร้าง Layout 3 คอลัมน์)
    ├── content-alignment.css       (การจัดวางเนื้อหา)
    │
    ├── left-top-config.css         (🟦 ซ้าย-บน: Profile)
    ├── left-mid-config.css         (🟦 ซ้าย-กลาง: Comments)
    ├── left-low-config.css         (🟦 ซ้าย-ล่าง: Music Controls)
    │
    ├── middle-top-config.css       (🟩 กลาง-บน: Platform Boxes)
    ├── middle-config.css           (🟩 กลาง-กลาง: YouTube Player)
    ├── mid-low-config.css          (🟩 กลาง-ล่าง: Caster Cards)
    │
    ├── right-top-config.css        (🟨 ขวา-บน: Header)
    ├── right-mid-config.css        (🟨 ขวา-กลาง: Video List)
    └── right-low-config.css        (🟨 ขวา-ล่าง: Statistics)

    <!-- Inline Style -->
    └── CSS Variables สำหรับ Video Background Blur
</head>

2️⃣ BODY Section - เนื้อหาหลัก
html<body>
    <!-- 1. Audio Element -->
    <audio id="bgMusic" loop>
        └── เพลงพื้นหลัง (thailanddansmile_Music.MP3)
    
    <!-- 2. Video Background -->
    <video class="video-background" autoplay muted loop>
        └── วิดีโอพื้นหลัง (background.mp4) + Blur Effect
    
    <!-- 3. Main Container (3 คอลัมน์) -->
    <div class="container">
        
        <!-- 🟦 กล่องซ้าย -->
        <div class="left">
            ├── left_top.html       (Profile/Logo)
            ├── left_mid.html       (YouTube Comments)
            └── left_low.html       (Music Controls)
        
        <!-- 🟩 กล่องกลาง -->
        <div class="center">
            ├── middle_top.html     (Platform Boxes)
            ├── middle.html         (YouTube Player)
            └── mid-low.html        (Caster Cards)
        
        <!-- 🟨 กล่องขวา -->
        <div class="right">
            ├── right_Box-top.html  (Title/Header)
            ├── right_Box.html      (Video List)
            └── right_Box-low.html  (Statistics)
    </div>
</body>

3️⃣ SCRIPTS Section - JavaScript
javascript<!-- External Script -->
<script src="https://www.youtube.com/iframe_api"></script>

<!-- Inline Scripts -->
<script>
    ├── 1. Global Variables
    │   ├── player (YouTube Player)
    │   ├── musicWasPausedByVideo
    │   ├── originalVolume
    │   └── volumeResumeTimeout
    │
    ├── 2. onYouTubeIframeAPIReady()
    │   └── สร้าง YouTube Player
    │
    ├── 3. onPlayerReady()
    │   └── Setup Video Card Click Listeners
    │
    ├── 4. setupVideoCardListeners()
    │   └── จัดการคลิกเปลี่ยนวิดีโอ
    │
    ├── 5. onPlayerStateChange()
    │   └── ควบคุมเพลงพื้นหลังตามสถานะวิดีโอ
    │       ├── ENDED: หยุดที่ frame แรก + รอ 30 วิ
    │       ├── PLAYING: ปิดเพลงพื้นหลัง
    │       └── PAUSED: รอ 30 วิ แล้วเปิดเพลง
    │
    ├── 6. getYouTubeVideoId()
    │   └── แยก Video ID จาก URL
    │
    ├── 7. Auto-play Background Music
    │   └── เล่นเพลงเมื่อคลิกหน้าจอครั้งแรก
    │
    ├── 8. Window Load Event
    │   └── Initialize YouTube API + Load Comments
    │
    └── 9. loadYouTubeComments()
        └── ดึงคอมเมนท์จาก API แสดงใน left_mid.html
</script>
```

---

## 📊 **สรุปโครงสร้าง:**
```
black.html
│
├── 📦 CSS (12 ไฟล์)
│   ├── 2 ไฟล์ Layout (layout-config, content-alignment)
│   └── 9 ไฟล์ Components (left x3, center x3, right x3)
│
├── 🎬 Media Files
│   ├── background.mp4 (วิดีโอพื้นหลัง)
│   └── thailanddansmile_Music.MP3 (เพลง)
│
├── 🧩 HTML Components (9 ไฟล์)
│   ├── left_top.html, left_mid.html, left_low.html
│   ├── middle_top.html, middle.html, mid-low.html
│   └── right_Box-top.html, right_Box.html, right_Box-low.html
│
└── ⚙️ JavaScript
    ├── YouTube IFrame API
    ├── Music Control Logic
    ├── Video Switching System
    └── Comment Loading System

🎯 หน้าที่หลัก:

โหลด CSS → ตกแต่งทุกส่วน
แสดงวิดีโอพื้นหลัง → background.mp4 + blur
แสดง Layout 3 คอลัมน์ → ซ้าย/กลาง/ขวา
โหลด 9 Components → ส่วนต่างๆ ของเพจ
จัดการ YouTube Player → เล่น/หยุด/เปลี่ยนวิดีโอ
ควบคุมเพลงพื้นหลัง → ปิด/เปิดตามสถานะวิดีโอ
โหลดคอมเมนท์ → ดึงจาก YouTube API


รวม: 1 ไฟล์หลัก + 21 ไฟล์ย่อย (12 CSS + 9 HTML Components)
