from flask import Flask
from flask_cors import CORS
from app.routes.url import url_bp
from app.routes.text import text_bp

app = Flask(__name__)
CORS(app)

# Register URL routes
app.register_blueprint(url_bp)
app.register_blueprint(text_bp)

if __name__ == "__main__":
    app.run(debug=True)