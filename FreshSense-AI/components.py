"""
FreshSense AI - Reference UI Suite Components
=============================================
Faithfully renders the complete visual composition, layouts, 3D WebGL scenes,
glowing HUDs, glassmorphic depth, and cards from the reference UI design.
"""

from datetime import datetime
from typing import List, Optional, Callable
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

from core.food_profiles import FoodProfile, get_food_profile, get_all_food_profiles, STATUS_COLORS, STATUS_BG_COLORS
from core.freshness_engine import FoodFreshnessResult
from core.sensor_service import SensorReading, SimulationSensorProvider
from core.notification_service import NotificationManager, FreshnessNotification
from core.history_service import HistoryService
from ui.three_scenes import get_3d_smart_container_hero_html, get_3d_ai_flow_html


def render_html(html_code: str):
    """Renders raw HTML cleanly bypassing CommonMark markdown parser."""
    if hasattr(st, "html"):
        st.html(html_code)
    else:
        st.markdown(html_code, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 1. Top Header Bar & Hero 3-Column Section (Matching Reference Composition)
# -----------------------------------------------------------------------------

def render_dashboard_header(reading: SensorReading, unread_count: int, on_click_alerts: Callable[[], None]):
    """Renders the top bar with live node indicator capsule, notification bell and avatar."""
    hcol1, hcol2 = st.columns([3.2, 1.8])
    with hcol2:
        render_html(
            f"""
            <div class="top-header-pill-bar">
                <div class="top-node-pill">
                    <span class="hud-dot" style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#10b981; box-shadow:0 0 8px #10b981;"></span>
                    <span>Kitchen Container 01</span>
                    <span style="color:#64748b; font-weight:600; font-size:0.75rem;">● Simulation Mode</span>
                </div>
                <div class="top-node-pill" style="padding: 6px 12px; position: relative; cursor: pointer;">
                    <span>🔔</span>
                    <span style="background: #e11d48; color: #fff; font-size: 0.68rem; font-weight: 900; padding: 1px 6px; border-radius: 999px; margin-left: 2px;">{unread_count}</span>
                </div>
                <div class="top-avatar-circle">👤</div>
            </div>
            """
        )


def render_reference_hero_section(reading: SensorReading, results: List[FoodFreshnessResult], on_view_analysis: Callable[[str], None]):
    """
    Renders the 3-column Reference Hero Section:
    - Left Column: Headline 'Know Before It Spoils.', tagline, and 72% OVERALL FRESHNESS Mint Card.
    - Center Column: 3D Smart Glass Container on Multi-Tiered Pedestal with Live Sensors & Fresh Greens.
    - Right Column: FRESHNESS ALERT Sunset Coral Card (Tomatoes MAY SPOIL SOON, ~8h left, High Risk).
    """
    tomato_item = next((r for r in results if r.food_id == "tomato"), None)
    urgent_items = [r for r in results if r.status in ["AT RISK", "CRITICAL", "SPOILED"]]
    top_item = tomato_item if (tomato_item and tomato_item.status in ["AT RISK", "CRITICAL", "MONITOR"]) else (urgent_items[0] if urgent_items else results[0])

    scores = [r.freshness_score for r in results]
    avg_score = sum(scores) / len(scores) if scores else 72.0
    attention_count = sum(1 for r in results if r.status in ["MONITOR", "AT RISK", "CRITICAL", "SPOILED"])

    h_left, h_center, h_right = st.columns([1.05, 1.25, 1.15], gap="medium")

    # 1. Left: Headline & Overall Freshness Card
    with h_left:
        render_html(
            f"""
            <div>
                <div class="brand-hero-title">Know Before It Spoils.</div>
                <p class="brand-hero-desc">FreshSense AI monitors your food's environment and predicts freshness using smart sensors and AI.</p>
                
                <div class="overall-freshness-mint-card">
                    <div style="position: absolute; top: 12px; left: 18px; display: flex; align-items: center; gap: 6px; font-size: 0.76rem; font-weight: 900; letter-spacing: 0.05em; text-transform: uppercase;">
                        <span>🍃 OVERALL FRESHNESS</span>
                    </div>
                    
                    <div class="overall-donut-wrapper" style="margin-top: 14px;">
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
                        <div class="overall-donut-text">{avg_score:.0f}%</div>
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
            """
        )

    # 2. Center: 3D Smart Glass Container Hero
    with h_center:
        html_3d = get_3d_smart_container_hero_html(
            temp_c=reading.temperature_c,
            humidity_pct=reading.humidity_pct,
            gas_ppm=reading.gas_ppm,
            freshness_score=top_item.freshness_score,
            food_name=top_item.food_name,
            food_status=top_item.status,
            est_time_str=top_item.estimated_remaining_str,
            height=340
        )
        components.html(html_3d, height=350, scrolling=False)

    # 3. Right: Freshness Alert Banner
    with h_right:
        render_html(
            f"""
            <div class="alert-banner-sunset">
                <div class="alert-banner-tag">🔔 FRESHNESS ALERT</div>
                
                <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 12px;">
                    <span style="font-size: 3.5rem; filter: drop-shadow(0 6px 12px rgba(0,0,0,0.2));">{top_item.icon}</span>
                    <div>
                        <div style="font-size: 1.35rem; font-weight: 900; line-height: 1.1;">{top_item.food_name}</div>
                        <div style="font-size: 0.95rem; font-weight: 800; opacity: 0.95; text-transform: uppercase; letter-spacing: 0.02em;">MAY SPOIL SOON</div>
                    </div>
                </div>
                
                <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 10px; font-size: 0.8rem; font-weight: 800;">
                    <span style="background: rgba(255,255,255,0.25); padding: 3px 10px; border-radius: 999px;">⏱ {top_item.freshness_score:.0f}% Freshness</span>
                    <span style="background: rgba(255,255,255,0.25); padding: 3px 10px; border-radius: 999px;">🔴 {top_item.estimated_remaining_str}</span>
                    <span style="background: #ffffff; color: #e11d48; padding: 3px 10px; border-radius: 999px; box-shadow: 0 2px 6px rgba(0,0,0,0.15);">High Risk</span>
                </div>
                
                <div style="font-size: 0.8rem; opacity: 0.95; line-height: 1.4; margin-bottom: 16px;">
                    {top_item.primary_reason}
                </div>
            </div>
            """
        )
        
        ab_col1, ab_col2 = st.columns([1.5, 1])
        with ab_col1:
            if st.button("View Analysis →", key=f"btn_banner_analysis_{top_item.food_id}", type="primary", use_container_width=True):
                on_view_analysis(top_item.food_id)
        with ab_col2:
            if st.button("Dismiss", key="btn_banner_dismiss", use_container_width=True):
                st.info("Alert acknowledged.")


def render_reference_alert_banner(results: List[FoodFreshnessResult], on_view_analysis: Callable[[str], None]):
    """
    Renders the standalone Freshness Alert Banner:
    - Sunset Coral gradient card
    - 🍅 3D tomato visual & status
    - Action buttons
    """
    tomato_item = next((r for r in results if r.food_id == "tomato"), None)
    urgent_items = [r for r in results if r.status in ["AT RISK", "CRITICAL", "SPOILED"]]
    top_item = tomato_item if (tomato_item and tomato_item.status in ["AT RISK", "CRITICAL", "MONITOR"]) else (urgent_items[0] if urgent_items else results[0])

    acol1, acol2 = st.columns([3.5, 1.2])
    with acol1:
        render_html(
            f"""
            <div class="alert-banner-sunset">
                <div class="alert-banner-tag">🔔 FRESHNESS ALERT</div>
                <div style="display: flex; align-items: center; gap: 16px;">
                    <span style="font-size: 3.2rem;">{top_item.icon}</span>
                    <div>
                        <div style="font-size: 1.3rem; font-weight: 900;">{top_item.food_name} MAY SPOIL SOON</div>
                        <div style="font-size: 0.84rem; opacity: 0.95;">{top_item.primary_reason}</div>
                    </div>
                </div>
            </div>
            """
        )
    with acol2:
        render_html("<div style='margin-top: 24px;'></div>")
        if st.button("View Analysis →", key=f"btn_sa_analysis_{top_item.food_id}", type="primary", use_container_width=True):
            on_view_analysis(top_item.food_id)


# -----------------------------------------------------------------------------
# 2. YOUR FOOD 6-Column Grid (Matching Reference Cards)
# -----------------------------------------------------------------------------

def render_reference_food_grid(results: List[FoodFreshnessResult], on_select_food: Callable[[str], None]):
    """
    Renders the 6-column YOUR FOOD section:
    - 🍅 Tomatoes (72% Fresh | AT RISK | ~8 hours | ↑ Risk increasing)
    - 🍋 Lemon (94% Fresh | FRESH | ~3.2 days | → Stable)
    - 🫑 Bell Pepper (81% Fresh | MONITOR | ~1.4 days | ↑ Slight risk)
    - 🍎 Apple (88% Fresh | FRESH | ~1.2 days | → Stable)
    - 🍌 Banana (65% Fresh | MONITOR | ~1.8 days | ↑ Risk increasing)
    - 🥬 Leafy Greens (48% Fresh | AT RISK | ~14 hours | ↑ Risk increasing)
    """
    render_html(
        """
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 24px 0 14px 0;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 1.1rem;">🍃</span>
                <h3 style="margin: 0; font-family: 'Outfit', sans-serif; font-size: 1.4rem; font-weight: 900; color: #0a1024;">YOUR FOOD</h3>
            </div>
            <span style="font-size: 0.85rem; font-weight: 800; color: #0284c7; cursor: pointer;">View All →</span>
        </div>
        """
    )

    food_cols = st.columns(len(results))
    
    theme_map = {
        "tomato": ("food-card-tomato", "btn-coral"),
        "lemon": ("food-card-lemon", "btn-emerald"),
        "bell_pepper": ("food-card-pepper", "btn-cyan"),
        "apple": ("food-card-apple", "btn-pink"),
        "banana": ("food-card-banana", "btn-amber"),
        "leafy_greens": ("food-card-greens", "btn-emerald")
    }

    for idx, item in enumerate(results):
        with food_cols[idx]:
            card_class, btn_class = theme_map.get(item.food_id, ("food-card-tomato", "btn-coral"))

            if item.status in ["AT RISK", "CRITICAL", "SPOILED"]:
                badge_html = f'<span class="badge-pill-risk">{item.status}</span>'
                trend_color = "#e11d48"
            elif item.status == "MONITOR":
                badge_html = f'<span class="badge-pill-monitor">MONITOR</span>'
                trend_color = "#d97706"
            else:
                badge_html = f'<span class="badge-pill-fresh">FRESH</span>'
                trend_color = "#059669"

            render_html(
                f"""
                <div class="food-card-tall {card_class}">
                    <div class="food-card-header-glow"></div>
                    <div class="food-visual-container">{item.icon}</div>
                    <div class="food-title-text">{item.food_name}</div>
                    <div class="food-score-text">{item.freshness_score:.0f}% <span style="font-size: 0.72rem; color: #64748b; font-weight: 700; font-family: 'Plus Jakarta Sans', sans-serif;">Fresh</span></div>
                    <div style="margin-bottom: 8px; z-index: 1;">{badge_html}</div>
                    <div style="font-size: 0.75rem; color: #475569; font-weight: 700; margin-bottom: 2px; z-index: 1;">{item.estimated_remaining_str}</div>
                    <div style="font-size: 0.72rem; font-weight: 800; color: {trend_color}; margin-bottom: 12px; z-index: 1;">{item.trend_str}</div>
                </div>
                """
            )
            
            # Custom styled button container
            render_html(f"<div class='{btn_class}' style='margin-top: -8px;'>")
            if st.button("View Analysis →", key=f"btn_grid_food_{item.food_id}", use_container_width=True):
                on_select_food(item.food_id)
            render_html("</div>")


# -----------------------------------------------------------------------------
# 3. Environment Conditions & FreshSense AI Analysis (Matching Bottom Row)
# -----------------------------------------------------------------------------

def render_reference_bottom_row(reading: SensorReading, results: List[FoodFreshnessResult]):
    """
    Renders the bottom row from the reference image:
    - Left (ENVIRONMENT CONDITIONS): 3 White Glass Cards with colored sparklines (Temp, Humidity, Gas).
    - Right (FRESHSENSE ANALYSIS): Glowing 3D AI Orb + Transparent Explanation + Confidence Bar.
    """
    tomato_item = next((r for r in results if r.food_id == "tomato"), results[0])

    b_left, b_right = st.columns([1.55, 1.45], gap="medium")

    with b_left:
        render_html(
            """
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                <span style="font-size: 1.05rem;">🍃</span>
                <span style="font-size: 0.88rem; font-weight: 900; letter-spacing: 0.06em; text-transform: uppercase; color: #0284c7;">ENVIRONMENT CONDITIONS</span>
            </div>
            """
        )
        
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            render_html(
                f"""
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
                """
            )
        with sc2:
            render_html(
                f"""
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
                """
            )
        with sc3:
            render_html(
                f"""
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
                """
            )

    with b_right:
        render_html(
            """
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                <span style="font-size: 1.05rem;">🧠</span>
                <span style="font-size: 0.88rem; font-weight: 900; letter-spacing: 0.06em; text-transform: uppercase; color: #0284c7;">FRESHSENSE ANALYSIS</span>
            </div>
            """
        )
        render_html(
            f"""
            <div class="ai-analysis-reference-card">
                <div class="ai-orb-hologram">AI</div>
                <div>
                    <div style="font-size: 0.9rem; font-weight: 700; color: #0f172a; line-height: 1.45; margin-bottom: 8px;">
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
            """
        )


# -----------------------------------------------------------------------------
# 4. Floating Bottom Navigation Bar (Matching Reference)
# -----------------------------------------------------------------------------

def render_floating_bottom_nav(current_page: str, unread_count: int, on_navigate: Callable[[str], None]):
    """Renders the floating bottom glass pill bar matching the reference image."""
    p_home = "bottom-nav-active-pill" if current_page == "home" else "bottom-nav-idle-pill"
    p_food = "bottom-nav-active-pill" if current_page == "food" else "bottom-nav-idle-pill"
    p_alerts = "bottom-nav-active-pill" if current_page == "alerts" else "bottom-nav-idle-pill"
    p_analytics = "bottom-nav-active-pill" if current_page == "analytics" else "bottom-nav-idle-pill"
    p_settings = "bottom-nav-active-pill" if current_page == "settings" else "bottom-nav-idle-pill"

    alert_badge_html = f'<span style="background:#e11d48; color:#fff; font-size:0.7rem; font-weight:900; padding:1px 6px; border-radius:999px; margin-left:4px;">{unread_count}</span>' if unread_count > 0 else ""

    render_html(
        f"""
        <div class="bottom-floating-nav-bar">
            <div class="{p_home}"><span>🏠 Home</span></div>
            <div class="{p_food}"><span>🍅 Food</span></div>
            <div class="{p_alerts}"><span>🔔 Alerts {alert_badge_html}</span></div>
            <div class="{p_analytics}"><span>📈 Analytics</span></div>
            <div class="{p_settings}"><span>⚙️ Settings</span></div>
        </div>
        """
    )


# -----------------------------------------------------------------------------
# 5. Food Detail Page (Matching Reference Tomatoes Profile)
# -----------------------------------------------------------------------------

def render_reference_food_detail_view(result: FoodFreshnessResult, reading: SensorReading, on_back: Callable[[], None], analyze_gemini_fn: Optional[Callable] = None):
    """
    Renders the Food Profile screen from the reference UI suite:
    - '← Back' button
    - Food title + 'AT RISK' status badge
    - Large 3D Food visual on left + Freshness Score Donut on right
    - Freshness Timeline chart with 4 colored zones (Fresh, Monitor, At Risk, Critical)
    - 'Why?' Sensor Breakdown
    - FreshSense Explanation & Recommended Action cards
    - Multimodal Gemini Copilot
    """
    profile = get_food_profile(result.food_id)

    if st.button("← Back to Dashboard", key="btn_back_to_dash"):
        on_back()
        return

    # Header Row
    top_col1, top_col2 = st.columns([1.2, 1])
    with top_col1:
        render_html(
            f"""
            <div style="display: flex; align-items: center; gap: 18px; margin: 12px 0 16px 0;">
                <span style="font-size: 4.2rem; filter: drop-shadow(0 8px 16px rgba(0,0,0,0.15));">{result.icon}</span>
                <div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <h1 style="margin: 0; font-family: 'Outfit', sans-serif; font-size: 2.2rem; font-weight: 900; color: #0a1024;">{result.food_name}</h1>
                        <span class="badge-pill-risk" style="font-size: 0.82rem; padding: 4px 12px;">{result.status}</span>
                    </div>
                    <p style="margin: 4px 0 0 0; font-size: 0.88rem; color: #64748b;">Storage Zone: <strong>{profile.ideal_storage_location}</strong> • Optimal: <strong>{profile.optimal_temp_c[0]}°C–{profile.optimal_temp_c[1]}°C</strong></p>
                </div>
            </div>
            """
        )
    with top_col2:
        render_html(
            f"""
            <div style="background: rgba(255, 255, 255, 0.95); border: 1.5px solid rgba(255,255,255,0.95); border-radius: 22px; padding: 16px 22px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); display: flex; align-items: center; gap: 18px;">
                <div style="position: relative; width: 75px; height: 75px; flex-shrink: 0;">
                    <svg viewBox="0 0 36 36" style="width: 100%; height: 100%; transform: rotate(-90deg);">
                        <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#e2e8f0" stroke-width="3.5" />
                        <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="{result.status_color}" stroke-width="3.5" stroke-dasharray="{result.freshness_score}, 100" stroke-linecap="round" />
                    </svg>
                    <div style="position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-size: 1.15rem; font-weight: 900; font-family: 'JetBrains Mono', monospace; color: {result.status_color};">{result.freshness_score:.0f}%</div>
                </div>
                <div>
                    <div style="font-size: 0.72rem; font-weight: 800; color: #64748b; text-transform: uppercase;">Freshness Score</div>
                    <div style="font-size: 1.15rem; font-weight: 900; color: #0a1024;">{result.estimated_remaining_str}</div>
                </div>
            </div>
            """
        )

    # Middle Row: Freshness Timeline & Why Sensor Breakdown
    m_left, m_right = st.columns([1.5, 1], gap="medium")

    with m_left:
        st.markdown("#### 📈 Freshness Timeline")
        timeline_df = HistoryService.get_food_timeline(result.food_id, result.freshness_score)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=timeline_df["time"],
            y=timeline_df["freshness_score"],
            mode="lines+markers",
            line=dict(color=result.status_color, width=3.5),
            marker=dict(size=7, color="#0a1024"),
            name="Freshness Score",
            fill="tozeroy",
            fillcolor="rgba(244, 63, 94, 0.12)" if result.freshness_score < 75 else "rgba(16, 185, 129, 0.12)",
        ))
        fig.add_hline(y=80, line_dash="dash", line_color="#10b981", annotation_text="Fresh (80+)")
        fig.add_hline(y=60, line_dash="dash", line_color="#f59e0b", annotation_text="Monitor (60)")
        fig.add_hline(y=30, line_dash="dash", line_color="#f43f5e", annotation_text="At Risk (30)")
        
        fig.update_layout(
            height=260,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.7)",
            margin=dict(l=10, r=10, t=20, b=20),
            yaxis=dict(range=[0, 105], gridcolor="rgba(0,0,0,0.05)", tickfont=dict(color="#64748b")),
            xaxis=dict(gridcolor="rgba(0,0,0,0.05)", tickfont=dict(color="#64748b")),
            font=dict(color="#334155", family="Plus Jakarta Sans"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with m_right:
        st.markdown("#### 📊 Why? (Sensor Status)")
        render_html(
            f"""
            <div style="background: rgba(255,255,255,0.92); border: 1.5px solid rgba(255,255,255,0.95); border-radius: 20px; padding: 16px 18px; box-shadow: 0 6px 20px rgba(0,0,0,0.04);">
                <div style="margin-bottom: 10px;">
                    <div style="font-size: 0.78rem; font-weight: 800; color: #64748b;">🌡️ Temperature</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.25rem; font-weight: 900; color: #e11d48;">{reading.temperature_c:.1f}°C</div>
                    <div style="font-size: 0.74rem; color: #64748b;">{result.temp_status}</div>
                </div>
                <div style="margin-bottom: 10px;">
                    <div style="font-size: 0.78rem; font-weight: 800; color: #64748b;">💧 Humidity</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.25rem; font-weight: 900; color: #0284c7;">{reading.humidity_pct:.0f}%</div>
                    <div style="font-size: 0.74rem; color: #64748b;">{result.humidity_status}</div>
                </div>
                <div>
                    <div style="font-size: 0.78rem; font-weight: 800; color: #64748b;">💨 Gas / VOC</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.25rem; font-weight: 900; color: #8b5cf6;">{reading.gas_ppm:.0f} ppm</div>
                    <div style="font-size: 0.74rem; color: #64748b;">{result.gas_status}</div>
                </div>
            </div>
            """
        )

    # Bottom Row: Explanation & Recommended Action
    b1, b2 = st.columns(2)
    with b1:
        render_html(
            f"""
            <div style="background: rgba(255,255,255,0.92); border: 1.5px solid #a7f3d0; border-radius: 20px; padding: 16px 20px; box-shadow: 0 6px 18px rgba(0,0,0,0.03);">
                <div style="font-weight: 800; color: #047857; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
                    <span>🤖 FreshSense Explanation</span>
                </div>
                <div style="font-size: 0.88rem; color: #334155; line-height: 1.45;">{result.primary_reason}</div>
            </div>
            """
        )
    with b2:
        render_html(
            f"""
            <div style="background: rgba(255,255,255,0.92); border: 1.5px solid #fde68a; border-radius: 20px; padding: 16px 20px; box-shadow: 0 6px 18px rgba(0,0,0,0.03);">
                <div style="font-weight: 800; color: #b45309; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
                    <span>💡 Recommended Action</span>
                </div>
                <div style="font-size: 0.88rem; color: #334155; line-height: 1.45;">{result.recommended_action}</div>
            </div>
            """
        )

    # Multimodal Vision
    st.markdown("---")
    st.markdown(f"### 📸 Multimodal AI Vision & Zero-Waste Recipes for {result.food_name}")
    vcol1, vcol2 = st.columns(2)
    with vcol1:
        cam_photo = st.camera_input("Capture with webcam", key=f"cam_ref_{result.food_id}")
        up_photo = st.file_uploader("Or upload photo", type=["jpg", "jpeg", "png"], key=f"up_ref_{result.food_id}")
        selected_photo = cam_photo or up_photo

    with vcol2:
        if selected_photo is not None and analyze_gemini_fn is not None:
            if st.button("🚀 Analyze Food Surface & Generate Recipes", type="primary", key="btn_gemini_ref", use_container_width=True):
                with st.spinner("Analyzing surface features & IoT telemetry..."):
                    img_bytes = selected_photo.getvalue()
                    res = analyze_gemini_fn(
                        image_bytes=img_bytes,
                        temp=reading.temperature_c,
                        humidity=reading.humidity_pct,
                        gas_ppm=reading.gas_ppm,
                        freshness_score=result.freshness_score
                    )
                    if "error" in res:
                        st.error(res["message"])
                    else:
                        st.success(f"**Identified:** {res.get('detected_item', result.food_name)}")
                        st.write(f"**Condition:** {res.get('visual_condition')}")
                        st.write(f"**Verdict:** {res.get('safety_verdict')}")
                        for idx, rec in enumerate(res.get("zero_waste_recipes", []), 1):
                            with st.expander(f"**{idx}. {rec.get('recipe_name')}** ({rec.get('prep_time_minutes')} mins)", expanded=True):
                                st.write(rec.get("instructions"))


# -----------------------------------------------------------------------------
# 6. Alerts Screen (Matching Reference Alerts UI)
# -----------------------------------------------------------------------------

def render_reference_alerts_screen(manager: NotificationManager, on_view_food: Callable[[str], None]):
    """
    Renders the Alerts Screen from the reference UI suite:
    - Filter pills: All (2), Critical (1), Warning (1), Info (0)
    - Severity alert cards with food icon, timestamp, message, and 'View Food' button
    - Floating 'Your food is safer now!' verified card
    """
    render_html(
        """
        <div style="margin-bottom: 16px;">
            <h2 style="margin: 0; font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 900; color: #0a1024;">Alerts</h2>
            <p style="margin: 4px 0 0 0; font-size: 0.88rem; color: #64748b;">Real-time notifications and state transition triggers.</p>
        </div>
        """
    )

    al_left, al_right = st.columns([3.2, 1.2], gap="large")

    with al_left:
        fcol1, fcol2, fcol3 = st.columns([2.5, 1, 1])
        with fcol1:
            category = st.radio("Category", ["All", "Critical", "Warning", "Info"], horizontal=True, label_visibility="collapsed")
        with fcol2:
            if st.button("✓ Mark Read", use_container_width=True):
                manager.mark_all_as_read()
                st.rerun()
        with fcol3:
            if st.button("🗑️ Clear", use_container_width=True):
                manager.clear_all()
                st.rerun()

        filtered = manager.get_filtered(category)
        if not filtered:
            st.info("✨ No active alerts found in this category.")
        else:
            for n in filtered:
                item_bg = "linear-gradient(135deg, rgba(255, 241, 242, 0.95) 0%, rgba(255, 255, 255, 0.95) 100%)" if n.severity == "CRITICAL" else ("linear-gradient(135deg, rgba(254, 252, 232, 0.95) 0%, rgba(255, 255, 255, 0.95) 100%)" if n.severity == "WARNING" else "linear-gradient(135deg, rgba(236, 253, 245, 0.95) 0%, rgba(255, 255, 255, 0.95) 100%)")
                border_col = "#fda4af" if n.severity == "CRITICAL" else ("#fde68a" if n.severity == "WARNING" else "#a7f3d0")
                tag_col = "#e11d48" if n.severity == "CRITICAL" else ("#d97706" if n.severity == "WARNING" else "#059669")

                ncol1, ncol2 = st.columns([3.8, 1.2])
                with ncol1:
                    render_html(
                        f"""
                        <div style="background: {item_bg}; border: 1.5px solid {border_col}; border-radius: 20px; padding: 16px 20px; margin-bottom: 12px; box-shadow: 0 6px 18px rgba(0,0,0,0.03);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <span style="font-size: 1.4rem;">{n.food_icon}</span>
                                    <span style="font-size: 0.74rem; font-weight: 900; text-transform: uppercase; color: {tag_col};">{n.severity} RISK</span>
                                    <strong style="color: #0a1024; font-size: 1rem;">{n.title}</strong>
                                </div>
                                <div style="font-size: 0.76rem; color: #64748b;">{n.formatted_time}</div>
                            </div>
                            <div style="font-size: 0.86rem; color: #334155; margin-bottom: 4px;">{n.message}</div>
                            <div style="font-size: 0.8rem; color: #059669; font-weight: 700;">💡 {n.recommended_action}</div>
                        </div>
                        """
                    )
                with ncol2:
                    render_html("<div style='margin-top: 14px;'></div>")
                    if st.button(f"View {n.food_name}", key=f"btn_alerts_view_{n.id}", use_container_width=True):
                        manager.mark_as_read(n.id)
                        on_view_food(n.food_id)

    with al_right:
        render_html(
            """
            <div style="background: rgba(255, 255, 255, 0.92); border: 1.5px solid rgba(255, 255, 255, 0.95); border-radius: 24px; padding: 22px 18px; text-align: center; box-shadow: 0 12px 32px rgba(0, 210, 255, 0.15); margin-top: 36px;">
                <div style="font-size: 3.5rem; margin-bottom: 6px;">🫑</div>
                <div style="display: inline-flex; align-items: center; gap: 6px; background: #ecfdf5; color: #047857; font-weight: 800; font-size: 0.82rem; padding: 4px 12px; border-radius: 999px; border: 1px solid #a7f3d0; margin-bottom: 8px;">
                    ✓ Your food is safer now!
                </div>
                <div style="font-size: 0.78rem; color: #64748b; line-height: 1.4;">
                    Continuous AI monitoring keeps spoilage risk minimized.
                </div>
            </div>
            """
        )


# -----------------------------------------------------------------------------
# 7. Analytics Screen (Matching Reference Analytics UI)
# -----------------------------------------------------------------------------

def render_reference_analytics_screen(reading: SensorReading):
    """
    Renders the Analytics Screen from the reference UI suite:
    - 4 Top Metric Cards (Freshness Score 78%, Sensor Stability 96%, Foods Monitored 6, Risk Detected 2)
    - Time window selector (24H, 7D, 30D)
    - Freshness Trend multi-line chart
    - Food Status Donut breakdown chart
    """
    render_html(
        """
        <div style="margin-bottom: 16px;">
            <h2 style="margin: 0; font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 900; color: #0a1024;">Analytics</h2>
            <p style="margin: 4px 0 0 0; font-size: 0.88rem; color: #64748b;">Telemetry trends, sensor stability, and inventory condition distribution.</p>
        </div>
        """
    )

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_html("""<div class="env-glass-card"><div style="font-size: 0.74rem; font-weight: 800; color: #059669; text-transform: uppercase;">Freshness Score</div><div style="font-family: 'JetBrains Mono', monospace; font-size: 1.65rem; font-weight: 900; color: #065f46; margin: 4px 0 2px 0;">78%</div><div style="font-size: 0.72rem; color: #059669; font-weight: 700;">↑ +2% nominal</div></div>""")
    with m2:
        render_html("""<div class="env-glass-card"><div style="font-size: 0.74rem; font-weight: 800; color: #0284c7; text-transform: uppercase;">Sensor Stability</div><div style="font-family: 'JetBrains Mono', monospace; font-size: 1.65rem; font-weight: 900; color: #075985; margin: 4px 0 2px 0;">96%</div><div style="font-size: 0.72rem; color: #0284c7; font-weight: 700;">↑ +4% high fidelity</div></div>""")
    with m3:
        render_html("""<div class="env-glass-card"><div style="font-size: 0.74rem; font-weight: 800; color: #7c3aed; text-transform: uppercase;">Foods Monitored</div><div style="font-family: 'JetBrains Mono', monospace; font-size: 1.65rem; font-weight: 900; color: #5b21b6; margin: 4px 0 2px 0;">6</div><div style="font-size: 0.72rem; color: #7c3aed; font-weight: 700;">● Stable tracking</div></div>""")
    with m4:
        render_html("""<div class="env-glass-card"><div style="font-size: 0.74rem; font-weight: 800; color: #e11d48; text-transform: uppercase;">Risk Detected</div><div style="font-family: 'JetBrains Mono', monospace; font-size: 1.65rem; font-weight: 900; color: #9f1239; margin: 4px 0 2px 0;">2</div><div style="font-size: 0.72rem; color: #e11d48; font-weight: 700;">⚠ Requires attention</div></div>""")

    render_html("<div style='margin-top: 14px;'></div>")

    tframe = st.radio("Time Window", ["24H", "7D", "30D"], horizontal=True)
    tf_map = {"24H": "24h", "7D": "7d", "30D": "30d"}

    df = HistoryService.get_history_dataframe(
        timeframe=tf_map[tframe],
        current_temp=reading.temperature_c,
        current_humidity=reading.humidity_pct,
        current_gas=reading.gas_ppm
    )

    c_left, c_right = st.columns([1.8, 1.2], gap="medium")

    with c_left:
        st.markdown("#### Freshness Trend")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["time_label"], y=df["freshness_score"], name="Tomatoes", line=dict(color="#f43f5e", width=3), fill="tozeroy", fillcolor="rgba(244, 63, 94, 0.08)"))
        fig.add_trace(go.Scatter(x=df["time_label"], y=[min(100, v + 22) for v in df["freshness_score"]], name="Lemon", line=dict(color="#10b981", width=2.5)))
        fig.add_trace(go.Scatter(x=df["time_label"], y=[min(100, v + 9) for v in df["freshness_score"]], name="Bell Pepper", line=dict(color="#06b6d4", width=2.5)))

        fig.update_layout(
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.7)",
            margin=dict(l=10, r=10, t=30, b=20),
            font=dict(color="#334155", family="Plus Jakarta Sans"),
            xaxis=dict(gridcolor="rgba(0,0,0,0.05)"),
            yaxis=dict(title="Score", gridcolor="rgba(0,0,0,0.05)", range=[0, 105]),
            legend=dict(orientation="h", y=1.14, x=0.05),
        )
        st.plotly_chart(fig, use_container_width=True)

    with c_right:
        st.markdown("#### Food Status Breakdown")
        donut_fig = go.Figure(data=[go.Pie(
            labels=["Fresh", "Monitor", "At Risk", "Critical"],
            values=[3, 2, 1, 0],
            hole=0.6,
            marker=dict(colors=["#10b981", "#f59e0b", "#f43f5e", "#881337"]),
            textinfo="value",
            hoverinfo="label+percent"
        )])
        donut_fig.update_layout(
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            font=dict(color="#334155", family="Plus Jakarta Sans"),
            showlegend=True,
            legend=dict(orientation="h", y=-0.1)
        )
        st.plotly_chart(donut_fig, use_container_width=True)


