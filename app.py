#!flask/bin/python
from flask import Flask, jsonify, request
from urlparse import urlparse, parse_qs
import urllib

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
		result = parseTimeline(url)
		return jsonify({'result': result})
	else:
		return jsonify({'result': "This is an erroneous request."})

def parseTimeline(url):
	timelineURL = urlparse(urllib.unquote(url).decode('utf8'))
	if("timeline" in timelineURL.path):
		print(parse_qs(timelineURL.query))

	else:
		print("It's an error!")

	return timelineURL

# def structureJSON(type, ):
	

if __name__ == '__main__':
    app.run(debug=True)