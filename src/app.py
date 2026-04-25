import base64
from pathlib import Path
from typing import Optional

import streamlit as st
from streamlit import session_state as state

from . import auth, db, storage, utils


PAGE_CONFIG = {
    "page_title": "Cloud File Storage System",
    "page_icon": "☁️",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}


def inject_styles() -> None:
    st.markdown(
        """
        <style>
            body {
                color: #e5e5e5;
                background-color: #0e1117;
            }
            .css-1d391kg {
                background-color: #11161f;
            }
            .stButton>button {
                background-color: #2563eb;
                color: white;
            }
            .stButton>button:hover {
                background-color: #1d4ed8;
            }
            .stTextInput>div>div>input,
            .stTextArea>div>div>textarea,
            .stSelectbox>div>div>div>select {
                background-color: #121827;
                color: #e5e5e5;
                border-color: #374151;
            }
            .stFileUploader>div>div {
                border: 1px solid #334155;
            }
            .streamlit-expanderHeader {
                font-weight: 600;
            }
            .stAlert {
                background-color: #1f2937;
                color: #e5e5e5;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_app() -> None:
    st.set_page_config(**PAGE_CONFIG)
    auth.init_session()
    db.init_db()
    if "search_term" not in state:
        state.search_term = ""
    if "selected_file_id" not in state:
        state.selected_file_id = None


def show_welcome_card() -> None:
    st.markdown("## Welcome to your secure cloud workspace")
    st.write(
        "Upload, search, preview, download, and manage your files in a polished dark interface. "
        "Your files are stored locally in SQLite-backed storage for the app environment."
    )


def show_login_form() -> None:
    st.subheader("Login")
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Sign In")
        if submit:
            if auth.login(username, password):
                st.success("Login successful. Welcome back!")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password.")


def show_signup_form() -> None:
    st.subheader("Sign up")
    with st.form("signup_form", clear_on_submit=False):
        full_name = st.text_input("Full name")
        username = st.text_input("Choose a username")
        password = st.text_input("Choose a password", type="password")
        confirm = st.text_input("Confirm password", type="password")
        submit = st.form_submit_button("Create account")
        if submit:
            if not username or not password:
                st.error("Username and password are required.")
                return
            if password != confirm:
                st.error("Passwords do not match.")
                return
            if auth.signup(username, password, full_name):
                st.success("Account created successfully. Please log in.")
            else:
                st.error("Username already exists. Try a different username.")


def show_auth_page() -> None:
    st.title("Cloud File Storage System")
    st.markdown("### Secure login and file management for modern workflows")
    col1, col2 = st.columns(2)
    with col1:
        show_login_form()
    with col2:
        show_signup_form()
    st.markdown("---")
    show_welcome_card()


def create_upload_card(user: dict) -> None:
    st.subheader("Upload a new file")
    with st.form("upload_form", clear_on_submit=True):
        uploaded_file = st.file_uploader("Choose a file", type=None)
        description = st.text_area("Description", max_chars=250)
        folder = st.text_input("Folder name (optional)")
        submit = st.form_submit_button("Upload file")
        if submit:
            if not uploaded_file:
                st.error("Please select a file to upload.")
                return
            storage_path = storage.save_file(user["username"], uploaded_file, folder)
            db.add_file_record(
                user_id=user["user_id"],
                original_name=uploaded_file.name,
                storage_path=str(storage_path.relative_to(storage.UPLOAD_ROOT)),
                mime_type=uploaded_file.type or "application/octet-stream",
                size=uploaded_file.size,
                description=description.strip() or None,
            )
            st.success("File uploaded successfully.")
            st.experimental_rerun()


def show_stats(user: dict) -> None:
    statistics = db.get_user_stats(user["user_id"])
    col1, col2, col3 = st.columns(3)
    col1.metric("Files stored", statistics["total_files"])
    col2.metric("Storage used", utils.format_bytes(statistics["total_bytes"]))
    col3.metric("Active user", user["username"])


def build_file_table(files: list[dict], user: dict) -> None:
    if not files:
        st.info("No files found. Upload your first document to get started.")
        return
    for file_row in files:
        file_id = file_row["id"]
        with st.expander(f"{utils.get_file_icon(file_row['mime_type'], file_row['original_name'])} {file_row['original_name']}"):
            st.write(f"**Type:** {file_row['mime_type']}  |  **Size:** {utils.format_bytes(file_row['size'])}")
            if file_row["description"]:
                st.write(f"**Description:** {file_row['description']}")
            preview_file_card(file_row)
            client_file_path = storage.get_file_path(file_row["storage_path"])
            file_bytes = storage.read_file_bytes(file_row["storage_path"])
            cols = st.columns([1, 1, 1])
            cols[0].download_button(
                label="Download",
                data=file_bytes,
                file_name=file_row["original_name"],
                mime=file_row["mime_type"],
            )
            if cols[1].button("Delete", key=f"delete_{file_id}"):
                if storage.remove_file(file_row["storage_path"]):
                    db.delete_file_record(file_id, user["user_id"])
                    st.success("File deleted.")
                    st.experimental_rerun()
                else:
                    st.error("Unable to delete the file from storage.")
            cols[2].write(f"Uploaded: {file_row['uploaded_at']}")


def preview_file_card(file_row: dict) -> None:
    if utils.is_previewable_image(file_row["mime_type"]):
        st.image(storage.read_file_bytes(file_row["storage_path"]), caption=file_row["original_name"], use_column_width=True)
    elif utils.is_previewable_pdf(file_row["mime_type"]):
        pdf_bytes = storage.read_file_bytes(file_row["storage_path"])
        pdf_url = storage.encode_pdf_bytes(pdf_bytes)
        st.markdown(
            f'<iframe src="{pdf_url}" width="100%" height="600" style="border:1px solid #334155; border-radius: 8px;"></iframe>',
            unsafe_allow_html=True,
        )
    else:
        st.info("Preview is available for images and PDFs only.")


def show_dashboard() -> None:
    user = auth.current_user()
    if not user:
        st.experimental_rerun()
        return
    st.sidebar.markdown(f"## Hello, {user['full_name']}\n---")
    if st.sidebar.button("Logout"):
        auth.logout()
        st.experimental_rerun()
    if state.flash_message:
        st.sidebar.success(state.flash_message)
        state.flash_message = ""

    st.title("Cloud Storage Dashboard")
    show_stats(user)
    st.markdown("---")
    create_upload_card(user)
    st.markdown("---")
    search_term = st.text_input("Search your files", value=state.search_term)
    state.search_term = search_term
    if search_term:
        files = db.search_user_files(user["user_id"], search_term)
        st.success(f"Showing {len(files)} result(s) for '{search_term}'.")
    else:
        files = db.get_user_files(user["user_id"])
    build_file_table(files, user)


def main() -> None:
    init_app()
    inject_styles()
    if state.authenticated:
        show_dashboard()
    else:
        show_auth_page()


if __name__ == "__main__":
    main()
