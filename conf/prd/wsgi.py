import os
import site
import sys

site.addsitedir('/home/apps/env/oembed-server/lib/python2.7/site-packages')
sys.path.append('/home/apps/sites/oembed-server')
sys.stdout = sys.stderr

from app import app as application
