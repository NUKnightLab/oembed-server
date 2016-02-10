#!flask/bin/python
from flask import Flask, jsonify, request, make_response
from urlparse import urlparse, parse_qs
import urllib

app = Flask(__name__)

#Function for clearly printing a dictionary's values
def dictPrint(dictIn):
	try: 
		for attribute, value in dictIn.items():
			print('{} : {}'.format(attribute, value))
		print('\n')
	except:
		f1.write('\n =============================== \n PRINTING ISSUE FOR UNICODE \n =============================== \n')

# Format for the oEmbed requests:
# oembed.knightlab.com?url=<a URL to a timeline>
@app.route('/', methods=['GET'])
def developEmbed():
	fullPath = request.url
	urlChunks = fullPath.split("/?url=")

	if len(urlChunks) == 2:
		url = urlChunks[1]
		result = parseTimeline(url)

		resp = make_response(jsonify(result))
		resp.headers['Content-type'] = 'application/json; charset=utf-8'

		return resp
	else:
		return jsonify({'result': "This is an erroneous request."}), 404


#This function needs to consider all of the options for timelines.
def parseTimeline(url):
	decodedURL = urllib.unquote(url).decode('utf8')
	timelineURL = urlparse(urllib.unquote(url).decode('utf8'))
	if("timeline" in timelineURL.path):

		#Set some defaults for height and width.
		width = 600
		height = 600

		params = parse_qs(timelineURL.query)
		dictPrint(params)

		#Find the height and width fields to set for iframe html
		for key, value in params.iteritems():
			if(key == 'width'):
				width = int(value[0])
			elif(key == 'height'):
				height = int(value[0])

		#Get an iframe with the correct format
		html = developIframe(decodedURL, width, height)

		#Structure and send request with the JSON response
		return structureResponse(html, width, height)

	else:
		print("It's an error!")

	return timelineURL

def developIframe(url, width, height):
	html = "<iframe src='%s' width='%d' height='%d' frameborder='0'></iframe>" % (url, width, height)
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


