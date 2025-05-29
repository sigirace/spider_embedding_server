## 작성법

- 최상위: 단수
  - domain/ application/ interface/ infra/ common/ config
- 도메인: 복수
- 하위 파일: 복수


## TODO

너가 제시하는 클린아키텍처 구조로 아래 요건을 만족한 코드를 MECE하게, 상세히 제시해

[common]

- domain
  - creator
  - updater
  - create_date
  - update_date
  
[app]

- domain
  - id (objectid)
  - app_name : str, null 불가능, app의 이름, 유저별로 중복 불가능
  - description : str, null 허용, app에 대한 설명
  - keywords : str의 list, null 허용, app에 대한 키워드
  - common

- create
  - 앱 생성

- read
  - 앱 목록 조회: 유저가 가지고 있는 앱 목록 조회
    - 권한체크: 요청자가 사용할 수 있는 권한있는 앱 목록 조회
  - 앱 상세 조회: 해당 앱의 상세 조회
    - 권한체크: 요청자에게 앱 사용 권한이 있을때만 수행

- update
  - 앱 수정: app_name, description, keywords 수정
    - 권한체크: 요청자에게 앱 사용 권한이 있을때만 수행

- delete
  - 앱 삭제
    - 앱에 속한 document도 삭제
      - 앱에 속한 document들의 실제 저장 위치를 임시 삭제 폴더로 이동
      - 만약 프로세스중 오류나면 다시 앱 폴더 하위에 파일 위치하여 롤백
    - 권한체크: 요청자와 생성자가 같을때만 수행


[document]

- domain
  - id (objectid)
  - app_id (domain app의 id, objectid)
  - document_name : str, null 불가능, 문서의 이름
  - hash : str, null 불가, 파일의 해시값
  - file_apth: str, null 허용, 문서 저장 로직 이후 경로 저장
  - size : str의 list, null 불가, 파일의 크기
  - type : str, null 불가, 파일의 유형
  - extension: str, null 불가, 파일 확장자
  - common

- create
  - 앱에 문서 생성: 업로드한 문서를 앱 기준으로 저장
    - 문서를 파일서버에 저장 (파일서버 로직 필요하다면 제시)
    - 파일 서버는 앱별로 구분
    - 요청한 앱에 이미 생성된 문서 중 hash와 size가 같은 경우 같은 문서로 판단하여 저장하지 않음
    - 권한체크: 요청자에게 앱 사용 권한이 있을때만 수행

- read
  - 앱의 문서 목록 조회: 앱 id 기준으로 문서 목록 조회
    - 권한체크: 요청자한테 앱 사용 권한이 있을때만 수행
  - 문서 상세 조회: 해당 문서의 상세 조회
    - 권한체크: 요청자한테 앱 사용 권한이 있을때만 수행

- update
  - 문서 수정: 앱에 생성된 document_name 수정
    - document_name 변경시 파일서버에 저장된 파일 이름도 변경
    - 저장된 파일 이름 변경 후 file_path 수정
    - 권한체크: 요청자한테 앱 사용 권한이 있을때만 수행

- delete (depends get_current_user)
  - 문서 삭제: 앱에 생성된 문서 삭제
    - 권한체크: 요청자가 앱 생성자 혹은 문서 생성자일 경우에만 수행

[데이터 베이스 가이드]
- mongo의 uow를 사용해야함

[로그 가이드]
- 사용하는 데이터베이스의 system_log에 로그를 기록해야함
- 로그 기록 시점은 controller 기준 요청이 들어왔을때와 수행완료 되었을때
- 오류가 난 경우도 로깅
- 로그는 모든 요청에 대한 정보를 남겨야함

[권한 가이드]
- jwt를 해석했을때, 권한 명이 나옴
- 앱 전체를 볼 수 있는 권한이 아니라 특정 엡, 특정 문서에 대한 권한을 체크할 필요가 있음

[프로젝트 가이드]
- 의존성 주입을 위한 container 필요
- service에 모든 로직을 포함하지 않고 usecase로 분리해야함
- interface쪽 dto필요
- .env 제시
- requirements.txt 제시

[파일 처리 가이드]
- document 서비스의 유즈케이스에서 파일을 저장, 삭제하기 위해 별도의 도메인 혹은 서비스가 필요하다면 반드시 제시
- 데이터와 파일의 관계를 반드시 일치시켜야하기에 트랜잭션 오류시 파일도 롤백시킴

[테스트 가이드]
- 모든 유즈케이스에 대해 테스트 코드까지 필요
- 테스트 실행 방법을 README.md 파일에 명시

[추가]
- 만약 내 도메인의 필드들이 부족하다면 추가 생성 가능
- 전체 코드를 반드시 모두 제시해야함


