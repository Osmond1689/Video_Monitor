from flask import Flask
import logging

app = Flask(__name__)


@app.route('/')
def root():
    app.logger.info('info log')
    app.logger.warning('warning log')
    return 'hello'

if __name__ == '__main__':
    app.debug = True
    handler = logging.FileHandler('flask.log')
    app.logger.addHandler(handler)
    app.run(debug=True, port=8080, host='0.0.0.0')