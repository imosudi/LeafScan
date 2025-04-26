import config
from app import app


if __name__ == '__main__':
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT, ssl_context=('./ssl_cert/cert.pem', './ssl_cert/key.pem'))

"""if __name__ == '__main__':
    app.run(port=config.PORT, host=config.HOST, debug=config.DEBUG)"""

