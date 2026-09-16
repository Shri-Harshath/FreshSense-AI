"""
FreshSense AI - High-Quality Animated UI Components
===================================================
Renders the complete visual hierarchy for FreshSense AI:
- Header with Brand, Tagline, Kitchen Container 01 ● Simulation Mode, and Animated Bell Badge (🔔 2)
- Overall Freshness Hero Card (72%, 2 items need attention)
- Main Freshness Alert Hero (⚠ FRESHNESS ALERT • 🍅 TOMATOES • MAY SPOIL SOON • ~8 hrs left)
- YOUR FOOD section with Filter Tabs & Responsive Cards (Tomatoes, Lemon, Bell Pepper, Apple, Banana, Leafy Greens)
- ENVIRONMENT CONDITIONS Cards (24.8°C Temp ↑ Rising, 68% Humidity → Stable, 420 ppm Gas ↑ Rising)
- FRESHSENSE AI Analysis Section (87% Confidence, Transparent Biological Reasoning)
- Deep-Dive Food Detail View with 48h Plotly Timeline, Sensor Breakdowns & Recipe Copilot
- Real Notification Center with Read/Unread tracking, Filters & Food Links
- Historical Analytics (24H / 7D / 30D)
- Simulation Panel with ⚡ RAPID SPOILAGE DEMO (94% FRESH -> 76% MONITOR -> 48% AT RISK -> 24% CRITICAL)
- Settings & Device Specifications
"""

from datetime import datetime
from typing import List, Optional, Callable
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

from core.food_profiles import FoodProfile, get_food_profile, get_all_food_profiles, STATUS_COLORS, STATUS_BG_COLORS
from core.freshness_engine import FoodFreshnessResult
from core.sensor_service import SensorReading, SimulationSensorProvider
from core.notification_service import NotificationManager, FreshnessNotification
from core.history_service import HistoryService


def render_html(html_code: str):
    """Renders raw HTML cleanly bypassing CommonMark markdown parser."""
    if hasattr(st, "html"):
        st.html(html_code)
    else:
        st.markdown(html_code, unsafe_allow_html=True)


def render_dashboard_header(reading: SensorReading, unread_count: int, on_click_alerts: Callable[[], None]):
    """Renders the top brand header, container node mode, and animated notification bell."""
    hcol1, hcol2 = st.columns([3, 1])
    with hcol1:
        render_html(
            """<div style="padding: 2px 0 6px 0;"><div style="font-size: 1.95rem; font-weight: 900; letter-spacing: -0.03em; background: linear-gradient(135deg, #ffffff 30%, #34d399 70%, #06b6d4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1.1;">FreshSense AI</div><div style="font-size: 0.95rem; font-weight: 600; color: #10b981; letter-spacing: 0.02em; margin-top: 2px;">Know Before It Spoils.</div><div style="display: flex; align-items: center; gap: 8px; margin-top: 6px;"><span style="font-size: 0.82rem; font-weight: 700; color: #cbd5e1;">Kitchen Container 01</span><span style="display: inline-flex; align-items: center; gap: 4px; font-size: 0.76rem; font-weight: 800; color: #34d399; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.35); padding: 2px 8px; border-radius: 999px;">● Simulation Mode</span></div></div>"""
        )

    with hcol2:
        bell_badge_text = f"🔔 {unread_count}" if unread_count > 0 else "🔔 0"
        btn_type = "primary" if unread_count > 0 else "secondary"
        render_html("<div style='margin-top: 6px;'></div>")
        if st.button(bell_badge_text, key="btn_header_bell", type=btn_type, use_container_width=True):
            on_click_alerts()