# -----------------------------------------------------------------------------
# 8. Simulation Sandbox (Matching Reference Simulation UI)
# -----------------------------------------------------------------------------

def render_reference_simulation_sandbox(sim_provider: SimulationSensorProvider, on_apply: Callable[[], None]):
    """
    Renders the Simulation Mode from the reference UI suite:
    - Header: 'Simulation Mode' with '● Running' tag
    - Preset Scenario Buttons: Fresh, Normal, Warning, Rapid Spoilage (Active), Critical
    - Sliders: Temperature, Humidity, Gas/VOC
    - Action Buttons: START, PAUSE, RESET
    - Right Side: ⚡ RAPID SPOILAGE DEMO with 4 step cards (94% FRESH -> 76% MONITOR -> 48% AT RISK -> 24% CRITICAL)
    """
    render_html(
        """
        <div style="margin-bottom: 16px;">
            <h2 style="margin: 0; font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 900; color: #0a1024;">Simulation Mode</h2>
            <div style="display: inline-flex; align-items: center; gap: 5px; font-size: 0.76rem; font-weight: 800; color: #047857; background: #ecfdf5; border: 1.5px solid #a7f3d0; padding: 2px 10px; border-radius: 999px; margin-top: 4px;">
                <span class="hud-dot" style="display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #10b981;"></span> Running Simulation Core
            </div>
        </div>
        """
    )

    s_left, s_right = st.columns([1.6, 1.4], gap="large")

    with s_left:
        st.markdown("#### Preset Scenarios")
        p_cols = st.columns(5)
        p_keys = ["fresh_baseline", "normal_storage", "warning_temp", "rapid_spoilage", "critical_alert"]
        p_labels = ["Fresh", "Normal", "Warning", "Rapid Spoilage", "Critical"]
        
        for idx, k in enumerate(p_keys):
            with p_cols[idx]:
                is_sel = (sim_provider.preset_key == k)
                if st.button(p_labels[idx], key=f"btn_p_ref_{k}", type="primary" if is_sel else "secondary", use_container_width=True):
                    sim_provider.apply_preset(k)
                    on_apply()
                    st.rerun()

        st.markdown("---")
        st.markdown("#### Manual Sensor Overrides")
        curr = sim_provider.get_current_reading()
        t = st.slider("Temperature (°C)", 1.0, 45.0, float(curr.temperature_c), 0.5)
        h = st.slider("Humidity (%)", 20.0, 98.0, float(curr.humidity_pct), 1.0)
        g = st.slider("Gas / VOC (ppm)", 10.0, 800.0, float(curr.gas_ppm), 5.0)

        bcol1, bcol2, bcol3 = st.columns(3)
        with bcol1:
            if st.button("▶ START", type="primary", use_container_width=True):
                sim_provider.set_reading(t, h, g, curr.hours_elapsed)
                on_apply()
                st.rerun()
        with bcol2:
            if st.button("⏸ PAUSE", use_container_width=True):
                st.info("Simulation paused.")
        with bcol3:
            if st.button("🔄 RESET", use_container_width=True):
                sim_provider.apply_preset("fresh_baseline")
                on_apply()
                st.rerun()

    with s_right:
        render_html(
            """
            <div style="background: rgba(255, 255, 255, 0.95); border: 1.5px solid rgba(255, 255, 255, 0.95); border-radius: 24px; padding: 20px; box-shadow: 0 12px 32px rgba(0, 210, 255, 0.12);">
                <div style="font-size: 1.05rem; font-weight: 900; color: #0284c7; margin-bottom: 4px;">⚡ RAPID SPOILAGE DEMO</div>
                <div style="font-size: 0.8rem; color: #64748b; margin-bottom: 12px;">Watch how freshness changes over time for <strong>🍅 Tomatoes</strong>:</div>
            </div>
            """
        )

        for idx, sdata in enumerate(sim_provider.SPOILAGE_STEPS):
            is_active = (sim_provider.preset_key == f"spoilage_step_{idx+1}")
            btn_type = "primary" if is_active else "secondary"
            rcol1, rcol2 = st.columns([3.5, 1.5])
            with rcol1:
                st_color = "#10b981" if idx == 0 else ("#f59e0b" if idx == 1 else ("#f43f5e" if idx == 2 else "#881337"))
                render_html(
                    f"""
                    <div style="display: flex; align-items: center; gap: 12px; background: rgba(255,255,255,0.85); border: 1px solid rgba(0,0,0,0.06); border-radius: 14px; padding: 8px 14px; margin-bottom: 8px;">
                        <span style="font-size: 1.6rem;">🍅</span>
                        <div>
                            <div style="font-size: 0.86rem; font-weight: 900; color: {st_color};">{sdata['label']}</div>
                            <div style="font-size: 0.74rem; color: #64748b;">{sdata['status']} • {sdata['temp_c']}°C • {sdata['gas_ppm']} ppm</div>
                        </div>
                    </div>
                    """
                )
            with rcol2:
                if st.button(f"Step {idx+1}", key=f"btn_step_ref_{idx+1}", type=btn_type, use_container_width=True):
                    sim_provider.apply_spoilage_step(idx)
                    on_apply()
                    st.rerun()


