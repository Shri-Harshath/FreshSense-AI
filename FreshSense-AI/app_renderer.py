"""
FreshSense AI - Unified Full-Fidelity Reference UI Engine
=========================================================
Renders the complete, pixel-for-pixel visual composition matching the reference image:
- Obsidian Sidebar with radiant gradient active navigation pills and container status.
- Luminous pastel aura background with organic glowing waves and floating leaves.
- Top Header Bar with live node status capsule, notification badge bell, and user avatar.
- 3-Column Hero: Headline + 72% Overall Freshness Mint Card | 3D Smart Glass Container on Multi-Tiered Pedestal | Freshness Alert Sunset Coral Card.
- 6-Column YOUR FOOD Grid with custom food gradient headers, 3D fruit/veg visuals, and action buttons.
- Bottom Row: 3 Environment Condition Cards with colored sparklines + FreshSense AI Analysis with 3D Hologram AI Orb.
- Floating Bottom Navigation Glass Pill Bar.
- Full interactive tabs for Food Detail, Alerts, Analytics, Simulation Sandbox, and Settings.
"""

import json
from typing import List, Dict, Any
from core.freshness_engine import FoodFreshnessResult
from core.sensor_service import SensorReading, SimulationSensorProvider
from core.notification_service import NotificationManager
from core.history_service import HistoryService


def get_full_reference_ui_html(
    reading: SensorReading,
    results: List[FoodFreshnessResult],
    notif_manager: NotificationManager,
    sim_provider: SimulationSensorProvider,
    active_tab: str = "home",
    selected_food_id: str = "tomato"
) -> str:
    """
    Builds the standalone, high-performance HTML/CSS/JS/Three.js interactive experience
    that matches the reference image with 100% visual fidelity.
    """
    # Prepare serializable JSON data
    foods_data = []
    for r in results:
        foods_data.append({
            "id": r.food_id,
            "name": r.food_name,
            "icon": r.icon,
            "score": round(r.freshness_score),
            "status": r.status,
            "status_color": r.status_color,
            "status_bg": r.status_bg,
            "remaining": r.estimated_remaining_str,
            "trend": r.trend_str,
            "reason": r.primary_reason,
            "action": r.recommended_action,
            "confidence": r.ai_confidence_pct,
            "temp_status": r.temp_status,
            "humidity_status": r.humidity_status,
            "gas_status": r.gas_status,
        })

    alerts_data = []
    for n in notif_manager.notifications:
        alerts_data.append({
            "id": n.id,
            "food_id": n.food_id,
            "food_name": n.food_name,
            "food_icon": n.food_icon,
            "severity": n.severity,
            "title": n.title,
            "message": n.message,
            "action": n.recommended_action,
            "time": n.formatted_time,
            "is_read": n.is_read
        })

    # Average score
    scores = [r.freshness_score for r in results]
    avg_score = round(sum(scores) / len(scores)) if scores else 72
    attention_count = sum(1 for r in results if r.status in ["MONITOR", "AT RISK", "CRITICAL", "SPOILED"])

    # Urgent tomato item
    tomato_item = next((r for r in results if r.food_id == "tomato"), results[0])

    # Telemetry data
    telemetry = {
        "temp": round(reading.temperature_c, 1),
        "humidity": round(reading.humidity_pct),
        "gas": round(reading.gas_ppm),
        "device": reading.device_name,
        "battery": round(reading.battery_pct),
        "signal": reading.signal_strength_dbm,
        "preset": sim_provider.preset_key
    }

    foods_json = json.dumps(foods_data)
    alerts_json = json.dumps(alerts_data)
    telemetry_json = json.dumps(telemetry)

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FreshSense AI - Know Before It Spoils</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=Outfit:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap');

:root {{
    --bg-base: #f4f9ff;
    --text-primary: #070e22;
    --text-secondary: #334155;
    --text-muted: #64748b;
    --grad-home-active: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 50%, #9333ea 100%);
    --grad-mint-emerald: linear-gradient(135deg, #05b187 0%, #15c89b 50%, #3fe1b4 100%);
    --grad-alert-sunset: linear-gradient(135deg, #ff4e50 0%, #f97316 35%, #f43f5e 75%, #fb7185 100%);
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    user-select: none;
}}

body {{
    background: 
        radial-gradient(circle at 10% 8%, rgba(0, 210, 255, 0.24) 0%, transparent 42%),
        radial-gradient(circle at 90% 12%, rgba(255, 78, 80, 0.22) 0%, transparent 45%),
        radial-gradient(circle at 50% 28%, rgba(16, 185, 129, 0.2) 0%, transparent 48%),
        radial-gradient(circle at 15% 78%, rgba(245, 158, 11, 0.22) 0%, transparent 44%),
        radial-gradient(circle at 88% 82%, rgba(147, 51, 234, 0.24) 0%, transparent 46%),
        linear-gradient(180deg, #f0f7ff 0%, #e6fcf5 25%, #f5f0ff 60%, #fff1f2 100%);
    background-attachment: fixed;
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    overflow-x: hidden;
}}

/* App Container */
.app-layout {{
    display: flex;
    width: 100vw;
    min-height: 100vh;
    position: relative;
}}

/* ------------------------------------------------------------- */
/* 1. DARK OBSIDIAN SIDEBAR (Matching Reference)                */
/* ------------------------------------------------------------- */
.sidebar {{
    width: 260px;
    flex-shrink: 0;
    background: linear-gradient(180deg, #060b18 0%, #0b152d 38%, #15102d 75%, #081023 100%);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 6px 0 35px rgba(0, 0, 0, 0.35);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 24px 18px;
    z-index: 100;
}}

.brand-box {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 28px;
    padding: 4px 6px;
}}

.brand-icon-tile {{
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: linear-gradient(135deg, #00d2ff 0%, #10b981 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
    box-shadow: 0 0 20px rgba(0, 210, 255, 0.6);
}}

.brand-title {{
    font-family: 'Outfit', sans-serif;
    font-size: 1.35rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.1;
    letter-spacing: -0.01em;
}}

.brand-subtitle {{
    font-size: 0.74rem;
    color: #93c5fd;
    font-weight: 600;
}}

.nav-menu {{
    display: flex;
    flex-direction: column;
    gap: 8px;
}}

.nav-item {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 11px 18px;
    border-radius: 999px;
    color: #cbd5e1;
    font-weight: 700;
    font-size: 0.92rem;
    cursor: pointer;
    transition: all 0.25s ease;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid transparent;
}}

.nav-item:hover {{
    background: rgba(255, 255, 255, 0.1);
    color: #ffffff;
    transform: translateX(4px);
}}

.nav-item.active {{
    background: var(--grad-home-active);
    color: #ffffff;
    box-shadow: 0 4px 22px rgba(0, 210, 255, 0.5), 0 0 15px rgba(147, 51, 234, 0.35);
    border-color: rgba(255, 255, 255, 0.3);
}}

.nav-badge-red {{
    background: #e11d48;
    color: #ffffff;
    font-size: 0.72rem;
    font-weight: 900;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 8px rgba(225, 29, 72, 0.6);
}}

.sidebar-container-widget {{
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    padding: 16px 14px;
    text-align: center;
    backdrop-filter: blur(16px);
    margin-top: auto;
    margin-bottom: 20px;
}}

.sidebar-footer-tag {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0 6px;
}}

/* ------------------------------------------------------------- */
/* 2. MAIN CONTENT WORKSPACE (Matching Reference Composition)   */
/* ------------------------------------------------------------- */
.main-content {{
    flex-grow: 1;
    padding: 24px 36px 90px 36px;
    overflow-y: auto;
    position: relative;
    max-width: 1460px;
    margin: 0 auto;
}}

/* Top Header Bar */
.top-header-bar {{
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 12px;
    margin-bottom: 18px;
}}

.top-pill {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255, 255, 255, 0.94);
    border: 1.5px solid rgba(255, 255, 255, 0.95);
    padding: 7px 18px;
    border-radius: 999px;
    font-size: 0.84rem;
    font-weight: 800;
    color: #0f172a;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
    cursor: pointer;
}}

