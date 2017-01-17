from app.exceptions import *
from app.token import generate_new_token
import datetime


class DB(object):
    rows = []
    last_id = 0
    def __init__(self,fields):
        self.fields = fields
    def clear(self):
        self.rows = []
        self.last_id = 0
    def create(self,obj):
        obj = {k: v for k, v in obj.items() if k in self.fields}
        self.last_id += 1
        obj['id'] = self.last_id
        self.rows.append(obj)
        return obj


__todo_db = DB(['title', 'done'])
__user_db = DB(['name', 'token'])


def clear():
    global __todo_db
    global __user_db
    __todo_db.clear()
    __user_db.clear()


def get_todo_list():
    global __todo_db
    return __todo_db.rows


def get_todo(todo_id=0):
    global __todo_db
    lst = [t for t in __todo_db.rows if t['id'] == todo_id]
    return lst[0] if len(lst) > 0 else None


def create_todo(todo):
    global __todo_db
    if 'title' not in todo:
        raise DatabaseValidationException('Title is a required field')
    todo['done'] = False
    todo = __todo_db.create(todo)
    return todo


def update_todo(todo_id, todo):
    global __todo_fields
    db_todo = get_todo(todo_id)
    if db_todo is not None:
        for field in __todo_db.fields:
            if field != 'id' and field in todo:
                db_todo[field] = todo[field]
    return db_todo


def delete_todo(todo_id):
    global __todo_db
    db_todo = get_todo(todo_id)
    if db_todo is not None:
        __todo_db.rows.remove(db_todo)
    return db_todo


def create_user(user):
    global __user_db
    if 'name' not in user:
        raise DatabaseValidationException('Name is a required field')
    user['token'] = generate_new_token({'user': user['name'], 'date' : str(datetime.datetime.now())})
    user = __user_db.create(user)
    return user


def get_user(user_id=0,token=''):
    global __user_db
    lst = []
    if user_id > 0:
        lst = [t for t in __user_db.rows if t['id'] == user_id]
    else:
        lst = [t for t in __user_db.rows if t['token'] == token]
    return lst[0] if len(lst) > 0 else None
