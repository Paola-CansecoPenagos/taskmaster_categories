from flask import Flask
from flask_cors import CORS
from infrastructure.routers.category_router import category_router

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(category_router)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
