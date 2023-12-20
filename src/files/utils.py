from fastapi import UploadFile
from config import FILES_DIR
import aiofiles
from .exceptions import FileSavingException
from pathlib import Path

CHUNK_SIZE = 1024 * 1024

async def save_file_in_filesystem(file: UploadFile, new_filename: str) -> None:
    path = Path(FILES_DIR, new_filename)
    try:
        async with aiofiles.open(path, 'wb') as f:
            while chunk := await file.read(CHUNK_SIZE):
                await f.write(chunk)
        await file.close()
    except Exception:
        await file.close()
        delete_file_from_filesystem(new_filename)
        raise FileSavingException
    
def delete_file_from_filesystem(filename: str) -> None:
    Path(FILES_DIR, filename).unlink(missing_ok=True)
