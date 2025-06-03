from pymilvus import connections, utility

# Milvus 서버 연결 설정
connections.connect(
    alias="default",  # 반드시 alias 설정
    host="localhost",  # 또는 Milvus 서버 IP
    port="19530",  # 기본 포트
)

collection_name = "kang"

# 컬렉션이 존재하면 삭제
if utility.has_collection(collection_name):
    utility.drop_collection(collection_name)
    print(f"컬렉션 '{collection_name}' 삭제 완료.")
else:
    print(f"컬렉션 '{collection_name}' 이 존재하지 않습니다.")
