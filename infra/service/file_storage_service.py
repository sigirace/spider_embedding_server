from pathlib import Path
import uuid
import hashlib

from common.exceptions import FileServiceError


class LocalFileStorageService:
    def __init__(self, base_dir: str = "./static/data"):
        self.base = Path(base_dir)
        self.trash = self.base / "__trash__"
        self.base.mkdir(parents=True, exist_ok=True)
        self.trash.mkdir(parents=True, exist_ok=True)

    async def compute_hash(self, content: bytes) -> str:
        try:
            hasher = hashlib.sha256()
            hasher.update(content)
            return hasher.hexdigest()
        except Exception as e:
            raise FileServiceError(detail=str(e))

    async def save_bytes(self, content: bytes, dest_rel: str) -> str:
        try:
            dest = self.base / dest_rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            with open(dest, "wb") as f:
                f.write(content)
            return str(dest)
        except Exception as e:
            raise FileServiceError(detail=str(e))

    async def get_image_path(self, app_id: str, document_id: str) -> str:
        return str(self.base / app_id / document_id)

    async def move_to_trash(self, path: str) -> str:
        try:
            src = Path(path)
            unique = f"{uuid.uuid4()}_{src.name}"
            dest = self.trash / unique
            src.rename(dest)
            return str(dest)
        except Exception as e:
            raise FileServiceError(detail=str(e))

    async def exist_file(self, path: str) -> bool:
        try:
            return Path(path).exists()
        except Exception as e:
            raise FileServiceError(detail=str(e))

    async def rename(self, old: str, new: str):
        try:
            if await self.exist_file(new):
                raise FileServiceError(detail=f"이미 존재하는 파일 경로입니다: {new}")
            Path(old).rename(new)
        except Exception as e:
            raise FileServiceError(detail=str(e))
