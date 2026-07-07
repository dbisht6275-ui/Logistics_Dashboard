import streamlit as st
from services.login import login_page
from services.roles import get_allowed_menu, get_allowed_reports, clear_role_cache

from pages.Home.overview_tab import show_overview
from pages.Home.comparison_tab import show_comparison
from pages.Home.Customer_Analysis import show_CustomerAnalysis
from pages.Home.Service_Analysis import show_service_level
from pages.IT.zone_booking_turnover import show_ZoneBookingTurnover

from pages.Accounts.GrCostingHeadWise import show_GrCostingHeadWise
from pages.Admin.user_management import show_UserManagement


st.set_page_config(
    page_title="Sugam Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================
# Modern Sidebar Styling
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #06172D 0%, #0A2240 55%, #07172D 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
    font-family: 'Inter', sans-serif;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 18px 14px;
}

[data-testid="stSidebar"] * {
    color: #EAF1FF;
}

.sidebar-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 800;
    font-size: 15px;
    margin-bottom: 18px;
}

.sidebar-logo {
    width: 28px;
    height: 28px;
    border-radius: 8px;
    background: rgba(255,255,255,0.08);
    display: flex;
    align-items: center;
    justify-content: center;
}

.sidebar-collapse {
    margin-left: auto;
    width: 24px;
    height: 24px;
    background: rgba(255,255,255,0.08);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.profile-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 13px;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.18);
}

.avatar {
    width: 44px;
    height: 44px;
    border-radius: 11px;
    background: linear-gradient(135deg, #FFB22E, #F59E0B);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
}

.emp-id {
    font-size: 13px;
    font-weight: 700;
    color: #F7FAFF;
}

.role-badge {
    display: inline-block;
    margin-top: 5px;
    background: rgba(245,158,11,0.18);
    color: #FBBF24;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 0.12em;
    padding: 2px 8px;
    border-radius: 20px;
}

.section-label {
    color: #7086A6 !important;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    margin: 18px 0 8px 3px;
}

[data-testid="stSidebar"] .stButton button {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 9px;
    font-size: 12px;
    font-weight: 600;
    color: #D7E4F8;
    min-height: 36px;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(255,255,255,0.08);
    border-color: rgba(139,92,246,0.5);
    color: #FFFFFF;
}

[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 4px;
}

[data-testid="stSidebar"] div[role="radiogroup"] label {
    min-height: 38px;
    padding: 9px 12px !important;
    margin: 0 !important;
    border-radius: 9px;
    border: 1px solid transparent;
    background: transparent;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.06);
}

[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(90deg, #5B45D8, #4A35B9);
    box-shadow: 0 8px 20px rgba(91,69,216,0.35);
}

[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
    display: none;
}

[data-testid="stSidebar"] div[role="radiogroup"] label p {
    font-size: 13px;
    font-weight: 600;
    color: #DCE8FA;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {
    color: #FFFFFF;
    font-weight: 700;
}

[data-testid="stSidebar"] input[type="text"] {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 10px;
    color: #EAF1FF;
    font-size: 12px;
}

[data-testid="stSidebar"] input[type="text"]::placeholder {
    color: #91A4C0;
}

[data-testid="stSidebar"] [data-testid="stExpander"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.08) !important;
}

.sidebar-footer {
    margin-top: 20px;
    font-size: 10px;
    color: #627896 !important;
    line-height: 1.6;
}

.sidebar-footer span {
    color: #2DD4BF !important;
}

[data-testid="stSidebar"] .stToggle label p {
    font-size: 12px;
    font-weight: 600;
}

