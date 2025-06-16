import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from crewai import Agent, Task, Crew, Process
from crewai import LLM
import pandas as pd
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


class QueryRequest(BaseModel):
    query: str

# Load environment variables
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM
llm = LLM(
    api_key=os.environ["WATSONX_API_KEY"],
    model=os.environ["MODEL_ID"],
    project_id=os.environ["PROJECT_ID"],
    watsonx_url = os.environ["WATSONX_API_BASE"],
    params={
        "decoding_method": "greedy",
        "max_new_tokens": 15000,
        "temperature": 0.1
        # "repetition_penalty": 1.05
    }
)

def get_db_connection():
    return sqlite3.connect('sales.db')

# SQL Query Generator Agent
def create_query_generator():
    return Agent(
        role="SQL Query Generator",
        goal="자연어로 제공되는 사용자 설명을 기반으로 적합한 SQL 쿼리문을 생성합니다",
        backstory="""당신은 자연어 요청을 효율적인 SQL 쿼리로 변환하는 전문 SQL 개발자입니다. 
        복잡한 데이터 관계를 이해하고 집계, 그룹화 및 날짜 연산을 포함하는 쿼리를 생성할 수 있습니다. 
        'month_year'와 'total_figure' 컬럼을 일관되게 유지하세요.""",
        llm=llm,
        allow_delegation=False
    )

def create_generation_task(agent, query):
    return Task(
        description=f"""자연어로 제공되는 사용자 설명을 기반으로 적절한 SQL 쿼리문을 생성하세요.
        
        사용자 설명: {query}
        
        Database Schema:
        Table: Sales
        Columns:
        - ID (INTEGER PRIMARY KEY)
        - Order ID (TEXT)
        - Order Date (TEXT, Format: YYYY-MM-DD)
        - Ship Date (TEXT, Format: YYYY-MM-DD)
        - Ship Mode (TEXT)
        - Customer ID (TEXT)
        - Customer Name (TEXT)
        - Segment (TEXT)
        - Country (TEXT)
        - City (TEXT)
        - State (TEXT)
        - Postal Code (TEXT)
        - Region (TEXT)
        - Product Name (TEXT) includes 'Xtralife'
        - Product_ID (TEXT)
        - Category (TEXT)
        - Sub Category (TEXT)
        - Sales (REAL)
        - Quantity (INTEGER)
        - Discount (REAL)
        - Profit (REAL)
        
        필수 요청 사항:
        1. 컬럼 이름
        - 항상 위 스키마에 표시된 정확한 컬럼 이름을 사용하세요
        - 집계된 컬럼에는 항상 의미 있는 별칭을 사용하세요
        - 예시: SUM(Sales)가 total_sales, AVG(Profit)가 avg_profit를 의미


        2. 날짜 연산
        - 완전한 월 쿼리에는 항상 고정된 YYYY-MM 값을 사용하세요
        - 완전한 월 형식: strftime('%Y-%m', "Order Date")
        - BETWEEN 대신 >=와 <=를 사용하세요

        3. 시간 창 패턴
        - 최근 N개월에 대한 쿼리 작성 시:
        - sqlCopystrftime('%Y-%m', "Order Date") >= strftime('%Y-%m', date('now', '-N months')) 
        - AND strftime('%Y-%m', "Order Date") < strftime('%Y-%m', date('now'))

        - 지난 달에 대한 쿼리:
        - sqlCopystrftime('%Y-%m', "Order Date") = (SELECT strftime('%Y-%m', date('now', '-1 month')))

        - 작년 같은 달에 대한 쿼리:
        - sqlCopystrftime('%Y-%m', "Order Date") = (SELECT strftime('%Y-%m', date('now', '-1 year')))


        4. 집계
        - 집계 함수를 사용할 때는 항상 GROUP BY를 포함하세요
        - 예시: SELECT "Product Name", SUM(Sales) as total_figure FROM Sales GROUP BY "Product Name"

        5. 필터링
        - 집계된 결과를 필터링할 때는 HAVING을 사용하세요
        - 원시 데이터를 필터링할 때는 WHERE를 사용하세요
        - 예시: HAVING total_sales > 1000

        6. 정렬
        - 정렬 방향을 지정하세요(ASC/DESC)
        - 예시: ORDER BY total_figure DESC
        
        어떤 부연 설명 없이 SQL 쿼리만을 답변으로 출력하세요.""",
        expected_output="""자연어로 제공되는 사용자 설명에 대한 정확하고 검증된 SQL 쿼리.""",
        agent=agent
    )

@app.post("/query")
async def process_query(request:QueryRequest):
    try:
        query_generator = create_query_generator()
        generation_task = create_generation_task(query_generator, request.query)
        
        generation_crew = Crew(
            agents=[query_generator],
            tasks=[generation_task],
            process=Process.sequential,
            verbose=True
        )
        
        sql_query = str(generation_crew.kickoff()).strip()
        
        # Execute the query
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            columns = [description[0] for description in cursor.description]
            results = cursor.fetchall()
            formatted_results = [dict(zip(columns, row)) for row in results]

        
        return {
            "result": formatted_results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
 