from flask import Flask, make_response
from app import api_v1p0
from app.exceptions import *

app = Flask(__name__)
app.register_blueprint(api_v1p0.blueprint)


@app.errorhandler(NotFoundException)
@app.errorhandler(404)
def not_found(error):
    msg = error.msg if hasattr(error, 'msg') else 'Not found'
    return make_response('{"error": "%s"}' % msg, 404)


@app.errorhandler(DatabaseValidationException)
@app.errorhandler(NoJsonException)
@app.errorhandler(400)
def bad_request(error):
    msg = error.msg if hasattr(error, 'msg') else 'Bad request'
    return make_response('{"error": "%s"}' % msg, 400)


if __name__ == '__main__':
    app.run(debug=True)