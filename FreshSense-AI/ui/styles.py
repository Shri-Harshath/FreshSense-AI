"""
FreshSense AI - Premium Animated Design System & Glassmorphism Styles
=====================================================================
Features vibrant color palettes, neon accents, glowing pulse animations,
glassmorphic frosted cards, and modern typography.
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap');

:root {
    --bg-dark: #070b14;
    --bg-card: rgba(15, 23, 42, 0.75);
    --bg-card-hover: rgba(22, 33, 58, 0.9);
    --border-glass: rgba(255, 255, 255, 0.08);
    --border-glow: rgba(16, 185, 129, 0.4);
    
    --neon-green: #10b981;
    --neon-green-glow: rgba(16, 185, 129, 0.4);
    --neon-amber: #f59e0b;
    --neon-amber-glow: rgba(245, 158, 11, 0.4);
    --neon-red: #f43f5e;
    --neon-red-glow: rgba(244, 63, 94, 0.5);
    --neon-cyan: #06b6d4;
    --neon-cyan-glow: rgba(6, 182, 212, 0.4);
    --neon-purple: #a855f7;
    --neon-purple-glow: rgba(168, 85, 247, 0.4);
    
    --text-main: #f8fafc;
    --text-dim: #94a3b8;
    --text-muted: #64748b;
}

html, body, [class*="css"] {
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--text-main);
    background-color: var(--bg-dark);
}

/* Background Ambient Lighting */
body {
    background: radial-gradient(circle at 15% 15%, rgba(16, 185, 129, 0.06) 0%, transparent 40%),
                radial-gradient(circle at 85% 20%, rgba(244, 63, 94, 0.07) 0%, transparent 45%),
                radial-gradient(circle at 50% 80%, rgba(6, 182, 212, 0.05) 0%, transparent 50%),
                #070b14 !important;
    background-attachment: fixed !important;
}

/* Base App Container */
.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 3.5rem !important;
    max-width: 680px !important;
    margin: 0 auto !important;
}

/* Animated Neon Pulse */
@keyframes pulse-red-hero {
    0% {
        box-shadow: 0 0 0 0 rgba(244, 63, 94, 0.6), 0 10px 30px rgba(244, 63, 94, 0.25);
        border-color: rgba(244, 63, 94, 0.7);
    }
    50% {
        box-shadow: 0 0 28px 6px rgba(244, 63, 94, 0.35), 0 14px 45px rgba(244, 63, 94, 0.35);
        border-color: rgba(251, 113, 133, 1);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(244, 63, 94, 0.6), 0 10px 30px rgba(244, 63, 94, 0.25);
        border-color: rgba(244, 63, 94, 0.7);
    }
}

@keyframes bell-ring {
    0%, 100% { transform: rotate(0); }
    12% { transform: rotate(16deg); }
    24% { transform: rotate(-14deg); }
    36% { transform: rotate(12deg); }
    48% { transform: rotate(-8deg); }
    60% { transform: rotate(4deg); }
    72% { transform: rotate(0); }
}

@keyframes live-dot-pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
    70% { transform: scale(1.1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

@keyframes shimmer-bar {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

@keyframes float-badge {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-2px); }
}

/* Smart Device Outer Frame */
.dashboard-device-shell {
    background: rgba(11, 17, 32, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 28px;
    padding: 24px;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 0 0 30px rgba(16, 185, 129, 0.06);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    margin-bottom: 24px;
}

/* Glowing Top Header */
.top-header-wrap {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(15, 23, 42, 0.8) 60%, rgba(6, 182, 212, 0.08) 100%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 16px 22px;
    margin-bottom: 18px;
    backdrop-filter: blur(16px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
}

.brand-title {
    font-size: 1.85rem;
    font-weight: 900;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #ffffff 25%, #34d399 75%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    line-height: 1.15;
}

.brand-tagline {
    font-size: 0.92rem;
    font-weight: 600;
    color: #10b981;
    letter-spacing: 0.02em;
    margin: 2px 0 0 0;
}

.notif-bell-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, rgba(244, 63, 94, 0.25) 0%, rgba(20, 12, 24, 0.85) 100%);
    border: 1px solid rgba(244, 63, 94, 0.55);
    border-radius: 999px;
    padding: 8px 16px;
    color: #ffffff;
    font-weight: 800;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.25s ease;
    box-shadow: 0 0 16px rgba(244, 63, 94, 0.35);
}

.notif-bell-badge:hover {
    transform: scale(1.05);
    box-shadow: 0 0 25px rgba(244, 63, 94, 0.6);
}

.bell-icon {
    font-size: 1.25rem;
    display: inline-block;
    animation: bell-ring 3.5s infinite ease-in-out;
}

/* Container Status Bar */
.container-status-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(16, 185, 129, 0.25);
    border-radius: 16px;
    padding: 12px 18px;
    margin-bottom: 18px;
    backdrop-filter: blur(14px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
}

.status-dot-pulse {
    width: 11px;
    height: 11px;
    border-radius: 50%;
    display: inline-block;
    background-color: #10b981;
    animation: live-dot-pulse 2s infinite ease-in-out;
}

/* Hero Freshness Alert Card */
.freshness-alert-hero {
    background: linear-gradient(135deg, rgba(244, 63, 94, 0.24) 0%, rgba(26, 12, 24, 0.95) 55%, rgba(15, 23, 42, 0.98) 100%);
    border: 1.5px solid rgba(244, 63, 94, 0.7);
    border-radius: 22px;
    padding: 24px 26px;
    margin-bottom: 22px;
    backdrop-filter: blur(20px);
    animation: pulse-red-hero 3s infinite ease-in-out;
    position: relative;
    overflow: hidden;
}

.freshness-alert-hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(244, 63, 94, 0.15) 0%, transparent 65%);
    pointer-events: none;
}

.alert-header-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.85rem;
    font-weight: 900;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #fca5a5;
    margin-bottom: 10px;
}

.alert-food-title {
    font-size: 2.1rem;
    font-weight: 900;
    color: #ffffff;
    margin: 0 0 2px 0;
    display: flex;
    align-items: center;
    gap: 12px;
    letter-spacing: -0.02em;
}

.alert-food-sub {
    font-size: 1.15rem;
    font-weight: 600;
    color: #f87171;
    margin-bottom: 16px;
}

.alert-stats-box {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(244, 63, 94, 0.3);
    border-radius: 16px;
    padding: 14px 22px;
    margin: 14px 0 16px 0;
}

.alert-stat-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.6rem;
    font-weight: 900;
    color: #ffffff;
}

.alert-stat-label {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    color: #fca5a5;
    letter-spacing: 0.06em;
    margin-bottom: 2px;
}

/* Freshness Progress Meter */
.freshness-meter-wrap {
    height: 8px;
    width: 100%;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 999px;
    overflow: hidden;
    margin: 8px 0 16px 0;
}

.freshness-meter-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #f43f5e 0%, #f59e0b 50%, #10b981 100%);
    background-size: 200% 100%;
    animation: shimmer-bar 3s infinite linear;
}

/* Your Food Section */
.section-header-title {
    font-size: 1.25rem;
    font-weight: 900;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #f8fafc;
    margin: 26px 0 12px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.food-row-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(18, 26, 45, 0.65);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 18px;
    padding: 14px 18px;
    margin-bottom: 10px;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    cursor: pointer;
}

.food-row-item:hover {
    background: rgba(28, 40, 70, 0.85);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateX(4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
}

.food-row-risk {
    border-left: 4.5px solid var(--neon-red) !important;
    background: linear-gradient(90deg, rgba(244, 63, 94, 0.14) 0%, rgba(18, 26, 45, 0.7) 100%) !important;
}

.food-row-monitor {
    border-left: 4.5px solid var(--neon-amber) !important;
    background: linear-gradient(90deg, rgba(245, 158, 11, 0.12) 0%, rgba(18, 26, 45, 0.7) 100%) !important;
}

.food-row-fresh {
    border-left: 4.5px solid var(--neon-green) !important;
    background: linear-gradient(90deg, rgba(16, 185, 129, 0.1) 0%, rgba(18, 26, 45, 0.7) 100%) !important;
}

/* Neon Badges */
.badge-neon-risk {
    background: rgba(244, 63, 94, 0.18);
    color: #fb7185;
    border: 1px solid rgba(244, 63, 94, 0.55);
    padding: 5px 14px;
    border-radius: 999px;
    font-size: 0.84rem;
    font-weight: 800;
    letter-spacing: 0.03em;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    box-shadow: 0 0 14px rgba(244, 63, 94, 0.35);
}

.badge-neon-fresh {
    background: rgba(16, 185, 129, 0.18);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.55);
    padding: 5px 14px;
    border-radius: 999px;
    font-size: 0.84rem;
    font-weight: 800;
    letter-spacing: 0.03em;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    box-shadow: 0 0 14px rgba(16, 185, 129, 0.35);
}

.badge-neon-monitor {
    background: rgba(245, 158, 11, 0.18);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.55);
    padding: 5px 14px;
    border-radius: 999px;
    font-size: 0.84rem;
    font-weight: 800;
    letter-spacing: 0.03em;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    box-shadow: 0 0 14px rgba(245, 158, 11, 0.35);
}

/* Sensor Conditions 3-Card Grid */
.sensor-conditions-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 24px;
}

.sensor-box-card {
    background: linear-gradient(135deg, rgba(18, 26, 45, 0.85) 0%, rgba(10, 15, 28, 0.95) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 16px 14px;
    text-align: center;
    backdrop-filter: blur(14px);
    transition: all 0.25s ease;
}

.sensor-box-card:hover {
    border-color: rgba(6, 182, 212, 0.45);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(6, 182, 212, 0.2);
}

.sensor-value-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.45rem;
    font-weight: 900;
    color: #ffffff;
    line-height: 1.15;
    margin-bottom: 4px;
}

.sensor-label-text {
    font-size: 0.82rem;
    font-weight: 800;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* Notification Alert Cards */
.notif-item {
    background: rgba(18, 26, 45, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 16px 20px;
    margin-bottom: 12px;
    backdrop-filter: blur(14px);
    transition: all 0.22s ease;
}

.notif-critical {
    border-left: 4px solid var(--neon-red) !important;
    background: linear-gradient(90deg, rgba(244, 63, 94, 0.15) 0%, rgba(18, 26, 45, 0.75) 100%) !important;
    box-shadow: 0 4px 20px rgba(244, 63, 94, 0.2);
}

.notif-warning {
    border-left: 4px solid var(--neon-amber) !important;
    background: linear-gradient(90deg, rgba(245, 158, 11, 0.12) 0%, rgba(18, 26, 45, 0.75) 100%) !important;
}

.notif-info {
    border-left: 4px solid var(--neon-cyan) !important;
    background: linear-gradient(90deg, rgba(6, 182, 212, 0.1) 0%, rgba(18, 26, 45, 0.75) 100%) !important;
}

/* Streamlit Button Overrides */
div.stButton > button {
    border-radius: 14px !important;
    font-weight: 800 !important;
    letter-spacing: 0.02em !important;
    padding: 10px 20px !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    background: rgba(22, 33, 58, 0.8) !important;
    color: #f8fafc !important;
}

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    border-color: rgba(16, 185, 129, 0.6) !important;
    box-shadow: 0 6px 22px rgba(16, 185, 129, 0.35) !important;
    background: rgba(30, 45, 78, 0.95) !important;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    border: 1px solid rgba(16, 185, 129, 0.8) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4) !important;
}

div.stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 26px rgba(16, 185, 129, 0.65) !important;
    transform: translateY(-2px) !important;
}

/* Navigation Dock Buttons */
.nav-dock-wrap {
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    padding: 10px 14px;
    margin-top: 24px;
    backdrop-filter: blur(24px);
    box-shadow: 0 10px 35px rgba(0, 0, 0, 0.5);
}

/* Hide default streamlit chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""

CHIME_AUDIO_SCRIPT = """
<script>
function playAlertChime() {
    try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (!AudioContext) return;
        const ctx = new AudioContext();
        
        // Two-tone smart alert chime (880Hz -> 1174Hz)
        const osc1 = ctx.createOscillator();
        const gain1 = ctx.createGain();
        osc1.type = 'sine';
        osc1.frequency.setValueAtTime(880, ctx.currentTime); // A5
        osc1.frequency.exponentialRampToValueAtTime(1174.66, ctx.currentTime + 0.15); // D6
        
        gain1.gain.setValueAtTime(0.3, ctx.currentTime);
        gain1.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.6);
        
        osc1.connect(gain1);
        gain1.connect(ctx.destination);
        
        osc1.start();
        osc1.stop(ctx.currentTime + 0.6);
    } catch(e) {
        console.log("AudioContext notice:", e);
    }
}
</script>
"""
