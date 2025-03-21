example_answer = [
    {
        "input": "소득은 어떻게 구분되나요?",
        "answer": """소득세법 제 4조(소득의 구분)에 따르면 소득은 아래와 같이 구분됩니다.
1. 종합소득
    - 이 법에 따라 과세되는 모든 소득에서 제2호 및 제3호에 따른 소득을 제외한 소득으로서 다음 각 목의 소득을 합산한 것
    - 가. 이자소득
    - 나. 배당소득
    - 다. 사업소득
    - 라. 근로소득
    - 마. 연금소득
    - 바. 기타소득
2. 퇴직소득
3. 양도소득
"""
    },
    {
        "input": "소득세의 과세 기간은 어떻게 되나요?",
        "answer": """소득세법 제5조(과세기간)에 따르면, 
일반적인 소득세의 과세기간은 1월 1일부터 12월 31일까지 1년입니다
하지만 거주자가 사망한 경우는 1월 1일부터 사망일까지, 
거주자가 해외로 이주한 경우 1월 1일부터 출국한 날까지 입니다"""
    },
    {
        "input": "원천징수 영수증은 언제 발급받을 수 있나요?",
        "answer": """소득세법 제143조(근로소득에 대한 원천징수영수증의 발급)에 따르면, 
근로소득을 지급하는 원천징수의무자는 해당 과세기간의 다음 연도 2월 말일까지 원천징수영수증을 근로소득자에게 발급해야하고. 
다만, 해당 과세기간 중도에 퇴직한 사람에게는 퇴직한 한 날의 다음 달 말일까지 발급하여야 하며, 
일용근로자에 대하여는 근로소득의 지급일이 속하는 달의 다음 달 말일까지 발급하여야 합니다.
만약 퇴사자가 원청징수영수증을 요청한다면 지체없이 바로 발급해야 합니다"""
    },
]

system_prompt = (
    "당신은 소득세법 전문가입니다. 사용자의 소득세법에 관한 질문에 답변해주세요"
    "아래에 제공된 문서를 활용해서 답변해주시고"
    "답변을 알 수 없다면 모른다고 답변해주세요"
    "답변을 제공할 때는 소득세법 (XX조)에 따르면 이라고 시작하면서 답변해주시고"
    "2-3 문장정도의 짧은 내용의 답변을 원합니다"
    "\n\n"
    "{context}"
)

human_dictionary = ["사람을 나타내는 표현 -> 거주자"]

contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)
