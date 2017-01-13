from flask import Blueprint, jsonify, request
from app import database
from app.exceptions import NotFoundException, NoJsonException

blueprint = Blueprint(name='api_v1p0', import_name=__name__, url_prefix="/api/v1.0", template_folder='templates')


def validate_json(json):
    if not json or not hasattr(json, 'items'):
        raise NoJsonException()


@blueprint.route('/todo', methods=['GET'])
def get_todo_list():
    return jsonify(database.get_todo_list())


@blueprint.route('/todo/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = database.get_todo(todo_id)
    if todo is None:
        raise NotFoundException('Todo %s not found' % todo_id)
    else:
        return jsonify(todo)


@blueprint.route('/todo', methods=['POST'])
def create_todo():
    validate_json(request.json)
    todo = database.create_todo(request.json)
    return jsonify(todo), 201


@blueprint.route('/todo/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    validate_json(request.json)
    todo = database.update_todo(todo_id, request.json)
    if todo is None:
        raise NotFoundException('Todo %s not found' % todo_id)
    else:
        return jsonify(todo), 201


@blueprint.route('/todo/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = database.delete_todo(todo_id)
    if todo is None:
        raise NotFoundException('Todo %s not found' % todo_id)
    else:
        return jsonify(todo), 201
