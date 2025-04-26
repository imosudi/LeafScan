import config
from app import app

if __name__ == '__main__':
    app.run(port=config.PORT, host=config.HOST, debug=config.DEBUG)