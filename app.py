import streamlit as st
import os
from datetime import datetime
from db import (init_db, get_user_by_username, get_user_by_email,
                create_user, update_password, save_file,
                get_files, delete_file, toggle_star, get_stats)

from utils import (ensure_dir, fmt_size, get_type, icon, color,
                   hash_pw, verify_pw, valid_email, safe_name)

# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Piyush Cloud", page_icon="⬡", layout="wide",
                   initial_sidebar_state="expanded")
init_db()
# ─────────────────────────────────────────────────────────────────────────────

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: #030712;
    color: #cbd5e1;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] > div:first-child { padding: 0; }

/* ── Animated background ── */
body::before {
    content: '';
    position: fixed; inset: 0; z-index: -1;
    background:
        radial-gradient(ellipse 80% 60% at 10% 20%, rgba(14,165,233,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 60% 80% at 90% 80%, rgba(139,92,246,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 50% 50% at 50% 50%, rgba(6,182,212,0.03) 0%, transparent 70%),
        #030712;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: rgba(3,7,18,0.95) !important;
    border-right: 1px solid rgba(14,165,233,0.12) !important;
    width: 270px !important;
    backdrop-filter: blur(20px);
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    transition: all 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: rgba(14,165,233,0.5) !important;
    box-shadow: 0 0 0 3px rgba(14,165,233,0.1) !important;
    background: rgba(14,165,233,0.04) !important;
}
.stTextInput > label, .stSelectbox > label, .stTextArea > label,
.stFileUploader > label, .stCheckbox > label {
    color: #64748b !important;
    font-size: 12px !important;
    letter-spacing: 0.05em !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 10px 20px !important;
    transition: all 0.25s cubic-bezier(0.4,0,0.2,1) !important;
    letter-spacing: 0.01em !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 30px rgba(14,165,233,0.35) !important;
    background: linear-gradient(135deg, #38bdf8, #0ea5e9) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Download button ── */
.stDownloadButton > button {
    background: rgba(255,255,255,0.05) !important;
    color: #94a3b8 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    padding: 6px 14px !important;
}
.stDownloadButton > button:hover {
    background: rgba(14,165,233,0.1) !important;
    color: #38bdf8 !important;
    border-color: rgba(14,165,233,0.3) !important;
    transform: translateY(-1px) !important;
    box-shadow: none !important;
}

/* ── Radio (nav) ── */
div[data-testid="stRadio"] > div { gap: 2px !important; }
div[data-testid="stRadio"] > div > label {
    border-radius: 10px !important;
    padding: 9px 14px !important;
    font-size: 14px !important;
    color: #475569 !important;
    transition: all 0.15s !important;
    cursor: pointer !important;
}
div[data-testid="stRadio"] > div > label:hover { background: rgba(14,165,233,0.08) !important; color: #94a3b8 !important; }
div[data-testid="stRadio"] > div > label[data-baseweb="radio"] > div:first-child { display: none !important; }

/* ── Select ── */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
}

/* ── File uploader ── */
[data-testid="stFileUploadDropzone"] {
    background: rgba(14,165,233,0.03) !important;
    border: 1.5px dashed rgba(14,165,233,0.25) !important;
    border-radius: 16px !important;
    transition: all 0.2s !important;
}
[data-testid="stFileUploadDropzone"]:hover {
    border-color: rgba(14,165,233,0.5) !important;
    background: rgba(14,165,233,0.06) !important;
}

/* ── Progress bar ── */
.stProgress > div > div > div { background: linear-gradient(90deg, #0ea5e9, #38bdf8) !important; border-radius: 99px !important; }
.stProgress > div > div { background: rgba(255,255,255,0.06) !important; border-radius: 99px !important; }

/* ── Alerts ── */
.stSuccess, .stError, .stWarning, .stInfo { border-radius: 12px !important; font-size: 13px !important; }

/* ── Checkbox ── */
.stCheckbox > label > span { color: #94a3b8 !important; font-size: 13px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(14,165,233,0.3); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgba(14,165,233,0.5); }

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.06) !important; margin: 16px 0 !important; }
</style>
"""

# ─── COMPONENTS ─────────────────────────────────────────────────────────────

def card(content, padding="22px 24px", border_color="rgba(255,255,255,0.07)", glow=""):
    glow_style = f"box-shadow: 0 0 40px {glow};" if glow else ""
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.025);border:1px solid {border_color};
        border-radius:18px;padding:{padding};{glow_style}backdrop-filter:blur(10px);">
        {content}
    </div>""", unsafe_allow_html=True)

def badge(text, bg, fg="white"):
    return f'<span style="background:{bg}22;color:{bg};border:1px solid {bg}44;border-radius:6px;padding:2px 8px;font-size:11px;font-weight:600;letter-spacing:0.03em;">{text}</span>'

def page_header(title, subtitle):
    st.markdown(f"""
    <div style="padding:36px 40px 0;">
        <h1 style="font-family:'Syne',sans-serif;font-size:28px;font-weight:700;
            color:#f1f5f9;margin:0;letter-spacing:-0.02em;">{title}</h1>
        <p style="color:#475569;font-size:14px;margin:6px 0 28px;font-weight:400;">{subtitle}</p>
    </div>""", unsafe_allow_html=True)

def wrap_open():  st.markdown("<div style='padding:0 40px;'>", unsafe_allow_html=True)
def wrap_close(): st.markdown("</div>", unsafe_allow_html=True)

# ─── SIDEBAR ────────────────────────────────────────────────────────────────

def sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding:28px 22px 20px;">
            <div style="display:flex;align-items:center;gap:11px;margin-bottom:28px;">
                <div style="width:38px;height:38px;
                    background:linear-gradient(135deg,#0ea5e9,#0284c7);
                    border-radius:11px;display:flex;align-items:center;
                    justify-content:center;font-size:19px;
                    box-shadow:0 6px 20px rgba(14,165,233,0.4);">⬡</div>
                <div>
                    <div style="font-family:'Syne',sans-serif;font-size:17px;
                        font-weight:800;color:#f1f5f9;letter-spacing:-0.02em;">
                        Piyush<span style="color:#0ea5e9;">Cloud</span>
                    </div>
                    <div style="font-size:10px;color:#334155;letter-spacing:0.12em;font-weight:500;">STORAGE PLATFORM</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        user = st.session_state.get("user")
        if user:
            initial = user["username"][0].upper()
            stats = get_stats(user["id"])
            pct = min(stats["total_size"] / stats["limit"] * 100, 100)
            bar_color = "#ef4444" if pct > 85 else "#f59e0b" if pct > 65 else "#0ea5e9"

            st.markdown(f"""
            <div style="margin-bottom:20px;padding:14px 16px;background:rgba(14,165,233,0.06);
                border:1px solid rgba(14,165,233,0.12);border-radius:14px;">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
                    <div style="width:32px;height:32px;background:linear-gradient(135deg,#0ea5e9,#7c3aed);
                        border-radius:50%;display:flex;align-items:center;justify-content:center;
                        font-size:13px;font-weight:700;color:white;font-family:'Syne',sans-serif;">
                        {initial}</div>
                    <div>
                        <div style="font-size:13px;font-weight:600;color:#e2e8f0;">{user['username']}</div>
                        <div style="font-size:11px;color:#475569;">Free Plan · 5 GB</div>
                    </div>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:11px;
                    color:#475569;margin-bottom:5px;">
                    <span>Storage</span>
                    <span style="color:#94a3b8;">{fmt_size(stats['total_size'])} / {fmt_size(stats['limit'])}</span>
                </div>
                <div style="background:rgba(255,255,255,0.06);border-radius:99px;height:4px;">
                    <div style="width:{pct:.1f}%;height:100%;background:{bar_color};
                        border-radius:99px;transition:width 0.6s ease;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div style="padding:0 4px;">', unsafe_allow_html=True)
        nav = st.radio("nav", ["⬡  Dashboard", "📁  My Files", "☁️  Upload", "⚙️  Settings"],
                       label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        if st.button("→  Sign Out", use_container_width=True):
            st.session_state.clear(); st.rerun()

        st.markdown("""
        <div style="position:fixed;bottom:0;left:0;width:270px;padding:16px 22px;
            background:rgba(3,7,18,0.95);border-top:1px solid rgba(255,255,255,0.05);">
            <div style="font-size:10px;color:#1e293b;text-align:center;letter-spacing:0.08em;">
                PIYUSH JHA · CLOUD STORAGE v2.0
            </div>
        </div>""", unsafe_allow_html=True)

    return nav.split("  ")[-1].strip()

# ─── AUTH ───────────────────────────────────────────────────────────────────

def auth_page():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.markdown("""
    <style>
    .auth-hero {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 40px 20px;
    }
    </style>
    <div style="min-height:100vh;display:flex;align-items:center;justify-content:center;padding:40px 20px;">
        <div style="width:100%;max-width:420px;">
            <!-- Logo -->
            <div style="text-align:center;margin-bottom:40px;">
                <div style="width:60px;height:60px;background:linear-gradient(135deg,#0ea5e9,#0284c7);
                    border-radius:18px;display:flex;align-items:center;justify-content:center;
                    font-size:28px;margin:0 auto 16px;
                    box-shadow:0 20px 60px rgba(14,165,233,0.4);">⬡</div>
                <div style="font-family:'Syne',sans-serif;font-size:32px;font-weight:800;
                    color:#f1f5f9;letter-spacing:-0.03em;line-height:1;">
                    Piyush<span style="color:#0ea5e9;">Cloud</span>
                </div>
                <div style="font-size:13px;color:#475569;margin-top:8px;">Your personal cloud storage platform</div>
            </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 10, 1])
    with col2:
        tab = st.radio("auth_tab", ["Sign In", "Create Account"], horizontal=True,
                       label_visibility="collapsed")

        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

        if tab == "Sign In":
            with st.form("login"):
                username = st.text_input("USERNAME", placeholder="Enter your username")
                password = st.text_input("PASSWORD", type="password", placeholder="••••••••")
                st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)
                submit = st.form_submit_button("Sign In →", use_container_width=True)

            if submit:
                if not username or not password:
                    st.error("Please fill in all fields.")
                else:
                    u = get_user_by_username(username)
                    if u and verify_pw(password, u["password_hash"]):
                        st.session_state.user = u
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please try again.")

        else:
            with st.form("signup"):
                username = st.text_input("USERNAME", placeholder="Choose a username")
                email    = st.text_input("EMAIL", placeholder="your@email.com")
                c1, c2   = st.columns(2)
                with c1: pw1 = st.text_input("PASSWORD", type="password", placeholder="Min 8 chars")
                with c2: pw2 = st.text_input("CONFIRM", type="password", placeholder="Repeat")
                st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)
                submit = st.form_submit_button("Create Account →", use_container_width=True)

            if submit:
                errs = []
                if not all([username, email, pw1, pw2]): errs.append("All fields required.")
                if username and len(username) < 3: errs.append("Username ≥ 3 chars.")
                if email and not valid_email(email): errs.append("Invalid email.")
                if pw1 and len(pw1) < 8: errs.append("Password ≥ 8 chars.")
                if pw1 and pw2 and pw1 != pw2: errs.append("Passwords don't match.")
                if not errs:
                    if get_user_by_username(username): errs.append("Username taken.")
                    elif get_user_by_email(email): errs.append("Email already registered.")
                if errs:
                    for e in errs: st.error(e)
                elif create_user(username, email, hash_pw(pw1)):
                    st.success("Account created! Sign in above.")

    st.markdown("</div></div>", unsafe_allow_html=True)

# ─── DASHBOARD ──────────────────────────────────────────────────────────────

def dashboard_page():
    user = st.session_state.user
    stats = get_stats(user["id"])
    hr = datetime.now().hour
    greet = "Good morning" if hr < 12 else "Good afternoon" if hr < 17 else "Good evening"

    page_header(f"{greet}, {user['username']} 👋",
                "Your cloud storage overview — everything at a glance.")
    wrap_open()

    # ── Stat cards ──
    cols = st.columns(4)
    cards_data = [
        ("📁", "Total Files", str(stats["total_files"]), "#0ea5e9"),
        ("💾", "Storage Used", fmt_size(stats["total_size"]), "#8b5cf6"),
        ("🖼️", "Images", str(stats["breakdown"].get("Image", {}).get("count", 0)), "#22d3ee"),
        ("📄", "Documents", str(stats["breakdown"].get("Document", {}).get("count", 0)), "#f59e0b"),
    ]
    for col, (ic, lbl, val, cl) in zip(cols, cards_data):
        with col:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);
                border-radius:18px;padding:22px 24px;position:relative;overflow:hidden;
                transition:transform 0.2s;">
                <div style="position:absolute;top:-20px;right:-20px;width:100px;height:100px;
                    background:radial-gradient(circle,{cl}15,transparent 70%);border-radius:50%;"></div>
                <div style="font-size:24px;margin-bottom:12px;">{ic}</div>
                <div style="font-family:'Syne',sans-serif;font-size:30px;font-weight:800;
                    color:#f1f5f9;line-height:1;">{val}</div>
                <div style="font-size:12px;color:#475569;margin-top:5px;font-weight:500;
                    letter-spacing:0.03em;text-transform:uppercase;">{lbl}</div>
                <div style="position:absolute;bottom:0;left:0;right:0;height:2px;
                    background:linear-gradient(90deg,{cl}00,{cl},{cl}00);opacity:0.4;"></div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── Storage bar + breakdown + recent ──
    col_l, col_r = st.columns([1.5, 1])

    with col_l:
        # Storage bar
        pct = min(stats["total_size"] / stats["limit"] * 100, 100)
        free = stats["limit"] - stats["total_size"]
        bar_c = "#ef4444" if pct > 85 else "#f59e0b" if pct > 65 else "#0ea5e9"
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);
            border-radius:18px;padding:22px 24px;margin-bottom:16px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
                <div style="font-family:'Syne',sans-serif;font-weight:600;color:#e2e8f0;font-size:15px;">
                    💾 Storage Overview
                </div>
                <div style="font-size:12px;color:#475569;">{pct:.1f}% used</div>
            </div>
            <div style="background:rgba(255,255,255,0.05);border-radius:99px;height:8px;overflow:hidden;margin-bottom:12px;">
                <div style="width:{pct:.1f}%;height:100%;
                    background:linear-gradient(90deg,{bar_c},{bar_c}bb);
                    border-radius:99px;transition:width 0.8s cubic-bezier(0.4,0,0.2,1);"></div>
            </div>
            <div style="display:flex;justify-content:space-between;">
                <div style="text-align:center;">
                    <div style="font-size:16px;font-weight:600;color:#f1f5f9;">{fmt_size(stats['total_size'])}</div>
                    <div style="font-size:11px;color:#475569;margin-top:2px;">Used</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:16px;font-weight:600;color:#22d3ee;">{fmt_size(free)}</div>
                    <div style="font-size:11px;color:#475569;margin-top:2px;">Available</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:16px;font-weight:600;color:#f1f5f9;">{fmt_size(stats['limit'])}</div>
                    <div style="font-size:11px;color:#475569;margin-top:2px;">Total</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Recent uploads
        st.markdown("""
        <div style="background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);
            border-radius:18px;padding:22px 24px;">
            <div style="font-family:'Syne',sans-serif;font-weight:600;color:#e2e8f0;
                font-size:15px;margin-bottom:16px;">🕐 Recent Uploads</div>
        """, unsafe_allow_html=True)

        if not stats["recent"]:
            st.markdown("<p style='color:#334155;font-size:13px;padding:12px 0;'>No files yet — upload something!</p>", unsafe_allow_html=True)
        else:
            for f in stats["recent"]:
                cl = color(f["file_type"]); ic = icon(f["file_type"])
                dt = f["upload_date"][:16].replace("T"," ")
                nm = f["original_name"]
                nm_disp = nm[:32]+"…" if len(nm)>32 else nm
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;padding:10px 0;
                    border-bottom:1px solid rgba(255,255,255,0.04);">
                    <div style="width:38px;height:38px;background:{cl}15;border-radius:11px;
                        display:flex;align-items:center;justify-content:center;
                        font-size:17px;flex-shrink:0;">{ic}</div>
                    <div style="flex:1;min-width:0;">
                        <div style="font-size:13px;color:#cbd5e1;font-weight:500;">{nm_disp}</div>
                        <div style="font-size:11px;color:#334155;margin-top:2px;">{dt}</div>
                    </div>
                    <div style="font-size:12px;color:#475569;flex-shrink:0;">{fmt_size(f['file_size'])}</div>
                </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_r:
        # File type breakdown
        st.markdown("""
        <div style="background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);
            border-radius:18px;padding:22px 24px;height:100%;">
            <div style="font-family:'Syne',sans-serif;font-weight:600;color:#e2e8f0;
                font-size:15px;margin-bottom:16px;">📊 File Types</div>
        """, unsafe_allow_html=True)

        if not stats["breakdown"]:
            st.markdown("<p style='color:#334155;font-size:13px;padding-top:12px;'>No files yet.</p>", unsafe_allow_html=True)
        else:
            total = sum(v["count"] for v in stats["breakdown"].values()) or 1
            for ft, info in sorted(stats["breakdown"].items(), key=lambda x: -x[1]["count"]):
                cl = color(ft); ic = icon(ft)
                pct_t = info["count"] / total * 100
                st.markdown(f"""
                <div style="margin-bottom:14px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                        <div style="display:flex;align-items:center;gap:8px;">
                            <span style="font-size:15px;">{ic}</span>
                            <span style="font-size:13px;color:#94a3b8;">{ft}</span>
                        </div>
                        <div style="display:flex;align-items:center;gap:8px;">
                            <span style="font-size:11px;color:#334155;">{fmt_size(info['size'])}</span>
                            <span style="font-size:12px;font-weight:600;color:{cl};">{info['count']}</span>
                        </div>
                    </div>
                    <div style="background:rgba(255,255,255,0.05);border-radius:99px;height:4px;overflow:hidden;">
                        <div style="width:{pct_t:.1f}%;height:100%;background:{cl};border-radius:99px;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    wrap_close()

# ─── UPLOAD ─────────────────────────────────────────────────────────────────

def upload_page():
    user = st.session_state.user
    stats = get_stats(user["id"])
    free  = stats["limit"] - stats["total_size"]

    page_header("☁️ Upload Files", "Drag & drop files or click to browse. Up to 100 MB per file.")
    wrap_open()

    # Info strip
    pct = min(stats["total_size"] / stats["limit"] * 100, 100)
    bar_c = "#ef4444" if pct > 85 else "#f59e0b" if pct > 65 else "#0ea5e9"
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);
        border-radius:14px;padding:14px 20px;margin-bottom:20px;
        display:flex;align-items:center;gap:20px;">
        <div style="flex:1;">
            <div style="display:flex;justify-content:space-between;font-size:12px;
                color:#475569;margin-bottom:6px;">
                <span>Storage</span><span>{fmt_size(stats['total_size'])} / {fmt_size(stats['limit'])}</span>
            </div>
            <div style="background:rgba(255,255,255,0.05);border-radius:99px;height:5px;">
                <div style="width:{pct:.1f}%;height:100%;background:{bar_c};border-radius:99px;"></div>
            </div>
        </div>
        <div style="font-size:13px;font-weight:600;color:{bar_c};white-space:nowrap;">
            {fmt_size(free)} free
        </div>
    </div>""", unsafe_allow_html=True)

    uploaded = st.file_uploader("DROP FILES HERE", accept_multiple_files=True,
                                 label_visibility="collapsed")

    if uploaded:
        st.markdown(f"""
        <div style="font-family:'Syne',sans-serif;font-size:15px;font-weight:600;
            color:#e2e8f0;margin:20px 0 12px;">
            {len(uploaded)} file{'s' if len(uploaded)>1 else ''} ready
        </div>""", unsafe_allow_html=True)

        valid, invalid = [], []
        for uf in uploaded:
            ok = uf.size <= 100*1024*1024 and uf.size <= free
            (valid if ok else invalid).append(uf)
            cl = color(get_type(uf.name, uf.type or ""))
            ic = icon(get_type(uf.name, uf.type or ""))
            status_color = "#22d3ee" if ok else "#ef4444"
            status_text  = fmt_size(uf.size) if ok else ("Too large" if uf.size > 100*1024*1024 else "No space")
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;padding:11px 16px;
                background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);
                border-radius:12px;margin-bottom:6px;">
                <div style="width:36px;height:36px;background:{cl}15;border-radius:10px;
                    display:flex;align-items:center;justify-content:center;font-size:16px;">{ic}</div>
                <div style="flex:1;min-width:0;">
                    <div style="font-size:13px;color:#cbd5e1;overflow:hidden;
                        text-overflow:ellipsis;white-space:nowrap;">{uf.name}</div>
                    <div style="font-size:11px;color:#334155;margin-top:2px;">
                        {get_type(uf.name)} · {fmt_size(uf.size)}</div>
                </div>
                <div style="font-size:12px;font-weight:600;color:{status_color};">{status_text}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="font-size:12px;color:#334155;margin:10px 0 16px;">
            Total: {fmt_size(sum(f.size for f in uploaded))} · 
            {len(valid)} uploadable · {len(invalid)} skipped
        </div>""", unsafe_allow_html=True)

        if st.button(f"☁️  Upload {len(valid)} File{'s' if len(valid)!=1 else ''}",
                     disabled=len(valid)==0):
            upload_dir = ensure_dir(user["id"])
            existing   = {f["filename"] for f in get_files(user["id"])}
            prog = st.progress(0, text="Starting upload…")
            for i, uf in enumerate(valid):
                sname = safe_name(uf.name, existing); existing.add(sname)
                with open(os.path.join(upload_dir, sname), "wb") as fp: fp.write(uf.getbuffer())
                save_file(user["id"], sname, uf.name, get_type(uf.name, uf.type or ""),
                          uf.size, uf.type or "")
                prog.progress((i+1)/len(valid), text=f"Uploading {uf.name}…")
            prog.empty()
            st.success(f"✅ {len(valid)} file{'s' if len(valid)>1 else ''} uploaded!")
            if len(valid) > 0: st.balloons()

    wrap_close()

# ─── FILES ──────────────────────────────────────────────────────────────────

def files_page():
    user = st.session_state.user
    upload_dir = ensure_dir(user["id"])

    page_header("📁 My Files", "Search, preview, download and organize your files.")
    wrap_open()

    # Controls
    c1, c2, c3 = st.columns([3, 1.5, 1.2])
    with c1:  search  = st.text_input("SEARCH", placeholder="Search by name…", label_visibility="collapsed")
    with c2:  ftype   = st.selectbox("TYPE", ["All","Image","Document","Video","Audio","Code","Archive","Spreadsheet","Other"], label_visibility="collapsed")
    with c3:  starred = st.checkbox("⭐ Starred only")

    files = get_files(user["id"], search=search, ftype=ftype)
    if starred: files = [f for f in files if f["is_starred"]]

    if not files:
        st.markdown("""
        <div style="text-align:center;padding:80px 20px;">
            <div style="font-size:56px;margin-bottom:16px;">📭</div>
            <div style="font-family:'Syne',sans-serif;font-size:18px;color:#1e293b;margin-bottom:6px;">
                Nothing here yet</div>
            <div style="font-size:14px;color:#334155;">Upload some files to get started</div>
        </div>""", unsafe_allow_html=True)
        wrap_close(); return

    st.markdown(f"""
    <div style="font-size:12px;color:#334155;margin:6px 0 16px;letter-spacing:0.03em;">
        {len(files)} FILE{'S' if len(files)!=1 else ''} FOUND
    </div>""", unsafe_allow_html=True)

    for i in range(0, len(files), 2):
        cols = st.columns(2, gap="medium")
        for j, col in enumerate(cols):
            if i+j >= len(files): break
            with col: _file_card(files[i+j], upload_dir, user["id"])

    wrap_close()

def _file_card(f, upload_dir, user_id):
    cl = color(f["file_type"]); ic = icon(f["file_type"])
    dt = f["upload_date"][:16].replace("T"," ")
    nm = f["original_name"]
    nm_disp = nm[:36]+"…" if len(nm)>36 else nm
    star_icon = "⭐" if f["is_starred"] else "☆"
    fp = os.path.join(upload_dir, f["filename"])

    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);
        border-radius:16px;padding:16px 18px;margin-bottom:4px;
        border-left:3px solid {cl};">
        <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:40px;height:40px;background:{cl}15;border-radius:12px;
                display:flex;align-items:center;justify-content:center;
                font-size:19px;flex-shrink:0;">{ic}</div>
            <div style="flex:1;min-width:0;">
                <div style="font-size:13px;color:#e2e8f0;font-weight:500;overflow:hidden;
                    text-overflow:ellipsis;white-space:nowrap;" title="{nm}">{nm_disp}</div>
                <div style="font-size:11px;color:#334155;margin-top:3px;">
                    <span style="color:{cl};font-weight:600;">{f['file_type']}</span>
                    &nbsp;·&nbsp;{fmt_size(f['file_size'])}
                    &nbsp;·&nbsp;{dt}
                </div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    a1, a2, a3, a4 = st.columns(4)

    with a1:
        if os.path.exists(fp):
            with open(fp, "rb") as file_data:
                st.download_button("⬇ Get", file_data.read(), file_name=nm,
                                   key=f"dl_{f['id']}", use_container_width=True)
    with a2:
        if st.button(star_icon, key=f"st_{f['id']}", use_container_width=True):
            toggle_star(f["id"], user_id); st.rerun()
    with a3:
        if f["file_type"] == "Image" and os.path.exists(fp):
            if st.button("👁", key=f"pv_{f['id']}", use_container_width=True):
                k = f"prev_{f['id']}"
                st.session_state[k] = not st.session_state.get(k, False)
    with a4:
        if st.button("🗑", key=f"del_{f['id']}", use_container_width=True):
            st.session_state[f"cdel_{f['id']}"] = True

    if st.session_state.get(f"prev_{f['id']}", False) and os.path.exists(fp):
        st.image(fp, use_container_width=True)

    if f["file_type"] in ("Code","Document") and os.path.exists(fp):
        if st.session_state.get(f"prev_{f['id']}", False):
            try:
                with open(fp,"r",errors="ignore") as fh: st.code(fh.read(2000), language="text")
            except: pass

    if st.session_state.get(f"cdel_{f['id']}", False):
        st.warning(f"Delete **{nm}**?")
        y, n = st.columns(2)
        with y:
            if st.button("Delete", key=f"y_{f['id']}", use_container_width=True):
                fname = delete_file(f["id"], user_id)
                if fname:
                    p = os.path.join(upload_dir, fname)
                    if os.path.exists(p): os.remove(p)
                st.session_state.pop(f"cdel_{f['id']}", None); st.rerun()
        with n:
            if st.button("Cancel", key=f"n_{f['id']}", use_container_width=True):
                st.session_state.pop(f"cdel_{f['id']}", None); st.rerun()

# ─── SETTINGS ───────────────────────────────────────────────────────────────

def settings_page():
    user  = st.session_state.user
    stats = get_stats(user["id"])

    page_header("⚙️ Settings", "Manage your account details and preferences.")
    wrap_open()

    col1, col2 = st.columns([1.1, 1], gap="large")

    with col1:
        initial = user["username"][0].upper()
        pct = min(stats["total_size"] / stats["limit"] * 100, 100)
        bar_c = "#ef4444" if pct > 85 else "#f59e0b" if pct > 65 else "#0ea5e9"

        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);
            border-radius:18px;padding:28px;margin-bottom:16px;">

            <div style="display:flex;align-items:center;gap:16px;margin-bottom:24px;">
                <div style="width:56px;height:56px;background:linear-gradient(135deg,#0ea5e9,#7c3aed);
                    border-radius:18px;display:flex;align-items:center;justify-content:center;
                    font-family:'Syne',sans-serif;font-size:24px;font-weight:800;color:white;
                    box-shadow:0 8px 24px rgba(14,165,233,0.35);">{initial}</div>
                <div>
                    <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:700;
                        color:#f1f5f9;">{user['username']}</div>
                    <div style="font-size:13px;color:#475569;">Free Plan</div>
                </div>
            </div>

            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:20px;">
                <div style="background:rgba(255,255,255,0.03);border-radius:12px;padding:14px;">
                    <div style="font-size:10px;color:#334155;letter-spacing:0.08em;font-weight:500;margin-bottom:6px;">EMAIL</div>
                    <div style="font-size:13px;color:#94a3b8;overflow:hidden;text-overflow:ellipsis;">{user['email']}</div>
                </div>
                <div style="background:rgba(255,255,255,0.03);border-radius:12px;padding:14px;">
                    <div style="font-size:10px;color:#334155;letter-spacing:0.08em;font-weight:500;margin-bottom:6px;">JOINED</div>
                    <div style="font-size:13px;color:#94a3b8;">{user.get('created_at','')[:10]}</div>
                </div>
                <div style="background:rgba(255,255,255,0.03);border-radius:12px;padding:14px;">
                    <div style="font-size:10px;color:#334155;letter-spacing:0.08em;font-weight:500;margin-bottom:6px;">TOTAL FILES</div>
                    <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:700;color:#0ea5e9;">{stats['total_files']}</div>
                </div>
                <div style="background:rgba(255,255,255,0.03);border-radius:12px;padding:14px;">
                    <div style="font-size:10px;color:#334155;letter-spacing:0.08em;font-weight:500;margin-bottom:6px;">STORAGE USED</div>
                    <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:700;color:#8b5cf6;">{fmt_size(stats['total_size'])}</div>
                </div>
            </div>

            <div>
                <div style="display:flex;justify-content:space-between;font-size:12px;
                    color:#475569;margin-bottom:6px;">
                    <span>Storage</span>
                    <span>{fmt_size(stats['total_size'])} / {fmt_size(stats['limit'])}</span>
                </div>
                <div style="background:rgba(255,255,255,0.05);border-radius:99px;height:6px;overflow:hidden;">
                    <div style="width:{pct:.1f}%;height:100%;background:{bar_c};border-radius:99px;"></div>
                </div>
                <div style="font-size:11px;color:#334155;margin-top:6px;">{pct:.1f}% · {fmt_size(stats['limit']-stats['total_size'])} remaining</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);
            border-radius:18px;padding:28px;">
            <div style="font-family:'Syne',sans-serif;font-weight:600;font-size:16px;
                color:#e2e8f0;margin-bottom:20px;">🔒 Change Password</div>
        </div>""", unsafe_allow_html=True)

        with st.form("change_pw"):
            cur  = st.text_input("CURRENT PASSWORD", type="password", placeholder="Your current password")
            new1 = st.text_input("NEW PASSWORD", type="password", placeholder="At least 8 characters")
            new2 = st.text_input("CONFIRM NEW", type="password", placeholder="Repeat new password")
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            save = st.form_submit_button("Update Password →", use_container_width=True)

        if save:
            if not all([cur, new1, new2]):        st.error("All fields required.")
            elif not verify_pw(cur, user["password_hash"]): st.error("Current password incorrect.")
            elif len(new1) < 8:                   st.error("New password ≥ 8 chars.")
            elif new1 != new2:                    st.error("Passwords don't match.")
            else:
                h = hash_pw(new1); update_password(user["id"], h)
                st.session_state.user["password_hash"] = h
                st.success("✅ Password updated!")

    wrap_close()

# ─── MAIN ROUTER ────────────────────────────────────────────────────────────

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

if "user" not in st.session_state:
    auth_page()
else:
    page = sidebar()
    if   page == "Dashboard": dashboard_page()
    elif page == "My Files":  files_page()
    elif page == "Upload":    upload_page()
    elif page == "Settings":  settings_page()
