import os, hashlib, re

UPLOAD_DIR = "data/uploads"

def ensure_dir(user_id):
    p = os.path.join(UPLOAD_DIR, str(user_id)); os.makedirs(p, exist_ok=True); return p

def fmt_size(b):
    if b < 1024: return f"{b} B"
    if b < 1024**2: return f"{b/1024:.1f} KB"
    if b < 1024**3: return f"{b/1024**2:.1f} MB"
    return f"{b/1024**3:.2f} GB"

def get_type(name, mime=""):
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    if ext in {"jpg","jpeg","png","gif","bmp","webp","svg","ico"} or mime.startswith("image/"): return "Image"
    if ext in {"mp4","avi","mov","mkv","webm"} or mime.startswith("video/"): return "Video"
    if ext in {"mp3","wav","ogg","flac","m4a"} or mime.startswith("audio/"): return "Audio"
    if ext in {"pdf","doc","docx","txt","md","rtf"}: return "Document"
    if ext in {"py","js","ts","html","css","java","cpp","c","go","rs","json","yaml","xml","sh"}: return "Code"
    if ext in {"zip","tar","gz","rar","7z"}: return "Archive"
    if ext in {"xls","xlsx","csv"}: return "Spreadsheet"
    return "Other"

ICONS  = {"Image":"🖼️","Video":"🎬","Audio":"🎵","Document":"📄","Code":"💻","Archive":"📦","Spreadsheet":"📊","Other":"📎"}
COLORS = {"Image":"#22d3ee","Video":"#f59e0b","Audio":"#f472b6","Document":"#818cf8","Code":"#34d399","Archive":"#fb923c","Spreadsheet":"#a3e635","Other":"#94a3b8"}

def icon(t): return ICONS.get(t, "📎")
def color(t): return COLORS.get(t, "#94a3b8")

def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()
def verify_pw(pw, h): return hash_pw(pw) == h
def valid_email(e): return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', e))

def safe_name(name, existing):
    base, ext = os.path.splitext(name)
    c, n = name, 1
    while c in existing: c = f"{base}_{n}{ext}"; n += 1
    return c
