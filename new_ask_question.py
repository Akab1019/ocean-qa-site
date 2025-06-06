from openai import OpenAI
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name='BAAI/bge-large-zh-v1.5')
vectordb = Chroma(
    persist_directory="my_vector_db_trial1",
    embedding_function=embedding
)

def ask_question(query, history=None):
    docs = vectordb.similarity_search(query, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])
    client = OpenAI(api_key="sk-a9b98dfa3f3747a088fd4ea6b64465d9", base_url="https://api.deepseek.com")
    
    # 构建多轮对话消息
    messages = [{"role": "system", "content": "你是一个知识丰富的助手"}]
    if history:
        messages.extend(history)  # history 是 [{'role': 'user', 'content': '...'}, {'role': 'assistant', 'content': '...'}, ...]
    messages.append({"role": "user", "content": f"根据以下上下文回答问题:\n{context}\n\n问题:{query}"})

    # 流式返回
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=messages,
        stream=True
    )
    answer = ""
    for chunk in response:
        if hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
            answer += chunk.choices[0].delta.content
            yield chunk.choices[0].delta.content  # 每次返回新内容

# 用法示例（在 Flask 里可以用 yield 生成流式响应）
# for token in ask_question("你的问题", history=[{"role": "user", "content": "你好"}]):
#     print(token, end="")