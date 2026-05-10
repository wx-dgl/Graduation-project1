from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import os

# 1. 加载PDF
pdf_path = "data/电力系统.pdf"
loader = PyPDFLoader(pdf_path)
documents = loader.load()

print(f"PDF页数: {len(documents)}")

# 2. 文本分块
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

docs = text_splitter.split_documents(documents)
print(f"分块数量: {len(docs)}")

# 3. 使用 Ollama embedding 模型
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 4. 构建向量数据库
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="vector_db"
)

vectorstore.persist()

print("向量库构建完成！")