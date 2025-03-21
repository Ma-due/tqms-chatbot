from langchain_community.document_loaders import Docx2txtLoader, csv_loader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200
)

loader = Docx2txtLoader('./tax.docx')
document_list = loader.load_and_split(text_splitter=text_splitter)

embedding = OpenAIEmbeddings(model='text-embedding-3-large')
index_name = 'test'
pc = Pinecone()

database = PineconeVectorStore.from_documents(document_list, embedding, index_name=index_name)
index = pc.Index(index_name)
print(index.describe_index_stats())