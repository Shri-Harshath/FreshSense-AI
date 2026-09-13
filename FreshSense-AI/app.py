"""
FreshSense AI - Smart Food Preservation & Freshness Monitoring System
=====================================================================
Main Application Controller implementing the complete user-specified visual layout:
- Header: FreshSense AI | Know Before It Spoils. | Kitchen Container 01 ● Simulation Mode | 🔔 2
- Hero Freshness: OVERALL FRESHNESS (72%, 2 items need attention)
- Main Alert: ⚠ FRESHNESS ALERT | 🍅 TOMATOES | MAY SPOIL SOON | ~8 hours remaining | Risk: HIGH
- Food Section: YOUR FOOD (Tomatoes, Lemon, Bell Pepper, Apple, Banana, Leafy Greens) with Filter Pills
- Environment Conditions: 24.8°C Temp ↑ Rising | 68% Humidity → Stable | 420 ppm Gas ↑ Rising
- FreshSense Analysis: 87% Confidence, transparent biological reasoning
- Pages: Home, Food, Alerts, Analytics, Simulation, Settings
"""

import streamlit as st
import pandas as pd

from core import (
    SimulationSensorProvider,
    FreshnessPredictionService,
    NotificationManager,
    HistoryService,
    get_all_food_profiles,
    get_food_profile,
)
from ui.styles import CUSTOM_CSS
from ui.components import (
    render_dashboard_header,
    render_overall_freshness_hero,
    render_main_alert_card,
    render_your_food_section,
    render_environment_conditions,
    render_freshsense_ai_analysis,
    render_food_detail_view,
    render_notification_center,
    render_analytics_dashboard,
    render_simulation_sandbox,
    render_settings_page,
    render_html,
)
from gemini_advisor import analyze_food