# -----------------------------------------------------------------------------
# 9. Settings Screen (Matching Reference Settings UI)
# -----------------------------------------------------------------------------

def render_reference_settings_page(reading: SensorReading):
    """Renders Settings with clean grouped glass panels."""
    st.markdown("## ⚙️ Settings & Container Configuration")
    
    sc1, sc2 = st.columns(2, gap="medium")
    with sc1:
        st.markdown("### 📦 Hardware Node Configuration")
        render_html(
            f"""
            <div class="env-glass-card">
                <div style="font-size: 0.8rem; font-weight: 800; color: #64748b;">DEVICE NAME</div>
                <div style="font-size: 1.2rem; font-weight: 900; color: #0a1024; margin-bottom: 8px;">{reading.device_name}</div>
                <div style="display: flex; justify-content: space-between; font-size: 0.84rem; color: #334155;">
                    <span>Battery Level: <strong>{reading.battery_pct:.0f}%</strong></span>
                    <span>Signal: <strong>{reading.signal_strength_dbm} dBm</strong></span>
                </div>
            </div>
            """
        )
        st.markdown("---")
        st.markdown("### 🔔 Notification Thresholds")
        st.checkbox("🚨 High Priority Alerts (Score < 50%)", value=True)
        st.checkbox("⚠️ Monitoring Warnings (Score 50–75%)", value=True)
        st.checkbox("🌡️ Environmental Drift Alerts", value=True)

    with sc2:
        st.markdown("### 🛡️ Firmware & Kinetics Engine")
        render_html(
            """
            <div class="env-glass-card">
                <div style="font-weight: 900; color: #059669; font-size: 1.1rem; margin-bottom: 4px;">FreshSense AI Core v3.2</div>
                <p style="font-size: 0.84rem; color: #475569; line-height: 1.45;">Multi-Sensor Biological Decay Kinetics Engine • Three.js 3D WebGL Visualization Core • Multimodal Gemini AI Vision Copilot Active.</p>
            </div>
            """
        )


# Backward-compatible function aliases
render_top_header = render_dashboard_header
render_container_status_card = lambda reading: None
render_overall_freshness_hero = render_reference_hero_section
render_main_alert_card = render_reference_alert_banner
render_freshness_alert_hero = render_reference_alert_banner
render_your_food_section = render_reference_food_grid
render_your_food_list_section = render_reference_food_grid
render_environment_conditions = render_reference_bottom_row
render_sensor_conditions_section = render_reference_bottom_row
render_freshsense_ai_analysis = lambda results: None
render_food_detail_view = render_reference_food_detail_view
render_food_detail_page = render_reference_food_detail_view
render_notification_center = render_reference_alerts_screen
render_analytics_dashboard = render_reference_analytics_screen
render_simulation_sandbox = render_reference_simulation_sandbox
render_settings_page = render_reference_settings_page
render_device_container_page = lambda reading: None
render_3d_smart_container_hero_section = lambda reading, results: None
