"""
FreshSense AI - Reference-Grade Visual Design System
===================================================
Faithfully recreates the visual language, composition, color richness,
3D product presentation, glassmorphic depth, radiant gradients, glowing HUDs,
and typography of the reference UI suite.
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=Outfit:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap');

:root {
    --bg-base: #f0f7ff;
    --text-primary: #0a1024;
    --text-secondary: #334155;
    --text-muted: #64748b;
    --text-subtle: #94a3b8;
    
    /* Vibrant Multi-Color Gradients */
    --grad-primary: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 50%, #8a2be2 100%);
    --grad-home-active: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 45%, #9333ea 100%);
    --grad-mint-emerald: linear-gradient(135deg, #05b187 0%, #15c89b 50%, #3fe1b4 100%);
    --grad-alert-sunset: linear-gradient(135deg, #ff4e50 0%, #f97316 35%, #f43f5e 75%, #fb7185 100%);
    --grad-lemon-lime: linear-gradient(135deg, #fbbf24 0%, #fde047 50%, #84cc16 100%);
    --grad-pepper-cyan: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
    --grad-apple-pink: linear-gradient(135deg, #f43f5e 0%, #ec4899 100%);
    --grad-banana-amber: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
    --grad-greens-mint: linear-gradient(135deg, #10b981 0%, #059669 100%);
    --grad-purple-violet: linear-gradient(135deg, #8b5cf6 0%, #a855f7 50%, #c084fc 100%);
    
    /* Glassmorphism */
    --card-glass: rgba(255, 255, 255, 0.88);
    --card-glass-hover: rgba(255, 255, 255, 0.98);
    --card-border: rgba(255, 255, 255, 0.9);
    
    /* Glows */
    --glow-cyan: rgba(0, 210, 255, 0.4);
    --glow-coral: rgba(255, 78, 80, 0.4);
    --glow-emerald: rgba(16, 185, 129, 0.4);
    --glow-purple: rgba(147, 51, 234, 0.4);
}

/* Global Reset & Base Typography */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--text-primary);
    background-color: var(--bg-base) !important;
}

/* Radiant Pastel Ambient Background */
body {
    background: 
        radial-gradient(circle at 10% 8%, rgba(0, 210, 255, 0.22) 0%, transparent 42%),
        radial-gradient(circle at 90% 12%, rgba(255, 78, 80, 0.2) 0%, transparent 45%),
        radial-gradient(circle at 50% 28%, rgba(16, 185, 129, 0.18) 0%, transparent 48%),
        radial-gradient(circle at 15% 78%, rgba(245, 158, 11, 0.2) 0%, transparent 44%),
        radial-gradient(circle at 88% 82%, rgba(147, 51, 234, 0.22) 0%, transparent 46%),
        linear-gradient(180deg, #f0f7ff 0%, #e6fcf5 25%, #f5f0ff 60%, #fff1f2 100%) !important;
    background-attachment: fixed !important;
}

/* Main Container Max Width for Wide Layout */
.block-container {
    max-width: 1440px !important;
    padding: 1.2rem 2.2rem 5rem 2.2rem !important;
}

/* Header cleanup */
header[data-testid="stHeader"] {
    background: transparent !important;
}

/* ------------------------------------------------------------- */
/* 1. DARK OBSIDIAN SIDEBAR (Matching Reference)                */
/* ------------------------------------------------------------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060b18 0%, #0b152d 40%, #15102d 80%, #091325 100%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    box-shadow: 6px 0 35px rgba(0, 0, 0, 0.35) !important;
}

section[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1.1rem !important;
}

/* Sidebar Brand Header */
.sidebar-brand-box {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 12px;
    margin-bottom: 22px;
}

.sidebar-brand-icon {
    width: 38px;
    height: 38px;
    border-radius: 12px;
    background: linear-gradient(135deg, #00d2ff 0%, #10b981 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    box-shadow: 0 0 16px rgba(0, 210, 255, 0.6);
}

.sidebar-brand-text {
    font-family: 'Outfit', sans-serif;
    font-size: 1.25rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.01em;
    line-height: 1.1;
}

.sidebar-brand-tagline {
    font-size: 0.72rem;
    color: #93c5fd;
    font-weight: 600;
    letter-spacing: 0.02em;
}

/* Sidebar Navigation Items */
.sidebar-nav-active-pill {
    background: var(--grad-home-active) !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    border-radius: 999px !important;
    padding: 10px 18px !important;
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    box-shadow: 0 4px 20px rgba(0, 210, 255, 0.45), 0 0 15px rgba(147, 51, 234, 0.35) !important;
    margin-bottom: 8px !important;
    transition: all 0.25s ease !important;
}

.sidebar-nav-item {
    background: rgba(255, 255, 255, 0.04);
    color: #cbd5e1;
    font-weight: 600;
    border-radius: 999px;
    padding: 10px 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 8px;
    border: 1px solid transparent;
    transition: all 0.25s ease;
    cursor: pointer;
}

.sidebar-nav-item:hover {
    background: rgba(255, 255, 255, 0.1);
    color: #ffffff;
    border-color: rgba(255, 255, 255, 0.15);
    transform: translateX(4px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Sidebar Custom Radio buttons styling */
section[data-testid="stSidebar"] div[role="radiogroup"] > label {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 999px !important;
    padding: 9px 16px !important;
    margin-bottom: 6px !important;
    color: #cbd5e1 !important;
    font-weight: 600 !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
    background: rgba(255, 255, 255, 0.1) !important;
    color: #ffffff !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
    transform: translateX(4px) !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"] {
    background: var(--grad-home-active) !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    border-color: rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 4px 20px rgba(0, 210, 255, 0.45), 0 0 15px rgba(147, 51, 234, 0.35) !important;
}

/* Sidebar Lower Container Card */
.sidebar-container-preview {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 18px;
    padding: 14px 12px;
    margin-top: 24px;
    text-align: center;
    backdrop-filter: blur(16px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
}

.sidebar-container-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.4);
    color: #34d399;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 999px;
    margin-top: 6px;
}

/* ------------------------------------------------------------- */
/* 2. TOP HEADER CONTROLS (Matching Reference)                  */
/* ------------------------------------------------------------- */
.top-header-pill-bar {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 12px;
    margin-bottom: 18px;
}

.top-node-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255, 255, 255, 0.95);
    border: 1.5px solid rgba(255, 255, 255, 0.95);
    padding: 6px 16px;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 800;
    color: #0f172a;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.top-avatar-circle {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    font-size: 1rem;
    box-shadow: 0 2px 10px rgba(0, 210, 255, 0.4);
}

/* ------------------------------------------------------------- */
/* 3. HERO SECTION & CARDS (Matching Reference Composition)     */
/* ------------------------------------------------------------- */
.brand-hero-title {
    font-family: 'Outfit', sans-serif;
    font-size: 2.8rem;
    font-weight: 900;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #00b4d8 0%, #2563eb 50%, #7c3aed 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
    line-height: 1.1;
}

.brand-hero-desc {
    font-size: 0.95rem;
    color: #475569;
    line-height: 1.5;
    margin-bottom: 16px;
    font-weight: 500;
    max-width: 380px;
}

/* Overall Freshness Card (Mint-Emerald Gradient) */
.overall-freshness-mint-card {
    background: var(--grad-mint-emerald);
    border-radius: 28px;
    padding: 22px 24px;
    color: #ffffff;
    box-shadow: 0 14px 36px rgba(5, 177, 135, 0.32), 0 0 0 1px rgba(255, 255, 255, 0.4) inset;
    display: flex;
    align-items: center;
    gap: 20px;
    position: relative;
    overflow: hidden;
    margin-top: 8px;
}

.overall-freshness-mint-card::after {
    content: '';
    position: absolute;
    top: -40px;
    right: -40px;
    width: 140px;
    height: 140px;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.3) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}

.overall-donut-wrapper {
    position: relative;
    width: 112px;
    height: 112px;
    flex-shrink: 0;
}

.overall-donut-text {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.7rem;
    font-weight: 900;
    font-family: 'Outfit', sans-serif;
    color: #ffffff;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

/* Freshness Alert Banner (Sunset Coral Gradient) */
.alert-banner-sunset {
    background: var(--grad-alert-sunset);
    border-radius: 28px;
    padding: 22px 24px;
    color: #ffffff;
    box-shadow: 0 14px 38px rgba(255, 78, 80, 0.35), 0 0 0 1px rgba(255, 255, 255, 0.4) inset;
    position: relative;
    overflow: hidden;
    height: 100%;
}

.alert-banner-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.76rem;
    font-weight: 900;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    background: rgba(255, 255, 255, 0.28);
    backdrop-filter: blur(8px);
    padding: 4px 12px;
    border-radius: 999px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* ------------------------------------------------------------- */
/* 4. 6-COLUMN YOUR FOOD CARDS (Matching Reference Visuals)     */
/* ------------------------------------------------------------- */
.food-grid-wrapper {
    margin: 22px 0 14px 0;
}

.food-card-tall {
    background: rgba(255, 255, 255, 0.94);
    border: 1.5px solid rgba(255, 255, 255, 0.95);
    border-radius: 24px;
    padding: 16px 14px 14px 14px;
    text-align: center;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.05);
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.food-card-tall:hover {
    transform: translateY(-8px);
    box-shadow: 0 18px 38px rgba(0, 0, 0, 0.12);
    border-color: #ffffff;
}

.food-card-header-glow {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 95px;
    border-top-left-radius: 22px;
    border-top-right-radius: 22px;
    opacity: 0.85;
    z-index: 0;
}

.food-card-tomato .food-card-header-glow { background: radial-gradient(circle at 50% 30%, #ff8a80 0%, #ff5252 60%, transparent 100%); }
.food-card-lemon .food-card-header-glow { background: radial-gradient(circle at 50% 30%, #fff59d 0%, #fbc02d 60%, transparent 100%); }
.food-card-pepper .food-card-header-glow { background: radial-gradient(circle at 50% 30%, #a7f3d0 0%, #10b981 60%, transparent 100%); }
.food-card-apple .food-card-header-glow { background: radial-gradient(circle at 50% 30%, #fbcfe8 0%, #f43f5e 60%, transparent 100%); }
.food-card-banana .food-card-header-glow { background: radial-gradient(circle at 50% 30%, #fde68a 0%, #f59e0b 60%, transparent 100%); }
.food-card-greens .food-card-header-glow { background: radial-gradient(circle at 50% 30%, #bbf7d0 0%, #22c55e 60%, transparent 100%); }

.food-visual-container {
    position: relative;
    z-index: 1;
    font-size: 3.2rem;
    margin-bottom: 6px;
    filter: drop-shadow(0 6px 12px rgba(0, 0, 0, 0.12));
    transition: transform 0.3s ease;
}

.food-card-tall:hover .food-visual-container {
    transform: scale(1.12);
}

.food-title-text {
    font-family: 'Outfit', sans-serif;
    font-size: 1.05rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 2px;
    position: relative;
    z-index: 1;
}

.food-score-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.88rem;
    font-weight: 900;
    color: #0f172a;
    margin-bottom: 6px;
    position: relative;
    z-index: 1;
}

.badge-pill-risk {
    background: #ffe4e6;
    color: #e11d48;
    font-size: 0.72rem;
    font-weight: 900;
    padding: 3px 10px;
    border-radius: 999px;
    border: 1px solid #fecdd3;
    display: inline-block;
}

.badge-pill-fresh {
    background: #dcfce7;
    color: #059669;
    font-size: 0.72rem;
    font-weight: 900;
    padding: 3px 10px;
    border-radius: 999px;
    border: 1px solid #a7f3d0;
    display: inline-block;
}

.badge-pill-monitor {
    background: #fef3c7;
    color: #d97706;
    font-size: 0.72rem;
    font-weight: 900;
    padding: 3px 10px;
    border-radius: 999px;
    border: 1px solid #fde68a;
    display: inline-block;
}

/* ------------------------------------------------------------- */
/* 5. ENVIRONMENT & AI ANALYSIS (Matching Bottom Row)           */
/* ------------------------------------------------------------- */
.env-glass-card {
    background: rgba(255, 255, 255, 0.94);
    border: 1.5px solid rgba(255, 255, 255, 0.95);
    border-radius: 22px;
    padding: 16px 18px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
    transition: all 0.25s ease;
}

.env-glass-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 14px 30px rgba(0, 0, 0, 0.08);
}

.ai-analysis-reference-card {
    background: rgba(255, 255, 255, 0.94);
    border: 1.5px solid rgba(255, 255, 255, 0.95);
    border-radius: 24px;
    padding: 18px 22px;
    box-shadow: 0 10px 30px rgba(139, 92, 246, 0.12);
    display: flex;
    align-items: center;
    gap: 18px;
    position: relative;
    overflow: hidden;
}

.ai-orb-hologram {
    width: 62px;
    height: 62px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, #00d2ff 0%, #3a7bd5 50%, #9333ea 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    font-family: 'Outfit', sans-serif;
    font-weight: 900;
    font-size: 1.25rem;
    box-shadow: 0 0 24px rgba(0, 210, 255, 0.6), 0 0 35px rgba(147, 51, 234, 0.4);
    animation: orbPulseAnim 3s infinite alternate ease-in-out;
    flex-shrink: 0;
}

@keyframes orbPulseAnim {
    0% { transform: scale(0.96); box-shadow: 0 0 18px rgba(0, 210, 255, 0.5); }
    100% { transform: scale(1.06); box-shadow: 0 0 32px rgba(0, 210, 255, 0.8), 0 0 45px rgba(147, 51, 234, 0.6); }
}

/* ------------------------------------------------------------- */
/* 6. FLOATING BOTTOM NAVIGATION BAR                            */
/* ------------------------------------------------------------- */
.bottom-floating-nav-bar {
    position: fixed;
    bottom: 22px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1.5px solid rgba(255, 255, 255, 0.95);
    border-radius: 999px;
    padding: 8px 16px;
    box-shadow: 0 14px 40px rgba(0, 0, 0, 0.12), 0 0 20px rgba(0, 210, 255, 0.15);
    display: flex;
    align-items: center;
    gap: 12px;
    z-index: 9999;
}

.bottom-nav-active-pill {
    background: var(--grad-home-active);
    color: #ffffff !important;
    font-weight: 800;
    padding: 8px 20px;
    border-radius: 999px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    box-shadow: 0 4px 18px rgba(0, 210, 255, 0.45), 0 0 12px rgba(147, 51, 234, 0.35);
}

.bottom-nav-idle-pill {
    color: #475569;
    font-weight: 700;
    padding: 8px 16px;
    border-radius: 999px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    transition: all 0.2s ease;
    cursor: pointer;
}

.bottom-nav-idle-pill:hover {
    background: rgba(0, 0, 0, 0.04);
    color: #0f172a;
}

/* Universal Streamlit Buttons Styling */
div.stButton > button {
    border-radius: 999px !important;
    font-weight: 800 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    padding: 7px 18px !important;
    transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
}

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12) !important;
}

div.stButton > button[kind="primary"] {
    background: var(--grad-home-active) !important;
    border: none !important;
    color: #ffffff !important;
    box-shadow: 0 4px 16px rgba(0, 210, 255, 0.35) !important;
}

/* Custom Food Button Gradients */
.btn-coral div.stButton > button {
    background: linear-gradient(135deg, #ff4e50 0%, #f43f5e 100%) !important;
    color: #ffffff !important;
}
.btn-emerald div.stButton > button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    color: #ffffff !important;
}
.btn-cyan div.stButton > button {
    background: linear-gradient(135deg, #06b6d4 0%, #0284c7 100%) !important;
    color: #ffffff !important;
}
.btn-pink div.stButton > button {
    background: linear-gradient(135deg, #ec4899 0%, #d946ef 100%) !important;
    color: #ffffff !important;
}
.btn-amber div.stButton > button {
    background: linear-gradient(135deg, #f59e0b 0%, #ea580c 100%) !important;
    color: #ffffff !important;
}
</style>
"""

CHIME_AUDIO_SCRIPT = """
<script>
function playFreshnessChime() {
    try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (!AudioContext) return;
        const ctx = new AudioContext();
        
        const now = ctx.currentTime;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        
        osc.type = 'sine';
        osc.frequency.setValueAtTime(587.33, now); // D5
        osc.frequency.exponentialRampToValueAtTime(880.00, now + 0.12); // A5
        osc.frequency.exponentialRampToValueAtTime(1174.66, now + 0.25); // D6
        
        gain.gain.setValueAtTime(0.01, now);
        gain.gain.linearRampToValueAtTime(0.2, now + 0.05);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.55);
        
        osc.connect(gain);
        gain.connect(ctx.destination);
        
        osc.start(now);
        osc.stop(now + 0.6);
    } catch(e) {
        console.log("Audio chime skipped:", e);
    }
}
playFreshnessChime();
</script>
"""
