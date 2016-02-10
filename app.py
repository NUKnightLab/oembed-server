#!flask/bin/python
from flask import Flask, jsonify, request
from urlparse import urlparse

app = Flask(__name__)

# Format for the oEmbed requests:
# oembed.knightlab.com?url=<a URL to a timeline>
# 
@app.route('/', methods=['GET'])
def get_url_param():
	fullPath = request.url
	urlChunks = fullPath.split("/?url=")

	if len(urlChunks) <= 2:
		url = urlChunks[1]
		return jsonify({'result': url})
	else:
		return jsonify({'result': "This is an erroneous request."})

# def parseTimeline(url):





if __name__ == '__main__':
    app.run(debug=True)