def render_overall_freshness_hero(results: List[FoodFreshnessResult]):
    """
    Renders the OVERALL FRESHNESS Hero Card:
    - OVERALL FRESHNESS
    - 72%
    - 2 items need attention
    """
    scores = [r.freshness_score for r in results]
    avg_score = sum(scores) / len(scores) if scores else 72.0
    attention_count = sum(1 for r in results if r.status in ["MONITOR", "AT RISK", "CRITICAL", "SPOILED"])
    
    status_text = f"{attention_count} items need attention" if attention_count > 0 else "All items in peak condition"

    gauge_color = "#10b981" if avg_score >= 80 else ("#f59e0b" if avg_score >= 60 else "#f43f5e")

    render_html(
        f"""<div style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.85) 0%, rgba(20, 32, 58, 0.9) 100%); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 18px 22px; margin-top: 10px; margin-bottom: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.35);"><div style="display: flex; justify-content: space-between; align-items: center;"><div style="font-size: 0.82rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; color: #94a3b8;">OVERALL FRESHNESS</div><div style="font-size: 0.82rem; font-weight: 700; color: #38bdf8; background: rgba(56, 189, 248, 0.12); padding: 3px 10px; border-radius: 999px; border: 1px solid rgba(56, 189, 248, 0.25);">Active Multi-Sensor Telemetry</div></div><div style="display: flex; align-items: baseline; gap: 10px; margin: 8px 0 4px 0;"><span style="font-size: 2.7rem; font-weight: 900; font-family: 'JetBrains Mono', monospace; color: {gauge_color}; line-height: 1;">{avg_score:.0f}%</span><span style="font-size: 1rem; font-weight: 700; color: #f87171;">{status_text}</span></div><div style="height: 6px; width: 100%; background: rgba(255, 255, 255, 0.08); border-radius: 999px; overflow: hidden; margin-top: 6px;"><div style="height: 100%; width: {avg_score}%; background: linear-gradient(90deg, #f43f5e 0%, #f59e0b 50%, #10b981 100%); border-radius: 999px;"></div></div></div>"""
    )


def render_main_alert_card(results: List[FoodFreshnessResult], on_view_analysis: Callable[[str], None]):
    """
    Renders the MAIN ALERT CARD (The most important card on the dashboard):
    ⚠ FRESHNESS ALERT
    🍅 TOMATOES
    MAY SPOIL SOON
    72% Freshness
    ~8 hours remaining
    Risk: HIGH
    Why: Temperature and gas readings are trending upward.
    [ VIEW ANALYSIS ]
    """
    tomato_item = next((r for r in results if r.food_id == "tomato"), None)
    urgent_items = [r for r in results if r.status in ["AT RISK", "CRITICAL", "SPOILED"]]
    top_item = tomato_item if (tomato_item and tomato_item.status in ["AT RISK", "CRITICAL", "MONITOR"]) else (urgent_items[0] if urgent_items else results[0])

    stat_color = "#f43f5e" if top_item.freshness_score < 75 else "#f59e0b"
    risk_badge = "HIGH" if top_item.status == "AT RISK" else ("CRITICAL" if top_item.status == "CRITICAL" else "MODERATE")

    render_html(
        f"""<div class="freshness-alert-hero" style="margin-top: 4px; margin-bottom: 18px;"><div class="alert-header-tag"><span style="font-size: 1.15rem;">⚠</span> FRESHNESS ALERT</div><div class="alert-food-title"><span style="font-size: 2.2rem;">{top_item.icon}</span> <span>{top_item.food_name.upper()}</span></div><div class="alert-food-sub" style="text-transform: uppercase; letter-spacing: 0.04em;">MAY SPOIL SOON</div><div class="freshness-meter-wrap"><div class="freshness-meter-fill" style="width: {top_item.freshness_score}%;"></div></div><div class="alert-stats-box"><div><div class="alert-stat-label">Freshness Score</div><div class="alert-stat-val" style="color: {stat_color};">{top_item.freshness_score:.0f}% <span style="font-size: 0.9rem; font-weight: 700; color: #fca5a5;">Fresh</span></div></div><div style="text-align: center;"><div class="alert-stat-label">Risk Level</div><div class="alert-stat-val" style="color: #f43f5e; font-size: 1.25rem;">{risk_badge}</div></div><div style="text-align: right;"><div class="alert-stat-label">Remaining Time</div><div class="alert-stat-val" style="color: #ffffff; font-size: 1.25rem;">{top_item.estimated_remaining_str}</div></div></div><div style="font-size: 0.86rem; color: #fecdd3; background: rgba(0,0,0,0.3); padding: 8px 14px; border-radius: 10px; border-left: 3px solid #f43f5e; margin-bottom: 14px;"><strong>Why:</strong> {top_item.primary_reason}</div></div>"""
    )

    if st.button(f"🔍 [ VIEW ANALYSIS FOR {top_item.food_name.upper()} ]", key=f"btn_hero_view_{top_item.food_id}", type="primary", use_container_width=True):
        on_view_analysis(top_item.food_id)


