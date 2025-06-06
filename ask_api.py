from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from ask_question import ask_question

app = Flask(__name__)
CORS(app)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')
    answer = ask_question(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)