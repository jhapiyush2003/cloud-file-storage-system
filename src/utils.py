import re

IMAGE_TYPES = ("image/png", "image/jpeg", "image/jpg", "image/gif", "image/webp")
PDF_TYPES = ("application/pdf",)


def secure_filename(filename: str) -> str:
    sanitized = filename.strip().replace(" ", "_")
    sanitized = re.sub(r"[^A-Za-z0-9_.-]", "", sanitized)
    return sanitized[:255] if sanitized else "file"


def format_bytes(size: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"


def is_previewable_image(mime_type: str) -> bool:
    return mime_type.lower() in IMAGE_TYPES


def is_previewable_pdf(mime_type: str) -> bool:
    return mime_type.lower() in PDF_TYPES


def get_file_icon(mime_type: str, filename: str) -> str:
    if is_previewable_image(mime_type):
        return "🖼️"
    if is_previewable_pdf(mime_type):
        return "📄"
    if filename.lower().endswith((".zip", ".rar", ".tar", ".gz")):
        return "🗜️"
    return "📁"
