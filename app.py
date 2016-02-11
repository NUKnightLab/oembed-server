#!flask/bin/python
from flask import Flask, jsonify, request, make_response
from urlparse import urlparse, parse_qs
import urllib
from helper import *

app = Flask(__name__)

# Format for the oEmbed requests:
# oembed.knightlab.com?url=<a URL to a timeline>
@app.route('/', methods=['GET'])
def index():
	return jsonify({"message" : "More info about how to use the oEmbed server to come soon"})

@app.route('/timeline/', methods=['GET'])
def timelineRequest():
	return handleRequest(request.url)

@app.route('/storymap/', methods=['GET'])
def storymapRequest():
	return handleRequest(request.url)

@app.route('/juxtapose/', methods=['GET'])
def juxtaposeRequest():
	return handleRequest(request)

def handleRequest(request):
	#Error Response formats
	status404 = jsonify({'result': "This is an erroneous request."}), 404
	# status501
	# status401

	params = request.args
	maxwidth = None
	maxheight = None

	if "url" in params:
		url = params["url"]

		#Check to see if maxwidth or maxheight are in the request
		if("maxwidth" in params):
			maxwidth = params["maxwidth"]
		if("maxheight" in params):
			maxheight = params["maxheight"]

 		result = parseURLs(url, maxwidth, maxheight)
		
		if(result == None):
			return status404

		resp = make_response(jsonify(result))
		resp.headers['Content-type'] = 'application/json; charset=utf-8'

		return resp
	else:
		return status404

#This function needs to consider all of the options for KL tools.
def parseURLs(url, maxwidth, maxheight):
	decodedURL = urllib.unquote(url).decode('utf8')
	parsedURL = urlparse(urllib.unquote(url).decode('utf8'))
	
	if("timeline" in parsedURL.path):
		#Set some defaults for height and width.
		width = 600
		height = 600

		#Find the height and width fields to set for iframe html
		for key, value in params.iteritems():
			if(key == 'width'):
				width = [value[0] if "%" in value[0] else int(value[0])]
			elif(key == 'height'):
				height = [value[0] if "%" in value[0] else int(value[0])]

	elif("storymapjs" in parsedURL.path):
		#Set some defaults for height and width.
		width = '100%'
		height = 800

	elif("juxtapose" in parsedURL.path):
		#Set some defaults for height and width.
		width = '100%'
		height = 600

	else:
		return None

	#Get an iframe with the correct format
	html = developIframe(decodedURL, width, height, maxwidth, maxheight)

	#Structure and send request with the JSON response
	return structureResponse(html, width, height)

def developIframe(url, width, height, maxwidth, maxheight):
	# print("MaxWidth: {}, MaxHeight: {}".format(maxwidth, maxheight))

	html = "<iframe src='{}' width='{}' height='{}'"
	
	#Add the Juxtapose class
	if("juxtapose" in url):
		html += " class='juxtapose' "

	html += " frameborder='0'></iframe>"

	html = html.format(url, width, height)

	return html

def structureResponse(html, width, height):

	responseJSON = {}

	#For Knight Lab Tools, we will need a `rich` type.
	#As well a provider information
	responseJSON['type'] = 'rich'
	responseJSON['provider_name'] = "Knight Lab"
	responseJSON['provider_url'] = "http://knightlab.northwestern.edu/"

	#oEmbed explains that the version must be 1.
	responseJSON['version'] = '1.0'

	#For rich-type content, oEmbed requires html, 
	#width, and height parameters.
	responseJSON['html'] = html
	responseJSON['width'] = width
	responseJSON['height'] = height

	return responseJSON


if __name__ == '__main__':
    app.run(debug=True)


