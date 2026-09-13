"""
FreshSense AI - UI Package
"""
from .styles import CUSTOM_CSS, CHIME_AUDIO_SCRIPT
from .components import (
    render_dashboard_header,
    render_overall_freshness_hero,
    render_main_alert_card,
    render_your_food_section,
    render_environment_conditions,
    render_freshsense_ai_analysis,
    render_food_detail_view,
    render_notification_center,
    render_simulation_sandbox,
    render_analytics_dashboard,
    render_settings_page,
    # Backward-compatible aliases
    render_top_header,
    render_container_status_card,
    render_freshness_alert_hero,
    render_your_food_list_section,
    render_sensor_conditions_section,
    render_device_container_page,
    render_food_gallery_page,
)
from .three_scenes import (
    get_3d_smart_container_hero_html,
    get_3d_ai_flow_html,
)
