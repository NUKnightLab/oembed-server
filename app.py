#!flask/bin/python
from flask import Flask, jsonify, request, make_response, render_template
from functools import wraps
from urlparse import urlparse, parse_qs, urlunparse
import urllib
from urllib import urlencode
import math
import re

app = Flask(__name__)

def xml_is_not_supported(f):
	@wraps(f)
	def func(*args, **kwargs):
		params = request.args
		if params.get("format") == "xml":
			status501 = jsonify({'result': "Not supported."}), 501
			return(status501)
		return f(*args, **kwargs)
	return func

def url_pattern_tester(pattern_string):
	"""Ensure that there's a URL, and that it is appropriate for the path."""
	def decorator(f):
		@wraps(f)
		def func(*args, **kwargs):
			pattern = re.compile(pattern_string)
			status404 = jsonify({'result': "This is an erroneous request."}), 404
			params = request.args
			try:
				if pattern.match(params['url']):
					return f(*args, **kwargs)
			except KeyError: 
				pass
			return status404
		return func
	return decorator


# Format for the oEmbed requests:
# oembed.knightlab.com?url=<a URL to a timeline>
@app.route('/', methods=['GET'])
def index():
	# maybe get clever and have a single point?
	# if 'url' in request.args:
	# 	url = request.args['url']
	# 	for pattern in REDIRECT_PATTERNS:
	# 		if pattern.match(url):
	# 			redir_url = url_for(REDIRECT_PATTERNS[])
	# 			return redirect
	return render_template('index.html')

@app.route('/timeline/', methods=['GET'])
@url_pattern_tester('^.+timeline3?.*$')
@xml_is_not_supported
def timelineRequest():
	return handleRequest(request, 700, 500)

@app.route('/storymap/', methods=['GET'])
@url_pattern_tester('^.+storymap.*$')
@xml_is_not_supported
def storymapRequest():
	return handleRequest(request, 700, 700)

@app.route('/juxtapose/', methods=['GET'])
@url_pattern_tester('^.+juxtapose.*$')
@xml_is_not_supported
def juxtaposeRequest():
	return handleRequest(request, 700, 500)

@app.route('/scenevr/', methods=['GET'])
@url_pattern_tester('^.+scenevr.*$')
@xml_is_not_supported
def sceneRequest():
	return handleRequest(request, '100%', 600)

@app.route('/theydrawit/', methods=['GET'])
@url_pattern_tester('^.+theydrawit.*$')
@xml_is_not_supported
def drawItRequest():
	return handleRequest(request, 700, 500)

@app.route('/storyline/', methods=['GET'])
@url_pattern_tester('^.+storyline.*$')
@xml_is_not_supported
def storylineRequest():
	return handleRequest(request, 700, 500)

def handleRequest(request, default_width, default_height):

	params = request.args
	url = params['url']
	#Set some defaults for height and width.
	#Check to see if maxwidth or maxheight are in the request
	maxwidth = params.get("maxwidth", None)
	maxheight = params.get("maxheight", None)

	decodedURL = urllib.unquote(url).decode('utf8')

	url_width, url_height = dims_from_url(decodedURL)

	if url_width is not None: 
		default_width = url_width
	if url_height is not None:
		default_height = url_height

	# oembed service parameters take precedence
	width = params.get("width", default_width)
	height = params.get("height", default_height)


	if(maxwidth != None):
		if (("%" not in maxwidth) and (int(maxwidth) < int(width))):
			width = int(maxwidth)
	if(maxheight != None):
		if (("%" not in maxheight) and (int(maxheight) < int(height))):
			height = int(maxheight)

	#Get an iframe with the correct format
	html = developIframe(decodedURL, width, height)

	#Structure and send request with the JSON response
	result = structureResponse(html, width, height)

	resp = make_response(jsonify(result))
	resp.headers['Content-type'] = 'application/json; charset=utf-8'

	return resp

def dims_from_url(url):
	"""Return a tuple (w,h) based on extracting parameters named 'width' and 'height' from the given URL. Return None for either if not present."""
	w = None
	h = None

	scheme, netloc, path, params, query, fragment = urlparse(url)
	
	#Take params from the Timeline URL
	contentParams = parse_qs(query)

	#Find the height and width fields to set for iframe html
	for key, value in contentParams.iteritems():
		if(key == 'width'):
			w = value[0] if "%" in value[0] else int(value[0])
		elif(key == 'height'):
			h = value[0] if "%" in value[0] else int(value[0])

	return (w,h)



def scaleHeight(width, maxwidth, height):
	newWidth = maxwidth
	newHeight =  math.ceil(((maxwidth * height))/width)
	return int(newHeight)
	
def developIframe(url, width, height):

	html = """<iframe src='{url}' width='{width}' height='{height}' {cls} frameborder='0' allowfullscreen></iframe>"""
	
	format_context = {
		'url': url,
		'width': width,
		'height': height,
		'cls': ''
	}

	#Add the Juxtapose class
	if("juxtapose" in url):
		format_context['cls'] = " class='juxtapose' "

	return html.format(**format_context)

def structureResponse(html, width, height):

	responseJSON = {}

	#For Knight Lab Tools, we will need a `rich` type.
	#As well a provider information
	responseJSON['type'] = 'rich'
	responseJSON['provider_name'] = "Knight Lab"
	responseJSON['provider_url'] = "https://knightlab.northwestern.edu/"

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


