curl -X POST \
  https://text2sql-crewai.1wradzln6ree.us-south.codeengine.appdomain.cloud/components/schemas/Text2SQLRequest \
  -H "Content-Type: application/json" \
  -u "test:test" \
  -d '{
    "query": "지난 달 총 매출액은 얼마인가요?"
  }'
