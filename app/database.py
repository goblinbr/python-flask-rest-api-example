from app.exceptions import *

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
    lst = [t for t in __todo_list if t['id'] == todo_id]
    return lst[0] if len(lst) > 0 else None


def create_todo(todo):
    global __last_id
    global __todo_fields
    global __todo_list
    if 'title' not in todo:
        raise DatabaseValidationException('Title is a required field')
    todo = {k: v for k, v in todo.items() if k in __todo_fields}
    __last_id += 1
    todo['id'] = __last_id
    todo['done'] = False
    __todo_list.append(todo)
    return todo


def update_todo(todo_id, todo):
    global __todo_fields
    db_todo = get_todo(todo_id)
    if db_todo is not None:
        for field in __todo_fields:
            if field != 'id' and field in todo:
                db_todo[field] = todo[field]
    return db_todo


def delete_todo(todo_id):
    global __todo_list
    db_todo = get_todo(todo_id)
    if db_todo is not None:
        __todo_list.remove(db_todo)
    return db_todo
