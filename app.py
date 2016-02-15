#!flask/bin/python
from flask import Flask, jsonify, request, make_response
from urlparse import urlparse, parse_qs
import urllib
from helper import *
import math

app = Flask(__name__)

# Format for the oEmbed requests:
# oembed.knightlab.com?url=<a URL to a timeline>
@app.route('/', methods=['GET'])
def index():
	return jsonify({"message" : "More info about how to use the oEmbed server to come soon"})

@app.route('/timeline/', methods=['GET'])
def timelineRequest():
	return handleTimelineRequest(request)

@app.route('/storymap/', methods=['GET'])
def storymapRequest():
	return handleStorymapRequest(request)

@app.route('/juxtapose/', methods=['GET'])
def juxtaposeRequest():
	return handleJuxtaposeRequest(request)

def handleTimelineRequest(request):
	#Error Response formats
	status404 = jsonify({'result': "This is an erroneous request."}), 404
	# status501
	# status401

	params = request.args

	#Set some defaults for height and width.
	width = 600
	height = 600
	maxwidth = None
	maxheight = None

	if "url" in params:
		url = params["url"]
		if("timeline" in url):
			#Check to see if maxwidth or maxheight are in the request
			if("maxwidth" in params):
				maxwidth = params["maxwidth"]
			if("maxheight" in params):
				maxheight = params["maxheight"]

	 		decodedURL = urllib.unquote(url).decode('utf8')
			parsedURL = urlparse(decodedURL)
			
			#Take params from the Timeline URL
			contentParams = parse_qs(parsedURL.query)
			print(contentParams)

			#Find the height and width fields to set for iframe html
			for key, value in contentParams.iteritems():
				if(key == 'width'):
					width = value[0] if "%" in value[0] else int(value[0])
				elif(key == 'height'):
					height = value[0] if "%" in value[0] else int(value[0])

			print(maxwidth)
			print(width)

			if(int(maxwidth) < int(width)):
				height = scaleHeight(int(width), int(maxwidth), int(height))
				width = int(maxwidth)
				print(height)

			#Get an iframe with the correct format
			html = developIframe(decodedURL, width, height)

			#Structure and send request with the JSON response
			result = structureResponse(html, width, height)

			resp = make_response(jsonify(result))
			resp.headers['Content-type'] = 'application/json; charset=utf-8'

			return resp
		else:
			return status404
	else:
		return status404

def handleStorymapRequest(request):
	#Error Response formats
	status404 = jsonify({'result': "This is an erroneous request."}), 404
	# status501
	# status401

	params = request.args

	#Set some defaults for height and width.
	width = '100%'
	height = 800
	maxwidth = None
	maxheight = None

	if "url" in params:
		url = params["url"]
		if("storymap" in url):
			#Check to see if maxwidth or maxheight are in the request
			if("maxwidth" in params):
				maxwidth = params["maxwidth"]
			if("maxheight" in params):
				maxheight = params["maxheight"]

			# if(int(maxwidth) < int(width)):
			# 	width = int(maxwidth)
			# 	height = scaleHeight(int(width), int(maxwidth), int(height))

			decodedURL = urllib.unquote(url).decode('utf8')

			#Get an iframe with the correct format
			html = developIframe(decodedURL, width, height)

			#Structure and send request with the JSON response
			result = structureResponse(html, width, height)

			resp = make_response(jsonify(result))
			resp.headers['Content-type'] = 'application/json; charset=utf-8'

			return resp
		else:
			return status404
	else:
		return status404

def handleJuxtaposeRequest(request):
	#Error Response formats
	status404 = jsonify({'result': "This is an erroneous request."}), 404
	# status501
	# status401

	params = request.args

	#Set some defaults for height and width.
	width = '100%'
	height = 600
	maxwidth = None
	maxheight = None

	if "url" in params:
		url = params["url"]
		if("juxtapose" in url):
			#Check to see if maxwidth or maxheight are in the request
			if("maxwidth" in params):
				maxwidth = params["maxwidth"]
			if("maxheight" in params):
				maxheight = params["maxheight"]

			decodedURL = urllib.unquote(url).decode('utf8')

			# if(int(maxwidth) < int(width)):
			# 	width = int(maxwidth)
			# 	height = scaleHeight(int(width), int(maxwidth), int(height))

			#Get an iframe with the correct format
			html = developIframe(decodedURL, width, height)

			#Structure and send request with the JSON response
			result = structureResponse(html, width, height)

			resp = make_response(jsonify(result))
			resp.headers['Content-type'] = 'application/json; charset=utf-8'

			return resp
		else:
			return status404
	else:
		return status404

def scaleHeight(width, maxwidth, height):
	print("Initial Width was {}. Initial Height was {}.".format(width, height))
	newWidth = maxwidth
	newHeight =  math.ceil(((maxwidth * height))/width)
	print("New Width is {}".format(newWidth))
	print("New Height is {}".format(newHeight))
	return int(newHeight)
	#CHANGE THE URL'S WIDTH PARAM VALUE
	
def developIframe(url, width, height):
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


