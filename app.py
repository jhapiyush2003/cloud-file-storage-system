
import streamlit as st
from src.db import init_db
from src.auth import login_page, signup_page
from src.dashboard import dashboard_page
from src.files import files_page
from src.upload import upload_page
from src.settings import settings_page
 
st.set_page_config(
    page_title="NexCloud Storage",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
init_db()
 
# ── Global CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
 
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #070b14;
    color: #e2e8f0;
}
 
/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; }
 
/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #0a0f1e 100%);
    border-right: 1px solid rgba(99,102,241,0.15);
    width: 260px !important;
}
section[data-testid="stSidebar"] > div { padding: 0; }
 
/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #6366f1; border-radius: 4px; }
 
/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(99,102,241,0.25) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    padding: 10px 14px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}
 
/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    transition: all 0.2s !important;
    letter-spacing: 0.3px;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 25px rgba(99,102,241,0.4) !important;
}
 
/* File uploader */
[data-testid="stFileUploadDropzone"] {
    background: rgba(99,102,241,0.04) !important;
    border: 2px dashed rgba(99,102,241,0.4) !important;
    border-radius: 16px !important;
}
 
/* Radio (nav) */
.stRadio > div { gap: 4px; }
.stRadio > div > label {
    border-radius: 10px;
    padding: 8px 14px;
    cursor: pointer;
    transition: all 0.15s;
    color: #94a3b8 !important;
    font-size: 14px;
}
.stRadio > div > label:hover { background: rgba(99,102,241,0.1); color: white !important; }
.stRadio [data-testid="stMarkdownContainer"] p { margin: 0; }
 
/* Success / error */
.stAlert { border-radius: 12px !important; }
 
/* Metric */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 16px;
}
 
/* Table */
.stDataFrame { border-radius: 12px; overflow: hidden; }
thead th { background: #1e1b4b !important; }
</style>
""", unsafe_allow_html=True)
 
 
def sidebar_nav():
    with st.sidebar:
        st.markdown("""
        <div style="padding:24px 20px 16px;">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                <div style="width:36px;height:36px;background:linear-gradient(135deg,#6366f1,#8b5cf6);
                    border-radius:10px;display:flex;align-items:center;justify-content:center;
                    font-size:18px;">☁️</div>
                <div>
                    <div style="font-size:18px;font-weight:800;color:white;letter-spacing:-0.5px;">NexCloud</div>
                    <div style="font-size:11px;color:#6366f1;font-weight:600;letter-spacing:1px;">STORAGE</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
 
        user = st.session_state.get("user")
        if user:
            st.markdown(f"""
            <div style="margin:0 12px 16px;padding:12px 14px;background:rgba(99,102,241,0.08);
                border-radius:12px;border:1px solid rgba(99,102,241,0.15);">
                <div style="font-size:12px;color:#94a3b8;">Signed in as</div>
                <div style="font-size:14px;font-weight:600;color:white;margin-top:2px;">
                    👤 {user['username']}</div>
            </div>
            """, unsafe_allow_html=True)
 
        st.markdown("<div style='padding:0 12px;'>", unsafe_allow_html=True)
        page = st.radio(
            "nav",
            ["🏠  Dashboard", "📁  My Files", "📤  Upload", "⚙️  Settings"],
            label_visibility="collapsed"
        )
        st.markdown("</div>", unsafe_allow_html=True)
 
        st.markdown("<div style='position:absolute;bottom:20px;width:100%;padding:0 12px;box-sizing:border-box;'>", unsafe_allow_html=True)
        if st.button("🚪  Sign Out", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
 
    return page
 
 
# ── Router ──────────────────────────────────────────────────────────────────
if "user" not in st.session_state:
    # Auth flow
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
        auth_tab = st.radio("auth", ["Sign In", "Create Account"], horizontal=True, label_visibility="collapsed")
        if auth_tab == "Sign In":
            login_page()
        else:
            signup_page()
else:
    page = sidebar_nav()
    page_key = page.strip().split("  ")[-1]
 
    if page_key == "Dashboard":
        dashboard_page()
    elif page_key == "My Files":
        files_page()
    elif page_key == "Upload":
        upload_page()
    elif page_key == "Settings":
        settings_page()
