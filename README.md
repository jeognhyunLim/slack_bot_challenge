# SSAFY Start Camp 챗봇 퀘스트

SEOUL_8_임정현 https://github.com/jeonghyunLim/slack_bot_challenge
    

## I. 스펙(Specification)

잡코리아에서 IT 직무 채용 정보를 보여줍니다.
1. 사용법안내
    * 봇을 호출하면 사용법을 안내해줍니다
    * 정해진 입력 외의 입력이 들어오면 사용법을 안내해줍니다.
2. 지역별 
    * 지역을 옵션으로 주면 해당 지역의 채용정보를 안내합니다.
    * 지역은 여러가지 선택 가능합니다.
3. 고용형태별
    * 고용형태를 옵션으로 주면 해당 고용 형태의 채용정보를 안내합니다.
    * 여러가지 선택 가능합니다.
4. 정렬 순서
    * 정렬 옵션을 주면 해당 방법으로 정렬한 채용정보를 안내합니다.
    * 등록순/마감순 둘 중 하나만 선택 가능합니다.
    
# II. 회고(Retrospective)

어플리케이션 구현 과정에서의 어려움과 문제점
* 데이터를 크롤링 할 때 결과가 없는 경우를 예외처리 해야 했습니다.
* 데이터가 워낙 많기 때문에 일정 수준까지만 보여줄 수 있었습니다. 
* 컨펌 버튼의 결과값에 따라 다른 행동을 하도록 하는 방법이 어려워 구현하지 못하고 url 만 연결하였습니다.


# III. 보완 계획(Feedback)

현재 미완성이지만 추가로 구현할 기능 및 기존 문제점 보완 계획
1. 다른 취업 사이트연계 
    * 잡코리아 이외의 여러 사이트의 정보 연계
2. 기업 정보 안내
    * 채용 정보뿐 아니라 기업 정보에 대한 안내도 추가합니다.
3. 자소서 항목 안내
    * 해당 채용 정보의 자소서 항목을 안내해 줍니다.
    

