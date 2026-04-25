# ☁️ Piyush Cloud Storage

A premium cloud storage dashboard built using Python, Streamlit, SQLite and modern UI design.

## 🚀 Features

- Secure Login / Signup
- File Upload System
- Dashboard Analytics
- Search Files
- Storage Usage Cards
- Beautiful Responsive UI
- SQLite Database
- Streamlit Deployment

## 🛠 Tech Stack

- Python
- Streamlit
- SQLite
- CSS Custom UI

## 🌐 Live Demo

https://piyush-cloud-storage.streamlit.app/

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the app:

```bash
streamlit run app.py
```

3. Open the local Streamlit URL in your browser.

## Project structure

- `app.py` - root launcher for the Streamlit app
- `src/app.py` - main Streamlit application UI and workflow
- `src/db.py` - SQLite database initialization and query helpers
- `src/auth.py` - authentication and session management
- `src/storage.py` - file storage helpers and preview utilities
- `src/utils.py` - file formatting and preview utilities
- `data/` - generated storage database and uploads directory

## Notes

The app stores uploads under `data/uploads/` and metadata in `data/storage.db`. This repo is designed for development and demonstration purposes.
