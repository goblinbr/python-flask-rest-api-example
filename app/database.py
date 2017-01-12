__todo_list = []
__last_id = 0 if len(__todo_list) < 1 else __todo_list[-1]['id']
__todo_fields = ['id', 'title', 'done']


def clear():
    global __todo_list
    global __last_id
    __todo_list = []
    __last_id = 0


def get_todo_list():
    global __todo_list
    return __todo_list


def get_todo(todo_id=0):
    global __todo_list
    todos = [t for t in __todo_list if t['id'] == todo_id]
    return todos[0] if len(todos) > 0 else None


def create_todo(todo):
    global __last_id
    global __todo_fields
    if 'title' not in todo:
        raise ValueError('Title is a required field')
    todo = {k: v for k, v in todo.items() if k in __todo_fields}
    __last_id += 1
    todo['id'] = __last_id
    todo['done'] = False
    __todo_list.append(todo)
    return todo