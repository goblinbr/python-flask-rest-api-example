from flask import Flask, make_response
from app import api_v1p0

app = Flask(__name__)
app.register_blueprint(api_v1p0.blueprint)


@app.errorhandler(404)
def not_found(error):
    return make_response('{"error": "Not found"}', 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response('{"error": "%s"}' % error.description, 400)

if __name__ == '__main__':
    app.run(debug=True)