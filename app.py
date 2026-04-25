import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="safe Cloud Storage",
    page_icon="☁️",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #0a0f1f;
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#1b103d,#120a2f);
    color:white;
}

.sidebar-title{
    font-size:30px;
    font-weight:700;
    margin-bottom:10px;
}

.card{
    background: rgba(255,255,255,0.05);
    padding:25px;
    border-radius:18px;
    border:1px solid rgba(255,255,255,0.08);
    box-shadow: 0 0 20px rgba(162,89,255,0.08);
    text-align:center;
}

.big-title{
    font-size:52px;
    font-weight:800;
    color:#d6a4ff;
}

.sub{
    font-size:22px;
    color:#cccccc;
}

.upload-box{
    padding:25px;
    border-radius:18px;
    background: rgba(255,255,255,0.04);
    border:1px dashed #a259ff;
}

.footer{
    text-align:center;
    color:#999;
    margin-top:50px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown('<div class="sidebar-title">☁️ Cloud Panel</div>', unsafe_allow_html=True)
st.sidebar.write("Premium Storage Dashboard")
st.sidebar.divider()

menu = st.sidebar.radio(
    "Navigation",
    ["📁 My Files", "📤 Upload", "⚙️ Settings", "🚪 Logout"]
)

# ---------------- MAIN HEADER ----------------
st.markdown('<div class="big-title">☁️ Piyush Cloud Storage</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Secure • Premium • Personal Cloud Workspace</div>', unsafe_allow_html=True)

st.write("")

# Search
st.text_input("🔎 Search files")

st.write("")

# ---------------- DASHBOARD CARDS ----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="card"><h2>📁 Files</h2><h1>28</h1></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card"><h2>💾 Used</h2><h1>1.2 GB</h1></div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card"><h2>🖼️ Images</h2><h1>14</h1></div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="card"><h2>📄 PDFs</h2><h1>6</h1></div>', unsafe_allow_html=True)

st.write("")
st.write("")

# ---------------- UPLOAD SECTION ----------------
st.subheader("📤 Upload File")

st.markdown('<div class="upload-box">', unsafe_allow_html=True)
uploaded = st.file_uploader("Choose file")
if uploaded:
    st.success(f"{uploaded.name} uploaded successfully!")
st.markdown('</div>', unsafe_allow_html=True)

st.write("")
st.write("")

# ---------------- FILE TABLE ----------------
st.subheader("📁 Recent Files")

data = {
    "File Name": ["resume.pdf", "profile.png", "project.zip"],
    "Type": ["PDF", "Image", "ZIP"],
    "Size": ["2 MB", "1 MB", "15 MB"]
}

st.table(data)

# ---------------- FOOTER ----------------
st.markdown('<div class="footer">Made by Piyush Jha 🚀</div>', unsafe_allow_html=True)
