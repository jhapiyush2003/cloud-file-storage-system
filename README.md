# Cloud File Storage System

A polished Streamlit-based cloud storage interface built with local SQLite persistence, secure password hashing, uploads, downloads, previews, search, and user dashboards.

## Features

- User signup and login
- Password hashing with SHA-256
- SQLite backend for users and file metadata
- File upload, download, delete
- Search by filename and description
- Image and PDF preview in the browser
- Personal user dashboard with storage metrics
- Modern dark UI styling

## Run locally

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
