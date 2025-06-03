1. model
2. repository
3. repository_impl
4. application
	- service
5. dto
6. mapper
7. router


[Todo]
- app
	- app 복사시 이름에 태그 붙임, 복사는 가능한가?
- base repository 만들기

[app]
- Schema
	- id (pk)
	- app_name
	- keywords
- Dto
	- app_create
		- request
			- app_name
			- keywords
		- response
			- id
			- app_name
			- keywords
	- app_read/ app_delete
		- request
			- id
		- response
			- message
	- app_update
		- request
			- id
			- app_name
			- keywords
		- response
			- id
			- app_name
			- keywords

- Create
	- param
		- app_create_request
	- user별 app_name 중복 불가
		- service
			- get_app_by_user
			- create_app
- Read
	- param
		- app_id
	- app 조회
	- app에 대한 유저 권한 체크
		- service
			- get_app
- Update
	- param
		- app_update_request
	- app_name 수정
		- user별 app_name 중복 불가
	- keywords 수정
		- service
			- get_app
			- get_app_by_user
			- update_app
- Delete
	- param
		- app_id
	- 앱 삭제
		- 삭제할 때 앱에 대한 유저 권한 체크
		- app 권한이 있으면 하위 모두 삭제 가능
		- 하위: 문서, 청크, 이미지, 임베딩 삭제 (service 레이어에서 repository 사용)
			- service
				- 임베딩 삭제
					- app에 해당하는 임베딩 모두 조회 -> get_embed_by_app
					- app에 해당하는 임베딩 모두 삭제 -> delete_embed_by_app
					- 벡터스토리지에서 삭제 -> delete_vector_by_app
						- drop collection(app_id)
				- 이미지 삭제
					- app에 해당하는 image 모두 조회 -> get_image_by_app
					- app에 해당하는 이미지 모두 삭제 -> delete_image_by_app
					- 파일서버에서 삭제 -> delete_file_by_app
						- delete_folder(path:app_id)
				- app에 해당하는 청크 모두 삭제 delete_chunk_by_app
				- app에 해당하는 문서 모두 삭제 delete_document_by_app


[document]

**create**
	1. app 기준 문서 집합 업로드 : POST /document
		- 권한: app 생성자 = 요청자

**read**
	1. document_id 기준 문서 상세 조회 : GET /document/{document_id} [v]
		- 권한: document 생성자 = 요청자
		- 없으면 exception
	2. app 기준 문서 집합 조회	: GET /document/list/{app_id} [v]
		- 권한: app 생성자 = 요청자
		- 없으면 빈 리스트

**update**
	1. document_id 기준 문서 수정 : PUT /document/{document_id}
		- 권한: document 생성자 = 요청자


[chunk]


**create**
-  chunk 생성의 기준은 document_id
	1. 단일 document로부터 chunk 생성 : POST /chunk/{document_id}
		- 특정 문서 한개 (document_id)
			- validator -> documnet_validate
			- document_id 기준으로 청크 삭제 후 재등록
			- chunking 수행
				- 파일 이미지 저장
			- 모델 저장

	2. 여러 document로부터 chunk 생성 : POST /chunk/list
		- body: [document_id, document_id, ...]
			- create

**read**
	1. chunk_id 기준 상세 조회 : GET /chunk/{chunk_id}
		- get
		- 청크 클릭하면 상세 내역이 보이게 함 -> 수정 가능 
	2. document_id 기준 전체 chunk 조회: GET /chunk/list/{document_id}
		- get_document

**update**
- milvus 삭제
	1. chunk 내용 수정 : PUT /chunk/{chunk_id}
		- content, tag 수정


[image]

**create**
- 기능 없음

**read**
	1. chunk_id 기준 조회
	2. image_id 기준 조회

**update**
- milvus 삭제
	1. image_description 수정
	2. image_description 생성

**delete**




[embed]

**create**
	1. chunk_list에 대한 embed
		- chunk에 대한 권한 확인
		- request: chunk_id list
		- response: success_list, error_list
		- 생성시 어떤 필드가 들어갈지 고려
		- milvus 구현체 연결
		- embedder 구현체 연결
		- embedder 서비스 생성
			- service1: 생성시 milvus에 존재하는 값 pk로 삭제
			- service2: milvus 저장
				- session
					- chunk의 embed_state 변경
					- 임베딩 테이블 저장

**read**
- 필요 없음

**update**
- 필요 없음

**delete**
	1. chunk_list에 대한 embed 삭제
		- chunk에 대한 권한 확인
		- request: chunk_id list
		- response: success_list, error_list

**deleter 서비스**
	- embed_delete
	- chunk_delete
	- image_delete
	- document_delete
	- app_delete



[delete_app_uc]
- app_id 기준 문서 삭제 (app_id)
- document_list 조회	doc_list = document_repo.get_document_by_app(app_id)
- document_list 기준 문서 삭제 호출	delete_doc_list_uc(doc_list)

[delete_doc_list_uc]
- document_list 기준 문서 삭제 (doc_list)
- document_id 기준 문서 삭제 호출 delete_doc_uc(doc_id) for doc_id in doc_list

