"""Simple test rig adapted from http://flask.pocoo.org/docs/1.0/testing/"""
from urllib import urlencode
import json

import pytest

import app

TEST_CASES = [
    
    {
        'path': '/timeline/',
        'url': 'https://cdn.knightlab.com/libs/timeline3/latest/embed/index.html?source=1xuY4upIooEeszZ_lCmeNx24eSFWe0rHe9ZdqH2xqVNk&font=Default&lang=en&initial_zoom=2&height=100%',
        'w': 700,
        'h': '100%' # app looks at URL to override params.
    },
    {
        'path': '/juxtapose/',
        'url': 'https://cdn.knightlab.com/libs/juxtapose/latest/embed/index.html?uid=b38faf7a-c341-11e6-bd02-0edaf8f81e27',
        'w': 700,
        'h': 500
    },
    {
        'path': '/timeline/',
        'url': 'https://cdn.knightlab.com/libs/timeline3/latest/embed/index.html?source=1xuY4upIooEeszZ_lCmeNx24eSFWe0rHe9ZdqH2xqVNk&font=Default&lang=en&initial_zoom=2',
        'w': 700,
        'h': 500 # if no height specified in URL
    },
    {
        'path': '/storymap/',
        'url': 'https://cdn.knightlab.com/libs/storymapjs/latest/embed/?url=https://uploads.knightlab.com/storymapjs/a1a349b51799ee49e96bed10cc235e7f/aryas-journey/published.json',
        'w': 700,
        'h': 700
    }
]




@pytest.fixture
def client():
    app.app.config['TESTING'] = True
    yield app.app.test_client()

def test_xml_unsupported(client):
    """XML format is not supported for any of ours."""
    for case in TEST_CASES:
        path = case['path']
        params = {
            'url': case['url'],
            'format': 'xml'
        }

        rv = client.get('{}?{}'.format(path, urlencode(params)))
        assert rv.status_code == 501

def test_unsupported_urls(client):
    paths = [x['path'] for x in TEST_CASES]
    urls = [x['url'] for x in TEST_CASES]
    urls.append(urls.pop(0)) # 'rotate' the list; it's possible that changes to TEST_VALUES would result in this not making a list of unsupported URLs but good for now

    for path, url in zip(paths, urls):
        params = {
            'url': url,
            'format': 'json'
        }

        rv = client.get('{}?{}'.format(path, urlencode(params)))
        assert rv.status_code == 404, "URLs which aren't appropriate for the endpoint path should be 404"

def test_missing_urls(client):
    for case in TEST_CASES:
        rv = client.get(case['path'])
        assert rv.status_code == 404, "If no URL is provided, should be 404"

def test_timeline_json(client):
    path = '/timeline/'
    for case in TEST_CASES:
        if case['path'] == path:
            params = {
                'url': case['url'],
                'format': 'json'
            }

            rv = client.get('{}?{}'.format(path, urlencode(params)))
            assert rv.status_code == 200, "response should be OK 200 for url [{}]".format(case['url'])
            j = json.loads(rv.data)
            assert j['type'] == 'rich', "response should be type 'rich'"
            assert 'html' in j 
            assert len(j['html']) > 0
            assert 'width' in j 
            assert j['width'] == case['w']
            assert 'height' in j 
            assert j['height'] == case['h']

def test_juxtapose_json(client):
    path = '/juxtapose/'
    for case in TEST_CASES:
        if case['path'] == path:
            params = {
                'url': case['url'],
                'format': 'json'
            }

            rv = client.get('{}?{}'.format(path, urlencode(params)))
            assert rv.status_code == 200
            j = json.loads(rv.data)
            assert j['type'] == 'rich'
            assert 'html' in j 
            assert len(j['html']) > 0
            assert 'width' in j 
            assert j['width'] == case['w']
            assert 'height' in j 
            assert j['height'] == case['h']

def test_storymap_json(client):
    """JSON format is supported."""
    path = '/storymap/'
    for case in TEST_CASES:
        if case['path'] == path:
            params = {
                'url': case['url'],
                'format': 'json'
            }

            rv = client.get('{}?{}'.format(path, urlencode(params)))
            assert rv.status_code == 200
            j = json.loads(rv.data)
            assert j['type'] == 'rich'
            assert 'html' in j 
            assert len(j['html']) > 0
            assert 'width' in j 
            assert j['width'] == case['w']
            assert 'height' in j 
            assert j['height'] == case['h']
