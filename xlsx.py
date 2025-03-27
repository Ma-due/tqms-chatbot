import pandas as pd
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()
os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")

# 엑셀 파일 경로
file_path = r'C:\Users\Administrator\PycharmProjects\tqms-chatbot\TRBL_REPORT_INFO_250321.xlsx'

# "장애보고서" 시트 읽기
sheet_name = "장애보고서"
df = pd.read_excel(file_path, sheet_name=sheet_name)

# 원하는 컬럼만 선택
columns_to_show = ['TRBL_ACCP_NO', 'TRBLTITLCNTN', 'ISACCUSTCONM', 'TRBLPRTCCAUSCNTN', 'SVCNM']
filtered_df = df[columns_to_show]

# 2행(인덱스 1) 제외
filtered_df = filtered_df.drop(index=1)

# 문서 리스트 생성
documents = []
for index, row in filtered_df.iterrows():
    row_list = row.tolist()  # 행을 리스트로 변환

    # 리스트를 문자열로 변환 (page_content)
    content = (
        f"TRBL_ACCP_NO: {row_list[0]}\n"
        f"TRBLTITLCNTN: {row_list[1]}\n"
        f"ISACCUSTCONM: {row_list[2]}\n"
        f"TRBLPRTCCAUSCNTN: {row_list[3]}\n"
        f"SVCNM: {row_list[4]}"
    )

    # 메타데이터 추가
    metadata = {
        "source": sheet_name,
        "row_index": index,
        "trbl_accp_no": str(row_list[0])  # 검색용으로 고유 ID 추가
    }

    # Document 객체 생성
    doc = Document(page_content=content, metadata=metadata)
    documents.append(doc)

# 출력으로 확인 (선택 사항)
print(f"총 문서 수: {len(documents)}")
for i, doc in enumerate(documents[:2]):  # 처음 2개만 미리보기
    print(f"\n문서 {i}:")
    print("내용:", doc.page_content)
    print("메타데이터:", doc.metadata)

# Pinecone 설정 및 업로드
embedding = OpenAIEmbeddings(model="text-embedding-3-large")
persist_directory = "./chroma_db"
"""
index_name = "tqms"
pc = Pinecone()
index = pc.Index(index_name)

# 기존 데이터 삭제 (선택 사항)
index.delete(delete_all=True)  # 주의: 모든 데이터 지움

# Pinecone에 문서 업로드
# database = PineconeVectorStore.from_documents(documents, embedding, index_name=index_name)
# 인덱스 상태 확인
print("\nPinecone 인덱스 상태:")
print(index.describe_index_stats())
"""

database = Chroma.from_documents(
    documents=documents,
    embedding=embedding,
    persist_directory=persist_directory,
    collection_name="tqms"
)

# Chroma 상태 확인 (저장된 벡터 수 확인)
print("\nChroma 벡터 저장소 상태:")
print(f"저장된 문서 수: {database._collection.count()}")