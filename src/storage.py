import base64
import shutil
from pathlib import Path
from typing import BinaryIO, Optional

from .utils import secure_filename

UPLOAD_ROOT = Path(__file__).resolve().parents[1] / "data" / "uploads"
UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)


def ensure_user_folder(username: str, folder_name: Optional[str] = None) -> Path:
    safe_username = secure_filename(username)
    if folder_name:
        safe_folder = secure_filename(folder_name)
        full_path = UPLOAD_ROOT / safe_username / safe_folder
    else:
        full_path = UPLOAD_ROOT / safe_username
    full_path.mkdir(parents=True, exist_ok=True)
    return full_path


def save_file(username: str, uploaded_file: BinaryIO, folder_name: Optional[str] = None) -> Path:
    target_folder = ensure_user_folder(username, folder_name)
    safe_name = secure_filename(uploaded_file.name)
    storage_path = target_folder / safe_name
    with storage_path.open("wb") as destination:
        shutil.copyfileobj(uploaded_file, destination)
    return storage_path


def get_file_path(storage_path: str) -> Path:
    path = Path(storage_path)
    if not path.is_absolute():
        path = UPLOAD_ROOT / path
    return path


def remove_file(storage_path: str) -> bool:
    path = get_file_path(storage_path)
    if path.exists() and path.is_file():
        path.unlink()
        return True
    return False


def read_file_bytes(storage_path: str) -> bytes:
    path = get_file_path(storage_path)
    with path.open("rb") as f:
        return f.read()


def encode_pdf_bytes(file_bytes: bytes) -> str:
    encoded = base64.b64encode(file_bytes).decode("utf-8")
    return f"data:application/pdf;base64,{encoded}"
