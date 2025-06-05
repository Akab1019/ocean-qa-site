from flask import Flask, request, jsonify
from flask_cors import CORS

# 导入你的问答函数和向量库
from ask_question import ask_question

app = Flask(__name__)
CORS(app)  # 允许跨域

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')
    answer = ask_question(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)