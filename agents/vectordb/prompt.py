#agents/vectordb/prompt.py
example_answer = [
    {
        "input": "SWING 오더 서비스의 장애 원인은 무엇인가요?",
        "answer": """엑셀 데이터에 따르면, 'SWING 오더' 서비스의 장애 원인은 주로 외부 기관 오류로 나타납니다. 예를 들어, 'KCB社 측 DB 오류'나 'KAIT 행공센 오류'가 빈번한 원인으로 기록되어 있습니다. 특정 장애의 자세한 원인을 알고 싶다면 장애 접수 번호를 말씀해 주세요."""
    },
    {
        "input": "2021년 1월에 발생한 장애 중 심각도가 3인 경우는 몇 건인가요?",
        "answer": """엑셀 데이터를 확인한 결과, 2021년 1월에 발생한 장애 중 심각도가 3인 경우는 총 7건입니다. 이 중 대부분은 'SWING 오더' 서비스와 관련된 장애로 확인됩니다."""
    },
    {
        "input": "장애 접수 번호 ER210105-000534의 원인은 무엇인가요?",
        "answer": """장애 접수 번호 ER210105-000534의 원인은 'KCB社 측 서비스 처리량 증가로 인한 DB 오류'입니다. 이로 인해 'SWING 오더' 서비스에 장애가 발생했습니다."""
    },
    {
        "input": "가장 오래 지속된 장애 사례는 무엇인가요?",
        "answer": """엑셀 데이터에 따르면, 가장 오래 지속된 장애는 장애 접수 번호 ER210201-000191로, 총 931분(약 15.5시간) 동안 지속되었습니다. 원인은 'SKP VAS G/W System 연동건수 증가 및 응답 처리 지연'입니다."""
    },
]

contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)