__todo_list = [
    {
        'id': 1,
        'title': 'Buy ice cream',
        'done': False
    },
    {
        'id': 2,
        'title': 'Visit grandpa',
        'done': False
    }
]

lastId = 1 if len(__todo_list) < 1 else __todo_list[-1]['id'];


def get_todo_list():
    return __todo_list;


def get_todo(todo_id=0):
    todos = [t for t in __todo_list if t['id'] == todo_id];
    return todos[0] if len(todos) > 0 else None
