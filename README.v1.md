## 작성법

- 최상위: 단수
  - domain/ application/ interface/ infra/ common/ config
- 도메인: 복수
- 하위 파일: 복수



1. 단일 기능으로 쌓아 올린다
2. 서비스 레이어에서는 단방향 api가 아닐 경우 repository만을 참조한다
3. 해당 레벨 조회시 없으면 exception, 상위 -> 하위 조회시 없으면 빈 리스트
4. 하위 레벨에는 모든 상위 레벨의 id 매핑
5. RESTful API 설계에서 **조회(GET), 삭제(DELETE), 수정(PUT/PATCH)**의 경우 리소스 식별자(ID)는 URL path로, 수정할 데이터는 request body로 전달하는 것이 REST 원칙에 부합
6. di 작성시, 레포를 먼저 작성하고, 유즈케이스를 의존성 역순으로 작성해야함
7. 전체에 대한 api는 제공할 필요 없으나 배치에 대한 처리는 제공함
8. repository의 함수명은 도메인 명을 포함하도록