def render_your_food_section(results: List[FoodFreshnessResult], on_select_food: Callable[[str], None], selected_filter: str = "All"):
    """
    Renders the 'YOUR FOOD' section with filter pills and detailed food cards:
    - 🍅 Tomatoes (72% Fresh | AT RISK | ~8 hours remaining | ↑ Risk increasing)
    - 🍋 Lemon (94% Fresh | FRESH | ~3.2 days remaining | → Stable)
    - 🫑 Bell Pepper (81% Fresh | MONITOR | ~1.4 days remaining | ↑ Risk increasing)
    - 🍎 Apple (88% Fresh | FRESH | ~12 days remaining | → Stable)
    - 🍌 Banana (65% Fresh | MONITOR | ~1.8 days remaining | ↑ Risk increasing)
    - 🥬 Leafy Greens (48% Fresh | AT RISK | ~14 hours remaining | ↑ Risk increasing)
    """
    render_html("""<div class="section-header-title">YOUR FOOD</div>""")

    # Filter pills
    fcol1, fcol2, fcol3, fcol4, fcol5 = st.columns(5)
    with fcol1:
        if st.button("All", key="tab_food_all", type="primary" if selected_filter == "All" else "secondary", use_container_width=True):
            st.session_state.food_filter = "All"
            st.rerun()
    with fcol2:
        if st.button("Fresh", key="tab_food_fresh", type="primary" if selected_filter == "Fresh" else "secondary", use_container_width=True):
            st.session_state.food_filter = "Fresh"
            st.rerun()
    with fcol3:
        if st.button("Monitor", key="tab_food_monitor", type="primary" if selected_filter == "Monitor" else "secondary", use_container_width=True):
            st.session_state.food_filter = "Monitor"
            st.rerun()
    with fcol4:
        if st.button("At Risk", key="tab_food_risk", type="primary" if selected_filter == "At Risk" else "secondary", use_container_width=True):
            st.session_state.food_filter = "At Risk"
            st.rerun()
    with fcol5:
        if st.button("Critical", key="tab_food_crit", type="primary" if selected_filter == "Critical" else "secondary", use_container_width=True):
            st.session_state.food_filter = "Critical"
            st.rerun()

    filter_choice = st.session_state.get("food_filter", "All")
    
    # Filter the results
    if filter_choice == "Fresh":
        display_items = [r for r in results if r.status == "FRESH"]
    elif filter_choice == "Monitor":
        display_items = [r for r in results if r.status == "MONITOR"]
    elif filter_choice == "At Risk":
        display_items = [r for r in results if r.status == "AT RISK"]
    elif filter_choice == "Critical":
        display_items = [r for r in results if r.status in ["CRITICAL", "SPOILED"]]
    else:
        display_items = results

    if not display_items:
        st.info(f"No items currently in '{filter_choice}' status.")
        return

    for item in display_items:
        if item.status in ["AT RISK", "CRITICAL", "SPOILED"]:
            badge_html = f'<span class="badge-neon-risk" style="background: {item.status_bg}; color: {item.status_color}; border: 1px solid {item.status_color};">⚠ {item.status}</span>'
            border_glow = f"border: 1px solid {item.status_color};"
        elif item.status == "MONITOR":
            badge_html = f'<span class="badge-neon-monitor" style="background: {item.status_bg}; color: {item.status_color}; border: 1px solid {item.status_color};">● MONITOR</span>'
            border_glow = "border: 1px solid rgba(245, 158, 11, 0.4);"
        else:
            badge_html = f'<span class="badge-neon-fresh" style="background: {item.status_bg}; color: {item.status_color}; border: 1px solid {item.status_color};">✓ FRESH</span>'
            border_glow = "border: 1px solid rgba(16, 185, 129, 0.3);"

        rcol1, rcol2 = st.columns([3.8, 1.2])
        with rcol1:
            render_html(
                f"""<div style="background: rgba(18, 26, 45, 0.75); {border_glow} border-radius: 16px; padding: 12px 16px; margin-bottom: 8px;"><div style="display: flex; justify-content: space-between; align-items: center;"><div style="display: flex; align-items: center; gap: 12px;"><span style="font-size: 1.8rem;">{item.icon}</span><div><div style="font-size: 1.05rem; font-weight: 800; color: #ffffff;">{item.food_name}</div><div style="font-size: 0.78rem; color: #94a3b8;">Est. remaining: <strong style="color: #e2e8f0;">{item.estimated_remaining_str}</strong></div></div></div><div>{badge_html}</div></div><div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px; font-size: 0.78rem; color: #cbd5e1;"><span style="font-weight: 700; color: {item.status_color};">{item.freshness_score:.0f}% Fresh</span><span style="color: {'#f87171' if 'increasing' in item.trend_str else '#34d399'}; font-weight: 600;">{item.trend_str}</span></div><div style="height: 4px; width: 100%; background: rgba(255,255,255,0.06); border-radius: 999px; overflow: hidden; margin-top: 4px;"><div style="height: 100%; width: {item.freshness_score}%; background: {item.status_color}; border-radius: 999px;"></div></div></div>"""
            )
        with rcol2:
            render_html("<div style='margin-top: 14px;'></div>")
            if st.button("Analysis", key=f"btn_row_analysis_{item.food_id}", use_container_width=True):
                on_select_food(item.food_id)