[data-testid="stSidebar"] .stSelectbox label {
    display: none;
}
</style>
""", unsafe_allow_html=True)


# =========================
# Full Menu Items
# =========================
FULL_MENU_ITEMS = [
    "🏠 Overview",
    "📊 Comparison",
    "📈 Branch Analysis",
    "👥 Customer Analysis",
    "🚛 Service Analysis",
    "📄 Reports",
    "🛠️ User Management",
]


REPORTS = {
    "🖥️ IT Reports": {
        "📊 Zone Booking Turnover": show_ZoneBookingTurnover,
    },
    "💰 Accounts Reports": {
        "📋 GR Costing Head Wise": show_GrCostingHeadWise,
    }
}


st.session_state["_all_menu_items"] = FULL_MENU_ITEMS
st.session_state["_all_reports"] = [
    name for reports in REPORTS.values() for name in reports.keys()
]


# =========================
# Login Session
# =========================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "selected_report" not in st.session_state:
    st.session_state["selected_report"] = None

if not st.session_state["logged_in"]:
    login_page()
    st.stop()


# =========================
# Role-based Access
# =========================
role = st.session_state.get("role", "viewer")

allowed_menu = get_allowed_menu(role)
allowed_reports = get_allowed_reports(role)

REPORTS_VISIBLE = {
    department: {
        report_name: report_fn
        for report_name, report_fn in reports.items()
        if report_name in allowed_reports
    }
    for department, reports in REPORTS.items()
}

REPORTS_VISIBLE = {
    dept: reports
    for dept, reports in REPORTS_VISIBLE.items()
    if reports
}


# =========================
# Sidebar
# =========================
with st.sidebar:

    st.markdown("""
        <div class="sidebar-title">
            <div class="sidebar-logo">📊</div>
            <span>Logistics BI</span>
            <span class="sidebar-collapse">‹</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="profile-card">
            <div class="avatar">👤</div>
            <div>
                <div class="emp-id">Employee ID: {st.session_state['employee_id']}</div>
                <span class="role-badge">{role.upper()}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("↪ Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    if not allowed_menu:
        st.warning("No access has been assigned to your role yet. Contact the admin.")
        st.stop()

    # Favorites
    st.markdown('<div class="section-label">Favorites</div>', unsafe_allow_html=True)

    if "👥 Customer Analysis" in allowed_menu:
        if st.button("⭐ Customer Analysis", use_container_width=True):
            st.session_state["menu_override"] = "👥 Customer Analysis"
            st.rerun()

    # Navigation
    st.markdown('<div class="section-label">Navigation</div>', unsafe_allow_html=True)

    search_menu = st.text_input(
        "Search menu",
        label_visibility="collapsed",
        placeholder="🔍 Search menu..."
    )

    filtered_menu = [
        item for item in allowed_menu
        if search_menu.lower() in item.lower()
    ] if search_menu else allowed_menu

    if not filtered_menu:
        st.info("No menu found.")
        st.stop()

    if "menu_override" in st.session_state:
        default_menu = st.session_state.pop("menu_override")
        index = filtered_menu.index(default_menu) if default_menu in filtered_menu else 0
    else:
        index = 0

    menu = st.radio(
        "Navigation",
        filtered_menu,
        index=index,
        label_visibility="collapsed"
    )

    # Reports Area
    if menu == "📄 Reports":
        st.markdown('<div class="section-label">Report Search</div>', unsafe_allow_html=True)

        search_text = st.text_input(
            "Search by report name",
            label_visibility="collapsed",
            placeholder="🔍 Search report..."
        )

        if search_text:
            for department, reports in REPORTS_VISIBLE.items():
                for report_name in reports.keys():
                    if search_text.lower() in report_name.lower():
                        if st.button(
                            report_name,
                            key=f"search_{report_name}",
                            use_container_width=True
                        ):
                            st.session_state["selected_report"] = report_name
                            st.rerun()

        st.markdown('<div class="section-label">Report Folders</div>', unsafe_allow_html=True)

        if not REPORTS_VISIBLE:
            st.info("No reports assigned to your role.")
        else:
            for department, reports in REPORTS_VISIBLE.items():
                with st.expander(department, expanded=False):
                    for report_name in reports.keys():
                        if st.button(
                            report_name,
                            key=f"{department}_{report_name}",
                            use_container_width=True
                        ):
                            st.session_state["selected_report"] = report_name
                            st.rerun()

    st.divider()

    # Quick Actions
    st.markdown('<div class="section-label">Quick Actions</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("↻", help="Refresh Data", use_container_width=True):
            st.cache_data.clear()
            clear_role_cache()
            st.success("Data refreshed!")

    with col2:
        st.button("⇩", help="Export", use_container_width=True)

    with col3:
        st.button("?", help="Help", use_container_width=True)

    # Settings
    st.markdown('<div class="section-label">Settings</div>', unsafe_allow_html=True)

    st.toggle("🌙 Theme", value=True)

    st.selectbox(
        "Language",
        ["English"],
        label_visibility="collapsed"
    )

    st.markdown("""
        <div class="sidebar-footer">
            © 2024 Logistics BI<br>
            <span>●</span> All systems operational
        </div>
    """, unsafe_allow_html=True)


# =========================
# Page Routing
# =========================
if menu == "🏠 Overview":
    show_overview()

elif menu == "📊 Comparison":
    show_comparison()

elif menu == "📈 Branch Analysis":
    st.info("Branch Analysis page coming soon.")

elif menu == "👥 Customer Analysis":
    show_CustomerAnalysis()

elif menu == "🚛 Service Analysis":
    show_service_level()

elif menu == "🛠️ User Management":
    show_UserManagement()

elif menu == "📄 Reports":

    selected = st.session_state.get("selected_report")

    if selected is None:
        st.info("Please select a report from the sidebar.")

    elif selected not in allowed_reports:
        st.error("You don't have access to this report.")
        st.session_state["selected_report"] = None

    else:
        report_found = False

        for department, reports in REPORTS_VISIBLE.items():
            if selected in reports:
                reports[selected]()
                report_found = True
                break

        if not report_found:
            st.error("Selected report not found.")