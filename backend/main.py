from flask import Flask
from flask_cors import CORS
from routes.bot_routes import bot_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(bot_bp, url_prefix='/bot')

if __name__ == '__main__':
    app.run(port=5000, debug=True)