"""
FreshSense AI - Smart Food Preservation & Freshness Monitoring System
=====================================================================
Main Application Controller implementing the complete user-specified visual layout:
- Left Sidebar: Dark navy blue sidebar, brand logo, tagline, navigation items, container preview
- Top Header: Know Before It Spoils. | Kitchen Container 01 ● Simulation Mode | 🔔 unread count | 👤 avatar
- Hero Row: OVERALL FRESHNESS (Left) | 3D Smart Container on Pedestal (Center) | FRESHNESS ALERT (Right)
- Food Section: YOUR FOOD (Tomatoes, Lemon, Bell Pepper, Apple, Banana, Leafy Greens) with filter pills
- Bottom Row: Environment Conditions (Left) & FreshSense AI Analysis (Right)
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
from ui.assets_data import HERO_CONTAINER_B64
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

# 1. Page Configuration (Wide Layout & Expanded Sidebar matching Reference)
st.set_page_config(
    page_title="FreshSense AI - Know Before It Spoils",
    page_icon="🥑",
    layout="wide",
    initial_sidebar_state="expanded",
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


# 7. Left Sidebar Navigation (Matching Reference Design)
with st.sidebar:
    render_html(
        """
        <div class="sidebar-brand-box">
            <div class="sidebar-brand-icon">🍃</div>
            <div>
                <div class="sidebar-brand-text">FreshSense AI</div>
                <div class="sidebar-brand-tagline">Know Before It Spoils.</div>
            </div>
        </div>
        """
    )

    # Primary Navigation Links
    if st.button("🏠  Home", key="sb_btn_home", use_container_width=True, type="primary" if st.session_state.active_page == "Home" else "secondary"):
        set_page("Home")

    if st.button("🥗  Food", key="sb_btn_food", use_container_width=True, type="primary" if st.session_state.active_page == "Food" else "secondary"):
        set_page("Food")

    alert_sidebar_lbl = f"🔔  Alerts  ({unread_count})" if unread_count > 0 else "🔔  Alerts"
    if st.button(alert_sidebar_lbl, key="sb_btn_alerts", use_container_width=True, type="primary" if st.session_state.active_page == "Alerts" else "secondary"):
        set_page("Alerts")

    if st.button("📈  Analytics", key="sb_btn_analytics", use_container_width=True, type="primary" if st.session_state.active_page == "Analytics" else "secondary"):
        set_page("Analytics")

    if st.button("⚙️  Settings", key="sb_btn_settings", use_container_width=True, type="primary" if st.session_state.active_page == "Settings" else "secondary"):
        set_page("Settings")

    if st.button("🎮  Simulation Sandbox", key="sb_btn_sim", use_container_width=True, type="primary" if st.session_state.active_page == "Simulation" else "secondary"):
        set_page("Simulation")

    st.markdown("---")

    # Lower Sidebar: Kitchen Container 01 Preview Card
    render_html(
        f"""
        <div class="sidebar-container-preview">
            <div style="width: 75px; height: 75px; margin: 0 auto 6px auto; display: flex; align-items: center; justify-content: center;">
                <img src="{HERO_CONTAINER_B64}" alt="Kitchen Container 01" style="max-width: 100%; max-height: 100%; object-fit: contain; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));" />
            </div>
            <div style="font-size: 0.9rem; font-weight: 800; color: #ffffff;">{current_reading.device_name}</div>
            <div class="sidebar-container-tag">● Simulation Mode &gt;</div>
            <div style="font-size: 0.72rem; color: #94a3b8; margin-top: 10px; display: flex; align-items: center; justify-content: center; gap: 4px;">
                <span>🍃</span> <span>Fresh food / Better life</span>
            </div>
        </div>
        """
    )

    st.markdown("---")

    # Quick Scenario Presets in Sidebar
    with st.expander("⚡ Scenario Presets & Node Telemetry", expanded=False):
        preset_keys = list(st.session_state.sim_provider.PRESETS.keys())
        preset_names = [st.session_state.sim_provider.PRESETS[k]["name"] for k in preset_keys]
        
        current_p_idx = preset_keys.index(st.session_state.sim_provider.preset_key) if st.session_state.sim_provider.preset_key in preset_keys else 0
        selected_preset_lbl = st.selectbox("Active Scenario", preset_names, index=current_p_idx, key="sb_select_preset")
        target_key = preset_keys[preset_names.index(selected_preset_lbl)]
        
        if target_key != st.session_state.sim_provider.preset_key:
            if st.button("Apply Scenario", use_container_width=True, type="primary", key="sb_btn_apply_preset"):
                st.session_state.sim_provider.apply_preset(target_key)
                st.rerun()

        st.caption(f"Battery: {current_reading.battery_pct:.0f}% • Signal: {current_reading.signal_strength_dbm} dBm")


# 8. Main UI Layout Routing
if st.session_state.active_page == "Home":
    # 1. Top Brand Header with Bell Badge (🔔 2) and User Profile Avatar
    render_dashboard_header(
        reading=current_reading,
        unread_count=unread_count,
        on_click_alerts=lambda: set_page("Alerts")
    )

    # 2. Hero Row (Overall Freshness | 3D Smart Food Container | Freshness Alert)
    h_col1, h_col2, h_col3 = st.columns([1.05, 1.25, 1.15], gap="medium")
    with h_col1:
        render_overall_freshness_hero(
            results=freshness_results
        )

    with h_col2:
        render_html(
            f"""
            <div class="center-container-hero-card">
                <img src="{HERO_CONTAINER_B64}" alt="FreshSense AI Smart Food Container" class="center-container-img" />
            </div>
            """
        )

    with h_col3:
        render_main_alert_card(
            results=freshness_results,
            on_view_analysis=view_food_analysis
        )

    # 3. YOUR FOOD Section with Filter Pills & Individual Food Cards
    render_your_food_section(
        results=freshness_results,
        on_select_food=view_food_analysis,
        selected_filter=st.session_state.get("food_filter", "All")
    )

    # 4. Environment Conditions & FreshSense AI Analysis (Side by Side)
    b_col1, b_col2 = st.columns([1.55, 1.45], gap="medium")
    with b_col1:
        render_environment_conditions(
            reading=current_reading
        )

    with b_col2:
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


# 9. Bottom Navigation Floating Dock (Home, Food, Alerts, Analytics, Simulation)
render_html("<div style='margin-top: 24px;'></div><hr style='border-color: rgba(0,0,0,0.06); margin: 20px 0 14px 0;'>")

nav_cols = st.columns(5)
with nav_cols[0]:
    if st.button("🏠 Home", use_container_width=True, type="primary" if st.session_state.active_page == "Home" else "secondary", key="dock_btn_home"):
        set_page("Home")

with nav_cols[1]:
    if st.button("🥗 Food", use_container_width=True, type="primary" if st.session_state.active_page == "Food" else "secondary", key="dock_btn_food"):
        set_page("Food")

with nav_cols[2]:
    alert_lbl = f"🔔 Alerts ({unread_count})" if unread_count > 0 else "🔔 Alerts"
    if st.button(alert_lbl, use_container_width=True, type="primary" if st.session_state.active_page == "Alerts" else "secondary", key="dock_btn_alerts"):
        set_page("Alerts")

with nav_cols[3]:
    if st.button("📈 Analytics", use_container_width=True, type="primary" if st.session_state.active_page == "Analytics" else "secondary", key="dock_btn_analytics"):
        set_page("Analytics")

with nav_cols[4]:
    if st.button("🎮 Sim & Config", use_container_width=True, type="primary" if st.session_state.active_page in ["Simulation", "Settings"] else "secondary", key="dock_btn_sim"):
        set_page("Simulation")
