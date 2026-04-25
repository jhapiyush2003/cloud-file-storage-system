import hashlib
import streamlit as st
from typing import Optional

from . import db


SESSION_KEYS = ["authenticated", "username", "user_id", "full_name", "flash_message"]


def init_session() -> None:
    for key in SESSION_KEYS:
        if key not in st.session_state:
            st.session_state[key] = False if key == "authenticated" else ""


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash


def signup(username: str, password: str, full_name: Optional[str] = None) -> bool:
    password_hash = hash_password(password)
    return db.create_user(username.strip().lower(), password_hash, full_name.strip() if full_name else None)


def login(username: str, password: str) -> bool:
    user = db.get_user(username.strip().lower())
    if not user:
        return False
    if not verify_password(password, user["password_hash"]):
        return False
    st.session_state.authenticated = True
    st.session_state.username = user["username"]
    st.session_state.user_id = user["id"]
    st.session_state.full_name = user["full_name"] or user["username"]
    st.session_state.flash_message = ""
    return True


def logout() -> None:
    for key in SESSION_KEYS:
        if key == "authenticated":
            st.session_state[key] = False
        else:
            st.session_state[key] = ""
    st.session_state.flash_message = "You have been logged out successfully."


def current_user() -> Optional[dict]:
    if st.session_state.authenticated:
        return {
            "username": st.session_state.username,
            "user_id": st.session_state.user_id,
            "full_name": st.session_state.full_name,
        }
    return None