def render_environment_conditions(reading: SensorReading):
    """
    Renders the 'ENVIRONMENT CONDITIONS' supporting section:
    - Temperature: 24.8°C (↑ Rising)
    - Humidity: 68% (→ Stable)
    - Gas / VOC: 420 ppm (↑ Rising)
    """
    render_html("""<div class="section-header-title">ENVIRONMENT CONDITIONS</div>""")

    sc1, sc2, sc3 = st.columns(3)

    with sc1:
        temp_color = "#f43f5e" if reading.temperature_c > 22.0 else "#10b981"
        temp_trend = "↑ Rising" if reading.temperature_c > 22.0 else "→ Stable"
        render_html(
            f"""<div class="sensor-box-card"><div style="font-size: 1.3rem; margin-bottom: 2px;">🌡️</div><div class="sensor-value-text" style="color: {temp_color};">{reading.temperature_c:.1f}°C</div><div class="sensor-label-text">Temperature</div><div style="font-size: 0.72rem; font-weight: 700; color: {'#f87171' if 'Rising' in temp_trend else '#34d399'}; margin-top: 4px;">{temp_trend}</div></div>"""
        )

    with sc2:
        hum_color = "#06b6d4"
        hum_trend = "→ Stable"
        render_html(
            f"""<div class="sensor-box-card"><div style="font-size: 1.3rem; margin-bottom: 2px;">💧</div><div class="sensor-value-text" style="color: {hum_color};">{reading.humidity_pct:.0f}%</div><div class="sensor-label-text">Humidity</div><div style="font-size: 0.72rem; font-weight: 700; color: #38bdf8; margin-top: 4px;">{hum_trend}</div></div>"""
        )

    with sc3:
        gas_color = "#f43f5e" if reading.gas_ppm > 180 else "#10b981"
        gas_trend = "↑ Rising" if reading.gas_ppm > 150 else "→ Baseline"
        render_html(
            f"""<div class="sensor-box-card"><div style="font-size: 1.3rem; margin-bottom: 2px;">💨</div><div class="sensor-value-text" style="color: {gas_color};">{reading.gas_ppm:.0f} ppm</div><div class="sensor-label-text">Gas / VOC</div><div style="font-size: 0.72rem; font-weight: 700; color: {'#f87171' if 'Rising' in gas_trend else '#34d399'}; margin-top: 4px;">{gas_trend}</div></div>"""
        )


def render_freshsense_ai_analysis(results: List[FoodFreshnessResult]):
    """
    Renders the AI-style analysis section:
    FRESHSENSE ANALYSIS
    "Tomatoes are showing increasing spoilage indicators. Temperature and gas readings have increased over the recent monitoring period."
    Prediction confidence: 87%
    """
    tomato_item = next((r for r in results if r.food_id == "tomato"), results[0])
    render_html(
        f"""<div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(15, 23, 42, 0.85) 100%); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 18px; padding: 18px 20px; margin: 18px 0 10px 0;"><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;"><div style="font-size: 0.85rem; font-weight: 900; letter-spacing: 0.06em; text-transform: uppercase; color: #34d399;">🤖 FRESHSENSE ANALYSIS</div><span style="font-size: 0.78rem; font-weight: 800; color: #10b981; background: rgba(16, 185, 129, 0.15); padding: 3px 10px; border-radius: 999px; border: 1px solid rgba(16, 185, 129, 0.35);">Prediction confidence: {tomato_item.ai_confidence_pct}%</span></div><div style="font-size: 0.92rem; color: #f1f5f9; line-height: 1.5; margin-bottom: 8px;">"{tomato_item.food_name} are showing increasing spoilage indicators. Temperature and gas readings have increased over the recent monitoring period."</div><div style="font-size: 0.75rem; color: #94a3b8;">Estimated based on current sensor trends and calibrated biological decay kinetics.</div></div>"""
    )


