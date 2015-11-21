import sys, os

sys.path.append(os.getcwd())

import ConfigParser
cp = ConfigParser.ConfigParser();
cp.read('../.environ')
os.environ.update({key.upper():value for key, value in cp.items('env')}) 
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
