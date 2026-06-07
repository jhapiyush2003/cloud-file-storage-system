
import streamlit as st
from src.db import update_user_password, get_user_stats
from src.auth import hash_password, verify_password
from src.utils import format_size
 
def settings_page():
    user = st.session_state.user
    stats = get_user_stats(user["id"])
 
    st.markdown("""
    <div style="padding:32px 36px 0;">
        <h1 style="color:white;font-size:26px;font-weight:800;margin:0;">⚙️ Settings</h1>
        <p style="color:#64748b;margin:6px 0 24px;font-size:14px;">Manage your account and preferences</p>
    </div>
    <div style='padding:0 36px;'>
    """, unsafe_allow_html=True)
 
    col1, col2 = st.columns([1.2, 1])
 
    with col1:
        # Account Info Card
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
            border-radius:16px;padding:24px;margin-bottom:20px;">
            <div style="font-size:15px;font-weight:700;color:white;margin-bottom:16px;">👤 Account Info</div>
            <div style="margin-bottom:12px;">
                <div style="font-size:11px;color:#64748b;font-weight:500;letter-spacing:0.5px;margin-bottom:4px;">USERNAME</div>
                <div style="font-size:14px;color:#e2e8f0;">{user['username']}</div>
            </div>
            <div style="margin-bottom:12px;">
                <div style="font-size:11px;color:#64748b;font-weight:500;letter-spacing:0.5px;margin-bottom:4px;">EMAIL</div>
                <div style="font-size:14px;color:#e2e8f0;">{user['email']}</div>
            </div>
            <div>
                <div style="font-size:11px;color:#64748b;font-weight:500;letter-spacing:0.5px;margin-bottom:4px;">MEMBER SINCE</div>
                <div style="font-size:14px;color:#e2e8f0;">{user.get('created_at','')[:10]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
 
        # Storage Info
        pct = stats["total_size"] / stats["storage_limit"] * 100 if stats["storage_limit"] else 0
        color = "#ef4444" if pct > 85 else "#f59e0b" if pct > 60 else "#6366f1"
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
            border-radius:16px;padding:24px;">
            <div style="font-size:15px;font-weight:700;color:white;margin-bottom:16px;">💾 Storage</div>
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                <span style="font-size:13px;color:#94a3b8;">Used</span>
                <span style="font-size:13px;color:white;">{format_size(stats['total_size'])}</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                <span style="font-size:13px;color:#94a3b8;">Available</span>
                <span style="font-size:13px;color:#10b981;">{format_size(stats['storage_limit'] - stats['total_size'])}</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:12px;">
                <span style="font-size:13px;color:#94a3b8;">Total</span>
                <span style="font-size:13px;color:white;">{format_size(stats['storage_limit'])}</span>
            </div>
            <div style="background:rgba(255,255,255,0.07);border-radius:99px;height:6px;">
                <div style="width:{pct:.1f}%;height:100%;background:{color};border-radius:99px;"></div>
            </div>
            <div style="font-size:11px;color:#64748b;margin-top:6px;">{pct:.1f}% used</div>
        </div>
        """, unsafe_allow_html=True)
 
    with col2:
        # Change Password
        st.markdown("""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
            border-radius:16px;padding:24px;">
            <div style="font-size:15px;font-weight:700;color:white;margin-bottom:16px;">🔒 Change Password</div>
        </div>
        """, unsafe_allow_html=True)
 
        with st.form("change_password"):
            current = st.text_input("Current Password", type="password")
            new_pw = st.text_input("New Password", type="password")
            confirm = st.text_input("Confirm New Password", type="password")
            save = st.form_submit_button("Update Password", use_container_width=True)
 
        if save:
            if not all([current, new_pw, confirm]):
                st.error("All fields are required.")
            elif not verify_password(current, user["password_hash"]):
                st.error("Current password is incorrect.")
            elif len(new_pw) < 8:
                st.error("New password must be at least 8 characters.")
            elif new_pw != confirm:
                st.error("New passwords do not match.")
            else:
                new_hash = hash_password(new_pw)
                update_user_password(user["id"], new_hash)
                st.session_state.user["password_hash"] = new_hash
                st.success("✅ Password updated successfully!")
 
    st.markdown("</div>", unsafe_allow_html=True)