def render_food_detail_view(result: FoodFreshnessResult, reading: SensorReading, on_back: Callable[[], None], analyze_gemini_fn: Optional[Callable] = None):
    """Renders the dedicated food detail page with deep-dive analysis and AI vision recipe copilot."""
    profile = get_food_profile(result.food_id)

    if st.button("← Back to Dashboard", key="btn_back_to_dash"):
        on_back()
        return

    render_html(
        f"""<div style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(20, 30, 55, 0.9) 100%); border: 1.5px solid {result.status_color}; border-radius: 22px; padding: 22px; margin: 12px 0 18px 0; box-shadow: 0 0 30px {result.status_bg};"><div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;"><div style="display: flex; align-items: center; gap: 16px;"><span style="font-size: 3.2rem;">{result.icon}</span><div><div style="display: flex; align-items: center; gap: 10px;"><h1 style="margin: 0; font-size: 2rem; font-weight: 900; color: #ffffff;">{result.food_name}</h1><span style="background: {result.status_bg}; color: {result.status_color}; border: 1px solid {result.status_color}; font-size: 0.8rem; font-weight: 800; padding: 3px 10px; border-radius: 999px;">{result.status}</span></div><p style="margin: 4px 0 0 0; font-size: 0.88rem; color: #94a3b8;">Category: <strong>{result.category}</strong> • Storage Zone: <strong>{profile.ideal_storage_location}</strong></p></div></div><div style="text-align: right; background: rgba(0,0,0,0.35); padding: 10px 18px; border-radius: 14px; border: 1px solid rgba(255,255,255,0.08);"><div style="font-size: 0.72rem; color: #94a3b8; font-weight: 700; text-transform: uppercase;">FRESHNESS SCORE</div><div style="font-size: 2rem; font-weight: 900; color: {result.status_color}; font-family: 'JetBrains Mono', monospace;">{result.freshness_score:.0f}<span style="font-size: 1rem; color: #64748b;">/100</span></div><div style="font-size: 0.8rem; color: #cbd5e1;">Est: <strong>{result.estimated_remaining_str}</strong></div></div></div></div>"""
    )

    dcol1, dcol2 = st.columns(2)

    with dcol1:
        st.markdown("#### 📊 WHY? (Sensor Breakdown)")
        render_html(
            f"""<div style="background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 18px; padding: 16px;"><div style="margin-bottom: 10px;"><div style="display: flex; justify-content: space-between; font-size: 0.88rem; font-weight: 700;"><span>🌡️ Temperature</span><span style="color: {'#f43f5e' if reading.temperature_c > profile.optimal_temp_c[1] else '#10b981'};">{reading.temperature_c:.1f}°C</span></div><div style="font-size: 0.76rem; color: #94a3b8;">Preferred: {profile.optimal_temp_c[0]}°C – {profile.optimal_temp_c[1]}°C ({result.temp_status})</div></div><div style="margin-bottom: 10px;"><div style="display: flex; justify-content: space-between; font-size: 0.88rem; font-weight: 700;"><span>💧 Humidity</span><span style="color: {'#f59e0b' if reading.humidity_pct > profile.optimal_humidity_pct[1] else '#10b981'};">{reading.humidity_pct:.1f}%</span></div><div style="font-size: 0.76rem; color: #94a3b8;">Preferred: {profile.optimal_humidity_pct[0]}% – {profile.optimal_humidity_pct[1]}% ({result.humidity_status})</div></div><div style="margin-bottom: 10px;"><div style="display: flex; justify-content: space-between; font-size: 0.88rem; font-weight: 700;"><span>💨 Gas / VOC</span><span style="color: {'#f43f5e' if reading.gas_ppm > 150 else '#10b981'};">{reading.gas_ppm:.0f} ppm</span></div><div style="font-size: 0.76rem; color: #94a3b8;">Status: {result.gas_status}</div></div><hr style="margin: 12px 0; border-color: rgba(255,255,255,0.06);"><div style="font-size: 0.85rem; color: #e2e8f0; line-height: 1.45;"><strong>FRESHSENSE EXPLANATION:</strong><br>{result.primary_reason}</div><div style="margin-top: 8px; font-size: 0.84rem; color: #34d399;">💡 <strong>RECOMMENDED ACTION:</strong><br>{result.recommended_action}</div></div>"""
        )

    with dcol2:
        st.markdown("#### 📈 Freshness Timeline (48 Hours)")
        timeline_df = HistoryService.get_food_timeline(result.food_id, result.freshness_score)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=timeline_df["time"],
            y=timeline_df["freshness_score"],
            mode="lines+markers",
            line=dict(color=result.status_color, width=3),
            marker=dict(size=6, color="#ffffff"),
            name="Freshness Score",
            fill="tozeroy",
            fillcolor=result.status_bg,
        ))
        fig.add_hline(y=80, line_dash="dash", line_color="rgba(16, 185, 129, 0.4)", annotation_text="Fresh (80+)")
        fig.add_hline(y=60, line_dash="dash", line_color="rgba(245, 158, 11, 0.4)", annotation_text="Monitor (60)")
        fig.add_hline(y=30, line_dash="dash", line_color="rgba(239, 68, 68, 0.4)", annotation_text="At Risk (30)")
        
        fig.update_layout(
            height=250,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.5)",
            margin=dict(l=10, r=10, t=20, b=20),
            yaxis=dict(range=[0, 105], gridcolor="rgba(255,255,255,0.05)"),
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            font=dict(color="#94a3b8"),
        )
        st.plotly_chart(fig, use_container_width=True)

    # Multimodal AI Vision & Zero-Waste Culinary Copilot
    st.markdown("---")
    st.markdown(f"### 📸 Multimodal AI Vision & Zero-Waste Culinary Copilot for {result.food_name}")
    st.caption("Inspect physical surface features and generate zero-waste culinary recipes.")

    vcol1, vcol2 = st.columns(2)
    with vcol1:
        cam_photo = st.camera_input("Take a photo with webcam", key=f"cam_detail_{result.food_id}")
        up_photo = st.file_uploader("Or upload image file", type=["jpg", "jpeg", "png"], key=f"up_detail_{result.food_id}")
        selected_photo = cam_photo or up_photo

    with vcol2:
        if selected_photo is not None and analyze_gemini_fn is not None:
            if st.button("🚀 Analyze Food Snapshot & Generate Recipes", type="primary", key="btn_run_gemini_detail"):
                with st.spinner("Analyzing surface features & correlating with IoT telemetry..."):
                    img_bytes = selected_photo.getvalue()
                    res = analyze_gemini_fn(
                        image_bytes=img_bytes,
                        temp=reading.temperature_c,
                        humidity=reading.humidity_pct,
                        gas_ppm=reading.gas_ppm,
                        freshness_score=result.freshness_score
                    )
                    
                    if not isinstance(res, dict):
                        st.error("Received unexpected response format from AI analysis.")
                    elif res.get("error"):
                        err_msg = res.get("message") or res.get("error") or "AI analysis encountered an issue."
                        st.error(f"⚠️ {err_msg}")
                    else:
                        detected_item = res.get("detected_item") or result.food_name
                        safety_verdict = res.get("safety_verdict") or "Normal"
                        visual_condition = res.get("visual_condition") or "Visual features processed."
                        risk_reasoning = res.get("risk_reasoning") or "Environmental and visual telemetry correlated."

                        st.success(f"**Identified:** {detected_item}")
                        st.info(f"**Safety Verdict:** {safety_verdict}")
                        st.write(f"**Visual Observation:** {visual_condition}")
                        st.write(f"**Risk Reasoning:** {risk_reasoning}")
                        
                        recipes = res.get("zero_waste_recipes") or []
                        if recipes:
                            st.markdown("#### 🍳 Zero-Waste Recipes")
                            for idx, rec in enumerate(recipes, 1):
                                if isinstance(rec, dict):
                                    rec_title = rec.get("recipe_name") or f"Recipe {idx}"
                                    rec_time = rec.get("prep_time_minutes", 15)
                                    rec_inst = rec.get("instructions") or "Follow standard cooking guidelines."
                                    with st.expander(f"**{idx}. {rec_title}** ({rec_time} mins)", expanded=True):
                                        st.write(rec_inst)
                                elif isinstance(rec, str):
                                    with st.expander(f"**{idx}. Quick Recipe**", expanded=True):
                                        st.write(rec)
        else:
            st.info("💡 Capture or upload an image to run the multimodal visual inspection.")


