from flask import Blueprint, jsonify, abort
from app import database

blueprint = Blueprint(name='api_v1p0', import_name=__name__, url_prefix="/api/v1.0", template_folder='templates')


@blueprint.route('/todo', methods=['GET'])
def get_todo_list():
    return jsonify(database.get_todo_list())


@blueprint.route('/todo/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = database.get_todo(todo_id)
    if todo is None:
        abort(404)
    else:
        return jsonify(todo)
