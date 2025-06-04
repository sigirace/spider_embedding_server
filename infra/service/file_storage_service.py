from pathlib import Path
import shutil
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

    async def delete_folder(self, folder_name: str):
        """
        base_dir 아래에 있는 특정 폴더를 통째로 삭제함 (하위 파일 및 디렉토리 포함)
        예: folder_name = "app1/doc1"
        """
        try:
            target = (self.base / folder_name).resolve()

            # 보안: base 밖의 경로 삭제 방지
            if self.base not in target.parents:
                raise FileServiceError(
                    detail="삭제 대상이 base 디렉토리 외부에 있습니다."
                )

            if target.exists() and target.is_dir():
                shutil.rmtree(target)  # 하위 폴더 및 파일 포함 전체 삭제

        except Exception as e:
            raise FileServiceError(detail=str(e))

    async def delete_file(self, path: str):
        try:
            p = Path(path)
            if p.exists() and p.is_file():
                await self.move_to_trash(path=path)
                p.unlink()
            await self.delete_parent_dir_if_empty(file_path=path)
        except Exception as e:
            raise FileServiceError(detail=str(e))

    async def move_to_trash(self, path: str) -> str:
        try:
            src = Path(path)
            unique = f"{uuid.uuid4()}_{src.name}"
            dest = self.trash / unique
            src.rename(dest)
            return str(dest)
        except Exception as e:
            raise FileServiceError(detail=str(e))

    async def delete_parent_dir_if_empty(self, file_path: str):
        """
        파일이 속한 디렉토리(직계 상위 1단계)가 비어있으면 해당 디렉토리 삭제
        """
        try:
            file = Path(file_path)
            parent = file.parent

            if parent == self.base or self.base not in parent.parents:
                # base 디렉토리거나 base 밖의 디렉토리는 삭제 금지
                return

            if parent.exists() and parent.is_dir() and not any(parent.iterdir()):
                parent.rmdir()

        except Exception as e:
            raise FileServiceError(detail=str(e))
