curl -X POST \
  https://text2sql-text2sql-project.apps.itz-daq30p.osv.techzone.ibm.com/query \
  -H "Content-Type: application/json" \
  -u "test:test" \
  -d '{
    "query": "지난 달 총 매출액은 얼마인가요?"
  }'