def render_notification_center(manager: NotificationManager, on_view_food: Callable[[str], None]):
    """Renders the interactive alert center with filters, read tracking, and food links."""
    render_html(
        """<div style="margin-bottom: 16px;"><h2 style="margin: 0; font-size: 1.75rem; font-weight: 900; color: #ffffff;">🔔 Notification Center</h2><p style="margin: 4px 0 0 0; font-size: 0.88rem; color: #94a3b8;">Real-time food freshness alerts and container state transitions.</p></div>"""
    )

    fcol1, fcol2, fcol3 = st.columns([2, 1, 1])
    with fcol1:
        category = st.radio("Category", ["All", "Critical", "Warning", "Info"], horizontal=True, label_visibility="collapsed")
    with fcol2:
        if st.button("✓ Mark All Read", use_container_width=True):
            manager.mark_all_as_read()
            st.rerun()
    with fcol3:
        if st.button("🗑️ Clear Alerts", use_container_width=True):
            manager.clear_all()
            st.rerun()

    filtered = manager.get_filtered(category)
    if not filtered:
        st.info("✨ No active alerts found in this category.")
        return

    for n in filtered:
        item_class = "notif-item " + (
            "notif-critical" if n.severity == "CRITICAL" else ("notif-warning" if n.severity == "WARNING" else "notif-info")
        )
        ncol1, ncol2 = st.columns([4, 1])
        with ncol1:
            render_html(
                f"""<div class="{item_class}"><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;"><div style="display: flex; align-items: center; gap: 8px;"><span style="font-size: 1.3rem;">{n.food_icon}</span><strong style="color: #ffffff; font-size: 1rem;">{n.title}</strong>{' <span style="background: #f43f5e; color: white; font-size: 0.65rem; font-weight: 900; padding: 2px 6px; border-radius: 999px;">UNREAD</span>' if not n.is_read else ''}</div><div style="font-size: 0.78rem; color: #94a3b8;">{n.formatted_time}</div></div><div style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 6px;">{n.message}</div><div style="font-size: 0.8rem; color: #10b981;">💡 <strong>Recommended:</strong> {n.recommended_action}</div></div>"""
            )
        with ncol2:
            render_html("<div style='margin-top: 10px;'></div>")
            if st.button(f"View {n.food_name}", key=f"btn_notif_view_{n.id}", use_container_width=True):
                manager.mark_as_read(n.id)
                on_view_food(n.food_id)


