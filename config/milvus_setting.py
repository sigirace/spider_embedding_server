from config.setting import BaseAppSettings


class MilvusSetting(BaseAppSettings):
    milvus_host: str
    milvus_port: int
    milvus_alias: str
