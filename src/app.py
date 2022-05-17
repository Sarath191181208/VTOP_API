# create a basic flask app

from distutils.log import debug
from flask import Flask
PORT = 5000
app = Flask(__name__)

import logging
from utils import c_print
logging.basicConfig(filename='flask_logs.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# logging.debug('Debugging')
# logging.info('Information')
# logging.warning('Warning')
# logging.error('Error')
# logging.critical('Critical')

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == "__main__":
    app.run(debug=True, port=PORT)