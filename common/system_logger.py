import logging
import inspect
import threading
import multiprocessing
from datetime import datetime, UTC
from uuid import uuid4
from motor.motor_asyncio import AsyncIOMotorClient
from config import get_settings
from common.exception import DBConnectionError

MONGO = get_settings().mongo


class SystemLogger:
    LEVEL_MAP = {
        "DEBUG": 10,
        "INFO": 20,
        "WARNING": 30,
        "ERROR": 40,
        "CRITICAL": 50,
    }

    def __init__(self, client: AsyncIOMotorClient):
        self.col = client[MONGO.mongodb_db][MONGO.mongodb_log]
        self.stdout_logger = logging.getLogger("SystemLogger")
        if not self.stdout_logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] %(filename)s:%(funcName)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.stdout_logger.addHandler(handler)
            self.stdout_logger.setLevel(logging.DEBUG)

    async def log(self, level: str, message: str):
        now = datetime.now(UTC)
        frame = inspect.stack()[2]
        level_number = self.LEVEL_MAP.get(level.upper(), 0)

        record = {
            "when": now.isoformat(),
            "levelName": level.upper(),
            "levelNumber": level_number,
            "fileName": frame.filename.split("/")[-1],
            "functionName": frame.function,
            "processName": multiprocessing.current_process().name,
            "threadName": threading.current_thread().name,
            "message": message,
        }

        # 콘솔 출력
        self.stdout_logger.log(level_number, message)

        # MongoDB 저장
        try:
            await self.col.insert_one(record)
        except Exception as e:
            raise DBConnectionError(detail=str(e)) from e

    async def debug(self, message: str):
        await self.log("DEBUG", message)

    async def info(self, message: str):
        await self.log("INFO", message)

    async def warning(self, message: str):
        await self.log("WARNING", message)

    async def error(self, message: str):
        await self.log("ERROR", message)

    async def critical(self, message: str):
        await self.log("CRITICAL", message)
