# agents/common.py
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate


def get_few_shot_prompt(example_asnwer):
    example_prompt = ChatPromptTemplate.from_messages(
        [("human", "{input}"), ("ai", "{answer}")]
    )
    return FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=example_asnwer,
    )