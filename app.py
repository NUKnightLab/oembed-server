#!flask/bin/python
from flask import Flask, jsonify, request, make_response, render_template, url_for, redirect
from functools import wraps
import urllib
import math
import re

app = Flask(__name__)

def xmlize(result):
	import xml.etree.ElementTree as ET
	root = ET.Element('oembed')
	for k,v in result.items():
		node = ET.SubElement(root, k)
		node.text = str(v)
	return ET.tostring(root, encoding='utf8', method='xml')

SUPPORTED_SERVICES = [
	{'service': 'TimelineJS','homepage': 'https://timeline.knightlab.com', 'pattern': re.compile('^https?://cdn.knightlab.com/libs/timeline3/.+$'), 'width': 700, 'height': 500},
	{'service': 'StoryMapJS','homepage': 'https://storymap.knightlab.com', 'pattern': re.compile('^https?://uploads.knightlab.com/storymapjs/.+$'), 'width': 700, 'height': 700},
	{'service': 'JuxtaposeJS','homepage': 'https://juxtapose.knightlab.com', 'pattern': re.compile('^https?://cdn.knightlab.com/libs/juxtapose/.+$'), 'width': 700, 'height': 500},
	{'service': 'SceneVR','homepage': 'https://scene.knightlab.com', 'pattern': re.compile('^https?://uploads.knightlab.com/scenevr/.+$'), 'width': '100%', 'height': 600},
	{'service': 'StoryLineJS','homepage': 'https://storyline.knightlab.com', 'pattern': re.compile('^https?://cdn.knightlab.com/libs/storyline/.+$'), 'width': 700, 'height': 500},
	{'service': 'They Draw It','homepage': 'https://mucollective.co/theydrawit', 'pattern': re.compile('^https?://theydrawit.mucollective.co/vis/.+$'), 'width': 700, 'height': 500},
]

# Format for the oEmbed requests:
# oembed.knightlab.com?url=<a URL to a timeline>
@app.route('/', methods=['GET'])
def index():
	# maybe get clever and have a single point?
	if 'url' in request.args:
		url = request.args['url']
		app.logger.info(url)
		for svc in SUPPORTED_SERVICES:
			if svc['pattern'].match(url):
				return handleRequest(request, svc['width'], svc['height'])
		return (jsonify({'result': f'Not found: url {url} does not match any supported patterns'}), 404)
	return render_template('index.html',services=SUPPORTED_SERVICES)

@app.route('/timeline/', methods=['GET'])
def timelineRequest():
	return redirect(url_for('index',**request.args),code=301)

@app.route('/storymap/', methods=['GET'])
def storymapRequest():
	return redirect(url_for('index',**request.args),code=301)

@app.route('/juxtapose/', methods=['GET'])
def juxtaposeRequest():
	return redirect(url_for('index',**request.args),code=301)

@app.route('/scenevr/', methods=['GET'])
def sceneRequest():
	return redirect(url_for('index',**request.args),code=301)

@app.route('/theydrawit/', methods=['GET'])
def drawItRequest():
	return redirect(url_for('index',**request.args),code=301)

@app.route('/storyline/', methods=['GET'])
def storylineRequest():
	return redirect(url_for('index',**request.args),code=301)

def handleRequest(request, default_width, default_height):

	params = request.args

	fmt = params.get('format','json')
	if fmt not in ['json', 'xml']:
		status501 = jsonify({'result': "Format [{}] not supported.".format(fmt)}), 501
		return(status501)

	url = params['url']
	url = re.sub('^http:','https:',url) # force https for better compatibility

	#Set some defaults for height and width.
	#Check to see if maxwidth or maxheight are in the request
	maxwidth = params.get("maxwidth", None)
	maxheight = params.get("maxheight", None)

	decodedURL = urllib.parse.unquote(url)

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

	if fmt == 'xml':
		resp = make_response(xmlize(result))
		resp.headers['Content-type'] = 'text/xml; charset=utf-8'
	else:
		resp = make_response(jsonify(result))
		resp.headers['Content-type'] = 'application/json; charset=utf-8'

	return resp

def dims_from_url(url):
	"""Return a tuple (w,h) based on extracting parameters named 'width' and 'height' from the given URL. Return None for either if not present."""
	w = None
	h = None

	scheme, netloc, path, params, query, fragment = urllib.parse.urlparse(url)
	
	#Take params from the Timeline URL
	contentParams = urllib.parse.parse_qs(query)

	#Find the height and width fields to set for iframe html
	for key, value in contentParams.items():
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

	# convert strings to ints if they are
	try: width = int(width)
	except: pass

	try: height = int(height)
	except: pass

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
