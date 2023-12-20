from pathlib import Path
from config import AVATARS_DIR

def delete_avatar_from_filesystem(filename: str) -> None:
    path = Path(AVATARS_DIR, filename)
    path.unlink(missing_ok=True)