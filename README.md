☁️ NexCloud Storage
A fully-featured, production-grade cloud storage dashboard built with Python + Streamlit.
✨ Features

Real Authentication — Signup, login, hashed passwords (SHA-256), session management
File Upload — Multi-file upload with progress bar, validation, deduplication
File Manager — Search, filter by type, star files, download, delete with confirmation
Image Preview — Inline preview for uploaded images
Code Preview — View text/code files in-app
Live Dashboard — Real stats: file count, storage used, type breakdown, recent uploads
Storage Meter — Visual storage bar with color-coded warnings
Settings Page — Change password, view account info and storage breakdown
Beautiful Dark UI — Inter font, glassmorphism cards, gradient accents, smooth transitions

🛠 Tech Stack

Python 3.10+
Streamlit
SQLite (via stdlib)
Pure CSS (no external UI libraries needed)

🚀 Getting Started
bashpip install -r requirements.txt
streamlit run app.py
📁 Project Structure
app.py                  # Entry point, routing, global CSS
src/
  __init__.py
  db.py                 # SQLite database layer
  auth.py               # Login, signup, password hashing
  dashboard.py          # Dashboard page with real stats
  upload.py             # File upload with validation
  files.py              # File manager (search, delete, star, download)
  settings.py           # Account settings
  utils.py              # Helpers: format_size, file type detection
data/
  storage.db            # SQLite database (auto-created)
  uploads/              # Uploaded files (auto-created)
🔐 Security Notes

Passwords are hashed with SHA-256 before storing
Each user's files are stored in an isolated directory (data/uploads/<user_id>/)
File names are sanitized and deduplicated before saving
For production: use bcrypt, HTTPS, and cloud storage (S3/Supabase)

🌐 Deploying to Streamlit Cloud

Note: Streamlit Community Cloud has an ephemeral filesystem — files and the SQLite database reset on each redeploy. For persistent storage in production, swap data/uploads with Supabase Storage or AWS S3, and use Supabase/PlanetScale for the database.


Push to GitHub
Go to share.streamlit.io
Connect your repo, set app.py as entry point
Deploy!


Made by Piyush Jha 🚀
