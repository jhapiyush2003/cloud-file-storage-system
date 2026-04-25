import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Piyush Cloud Storage",
    page_icon="☁️",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
html, body, [class*="css"] {
    background: linear-gradient(135deg,#0b0618,#140a2b,#1d1038);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background: rgba(30,15,60,0.88);
    border-right:1px solid rgba(255,255,255,0.08);
}

/* Main title */
.main-title{
    font-size:42px;
    font-weight:800;
    background: linear-gradient(90deg,#c084fc,#e879f9);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.sub-title{
    color:#d1c4e9;
    margin-top:-8px;
    font-size:18px;
    margin-bottom:25px;
}

/* Cards */
.metric-card{
    background: rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:18px;
    padding:22px;
    text-align:center;
    backdrop-filter: blur(12px);
    box-shadow: 0 0 18px rgba(180,80,255,.15);
    transition:0.3s;
}
.metric-card:hover{
    transform: translateY(-5px);
    box-shadow: 0 0 28px rgba(180,80,255,.35);
}

/* Buttons */
.stButton > button{
    width:100%;
    background: linear-gradient(90deg,#8b5cf6,#d946ef);
    color:white;
    border:none;
    border-radius:12px;
    padding:10px;
    font-weight:700;
}
.stButton > button:hover{
    box-shadow:0 0 18px rgba(217,70,239,.45);
}

/* Inputs */
.stTextInput input{
    background: rgba(255,255,255,0.06);
    color:white;
    border-radius:12px;
    border:1px solid rgba(255,255,255,0.1);
}

/* Upload box */
[data-testid="stFileUploader"]{
    background: rgba(255,255,255,0.04);
    border:1px dashed #a855f7;
    border-radius:16px;
    padding:12px;
}

/* Table */
thead tr th{
    color:#d8b4fe !important;
}
tbody tr{
    background: rgba(255,255,255,0.03);
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("☁️ Cloud Panel")
    st.write("Premium Storage Dashboard")
    st.write("---")
    st.write("📁 My Files")
    st.write("📤 Upload")
    st.write("⚙️ Settings")
    st.write("🚪 Logout")

# ---------------- HEADER ----------------
st.markdown('<div class="main-title">☁️ Piyush Cloud Storage</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Secure • Premium • Personal Cloud Workspace</div>', unsafe_allow_html=True)

# ---------------- SEARCH ----------------
st.text_input("🔍 Search files")

# ---------------- STATS ----------------
c1,c2,c3,c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="metric-card">
    <h4>📁 Files</h4>
    <h1>28</h1>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="metric-card">
    <h4>💾 Used</h4>
    <h1>1.2 GB</h1>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="metric-card">
    <h4>🖼 Images</h4>
    <h1>14</h1>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="metric-card">
    <h4>📄 PDFs</h4>
    <h1>6</h1>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ---------------- FILE UPLOAD ----------------
st.subheader("📤 Upload File")
uploaded_file = st.file_uploader("Choose file")

if uploaded_file:
    st.success(f"{uploaded_file.name} uploaded successfully!")

# ---------------- FILE LIST ----------------
st.subheader("📁 Your Files")

data = {
    "File Name": ["resume.pdf", "photo.png", "notes.txt", "project.zip"],
    "Type": ["PDF", "Image", "Text", "ZIP"],
    "Size": ["2 MB", "1.5 MB", "120 KB", "25 MB"]
}

st.table(data)

# ---------------- ACTION BUTTONS ----------------
col1,col2,col3 = st.columns(3)

with col1:
    st.button("⬇️ Download")

with col2:
    st.button("🗑 Delete")

with col3:
    st.button("📂 Open")

# ---------------- FOOTER ----------------
st.write("")
st.caption("Made by Piyush Jha 🚀")git add .