def render_analytics_dashboard(reading: SensorReading):
    """Renders historical analytics with interactive multi-sensor charts."""
    render_html(
        """<div style="margin-bottom: 18px;"><h2 style="margin: 0; font-size: 1.75rem; font-weight: 900; color: #ffffff;">📈 Storage History & Kinetics Analytics</h2><p style="margin: 4px 0 0 0; font-size: 0.88rem; color: #94a3b8;">Telemetry history and multi-sensor correlation analysis.</p></div>"""
    )

    tframe = st.radio("Time Window", ["24 Hours", "7 Days", "30 Days"], horizontal=True)
    tf_map = {"24 Hours": "24h", "7 Days": "7d", "30 Days": "30d"}
    
    df = HistoryService.get_history_dataframe(
        timeframe=tf_map[tframe],
        current_temp=reading.temperature_c,
        current_humidity=reading.humidity_pct,
        current_gas=reading.gas_ppm
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["time_label"], y=df["freshness_score"], name="Overall Freshness", line=dict(color="#10b981", width=3), yaxis="y1"))
    fig.add_trace(go.Scatter(x=df["time_label"], y=df["gas_ppm"], name="MQ-135 Gas (ppm)", line=dict(color="#f43f5e", width=2, dash="dot"), yaxis="y2"))
    fig.add_trace(go.Scatter(x=df["time_label"], y=df["temperature_c"], name="Temperature (°C)", line=dict(color="#f59e0b", width=2), yaxis="y3"))

    fig.update_layout(
        height=340,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.6)",
        margin=dict(l=10, r=10, t=30, b=20),
        font=dict(color="#94a3b8"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(title="Freshness Score", gridcolor="rgba(255,255,255,0.05)", range=[0, 105]),
        yaxis2=dict(title="Gas PPM", overlaying="y", side="right", showgrid=False),
        yaxis3=dict(title="Temp (°C)", overlaying="y", side="right", position=0.95, showgrid=False),
        legend=dict(orientation="h", y=1.12, x=0.1),
    )
    st.plotly_chart(fig, use_container_width=True)


