import pandas as pd
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()
os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")

# 엑셀 파일 경로
file_path = r'./TRBL_REPORT_INFO_250321.xlsx'

# "장애보고서" 시트 읽기
sheet_name = "장애보고서"
df = pd.read_excel(file_path, sheet_name=sheet_name)

# 원하는 컬럼만 선택 (TRBLPRSTCNTN 추가)
columns_to_show = ['TRBL_ACCP_NO', 'TRBLTITLCNTN', 'ISACCUSTCONM', 'TRBLPRTCCAUSCNTN', 'SVCNM', 'TRBLPRSTCNTN']
filtered_df = df[columns_to_show]

# 2행(인덱스 1) 제외
filtered_df = filtered_df.drop(index=1)

# 문서 리스트 생성
documents = []
for index, row in filtered_df.iterrows():
    row_list = row.tolist()  # 행을 리스트로 변환

    # page_content: TRBLTITLCNTN, TRBLPRTCCAUSCNTN, TRBLPRSTCNTN만 포함
    content = (
        f"TRBLTITLCNTN: {row_list[1]}\n"
        f"TRBLPRTCCAUSCNTN: {row_list[3]}\n"
        f"TRBLPRSTCNTN: {row_list[5]}"
    )

    # 메타데이터: TRBL_ACCP_NO, ISACCUSTCONM, SVCNM 포함
    metadata = {
        "trbl_accp_no": str(row_list[0]),  # 검색용 고유 ID
        "isaccustconm": str(row_list[2]),  # ISACCUSTCONM
        "svcnm": str(row_list[4])          # SVCNM
    }

    # Document 객체 생성
    doc = Document(page_content=content, metadata=metadata)
    documents.append(doc)

# 출력으로 확인 (선택 사항)
print(f"총 문서 수: {len(documents)}")
for i, doc in enumerate(documents[:10]):  # 처음 2개만 미리보기
    print(f"\n문서 {i}:")
    print("내용:", doc.page_content)
    print("메타데이터:", doc.metadata)

# Chroma 설정 및 업로드
embedding = OpenAIEmbeddings(model="text-embedding-3-large")
persist_directory = "./chroma_db"

database = Chroma.from_documents(
    documents=documents,
    embedding=embedding,
    persist_directory=persist_directory,
    collection_name="tqms"
)

# Chroma 상태 확인 (저장된 벡터 수 확인)
print("\nChroma 벡터 저장소 상태:")
print(f"저장된 문서 수: {database._collection.count()}")