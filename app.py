#!flask/bin/python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/services/oembed', methods=['GET'])
def get_tasks():
	test = request.args.get('id')
	return jsonify({'result': test})



if __name__ == '__main__':
    app.run(debug=True)