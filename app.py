#!flask/bin/python
from flask import Flask, jsonify, request
from urlparse import urlparse, parse_qs
import urllib

app = Flask(__name__)

time

# Format for the oEmbed requests:
# oembed.knightlab.com?url=<a URL to a timeline>
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


#This function needs to consider all of the options for timelines.
def parseTimeline(url):
	timelineURL = urlparse(urllib.unquote(url).decode('utf8'))
	if("timeline" in timelineURL.path):
		print(parse_qs(timelineURL.query))

	else:
		print("It's an error!")

	return timelineURL


def structureJSON(html):

	responseJSON = {}

	#For Knight Lab Tools, we will need a `rich` type.
	responseJSON['type'] = 'rich'

	#oEmbed explains that the version must be 1.
	responseJSON['version'] = 1.0

	#For rich-type content, oEmbed requires html, 
	#width, and height parameters.
	responseJSON['html'] = html


if __name__ == '__main__':
    app.run(debug=True)


# type (required) : The resource type. Valid values, along with value-specific 
# parameters, are described below.

# version (required): The oEmbed version number. This must be 1.0.

# title (optional) : A text title, describing the resource.

# author_name (optional) : The name of the author/owner of the resource.

# author_url (optional) : A URL for the author/owner of the resource.

# provider_name (optional) : The name of the resource provider.

# provider_url (optional) : The url of the resource provider.

# cache_age (optional) : The suggested cache lifetime for this resource, in 
# seconds. Consumers may choose to use this value or not.

# thumbnail_url (optional) : A URL to a thumbnail image representing the resource. 
# The thumbnail must respect any maxwidth and maxheight parameters. If this parameter 
# is present, thumbnail_width and thumbnail_height must also be present.

# thumbnail_width (optional) : The width of the optional thumbnail. If this parameter
# is present, thumbnail_url and thumbnail_height must also be present.

# thumbnail_height (optional) : The height of the optional thumbnail. If this 
# parameter is present, thumbnail_url and thumbnail_width must also be present.