def render_simulation_sandbox(sim_provider: SimulationSensorProvider, on_apply: Callable[[], None]):
    """
    Renders the simulation controls including the RAPID SPOILAGE DEMO:
    - ⚡ RAPID SPOILAGE DEMO (Step 1: 94% FRESH -> Step 2: 76% MONITOR -> Step 3: 48% AT RISK -> Step 4: 24% CRITICAL)
    - Scenario Presets (Fresh Baseline, Normal Storage, Warning, Rapid Decay, Critical)
    - Manual Sliders
    """
    render_html(
        """<div style="margin-bottom: 18px;"><h2 style="margin: 0; font-size: 1.75rem; font-weight: 900; color: #ffffff;">🎮 Simulation Mode Sandbox</h2><p style="margin: 4px 0 0 0; font-size: 0.88rem; color: #94a3b8;">Demonstrate real-time decay kinetics and alerts with zero physical hardware attached.</p></div>"""
    )

    # ⚡ RAPID SPOILAGE DEMO SECTION
    render_html(
        """<div style="background: linear-gradient(135deg, rgba(244, 63, 94, 0.15) 0%, rgba(15, 23, 42, 0.85) 100%); border: 1px solid rgba(244, 63, 94, 0.4); border-radius: 18px; padding: 18px; margin-bottom: 22px;"><div style="font-size: 1.1rem; font-weight: 900; color: #fca5a5; margin-bottom: 6px;">⚡ RAPID SPOILAGE DEMONSTRATION</div><div style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 14px;">Step through the complete spoilage timeline for <strong>🍅 Tomatoes</strong> and observe sensor shifts, freshness degradation, and triggered notifications:</div></div>"""
    )

    step_cols = st.columns(4)
    for idx, sdata in enumerate(sim_provider.SPOILAGE_STEPS):
        with step_cols[idx]:
            btn_type = "primary" if sim_provider.preset_key == f"spoilage_step_{idx+1}" else "secondary"
            if st.button(f"Step {idx+1}\n{sdata['status']}", key=f"btn_step_{idx+1}", type=btn_type, use_container_width=True):
                sim_provider.apply_spoilage_step(idx)
                on_apply()
                st.rerun()

    # Show active step description if active
    if sim_provider.preset_key.startswith("spoilage_step_"):
        step_num = int(sim_provider.preset_key.split("_")[-1])
        active_step = sim_provider.SPOILAGE_STEPS[step_num - 1]
        st.success(f"**Active Step {step_num}: {active_step['label']}** — {active_step['description']}")

    st.markdown("---")
    st.markdown("#### 📦 Standard Scenario Presets")

    preset_keys = list(sim_provider.PRESETS.keys())
    preset_names = [sim_provider.PRESETS[k]["name"] for k in preset_keys]
    
    current_idx = 0
    if sim_provider.preset_key in preset_keys:
        current_idx = preset_keys.index(sim_provider.preset_key)

    chosen = st.radio("Select Scenario Preset", preset_names, index=current_idx)
    sel_key = preset_keys[preset_names.index(chosen)]
    
    st.info(f"ℹ️ {sim_provider.PRESETS[sel_key]['description']}")
    
    if st.button("⚡ Apply Selected Scenario", type="primary", use_container_width=True):
        sim_provider.apply_preset(sel_key)
        on_apply()
        st.success(f"Applied: {chosen}")
        st.rerun()

    st.markdown("---")
    st.markdown("#### 🎛️ Manual Slider Overrides")
    curr = sim_provider.get_current_reading()
    
    c1, c2 = st.columns(2)
    with c1:
        t = st.slider("Temperature (°C)", 1.0, 45.0, float(curr.temperature_c), 0.5)
        h = st.slider("Humidity (%)", 20.0, 98.0, float(curr.humidity_pct), 1.0)
    with c2:
        g = st.slider("Gas / VOC (ppm)", 10.0, 800.0, float(curr.gas_ppm), 5.0)
        hrs = st.slider("Storage Exposure (hrs)", 0.0, 120.0, float(curr.hours_elapsed), 1.0)

    if st.button("Apply Custom Values", use_container_width=True):
        sim_provider.set_reading(t, h, g, hrs)
        on_apply()
        st.success("Custom values applied!")
        st.rerun()


def render_settings_page(reading: SensorReading):
    """Renders settings, alert threshold preferences, and hardware specs."""
    st.markdown("## ⚙️ Settings & Device Specs")
    
    st.markdown("### 📦 Hardware Container Node")
    d1, d2, d3 = st.columns(3)
    with d1:
        st.metric("Device Name", reading.device_name)
    with d2:
        st.metric("Battery Level", f"{reading.battery_pct:.0f}%")
    with d3:
        st.metric("Operating Mode", "Simulation Telemetry")

    st.markdown("---")
    st.markdown("### 🔔 Alert & Notification Preferences")
    st.checkbox("🚨 High Priority / Critical Alerts", value=True)
    st.checkbox("⚠️ Monitoring Warnings (Approaching Threshold)", value=True)
    st.checkbox("🌡️ Environmental Shift Alerts", value=True)
    st.checkbox("🔊 Web Audio Synthesizer Chime", value=True)

    st.markdown("---")
    st.markdown("### 🛡️ Firmware & Architecture")
    st.caption("FreshSense AI OS v2.4 (Simulated IoT Core) • ESP32 Hardware Adapter Ready • Biological Decay Kinetics Engine v3.1")


# Backward-compatible function aliases
render_top_header = render_dashboard_header
render_container_status_card = render_overall_freshness_hero
render_freshness_alert_hero = render_main_alert_card
render_your_food_list_section = render_your_food_section
render_sensor_conditions_section = render_environment_conditions
render_device_container_page = render_settings_page
render_food_detail_page = render_food_detail_view
render_food_gallery_page = render_your_food_section


