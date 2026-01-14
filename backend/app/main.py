from flask import Flask
from flask_cors import CORS
from app.routes.url import url_bp
from app.routes.text import text_bp

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    
    # Register URL routes
    app.register_blueprint(url_bp)
    app.register_blueprint(text_bp)
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)