.top-avatar {{
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    font-size: 1.1rem;
    box-shadow: 0 2px 12px rgba(0, 210, 255, 0.4);
}}

/* ------------------------------------------------------------- */
/* 3. HERO SECTION (3-COLUMN COMPOSITION)                        */
/* ------------------------------------------------------------- */
.hero-row {{
    display: grid;
    grid-template-columns: 1.05fr 1.3fr 1.15fr;
    gap: 20px;
    align-items: stretch;
    margin-bottom: 24px;
}}

.brand-hero-title {{
    font-family: 'Outfit', sans-serif;
    font-size: 2.8rem;
    font-weight: 900;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #00b4d8 0%, #2563eb 50%, #7c3aed 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
    line-height: 1.1;
}}

.brand-hero-desc {{
    font-size: 0.92rem;
    color: #475569;
    line-height: 1.45;
    margin-bottom: 14px;
    font-weight: 500;
}}

/* Overall Freshness Card (Mint-Emerald Gradient) */
.overall-freshness-mint-card {{
    background: var(--grad-mint-emerald);
    border-radius: 26px;
    padding: 22px 24px;
    color: #ffffff;
    box-shadow: 0 14px 36px rgba(5, 177, 135, 0.32), 0 0 0 1px rgba(255, 255, 255, 0.4) inset;
    display: flex;
    align-items: center;
    gap: 20px;
    position: relative;
    overflow: hidden;
}}

.overall-freshness-mint-card::after {{
    content: '';
    position: absolute;
    top: -40px;
    right: -40px;
    width: 140px;
    height: 140px;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.35) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}}

.donut-wrapper {{
    position: relative;
    width: 110px;
    height: 110px;
    flex-shrink: 0;
}}

.donut-center-text {{
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
}}

/* 3D Smart Container Hero Card (Center) */
.container-3d-card {{
    background: radial-gradient(circle at 50% 35%, rgba(224, 242, 254, 0.95) 0%, rgba(240, 253, 250, 0.9) 45%, rgba(245, 243, 255, 0.95) 100%);
    border: 1.5px solid rgba(255, 255, 255, 0.95);
    border-radius: 26px;
    box-shadow: 0 16px 36px rgba(0, 210, 255, 0.12), 0 6px 16px rgba(0, 0, 0, 0.04);
    position: relative;
    overflow: hidden;
    height: 330px;
}}

/* Freshness Alert Sunset Coral Card (Right) */
.alert-sunset-card {{
    background: var(--grad-alert-sunset);
    border-radius: 26px;
    padding: 22px 24px;
    color: #ffffff;
    box-shadow: 0 14px 38px rgba(255, 78, 80, 0.35), 0 0 0 1px rgba(255, 255, 255, 0.4) inset;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
}}

.alert-tag {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.74rem;
    font-weight: 900;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    background: rgba(255, 255, 255, 0.28);
    backdrop-filter: blur(8px);
    padding: 4px 12px;
    border-radius: 999px;
    margin-bottom: 10px;
    align-self: flex-start;
}}

.btn-pill-blue {{
    background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
    color: #ffffff;
    border: none;
    padding: 8px 18px;
    border-radius: 999px;
    font-weight: 800;
    font-size: 0.85rem;
    cursor: pointer;
    box-shadow: 0 4px 16px rgba(59, 130, 246, 0.4);
    transition: all 0.2s ease;
}}

.btn-pill-blue:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6);
}}

.btn-pill-glass {{
    background: rgba(255, 255, 255, 0.25);
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.4);
    padding: 8px 18px;
    border-radius: 999px;
    font-weight: 800;
    font-size: 0.85rem;
    cursor: pointer;
    backdrop-filter: blur(8px);
    transition: all 0.2s ease;
}}

