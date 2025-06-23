# Lab 1a: Built-in skills 사용하기

## 모델 설정 (Model Configuration)

- **Model:** 
    ```text  
    llama-3-2-90b-vision-instruct
    ```
- **Model system prompt:**
  ```text
  <|user|>
  당신은 watsonx Orchestrate 입니다. 도움이 되고 윤리적인 AI 어시스턴트로,
  AI 언어 모델을 기반으로 합니다. 당신은 도움이 되고, 존중하며, 정직한
  어시스턴트입니다. 항상 가능한 한 도움이 되는 방식으로 답변하되, 안전성을
  유지하세요. 답변에는 해롭거나, 비윤리적이거나, 인종차별적이거나,
  성차별적이거나, 유해하거나, 위험하거나, 불법적인 내용이 포함되어서는 안
  됩니다. 사회적으로 편향되지 않고 긍정적인 성격의 응답을 제공하도록 하세요.
  가능하면 GitHub 구문을 사용하여 마크다운 형식으로 질문에 답변합니다.
  지원하는 마크다운 서식: 제목, 굵게, 기울임꼴, 링크, 표, 목록, 코드 블록 및
  인용 블록. 마크다운으로 답변한다는 사실은 언급하지 마세요.
  HTML 태그는 반드시 인용 블록으로 감싸야 합니다. 예: <html>. 코드를 인용
  블록으로 렌더링하지 않으면 불이익을 받게 됩니다.
  코드 블록 반환 시 언어를 지정하세요.
  인사말(예: 안녕하세요, 반갑습니다, 좋은 아침입니다, 좋은 오후입니다, 좋은
  저녁입니다, 잘 지내세요?, 만나서 반갑습니다, 안녕 등)에는 항상 "안녕하세요!
  저는 IBM 이 만든 watsonx Orchestrate 입니다. 오늘 어떻게
  도와드릴까요?"라고 응답하세요.
  질문이 이해되지 않거나 사실적으로 일관성이 없는 경우, 부정확한 내용으로
  답변하는 대신 이유를 설명하세요. 질문에 대한 답을 모른다면, 답변할 수
  없다고 인정하세요. 거짓 정보를 공유하지 마세요!
  현재 시간은 {current_time}입니다.
  <|assistant|>
  ```

## 내장 스킬 라우팅 설명 (Built-in Skill Routing Description)

### Salesforce (Get all accounts)
- **라우팅 설명 (Routing Description):** 
    ```text
        Salesforce에서 모든 제품 조회하기
    ```
- **질문:** 
    ```text
        Salesforce상의 모든 제품 조회
    ```

### Gmail
- **라우팅 설명 (Routing Description):** 
    ```text
        gmail로 메일을 작성하고 전송해주는 tool
    ```
- **질문 :** 
    ```text
        gmail 작성해줘
    ```
- **질문:** 
    ```text
    {메일계정@0000.com} 으로 메일보내줘
    ```
- **질문:** 
    ```text
    내 gmail 계정으로 고객에게 메일을 작성하고싶어. 아래 상세 내용을 토대로 메일 작성을 도와줘. (제목 추천 요청)
    ```
  - **고객 메일:** `{메일계정@gmail.com}`
  - **수신:** 없음
  - **메일 발송 내용:**
    ```text
    고객님 안녕하세요. 오늘도 저희 IBM과 함께해주셔서 감사합니다. 이번에 소개해드릴 제품은 watsonx.orchestrate 입니다. 해당 제품을 통해 business 진영에서의 Al agentautomation을 경험해보시기 바랍니다. 감사합니다.
    ```

# Lab 1b: 커스텀 스킬 사용하기 (Working with custom skills)

## 코드 설정 (Code Setting)

1.  zip 파일 다운로드
2.  zip 파일 압축 해제 후, 해당 파일에 우클릭하여 vscode로 열기
3.  터미널 열기 (Open terminal)
4.  다음 명령어를 실행하여 필요한 라이브러리를 설치합니다:
    ```bash
    pip install -r requirements.txt
    ```
5.  다음 명령어를 실행하여 스크립트를 테스트합니다:
    ```bash
    python crew_text2sql.py --query "Xtralife의 지난 1달 판매량은?"
    ```
6.  출력을 확인하세요! (Check the output!)

## 커스텀 스킬 라우팅 설명 (Built-in Skill Routing Description)

### Get Historic Sales (Text2SQL with Crew AI)
- **라우팅 설명 (Routing Description):**
    ```text
    자연어 쿼리를 가져와서 SQL 쿼리로 변환하고 실행한 후 본문과 결과를 반환합니다.
    예) 지난 3달 동안의 Xtralife의 매출 수량을 알려줘
    ```
- **질문 :**
    ```text
    지난 3달 동안의 Xtralife의 매출 수량을 알려줘
    ```
- **질문 :**
    ```text
    지난달 Xtralife의 매출을 알려줘
    ```

### Time Series Forecasting(AutoAI Predict)
- **라우팅 설명 (Routing Description):**
    ```text
    제공된 인풋을 활용하여 IBM watsonx에서 예측을 진행합니다. (예측에 사용되는 것은 단순한 숫자형태로 전달되어야 합니다. e.g. "1", "2", "3")
    ```
- **질문 :**
    ```text
    향후 3개월 간의 예상 판매량을 에측해주세요
    ```
- **질문 :**
    ```text
    다음달 예상 판매량을 예측해주세요
    ```

### Calculate Reorder Quantity(Optimal Reorder Quantity)
- **라우팅 설명 (Routing Description):**
    ```text
    최적의 재주문 수량을 계산하기 위해 과거 판매 및 예측을 진행 만일 한국어가 정확하게 출력되지 않으면 이를 수정해서 깔끔한 한국어답변으로 만들어주세요.
    ```
- **질문 :**
    ```text
    현재 재고가 1000개이고, 지난달 매출이 3400개였으며, 다음 달 예상 매출이 3107개라면 최적의 재주문 수량은 얼마여야 할까요?
    ```

# Lab 1d: 커스텀 에이전트 만들기 (Working with custom skills)
## Instruction 입력 (watsonx.ai Agent Lab)
Instructions 입력
```text
You are a helpful assistant that uses tools to answer questions in detail.
When the user asks about a company, find the latest news from the internet and summarize it to the user. Search English keyword on the internet.

When giving the final answer to the user, respond in Korean.

```
## Agent 추가 (watsonx Orchestrate)
- **Display name:** 
    ```text  
    [본인이름] Researcher Agent
    ```
- **Description:** 
    ```text  
    사용자가 특정 기업에 대한 최신 소식 혹은 뉴스에 대한 질문을 하면 인터넷에서 최신 뉴스를 검색하여 그 결과를 사용자에게 알려준다.
    ```
- **Authentication type:**   
    API Key를 선택 합니다.
- **API Key:**    
    임의의 값을 입력 합니다.
- **Service instance URL:** 
    ```text  
    https://research-agent-app.1wrbgjmhze46.us-south.codeengine.appdomain.cloud/chat/completions
    ```
