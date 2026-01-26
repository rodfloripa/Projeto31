import os
from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Redis
from langchain_text_splitters import RecursiveCharacterTextSplitter

app = Flask(__name__)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
REDIS_URL = "redis://redis:6379"

def process_pdf(path):
    reader = PdfReader(path)
    text = "".join([page.extract_text() or "" for page in reader.pages])
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
    return splitter.create_documents([text])

@app.route('/', methods=['GET'])
def health(): return "OK", 200

print("🚀 Inicializando Banco de Dados...")
docs = process_pdf("doc.pdf")
vectorstore = Redis.from_documents(docs, OpenAIEmbeddings(), redis_url=REDIS_URL, index_name="zenml_index")
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

@app.route('/ask', methods=['POST'])
def ask():
    query = request.get_json().get("input_text", "")
    context_docs = retriever.invoke(query)
    context_text = "\n\n".join([d.page_content for d in context_docs])
    prompt = f"Responda usando o contexto:\n{context_text}\n\nPergunta: {query}"
    response = llm.invoke(prompt)
    return jsonify({"resposta": response.content, "contextos": [d.page_content for d in context_docs]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
