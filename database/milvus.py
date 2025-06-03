from pymilvus import connections

from config import get_settings

milvus_setting = get_settings().milvus

MILVUS_HOST = milvus_setting.milvus_host
MILVUS_PORT = milvus_setting.milvus_port
MILVUS_ALIAS = milvus_setting.milvus_alias

connections.connect(
    alias=MILVUS_ALIAS,
    host=MILVUS_HOST,
    port=MILVUS_PORT,
)
