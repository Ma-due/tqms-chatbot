# agents/router/prompt.py
router_prompt_template = """
    사용자의 질문을 보고, 다음 도구 중 하나를 선택해주세요: {tools}.
    도구는 사용자의 질문에 가장 적합한 정보를 제공할 수 있어야 합니다.
    - "web": 웹 검색을 통해 최신 정보나 외부 데이터를 가져올 때
    - "db": 내부 데이터베이스에서 구조화된 데이터를 조회할 때
    - "vectordb": 벡터 데이터베이스에서 문서 검색이나 유사도 기반 검색을 할 때
    
    그러나 현재 개발이 미비하므로 "vectordb"만 간단히 반환해주세요.
    
    질문: {question}
"""

dictionary_prompt_template = """
You are a simple word replacement tool. Replace words in the user's question with their corresponding values from the dictionary, following these strict rules:  
- Replace only the exact words listed in the dictionary, leaving all other words unchanged.  
- Do not rephrase, expand, or answer the question; only perform word-for-word substitution.  
- If no dictionary words are found in the question, return the original question as is.  
- Output only the resulting question text, nothing else.  

Dictionary: {dictionary}
Question: {question}
"""
human_dictionary = {
    "네이트온": "nateon",
    "네이트온비즈": "nateon"
}