[delete_doc_uc]
- document_id 기준 문서 삭제 (doc_id)
- chunk_list 조회	chunk_list = chunk_repo.get_chunk_by_doc_id(doc_id)
- chunk_list 기준 문서 삭제	호출 delete_chunk_list_uc(chunk_list)

[delete_chunk_list_uc]
- chunk_id_list 기준 청크 삭제 (chunk_list)
- chunk_id 기준 청크 삭제 호출 delete_chunk_uc(chunk_id) for chunk_id in chunk_list

[delete_chunk_uc]
- chunk_id 기준 청크 삭제 (chunk_id)
- image_list 조회 image_list = image_repo.get_image_by_chunk_id(chunk_id)
- image_list 기준 image 삭제 호출 delete_image_list_uc(image_list)

[delete_image_list_uc]
- image_list 기준 이미지 삭제 (image_list)
- image_id 기준 이미지 삭제 호출 delete_image_uc(image_id) for image_id in image_list

[delete_image_uc]
- image_id 기준 이미지 삭제 (image_id)
- image_repo.delete(image_id)


## todo
- 이미지 삭제시에 청크의 속성중 임베딩 상태를 변경해야함
- 이미지 삭제시에 청크에 속한 임베딩 엔티티를 삭제해야함

'''
# 예시: delete_image_uc 내부
async def delete_image_uc(image_id: str):
    image = await image_repo.get(image_id)
    chunk_id = image.chunk_id

    # 실제 이미지 삭제
    await image_repo.delete(image_id)

    # TODO 반영
    await chunk_repo.update_embedding_status(chunk_id, "not_embedded")
    await embedding_repo.delete_by_chunk(chunk_id)
'''




- Field
	- id (pk)
	- app_id (fk)
	- name
	- hash
	- size
	- file_path
	- type
	- extension


[chunk]
- Field
	- id
	- app_id
	- document_id
	- content
	- tags
	- page
	- file_creation_date
	- file_mode_date
	- embed_state

- Update
	- 수정시에 embed_state 변경 필요

[image]
- Field
	- 

[embed]
- Field
	- id
	- app_id
	- document_id
	- chunk_id

- Create
	- by_app
		- app에 해당하는 chunk를 모두 가져옴
		- chunk -> embedding -> vector_db -> get vector pk
	- by_document
		- document에 해당하는 chunk를 모두 가져옴


[app]
    C
    	- [interface]
    		- DTO(app_id, description, keywords) -> AppSchema(id, app_id, description, keywords, creator, created_at, updated_at)
    	- [service]
    		- create_app (app_shcema)
    	- [repo]
    		- create_app (app_schema)
    R
    	- get_app (id)
    	- [s] get_app_list (user_id)
    U
    	- update_app (app_schema)
    D
    	- delete_app (app_id) [ToDo]
    		- get_app (app_id) -> find_meta_by_app (app_id) -> delete_meta (app_id, meta_id)

[document]

    C
    	- create_document (app_id, files)
    		- document_schema 생성 당시 id 부여
    		- app_id, files
    		- service에서 List를 돌며 Insert
   R
   		- get_document (document_id) : 특정 문서 조회
   		- get_document_by_app (app_id) : 앱에 해당하는 모든 문서 조회
   U
   		- update_document (document_id, param): 특정 문서 수정 -> 필요할까?
   D
   		- delete_document (document_id)
   		- delete_document_list (document_id_list):  
   		

[document]
id
app_id
hash
size
file_path
type:
extension:
file_creation_date:
file_mod_date:

Lifecycle

[chunk]
id
doc_id

page

images
tags
content

Lifecycle


[문서 생성]
- param: app_id

--- 

[문서 청크 생성]
post: /{doc_id}
- body: chunk_size, overlap
	- 해당 문서에 대한 청크를 생성함
	- 만약 이미 청크들이 생성되어있다면, 삭제 후 재생성

create_chunk_by_document
	delete_chunk_by_document_id
		get_chunk_by_document_id
			for chunk delete_chunk
				Rollback -> create_chunk


[청크 집합 생성]
post: /{app_id}
- body: doc_id_list, chunk_size, overlap
- app 단위로 청크 생성

create_chunk_by_app
	get_document_by_app
		for document create_chunk_by_document


[청크 조회]
get: /{chunk_id}
- 해당 chunk id에 대한 청크 조회

get_chunk

[청크 집합 조회]
get: /{doc_id}
- 해당 문서에 대한 전체 청크 리스트 조회

get_chunk_by_document_id

[청크 삭제]
delete: /{chunk_id}
- 해당 청크에 대한 삭제

delete_chunk

[청크 List 전체 삭세]
delete: /{doc_id}/all
- 해당 문서의 전체 청크 리스트 삭제

delete_chunk_by_document_id
	get_chunk_by_document_id
		for chunk_id delete_chunk
			rollback create_chunk


[청크 수정]
put: /{chunk_id}
- body: content, image, tag
	- 해당 청크에 대한 문서 수정
	
[청크 List 삭제]
delete: /{doc_id}/list
- body: chunk_id_list
	- 해당 문서의 청크 리스트에 대한 삭제


[embed-vector]
- id
- doc_id


