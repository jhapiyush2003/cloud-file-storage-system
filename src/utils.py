import os
 
UPLOAD_DIR = "data/uploads"
 
def ensure_upload_dir(user_id):
    path = os.path.join(UPLOAD_DIR, str(user_id))
    os.makedirs(path, exist_ok=True)
    return path
 
def format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes/1024:.1f} KB"
    elif size_bytes < 1024**3:
        return f"{size_bytes/1024**2:.1f} MB"
    else:
        return f"{size_bytes/1024**3:.2f} GB"
 
def get_file_type(filename, mime_type=""):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    image_exts = {"jpg", "jpeg", "png", "gif", "bmp", "webp", "svg", "ico"}
    video_exts = {"mp4", "avi", "mov", "mkv", "webm"}
    audio_exts = {"mp3", "wav", "ogg", "flac", "m4a"}
    doc_exts   = {"pdf", "doc", "docx", "odt", "rtf", "txt", "md"}
    code_exts  = {"py", "js", "ts", "html", "css", "java", "cpp", "c", "go", "rs", "json", "yaml", "yml", "xml", "sh"}
    archive_exts = {"zip", "tar", "gz", "rar", "7z"}
    sheet_exts = {"xls", "xlsx", "csv"}
 
    if ext in image_exts or mime_type.startswith("image/"): return "Image"
    if ext in video_exts or mime_type.startswith("video/"): return "Video"
    if ext in audio_exts or mime_type.startswith("audio/"): return "Audio"
    if ext in doc_exts or mime_type == "application/pdf":   return "Document"
    if ext in code_exts:                                     return "Code"
    if ext in archive_exts:                                  return "Archive"
    if ext in sheet_exts:                                    return "Spreadsheet"
    return "Other"
 
FILE_TYPE_ICON = {
    "Image":       "🖼️",
    "Video":       "🎬",
    "Audio":       "🎵",
    "Document":    "📄",
    "Code":        "💻",
    "Archive":     "📦",
    "Spreadsheet": "📊",
    "Other":       "📎",
}
 
FILE_TYPE_COLOR = {
    "Image":       "#10b981",
    "Video":       "#f59e0b",
    "Audio":       "#ec4899",
    "Document":    "#6366f1",
    "Code":        "#06b6d4",
    "Archive":     "#f97316",
    "Spreadsheet": "#84cc16",
    "Other":       "#94a3b8",
}
 
def file_icon(file_type):
    return FILE_TYPE_ICON.get(file_type, "📎")
 
def type_color(file_type):
    return FILE_TYPE_COLOR.get(file_type, "#94a3b8")
 
def safe_filename(filename, user_id, existing_names):
    base, ext = os.path.splitext(filename)
    candidate = f"{base}{ext}"
    counter = 1
    while candidate in existing_names:
        candidate = f"{base}_{counter}{ext}"
        counter += 1
    return candidate
