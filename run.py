from flask import Flask
from app import api_v1p0

app = Flask(__name__)
app.register_blueprint(api_v1p0.blueprint)

if __name__ == '__main__':
    app.run(debug=True)