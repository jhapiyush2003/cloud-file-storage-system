# ⬡ Piyush Cloud Storage

> A production-grade personal cloud storage platform — built as a flagship portfolio project.

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-22d3ee?style=flat-square)](LICENSE)

**Live Demo →** [piyush-cloud-storage.streamlit.app](https://piyush-cloud-storage.streamlit.app)

---

## ✨ Features

| Feature | Details |
|---------|---------|
| 🔐 Auth | Signup/login with SHA-256 hashed passwords, full session management |
| ☁️ Upload | Multi-file drag & drop, 100 MB limit, progress bar, deduplication |
| 📁 File Manager | Search, type filter, star, download, delete with confirmation |
| 👁️ Preview | Inline image preview + code/text viewer |
| 📊 Dashboard | Live stats — file count, storage meter, type breakdown, recent uploads |
| ⚙️ Settings | Change password, account info, storage analytics |
| 🎨 Premium UI | Syne + DM Sans fonts, animated backgrounds, glassmorphism, micro-interactions |

## 🛠 Tech Stack

- **Frontend:** Streamlit + Custom CSS (Syne font, glassmorphism, animated gradients)
- **Backend:** Python 3.10+
- **Database:** SQLite (stdlib — zero dependencies)
- **Auth:** SHA-256 password hashing + Streamlit session state

## 🚀 Run Locally

```bash
git clone https://github.com/jhapiyush2003/cloud-file-storage-system
cd cloud-file-storage-system
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Structure

```
app.py              ← Entire app: UI, routing, all pages
src/
  db.py             ← SQLite: users, files, stats queries
  utils.py          ← Helpers: file type detection, size formatting, hashing
  __init__.py
requirements.txt
README.md
```

## 📌 Deploy on Streamlit Cloud

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app
3. Set main file: `app.py`
4. Deploy 🚀

> **Note:** Streamlit Community Cloud uses an ephemeral filesystem. Files reset on redeploy.  
> For persistent production storage, integrate **Supabase** (DB + Storage) or **AWS S3**.

## 🔐 Security

- Passwords hashed with SHA-256 before storing
- Per-user isolated upload directories (`data/uploads/<user_id>/`)
- File names sanitized and deduplicated on upload
- For production: upgrade to bcrypt + HTTPS + cloud object storage

---

<div align="center">
  Made with ❤️ by <strong>Piyush Jha</strong>
</div>
