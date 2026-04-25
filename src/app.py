import streamlit as st

st.set_page_config(page_title="Piyush Cloud Storage", layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
html, body, [class*="css"]  {
    background-color: #0b1020;
    color: white;
}

section[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#1a103d,#24104f);
    color:white;
}

.main-title{
    font-size:52px;
    font-weight:800;
    color:#c084fc;
    margin-bottom:0px;
}

.sub-title{
    font-size:22px;
    color:#d1d5db;
    margin-top:-10px;
    margin-bottom:30px;
}

.card{
    background:#131a2a;
    padding:28px;
    border-radius:18px;
    text-align:center;
    box-shadow:0 0 15px rgba(168,85,247,.15);
    border:1px solid rgba(168,85,247,.2);
}

.card h2{
    font-size:20px;
    margin-bottom:12px;
}

.card p{
    font-size:42px;
    font-weight:800;
    color:white;
}

.block{
    background:#111827;
    padding:25px;
    border-radius:18px;
    border:1px solid rgba(168,85,247,.25);
}

.stButton>button{
    background:#7c3aed;
    color:white;
    border:none;
    border-radius:10px;
    padding:10px 18px;
    font-weight:700;
}

.stButton>button:hover{
    background:#6d28d9;
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.markdown("## ☁️ Cloud Panel")
st.sidebar.write("Premium Storage Dashboard")
st.sidebar.markdown("---")
st.sidebar.write("📁 My Files")
st.sidebar.write("📤 Upload")
st.sidebar.write("⚙️ Settings")
st.sidebar.write("🚪 Logout")

# ---------- HEADER ----------
st.markdown('<div class="main-title">☁️ Piyush Cloud Storage</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Secure • Premium • Personal Cloud Workspace</div>', unsafe_allow_html=True)

search = st.text_input("🔎 Search files")

# ---------- STATS ----------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown('<div class="card"><h2>📁 Files</h2><p>28</p></div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card"><h2>💾 Used</h2><p>1.2 GB</p></div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="card"><h2>🖼 Images</h2><p>14</p></div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="card"><h2>📄 PDFs</h2><p>6</p></div>', unsafe_allow_html=True)

st.write("")

# ---------- UPLOAD ----------
st.markdown("## 📤 Upload File")
st.markdown('<div class="block">', unsafe_allow_html=True)
uploaded = st.file_uploader("Choose file")
if uploaded:
    st.success(f"{uploaded.name} uploaded successfully!")
st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# ---------- RECENT FILES ----------
st.markdown("## 📂 Recent Files")

r1, r2, r3 = st.columns([4,2,2])

with r1:
    st.markdown('<div class="block">📄 Resume.pdf</div>', unsafe_allow_html=True)
with r2:
    st.button("⬇ Download")
with r3:
    st.button("📂 Open")

r1, r2, r3 = st.columns([4,2,2])

with r1:
    st.markdown('<div class="block">🖼 profile.png</div>', unsafe_allow_html=True)
with r2:
    st.button("⬇ Download ")
with r3:
    st.button("📂 Open ")

# ---------- FOOTER ----------
st.write("")
st.caption("Made by Piyush Jha 🚀")
