import aiofiles
from fastapi import UploadFile
from pathlib import Path


class FileGateway:
    async def save_upload_file(self, path: str, file: UploadFile):
        async with aiofiles.open(path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

    def check_file_exist(self, path: str) -> bool:
        file_name = Path(path)
        return file_name.is_file()
