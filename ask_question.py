from openai import OpenAI
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name='BAAI/bge-large-zh-v1.5')
vectordb = Chroma(
    persist_directory="my_vector_db_trial1",
    embedding_function=embedding
)

def ask_question(query):
    docs = vectordb.similarity_search(query, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])
    client = OpenAI(api_key="sk-a9b98dfa3f3747a088fd4ea6b64465d9", base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[
            {"role": "system", "content": "你是一个知识丰富的助手"},
            {"role": "user", "content": f"根据以下上下文回答问题:\n{context}\n\n问题:{query}"}
        ]
    )
    return response.choices[0].message.content

# question = "What is HIRA？"
# answer = ask_question(question)
# print("回答：", answer)