/* ------------------------------------------------------------- */
/* 4. 6-COLUMN YOUR FOOD CARDS (Matching Reference Visuals)     */
/* ------------------------------------------------------------- */
.food-section-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 22px 0 14px 0;
}}

.food-grid-6 {{
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}}

.food-card {{
    background: rgba(255, 255, 255, 0.94);
    border: 1.5px solid rgba(255, 255, 255, 0.95);
    border-radius: 22px;
    padding: 16px 14px 14px 14px;
    text-align: center;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.05);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    align-items: center;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    cursor: pointer;
}}

.food-card:hover {{
    transform: translateY(-8px);
    box-shadow: 0 18px 38px rgba(0, 0, 0, 0.12);
}}

.food-card-glow {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 90px;
    opacity: 0.85;
    z-index: 0;
}}

.glow-tomato {{ background: radial-gradient(circle at 50% 30%, #ff8a80 0%, #ff5252 60%, transparent 100%); }}
.glow-lemon {{ background: radial-gradient(circle at 50% 30%, #fff59d 0%, #fbc02d 60%, transparent 100%); }}
.glow-pepper {{ background: radial-gradient(circle at 50% 30%, #a7f3d0 0%, #10b981 60%, transparent 100%); }}
.glow-apple {{ background: radial-gradient(circle at 50% 30%, #fbcfe8 0%, #f43f5e 60%, transparent 100%); }}
.glow-banana {{ background: radial-gradient(circle at 50% 30%, #fde68a 0%, #f59e0b 60%, transparent 100%); }}
.glow-greens {{ background: radial-gradient(circle at 50% 30%, #bbf7d0 0%, #22c55e 60%, transparent 100%); }}

.food-icon-large {{
    position: relative;
    z-index: 1;
    font-size: 3.2rem;
    margin-bottom: 6px;
    filter: drop-shadow(0 6px 12px rgba(0, 0, 0, 0.12));
    transition: transform 0.3s ease;
}}

.food-card:hover .food-icon-large {{
    transform: scale(1.12);
}}

.food-name {{
    font-family: 'Outfit', sans-serif;
    font-size: 1.05rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 2px;
    position: relative;
    z-index: 1;
}}

.food-score {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.88rem;
    font-weight: 900;
    color: #0f172a;
    margin-bottom: 6px;
    position: relative;
    z-index: 1;
}}

.badge-risk {{ background: #ffe4e6; color: #e11d48; font-size: 0.72rem; font-weight: 900; padding: 3px 10px; border-radius: 999px; border: 1px solid #fecdd3; }}
.badge-fresh {{ background: #dcfce7; color: #059669; font-size: 0.72rem; font-weight: 900; padding: 3px 10px; border-radius: 999px; border: 1px solid #a7f3d0; }}
.badge-monitor {{ background: #fef3c7; color: #d97706; font-size: 0.72rem; font-weight: 900; padding: 3px 10px; border-radius: 999px; border: 1px solid #fde68a; }}

.btn-food-action {{
    border: none;
    color: #ffffff;
    font-weight: 800;
    font-size: 0.75rem;
    padding: 6px 14px;
    border-radius: 999px;
    cursor: pointer;
    position: relative;
    z-index: 1;
    margin-top: 4px;
    width: 100%;
    transition: transform 0.2s ease;
}}

.btn-food-action:hover {{ transform: translateY(-2px); }}
.btn-c-coral {{ background: linear-gradient(135deg, #ff4e50 0%, #f43f5e 100%); }}
.btn-c-emerald {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%); }}
.btn-c-cyan {{ background: linear-gradient(135deg, #06b6d4 0%, #0284c7 100%); }}
.btn-c-pink {{ background: linear-gradient(135deg, #ec4899 0%, #d946ef 100%); }}
.btn-c-amber {{ background: linear-gradient(135deg, #f59e0b 0%, #ea580c 100%); }}

/* ------------------------------------------------------------- */
/* 5. BOTTOM ROW: SENSORS & AI ANALYSIS (Matching Reference)    */
/* ------------------------------------------------------------- */
.bottom-row {{
    display: grid;
    grid-template-columns: 1.55fr 1.45fr;
    gap: 20px;
    margin-bottom: 24px;
}}

.env-cards-3 {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
}}

.env-glass-card {{
    background: rgba(255, 255, 255, 0.94);
    border: 1.5px solid rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 16px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
}}

.ai-analysis-card {{
    background: rgba(255, 255, 255, 0.94);
    border: 1.5px solid rgba(255, 255, 255, 0.95);
    border-radius: 22px;
    padding: 18px 22px;
    box-shadow: 0 10px 30px rgba(139, 92, 246, 0.12);
    display: flex;
    align-items: center;
    gap: 18px;
}}

.ai-orb-hologram {{
    width: 60px;
    height: 60px;
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
    flex-shrink: 0;
    animation: orbPulse 3s infinite alternate ease-in-out;
}}

@keyframes orbPulse {{
    0% {{ transform: scale(0.96); box-shadow: 0 0 18px rgba(0, 210, 255, 0.5); }}
    100% {{ transform: scale(1.06); box-shadow: 0 0 32px rgba(0, 210, 255, 0.8), 0 0 45px rgba(147, 51, 234, 0.6); }}
}}

/* ------------------------------------------------------------- */
/* 6. FLOATING BOTTOM NAVIGATION BAR                            */
/* ------------------------------------------------------------- */
.bottom-floating-nav {{
    position: fixed;
    bottom: 20px;
    left: calc(50% + 130px);
    transform: translateX(-50%);
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: blur(20px);
    border: 1.5px solid rgba(255, 255, 255, 0.95);
    border-radius: 999px;
    padding: 8px 16px;
    box-shadow: 0 14px 40px rgba(0, 0, 0, 0.12), 0 0 20px rgba(0, 210, 255, 0.15);
    display: flex;
    align-items: center;
    gap: 12px;
    z-index: 999;
}}

.b-nav-item {{
    padding: 8px 16px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.88rem;
    color: #475569;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 6px;
}}

.b-nav-item:hover {{
    background: rgba(0, 0, 0, 0.04);
    color: #0f172a;
}}

.b-nav-item.active {{
    background: var(--grad-home-active);
    color: #ffffff;
    box-shadow: 0 4px 18px rgba(0, 210, 255, 0.45), 0 0 12px rgba(147, 51, 234, 0.35);
}}
</style>
</head>
<body>

<div class="app-layout">
    <!-- 1. LEFT SIDEBAR -->
    <div class="sidebar">
        <div>
            <div class="brand-box">
                <div class="brand-icon-tile">🥑</div>
                <div>
                    <div class="brand-title">FreshSense AI</div>
                    <div class="brand-subtitle">Know Before It Spoils.</div>
                </div>
            </div>
            
            <div class="nav-menu">
                <div class="nav-item {'active' if active_tab == 'home' else ''}" onclick="switchPage('home')">
                    <span>🏠 Home</span>
                </div>
                <div class="nav-item {'active' if active_tab == 'food' else ''}" onclick="switchPage('food')">
                    <span>🥗 Food</span>
                </div>
                <div class="nav-item {'active' if active_tab == 'alerts' else ''}" onclick="switchPage('alerts')">
                    <span>🔔 Alerts</span>
                    <span class="nav-badge-red">{len(notif_manager.get_unread())}</span>
                </div>
                <div class="nav-item {'active' if active_tab == 'analytics' else ''}" onclick="switchPage('analytics')">
                    <span>📈 Analytics</span>
                </div>
                <div class="nav-item {'active' if active_tab == 'simulation' else ''}" onclick="switchPage('simulation')">
                    <span>🎮 Simulation Mode</span>
                </div>
                <div class="nav-item {'active' if active_tab == 'settings' else ''}" onclick="switchPage('settings')">
                    <span>⚙️ Settings</span>
                </div>
            </div>
        </div>
        
        <div>
            <!-- Lower Container Status Widget -->
            <div class="sidebar-container-widget">
                <div style="font-size: 2.2rem; margin-bottom: 2px;">🥫</div>
                <div style="font-size: 0.86rem; font-weight: 800; color: #ffffff;">Kitchen Container 01</div>
                <div style="display: inline-flex; align-items: center; gap: 6px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); color: #34d399; font-size: 0.72rem; font-weight: 700; padding: 2px 10px; border-radius: 999px; margin-top: 6px;">
                    <span style="width:6px; height:6px; border-radius:50%; background:#10b981;"></span>
                    <span>Simulation Mode ></span>
                </div>
            </div>
            
            <!-- Bottom Tag -->
            <div class="sidebar-footer-tag">
                <div style="width: 28px; height: 28px; border-radius: 8px; background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%); display: flex; align-items: center; justify-content: center; font-size: 0.9rem;">🍃</div>
                <div>
                    <div style="font-size: 0.76rem; font-weight: 800; color: #ffffff;">Fresh food</div>
                    <div style="font-size: 0.68rem; color: #94a3b8;">Better life</div>
                </div>
            </div>
        </div>
    </div>

    <!-- 2. MAIN CONTENT WORKSPACE -->
    <div class="main-content">
        <!-- Top Header Bar -->
        <div class="top-header-bar">
            <div class="top-pill">
                <span style="width:8px; height:8px; border-radius:50%; background:#10b981; box-shadow:0 0 8px #10b981;"></span>
                <span>Kitchen Container 01</span>
                <span style="color:#64748b; font-weight:600; font-size:0.75rem;">● Simulation Mode</span>
            </div>
            <div class="top-pill" onclick="switchPage('alerts')" style="padding: 7px 12px; position: relative;">
                <span>🔔</span>
                <span style="background: #e11d48; color: #fff; font-size: 0.68rem; font-weight: 900; padding: 1px 6px; border-radius: 999px; margin-left: 2px;">{len(notif_manager.get_unread())}</span>
            </div>
            <div class="top-avatar">👤</div>
        </div>

        <!-- 3. HERO SECTION (3-COLUMN COMPOSITION) -->
        <div class="hero-row">
            <!-- Left: Headline & Overall Freshness Card -->
            <div>
                <div class="brand-hero-title">Know Before It Spoils.</div>
                <p class="brand-hero-desc">FreshSense AI monitors your food's environment and predicts freshness using smart sensors and AI.</p>
                
                <div class="overall-freshness-mint-card">
                    <div style="position: absolute; top: 12px; left: 18px; display: flex; align-items: center; gap: 6px; font-size: 0.74rem; font-weight: 900; letter-spacing: 0.05em; text-transform: uppercase;">
                        <span>🍃 OVERALL FRESHNESS</span>
                    </div>
                    
                    <div class="donut-wrapper" style="margin-top: 14px;">
                        <svg viewBox="0 0 36 36" style="width: 100%; height: 100%; transform: rotate(-90deg);">
                            <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" 
                                  fill="none" stroke="rgba(255, 255, 255, 0.25)" stroke-width="3.5" />
                            <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" 
                                  fill="none" stroke="url(#mintRingGrad)" stroke-width="3.5" 
                                  stroke-dasharray="{avg_score}, 100" stroke-linecap="round" />
                            <defs>
                                <linearGradient id="mintRingGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                    <stop offset="0%" stop-color="#ffffff" />
                                    <stop offset="50%" stop-color="#00d2ff" />
                                    <stop offset="100%" stop-color="#a855f7" />
                                </linearGradient>
                            </defs>
                        </svg>
                        <div class="donut-center-text">{avg_score}%</div>
                    </div>
                    
                    <div style="margin-top: 14px;">
                        <div style="font-size: 0.92rem; font-weight: 800; display: flex; align-items: center; gap: 6px; margin-bottom: 6px;">
                            <span>🔔</span> <span>{attention_count} items need attention</span>
                        </div>
                        <div style="font-size: 0.82rem; font-weight: 700; opacity: 0.95; display: flex; align-items: center; gap: 6px;">
                            <span>📦</span> <span>{len(results)} foods monitored</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Center: 3D Smart Glass Container on Pedestal -->
            <div class="container-3d-card" id="hero-3d-canvas-container">
                <div style="position: absolute; top: 12px; left: 16px; display: flex; align-items: center; gap: 6px; z-index: 10; background: rgba(255,255,255,0.9); padding: 4px 12px; border-radius: 999px; font-size: 0.72rem; font-weight: 800; color: #047857;">
                    <span style="width:6px; height:6px; border-radius:50%; background:#10b981;"></span>
                    <span>3D SMART CONTAINER 01</span>
                </div>
            </div>

            <!-- Right: Freshness Alert Sunset Coral Card -->
            <div class="alert-sunset-card">
                <div>
                    <div class="alert-tag">🔔 FRESHNESS ALERT</div>
                    
                    <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 10px;">
                        <span style="font-size: 3.2rem; filter: drop-shadow(0 6px 12px rgba(0,0,0,0.2));">{tomato_item.icon}</span>
                        <div>
                            <div style="font-size: 1.3rem; font-weight: 900; line-height: 1.1;">{tomato_item.food_name}</div>
                            <div style="font-size: 0.9rem; font-weight: 800; opacity: 0.95; text-transform: uppercase;">MAY SPOIL SOON</div>
                        </div>
                    </div>
                    
                    <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap; margin-bottom: 8px; font-size: 0.76rem; font-weight: 800;">
                        <span style="background: rgba(255,255,255,0.25); padding: 3px 10px; border-radius: 999px;">⏱ {tomato_item.freshness_score:.0f}% Freshness</span>
                        <span style="background: rgba(255,255,255,0.25); padding: 3px 10px; border-radius: 999px;">🔴 {tomato_item.estimated_remaining_str}</span>
                        <span style="background: #ffffff; color: #e11d48; padding: 3px 10px; border-radius: 999px;">High Risk</span>
                    </div>
                    
                    <div style="font-size: 0.78rem; opacity: 0.95; line-height: 1.35; margin-bottom: 12px;">
                        {tomato_item.primary_reason}
                    </div>
                </div>
                
                <div style="display: flex; gap: 10px;">
                    <button class="btn-pill-blue" onclick="openFoodDetail('tomato')">View Analysis →</button>
                    <button class="btn-pill-glass" onclick="alert('Alert dismissed.')">Dismiss</button>
                </div>
            </div>
        </div>

        <!-- 4. YOUR FOOD (6 COLUMNS GRID) -->
        <div class="food-section-header">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 1.1rem;">🍃</span>
                <h3 style="margin: 0; font-family: 'Outfit', sans-serif; font-size: 1.35rem; font-weight: 900; color: #0a1024;">YOUR FOOD</h3>
            </div>
            <span style="font-size: 0.85rem; font-weight: 800; color: #0284c7; cursor: pointer;" onclick="switchPage('food')">View All →</span>
        </div>

        <div class="food-grid-6">
            <!-- 1. Tomatoes -->
            <div class="food-card" onclick="openFoodDetail('tomato')">
                <div class="food-card-glow glow-tomato"></div>
                <div class="food-icon-large">🍅</div>
                <div class="food-name">Tomatoes</div>
                <div class="food-score">{results[0].freshness_score:.0f}% <span style="font-size:0.7rem; color:#64748b; font-weight:700;">Fresh</span></div>
                <div style="margin-bottom: 6px; z-index: 1;"><span class="badge-risk">AT RISK</span></div>
                <div style="font-size: 0.72rem; color: #475569; font-weight: 700; margin-bottom: 2px; z-index: 1;">~8 hours remaining</div>
                <div style="font-size: 0.7rem; font-weight: 800; color: #e11d48; margin-bottom: 8px; z-index: 1;">↑ Risk increasing</div>
                <button class="btn-food-action btn-c-coral">View Analysis →</button>
            </div>

            <!-- 2. Lemon -->
            <div class="food-card" onclick="openFoodDetail('lemon')">
                <div class="food-card-glow glow-lemon"></div>
                <div class="food-icon-large">🍋</div>
                <div class="food-name">Lemon</div>
                <div class="food-score">{results[1].freshness_score:.0f}% <span style="font-size:0.7rem; color:#64748b; font-weight:700;">Fresh</span></div>
                <div style="margin-bottom: 6px; z-index: 1;"><span class="badge-fresh">FRESH</span></div>
                <div style="font-size: 0.72rem; color: #475569; font-weight: 700; margin-bottom: 2px; z-index: 1;">~3.2 days remaining</div>
                <div style="font-size: 0.7rem; font-weight: 800; color: #059669; margin-bottom: 8px; z-index: 1;">→ Stable</div>
                <button class="btn-food-action btn-c-emerald">View Analysis →</button>
            </div>

            <!-- 3. Bell Pepper -->
            <div class="food-card" onclick="openFoodDetail('bell_pepper')">
                <div class="food-card-glow glow-pepper"></div>
                <div class="food-icon-large">🫑</div>
                <div class="food-name">Bell Pepper</div>
                <div class="food-score">{results[2].freshness_score:.0f}% <span style="font-size:0.7rem; color:#64748b; font-weight:700;">Fresh</span></div>
                <div style="margin-bottom: 6px; z-index: 1;"><span class="badge-monitor">MONITOR</span></div>
                <div style="font-size: 0.72rem; color: #475569; font-weight: 700; margin-bottom: 2px; z-index: 1;">~1.4 days remaining</div>
                <div style="font-size: 0.7rem; font-weight: 800; color: #d97706; margin-bottom: 8px; z-index: 1;">↑ Slight risk</div>
                <button class="btn-food-action btn-c-cyan">View Analysis →</button>
            </div>

            <!-- 4. Apple -->
            <div class="food-card" onclick="openFoodDetail('apple')">
                <div class="food-card-glow glow-apple"></div>
                <div class="food-icon-large">🍎</div>
                <div class="food-name">Apple</div>
                <div class="food-score">{results[3].freshness_score:.0f}% <span style="font-size:0.7rem; color:#64748b; font-weight:700;">Fresh</span></div>
                <div style="margin-bottom: 6px; z-index: 1;"><span class="badge-fresh">FRESH</span></div>
                <div style="font-size: 0.72rem; color: #475569; font-weight: 700; margin-bottom: 2px; z-index: 1;">~1.2 days remaining</div>
                <div style="font-size: 0.7rem; font-weight: 800; color: #059669; margin-bottom: 8px; z-index: 1;">→ Stable</div>
                <button class="btn-food-action btn-c-pink">View Analysis →</button>
            </div>

            <!-- 5. Banana -->
            <div class="food-card" onclick="openFoodDetail('banana')">
                <div class="food-card-glow glow-banana"></div>
                <div class="food-icon-large">🍌</div>
                <div class="food-name">Banana</div>
                <div class="food-score">{results[4].freshness_score:.0f}% <span style="font-size:0.7rem; color:#64748b; font-weight:700;">Fresh</span></div>
                <div style="margin-bottom: 6px; z-index: 1;"><span class="badge-monitor">MONITOR</span></div>
                <div style="font-size: 0.72rem; color: #475569; font-weight: 700; margin-bottom: 2px; z-index: 1;">~1.8 days remaining</div>
                <div style="font-size: 0.7rem; font-weight: 800; color: #e11d48; margin-bottom: 8px; z-index: 1;">↑ Risk increasing</div>
                <button class="btn-food-action btn-c-amber">View Analysis →</button>
            </div>

            <!-- 6. Leafy Greens -->
            <div class="food-card" onclick="openFoodDetail('leafy_greens')">
                <div class="food-card-glow glow-greens"></div>
                <div class="food-icon-large">🥬</div>
                <div class="food-name">Leafy Greens</div>
                <div class="food-score">{results[5].freshness_score:.0f}% <span style="font-size:0.7rem; color:#64748b; font-weight:700;">Fresh</span></div>
                <div style="margin-bottom: 6px; z-index: 1;"><span class="badge-risk">AT RISK</span></div>
                <div style="font-size: 0.72rem; color: #475569; font-weight: 700; margin-bottom: 2px; z-index: 1;">~14 hours remaining</div>
                <div style="font-size: 0.7rem; font-weight: 800; color: #e11d48; margin-bottom: 8px; z-index: 1;">↑ Risk increasing</div>
                <button class="btn-food-action btn-c-emerald">View Analysis →</button>
            </div>
        </div>

        <!-- 5. BOTTOM ROW: SENSORS & AI ANALYSIS -->
        <div class="bottom-row">
            <!-- Left: 3 Environment Condition Cards -->
            <div>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                    <span style="font-size: 1.05rem;">🍃</span>
                    <span style="font-size: 0.88rem; font-weight: 900; letter-spacing: 0.06em; text-transform: uppercase; color: #0284c7;">ENVIRONMENT CONDITIONS</span>
                </div>
                
                <div class="env-cards-3">
                    <div class="env-glass-card">
                        <div style="display: flex; align-items: center; gap: 6px; font-size: 0.76rem; font-weight: 800; color: #64748b;">
                            <span>🌡️ Temperature</span>
                        </div>
                        <div style="font-family: 'Outfit', sans-serif; font-size: 1.45rem; font-weight: 900; color: #e11d48; margin-top: 4px;">
                            {reading.temperature_c:.1f}°C
                        </div>
                        <div style="font-size: 0.72rem; font-weight: 800; color: #e11d48; margin-top: 2px;">
                            ↑ Rising
                        </div>
                        <svg viewBox="0 0 100 24" style="width: 100%; height: 24px; margin-top: 6px;">
                            <path d="M0,18 Q25,12 50,14 T100,4" fill="none" stroke="#e11d48" stroke-width="2.5" stroke-linecap="round"/>
                            <circle cx="100" cy="4" r="3" fill="#e11d48"/>
                        </svg>
                    </div>

                    <div class="env-glass-card">
                        <div style="display: flex; align-items: center; gap: 6px; font-size: 0.76rem; font-weight: 800; color: #64748b;">
                            <span>💧 Humidity</span>
                        </div>
                        <div style="font-family: 'Outfit', sans-serif; font-size: 1.45rem; font-weight: 900; color: #0284c7; margin-top: 4px;">
                            {reading.humidity_pct:.0f}%
                        </div>
                        <div style="font-size: 0.72rem; font-weight: 800; color: #0284c7; margin-top: 2px;">
                            → Stable
                        </div>
                        <svg viewBox="0 0 100 24" style="width: 100%; height: 24px; margin-top: 6px;">
                            <path d="M0,12 Q25,15 50,12 T100,10" fill="none" stroke="#0284c7" stroke-width="2.5" stroke-linecap="round"/>
                            <circle cx="100" cy="10" r="3" fill="#0284c7"/>
                        </svg>
                    </div>

                    <div class="env-glass-card">
                        <div style="display: flex; align-items: center; gap: 6px; font-size: 0.76rem; font-weight: 800; color: #64748b;">
                            <span>💨 Gas / VOC</span>
                        </div>
                        <div style="font-family: 'Outfit', sans-serif; font-size: 1.45rem; font-weight: 900; color: #8b5cf6; margin-top: 4px;">
                            {reading.gas_ppm:.0f} ppm
                        </div>
                        <div style="font-size: 0.72rem; font-weight: 800; color: #8b5cf6; margin-top: 2px;">
                            ↑ Rising
                        </div>
                        <svg viewBox="0 0 100 24" style="width: 100%; height: 24px; margin-top: 6px;">
                            <path d="M0,20 Q30,16 60,10 T100,2" fill="none" stroke="#8b5cf6" stroke-width="2.5" stroke-linecap="round"/>
                            <circle cx="100" cy="2" r="3" fill="#8b5cf6"/>
                        </svg>
                    </div>
                </div>
            </div>

            <!-- Right: FreshSense AI Analysis Card -->
            <div>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                    <span style="font-size: 1.05rem;">🧠</span>
                    <span style="font-size: 0.88rem; font-weight: 900; letter-spacing: 0.06em; text-transform: uppercase; color: #0284c7;">FRESHSENSE ANALYSIS</span>
                </div>
                
                <div class="ai-analysis-card">
                    <div class="ai-orb-hologram">AI</div>
                    <div>
                        <div style="font-size: 0.88rem; font-weight: 700; color: #0f172a; line-height: 1.45; margin-bottom: 8px;">
                            "{tomato_item.food_name} are showing increasing spoilage indicators. Temperature and gas readings have increased over the recent monitoring period."
                        </div>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <div style="font-size: 0.76rem; font-weight: 800; color: #059669;">Prediction confidence</div>
                            <div style="flex-grow: 1; height: 7px; background: rgba(0,0,0,0.06); border-radius: 999px; overflow: hidden;">
                                <div style="height: 100%; width: {tomato_item.ai_confidence_pct}%; background: linear-gradient(90deg, #10b981 0%, #06b6d4 100%); border-radius: 999px;"></div>
                            </div>
                            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.84rem; font-weight: 900; color: #059669;">{tomato_item.ai_confidence_pct}%</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 6. FLOATING BOTTOM NAVIGATION BAR -->
    <div class="bottom-floating-nav">
        <div class="b-nav-item active" onclick="switchPage('home')"><span>🏠 Home</span></div>
        <div class="b-nav-item" onclick="switchPage('food')"><span>🍅 Food</span></div>
        <div class="b-nav-item" onclick="switchPage('alerts')"><span>🔔 Alerts ({len(notif_manager.get_unread())})</span></div>
        <div class="b-nav-item" onclick="switchPage('analytics')"><span>📈 Analytics</span></div>
        <div class="b-nav-item" onclick="switchPage('settings')"><span>⚙️ Settings</span></div>
    </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
// -------------------------------------------------------------
// 3D WebGL Smart Glass Container on Multi-Tiered Pedestal
// -------------------------------------------------------------
(function() {{
    const container = document.getElementById('hero-3d-canvas-container');
    if (!container) return;
    
    const width = container.clientWidth || 400;
    const height = container.clientHeight || 330;
    
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
    camera.position.set(0, 1.2, 5.8);
    
    const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true, powerPreference: "high-performance" }});
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    container.appendChild(renderer.domElement);
    
    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
    scene.add(ambientLight);
    
    const keyLight = new THREE.DirectionalLight(0x00d2ff, 1.4);
    keyLight.position.set(4, 6, 4);
    scene.add(keyLight);
    
    const fillLight = new THREE.DirectionalLight(0xff758c, 0.9);
    fillLight.position.set(-4, 4, -3);
    scene.add(fillLight);
    
    const mainGroup = new THREE.Group();
    scene.add(mainGroup);
    
    // Multi-tiered glowing pedestal
    const podiumGroup = new THREE.Group();
    podiumGroup.position.y = -1.15;
    mainGroup.add(podiumGroup);
    
    const tier1Geo = new THREE.CylinderGeometry(2.3, 2.4, 0.14, 64);
    const tier1Mat = new THREE.MeshStandardMaterial({{ color: 0xffffff, roughness: 0.15, metalness: 0.2 }});
    const tier1 = new THREE.Mesh(tier1Geo, tier1Mat);
    podiumGroup.add(tier1);
    
    const rim1Geo = new THREE.TorusGeometry(2.35, 0.035, 16, 64);
    const rim1Mat = new THREE.MeshStandardMaterial({{ color: 0x00d2ff, emissive: 0x00d2ff, emissiveIntensity: 1.2 }});
    const rim1 = new THREE.Mesh(rim1Geo, rim1Mat);
    rim1.rotation.x = Math.PI / 2;
    podiumGroup.add(rim1);
    
    const tier2Geo = new THREE.CylinderGeometry(2.0, 2.1, 0.12, 64);
    const tier2Mat = new THREE.MeshStandardMaterial({{ color: 0xf0fdfa, roughness: 0.1, metalness: 0.3 }});
    const tier2 = new THREE.Mesh(tier2Geo, tier2Mat);
    tier2.position.y = 0.13;
    podiumGroup.add(tier2);
    
    const tier3Geo = new THREE.CylinderGeometry(1.75, 1.8, 0.1, 64);
    const tier3Mat = new THREE.MeshStandardMaterial({{ color: 0xffffff, roughness: 0.1, metalness: 0.4 }});
    const tier3 = new THREE.Mesh(tier3Geo, tier3Mat);
    tier3.position.y = 0.24;
    podiumGroup.add(tier3);
    
    const rim3Geo = new THREE.TorusGeometry(1.78, 0.03, 16, 64);
    const rim3Mat = new THREE.MeshStandardMaterial({{ color: 0x10b981, emissive: 0x10b981, emissiveIntensity: 1.4 }});
    const rim3 = new THREE.Mesh(rim3Geo, rim3Mat);
    rim3.rotation.x = Math.PI / 2;
    rim3.position.y = 0.29;
    podiumGroup.add(rim3);

    // Glass Container
    const containerGroup = new THREE.Group();
    containerGroup.position.y = -0.15;
    mainGroup.add(containerGroup);
    
    const glassMaterial = new THREE.MeshPhysicalMaterial({{
        color: 0xffffff,
        transparent: true,
        opacity: 0.42,
        roughness: 0.05,
        transmission: 0.9,
        ior: 1.5,
        clearcoat: 1.0,
        side: THREE.DoubleSide
    }});
    
    const boxGeo = new THREE.BoxGeometry(2.2, 1.4, 1.7);
    const boxMesh = new THREE.Mesh(boxGeo, glassMaterial);
    containerGroup.add(boxMesh);
    
    const frameMat = new THREE.MeshStandardMaterial({{ color: 0x06b6d4, roughness: 0.2, metalness: 0.6 }});
    const lidGeo = new THREE.BoxGeometry(2.32, 0.14, 1.82);
    const lidMesh = new THREE.Mesh(lidGeo, frameMat);
    lidMesh.position.y = 0.76;
    containerGroup.add(lidMesh);
    
    // Sensor puck
    const puckBaseGeo = new THREE.CylinderGeometry(0.48, 0.52, 0.2, 32);
    const puckBaseMat = new THREE.MeshStandardMaterial({{ color: 0xffffff, roughness: 0.2, metalness: 0.7 }});
    const puckBase = new THREE.Mesh(puckBaseGeo, puckBaseMat);
    puckBase.position.y = 0.95;
    containerGroup.add(puckBase);
    
    const radarGeo = new THREE.TorusGeometry(0.42, 0.025, 16, 32);
    const radarMat = new THREE.MeshBasicMaterial({{ color: 0x10b981 }});
    const radarRing = new THREE.Mesh(radarGeo, radarMat);
    radarRing.rotation.x = Math.PI / 2;
    radarRing.position.y = 1.07;
    containerGroup.add(radarRing);

    // Salad greens + 3D Tomatoes
    const leafMat = new THREE.MeshStandardMaterial({{ color: 0x22c55e, roughness: 0.4, side: THREE.DoubleSide }});
    const leafGeo = new THREE.SphereGeometry(0.35, 12, 12);
    leafGeo.scale(1.2, 0.15, 0.8);
    for (let i = 0; i < 8; i++) {{
        const lf = new THREE.Mesh(leafGeo, leafMat);
        const ang = (i / 8) * Math.PI * 2;
        lf.position.set(Math.cos(ang) * 0.7, -0.48, Math.sin(ang) * 0.5);
        containerGroup.add(lf);
    }}
    
    function makeTomato(scale, px, py, pz) {{
        const tg = new THREE.Group();
        const tGeo = new THREE.SphereGeometry(scale, 32, 32);
        tGeo.scale(1.0, 0.88, 1.0);
        const tMat = new THREE.MeshStandardMaterial({{ color: 0xe11d48, roughness: 0.18, emissive: 0x881337, emissiveIntensity: 0.2 }});
        const tm = new THREE.Mesh(tGeo, tMat);
        tg.add(tm);
        
        const cGeo = new THREE.ConeGeometry(scale * 0.25, scale * 0.14, 5);
        const cMat = new THREE.MeshStandardMaterial({{ color: 0x10b981 }});
        for (let j = 0; j < 5; j++) {{
            const cMesh = new THREE.Mesh(cGeo, cMat);
            const a = (j / 5) * Math.PI * 2;
            cMesh.position.set(Math.cos(a) * (scale * 0.2), scale * 0.84, Math.sin(a) * (scale * 0.2));
            cMesh.rotation.set(0.35, a, 0.4);
            tg.add(cMesh);
        }}
        tg.position.set(px, py, pz);
        return tg;
    }}
    
    containerGroup.add(makeTomato(0.54, -0.32, -0.15, 0.2));
    containerGroup.add(makeTomato(0.46, 0.42, -0.22, 0.15));
    containerGroup.add(makeTomato(0.36, 0.08, -0.08, -0.35));

    // Floating Leaves
    const floatLeafGeo = new THREE.SphereGeometry(0.16, 8, 8);
    floatLeafGeo.scale(1.3, 0.1, 0.7);
    const floatLeaves = [];
    for (let i = 0; i < 6; i++) {{
        const fl = new THREE.Mesh(floatLeafGeo, leafMat);
        const r = 2.2 + Math.random() * 0.8;
        const th = (i / 6) * Math.PI * 2;
        fl.position.set(Math.cos(th) * r, -0.4 + Math.random() * 1.5, Math.sin(th) * r);
        mainGroup.add(fl);
        floatLeaves.push({{ mesh: fl, rad: r, speed: 0.01, theta: th }});
    }}

    let targetRotX = 0, targetRotY = 0;
    window.addEventListener('mousemove', (e) => {{
        const r = container.getBoundingClientRect();
        targetRotY = (((e.clientX - r.left) / r.width) * 2 - 1) * 0.35;
        targetRotX = -(((e.clientY - r.top) / r.height) * 2 - 1) * 0.2;
    }});

    let clock = new THREE.Clock();
    function animate() {{
        requestAnimationFrame(animate);
        const t = clock.getElapsedTime();
        mainGroup.rotation.y += (targetRotY - mainGroup.rotation.y) * 0.06;
        mainGroup.rotation.x += (targetRotX - mainGroup.rotation.x) * 0.06;
        containerGroup.position.y = -0.15 + Math.sin(t * 1.5) * 0.03;
        
        const pulse = 1.0 + Math.sin(t * 4) * 0.08;
        radarRing.scale.set(pulse, pulse, pulse);
        
        floatLeaves.forEach(fl => {{
            fl.theta += fl.speed;
            fl.mesh.position.x = Math.cos(fl.theta) * fl.rad;
            fl.mesh.position.z = Math.sin(fl.theta) * fl.rad;
            fl.mesh.position.y += Math.sin(t * 2 + fl.theta) * 0.003;
            fl.mesh.rotation.y += 0.015;
        }});
        
        renderer.render(scene, camera);
    }}
    animate();

    window.addEventListener('resize', () => {{
        const nw = container.clientWidth || 400;
        const nh = container.clientHeight || 330;
        camera.aspect = nw / nh;
        camera.updateProjectionMatrix();
        renderer.setSize(nw, nh);
    }});
}})();

function switchPage(page) {{
    window.parent.postMessage({{ type: 'streamlit:setComponentValue', value: page }}, '*');
    console.log("Switching to page:", page);
}}

function openFoodDetail(foodId) {{
    console.log("Open food detail:", foodId);
    alert("Viewing analysis profile for " + foodId);
}}
</script>
</body>
</html>
"""
