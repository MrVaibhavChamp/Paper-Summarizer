# app.py

import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv
import json

app = Flask(__name__)

# Load environment variables
load_dotenv()
api_host = os.environ.get("HOST", "api")
api_port = int(os.environ.get("PORT", 8080))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    interest = request.form['interest']
    question = request.form['question']

    if interest:
        with open('interest.json', 'w') as f:
            json.dump({"interests": interest.split(',')}, f)

    if question:
        url = f'http://{api_host}:{api_port}/'
        data = {"query": question}

        response = requests.post(url, json=data)

        if response.status_code == 200:
            return render_template('result.html', result=response.json())
        else:
            return f"Failed to send data to API. Status code: {response.status_code}", 500
    else:
        return "No question provided", 400


if __name__ == '__main__':
    app.run(debug=True)
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080)