# 1. Page Configuration
st.set_page_config(
    page_title="FreshSense AI - Know Before It Spoils",
    page_icon="🥑",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 2. Inject Custom CSS
render_html(CUSTOM_CSS)

# 3. Session State Initialization
if "sim_provider" not in st.session_state:
    st.session_state.sim_provider = SimulationSensorProvider("dashboard_mockup")

if "freshness_service" not in st.session_state:
    st.session_state.freshness_service = FreshnessPredictionService()

if "notif_manager" not in st.session_state:
    st.session_state.notif_manager = NotificationManager()

if "active_page" not in st.session_state:
    st.session_state.active_page = "Home"

if "selected_food_id" not in st.session_state:
    st.session_state.selected_food_id = "tomato"

if "food_filter" not in st.session_state:
    st.session_state.food_filter = "All"

# 4. Fetch Telemetry & Run Diagnostics
current_reading = st.session_state.sim_provider.get_current_reading()
freshness_results = st.session_state.freshness_service.analyze_all_foods(current_reading)

# 5. Process Notifications & State Transitions
st.session_state.notif_manager.process_results(freshness_results)
unread_count = st.session_state.notif_manager.get_unread_count()


# 6. Navigation Actions
def set_page(page_name: str):
    st.session_state.active_page = page_name
    st.rerun()


def view_food_analysis(food_id: str):
    st.session_state.selected_food_id = food_id
    st.session_state.active_page = "Food"
    st.rerun()


# 7. Sidebar Controls (Quick Scenarios & Telemetry Info)
with st.sidebar:
    st.markdown("### 🥑 FreshSense AI")
    st.caption("Smart Food Preservation System")
    st.markdown("---")
    
    st.markdown("#### ⚡ Scenario Presets")
    preset_keys = list(st.session_state.sim_provider.PRESETS.keys())
    preset_names = [st.session_state.sim_provider.PRESETS[k]["name"] for k in preset_keys]
    
    current_p_idx = preset_keys.index(st.session_state.sim_provider.preset_key) if st.session_state.sim_provider.preset_key in preset_keys else 0
    selected_preset_lbl = st.selectbox("Active Scenario", preset_names, index=current_p_idx)
    target_key = preset_keys[preset_names.index(selected_preset_lbl)]
    
    if target_key != st.session_state.sim_provider.preset_key:
        if st.button("Apply Scenario", use_container_width=True, type="primary"):
            st.session_state.sim_provider.apply_preset(target_key)
            st.rerun()

    st.markdown("---")
    st.markdown(f"**Container Node:** {current_reading.device_name}")
    st.markdown(f"**Mode:** Simulation Telemetry")
    st.markdown(f"**Battery:** {current_reading.battery_pct:.0f}%")
    st.markdown(f"**Signal:** {current_reading.signal_strength_dbm} dBm")
    
    st.markdown("---")
    if st.button("🎮 Open Simulation Sandbox", use_container_width=True):
        set_page("Simulation")


# 8. Main UI Layout Routing
if st.session_state.active_page == "Home":
    # 1. Top Brand Header with Bell Badge (🔔 2)
    render_dashboard_header(
        reading=current_reading,
        unread_count=unread_count,
        on_click_alerts=lambda: set_page("Alerts")
    )

    # 2. Hero Overall Freshness Card (72%, 2 items need attention)
    render_overall_freshness_hero(
        results=freshness_results
    )

    # 3. Main Alert Hero (⚠ FRESHNESS ALERT • 🍅 TOMATOES • MAY SPOIL SOON)
    render_main_alert_card(
        results=freshness_results,
        on_view_analysis=view_food_analysis
    )

    # 4. YOUR FOOD Section with Filter Pills & Food Cards
    render_your_food_section(
        results=freshness_results,
        on_select_food=view_food_analysis,
        selected_filter=st.session_state.get("food_filter", "All")
    )

    # 5. ENVIRONMENT CONDITIONS (24.8°C Temp ↑ Rising, 68% Humidity → Stable, 420 ppm Gas ↑ Rising)
    render_environment_conditions(
        reading=current_reading
    )

    # 6. FRESHSENSE AI Analysis Section (87% Confidence)
    render_freshsense_ai_analysis(
        results=freshness_results
    )

elif st.session_state.active_page == "Food":
    active_res = next((r for r in freshness_results if r.food_id == st.session_state.selected_food_id), freshness_results[0])
    render_food_detail_view(
        result=active_res,
        reading=current_reading,
        on_back=lambda: set_page("Home"),
        analyze_gemini_fn=analyze_food
    )

elif st.session_state.active_page == "Alerts":
    if st.button("← Back to Dashboard", key="btn_back_from_alerts"):
        set_page("Home")
    render_notification_center(
        manager=st.session_state.notif_manager,
        on_view_food=view_food_analysis
    )

elif st.session_state.active_page == "Analytics":
    if st.button("← Back to Dashboard", key="btn_back_from_analytics"):
        set_page("Home")
    render_analytics_dashboard(current_reading)

elif st.session_state.active_page == "Simulation":
    if st.button("← Back to Dashboard", key="btn_back_from_sim"):
        set_page("Home")
    render_simulation_sandbox(st.session_state.sim_provider, on_apply=st.rerun)

elif st.session_state.active_page == "Settings":
    if st.button("← Back to Dashboard", key="btn_back_from_settings"):
        set_page("Home")
    render_settings_page(current_reading)


# 9. Bottom Navigation Dock (Home, Food, Alerts, Analytics, Simulation)
render_html("<div style='margin-top: 24px;'></div><hr style='border-color: rgba(255,255,255,0.08); margin: 20px 0 14px 0;'>")

nav_cols = st.columns(5)
with nav_cols[0]:
    if st.button("🏠 Home", use_container_width=True, type="primary" if st.session_state.active_page == "Home" else "secondary"):
        set_page("Home")

with nav_cols[1]:
    if st.button("🥗 Food", use_container_width=True, type="primary" if st.session_state.active_page == "Food" else "secondary"):
        set_page("Food")

with nav_cols[2]:
    alert_lbl = f"🔔 Alerts ({unread_count})" if unread_count > 0 else "🔔 Alerts"
    if st.button(alert_lbl, use_container_width=True, type="primary" if st.session_state.active_page == "Alerts" else "secondary"):
        set_page("Alerts")

with nav_cols[3]:
    if st.button("📈 Analytics", use_container_width=True, type="primary" if st.session_state.active_page == "Analytics" else "secondary"):
        set_page("Analytics")

with nav_cols[4]:
    if st.button("🎮 Sim & Config", use_container_width=True, type="primary" if st.session_state.active_page in ["Simulation", "Settings"] else "secondary"):
        set_page("Simulation")
