from flask import Flask, request, jsonify,Response, stream_with_context
from flask_cors import CORS
import os

from new_ask_question import ask_question  # 注意导入你的流式版本

app = Flask(__name__)
CORS(app)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')
    history = data.get('history', None)  # 支持多轮对话
    # 流式响应
    def generate():
        for chunk in ask_question(question, history):
            yield chunk
    return Response(stream_with_context(generate()), mimetype='text/plain; charset=utf-8')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)