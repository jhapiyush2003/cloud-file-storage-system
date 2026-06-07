PY
import streamlit as st
import hashlib
import re
from src.db import get_user_by_username, get_user_by_email, create_user
 
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
 
def verify_password(password, hashed):
    return hash_password(password) == hashed
 
def is_valid_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is not None
 
def auth_card(content_fn):
    st.markdown("""
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(99,102,241,0.2);
        border-radius:20px;padding:36px 32px;margin-top:10px;">
    """, unsafe_allow_html=True)
    content_fn()
    st.markdown("</div>", unsafe_allow_html=True)
 
def login_page():
    st.markdown("""
    <div style='text-align:center;margin-bottom:28px;'>
        <div style='font-size:36px;margin-bottom:4px;'>☁️</div>
        <h2 style='color:white;margin:0;font-size:26px;font-weight:800;'>Welcome back</h2>
        <p style='color:#64748b;margin:6px 0 0;font-size:14px;'>Sign in to your NexCloud account</p>
    </div>
    """, unsafe_allow_html=True)
 
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        submitted = st.form_submit_button("Sign In →", use_container_width=True)
 
    if submitted:
        if not username or not password:
            st.error("Please fill in all fields.")
            return
        user = get_user_by_username(username)
        if user and verify_password(password, user["password_hash"]):
            st.session_state.user = user
            st.success(f"Welcome back, {username}! 🎉")
            st.rerun()
        else:
            st.error("Invalid username or password.")
 
def signup_page():
    st.markdown("""
    <div style='text-align:center;margin-bottom:28px;'>
        <div style='font-size:36px;margin-bottom:4px;'>🚀</div>
        <h2 style='color:white;margin:0;font-size:26px;font-weight:800;'>Create account</h2>
        <p style='color:#64748b;margin:6px 0 0;font-size:14px;'>Start with 5 GB of free cloud storage</p>
    </div>
    """, unsafe_allow_html=True)
 
    with st.form("signup_form"):
        username = st.text_input("Username", placeholder="Choose a username")
        email = st.text_input("Email", placeholder="your@email.com")
        password = st.text_input("Password", type="password", placeholder="Min. 8 characters")
        confirm = st.text_input("Confirm Password", type="password", placeholder="Repeat password")
        submitted = st.form_submit_button("Create Account →", use_container_width=True)
 
    if submitted:
        if not all([username, email, password, confirm]):
            st.error("All fields are required.")
            return
        if len(username) < 3:
            st.error("Username must be at least 3 characters.")
            return
        if not is_valid_email(email):
            st.error("Please enter a valid email address.")
            return
        if len(password) < 8:
            st.error("Password must be at least 8 characters.")
            return
        if password != confirm:
            st.error("Passwords do not match.")
            return
        if get_user_by_username(username):
            st.error("Username already taken.")
            return
        if get_user_by_email(email):
            st.error("An account with this email already exists.")
            return
        if create_user(username, email, hash_password(password)):
            st.success("Account created! Please sign in.")
        else:
            st.error("Something went wrong. Please try again.")
