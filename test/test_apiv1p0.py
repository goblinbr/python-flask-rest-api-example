import unittest

from run import app
from app import database
import json


class TestApiv1p0(unittest.TestCase):

    def setUp(self):
        self.server = app.test_client()
        database.clear()
        self.user1 = database.create_user({'name': 'new user 1'})
        self.user2 = database.create_user({'name': 'new user 2'})
        self.headers_user1 = {'Authorization' : 'token %s' % self.user1['token']}
        self.headers_user2 = {'Authorization': 'token %s' % self.user2['token']}

    def test_get_todo_list(self):
        database.create_todo(self.user1, {'title': 'Buy ice cream'})
        database.create_todo(self.user1, {'title': 'Visit grandpa'})
        database.create_todo(self.user2, {'title': 'Watch star wars'})
        response = self.server.get('/api/v1.0/todo', headers=self.headers_user1)
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data)
        self.assertEqual(2, len(data))
        self.assertEqual(1, data[0]['id'])
        self.assertEqual('Buy ice cream', data[0]['title'])
        self.assertEqual(False, data[0]['done'])
        self.assertEqual(2, data[1]['id'])
        self.assertEqual('Visit grandpa', data[1]['title'])
        self.assertEqual(False, data[1]['done'])

    def test_get_todo(self):
        todo = database.create_todo(self.user1, {'title': 'Buy ice cream'})
        response = self.server.get('/api/v1.0/todo/%s' % todo['id'], headers=self.headers_user1)
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data)
        self.assertEqual(1, data['id'])
        self.assertEqual('Buy ice cream', data['title'])
        self.assertEqual(False, data['done'])

    def test_get_todo_with_invalid_id(self):
        response = self.server.get('/api/v1.0/todo/12154', headers=self.headers_user1)
        self.assertEqual(404, response.status_code)
        data = json.loads(response.data)
        self.assertEqual('Todo 12154 not found', data['error'])

    def test_get_todo_from_another_user(self):
        todo = database.create_todo(self.user2, {'title': 'Buy ice cream'})
        response = self.server.get('/api/v1.0/todo/%s' % todo['id'], headers=self.headers_user1)
        self.assertEqual(404, response.status_code)
        data = json.loads(response.data)
        self.assertEqual('Todo %s not found' % todo['id'], data['error'])

    def test_create_todo(self):
        response = self.server.post('/api/v1.0/todo', data='{"title": "Test todo"}', content_type='application/json', headers=self.headers_user1)
        self.assertEqual(201, response.status_code)
        data = json.loads(response.data)
        self.assertEqual(1, data['id'])
        self.assertEqual('Test todo', data['title'])
        self.assertEqual(False, data['done'])
        self.assertEqual(self.user1['id'], data['user_id'])

        response = self.server.post('/api/v1.0/todo', data='{"title": "Test todo 2"}', content_type='application/json', headers=self.headers_user1)
        self.assertEqual(201, response.status_code)
        data = json.loads(response.data)
        self.assertEqual(2, data['id'])
        self.assertEqual('Test todo 2', data['title'])
        self.assertEqual(False, data['done'])

    def test_create_todo_without_title(self):
        response = self.server.post('/api/v1.0/todo', data='{"titlex": "Test todo"}', content_type='application/json', headers=self.headers_user1)
        self.assertEqual(400, response.status_code)
        data = json.loads(response.data)
        self.assertEqual('Title is a required field', data['error'])

    def test_create_todo_with_other_fields(self):
        response = self.server.post('/api/v1.0/todo', data='{"title": "Test todo", "answer": 42, "id": 5}', content_type='application/json', headers=self.headers_user1)
        self.assertEqual(201, response.status_code)
        data = json.loads(response.data)
        self.assertEqual(1, data['id'])
        self.assertEqual('Test todo', data['title'])
        self.assertEqual(False, 'answer' in data)

    def test_create_with_invalid_json(self):
        response = self.server.post('/api/v1.0/todo', data='{jovemnerd.com.br}', headers=self.headers_user1)
        self.assertEqual(400, response.status_code)
        data = json.loads(response.data)
        self.assertEqual('No JSON found', data['error'])

    def test_update_todo(self):
        created_todo = database.create_todo(self.user1, {"title": "Test todo"})
        response = self.server.put('/api/v1.0/todo/%s' % created_todo['id'], data='{"title": "Renamed todo", "done": true}', content_type='application/json', headers=self.headers_user1)
        self.assertEqual(201, response.status_code)
        data = json.loads(response.data)
        self.assertEqual(created_todo['id'], data['id'])
        self.assertEqual('Renamed todo', data['title'])
        self.assertEqual(True, data['done'])

        todo = database.get_todo(self.user1, created_todo['id'])
        self.assertEqual('Renamed todo', todo['title'])
        self.assertEqual(True, todo['done'])

    def test_update_todo_with_invalid_id(self):
        response = self.server.put('/api/v1.0/todo/213', data='{"title": "Renamed todo"}', content_type='application/json', headers=self.headers_user1)
        self.assertEqual(404, response.status_code)
        data = json.loads(response.data)
        self.assertEqual('Todo 213 not found', data['error'])

    def test_update_todo_with_other_fields(self):
        created_todo = database.create_todo(self.user1, {"title": "Test todo"})
        response = self.server.put('/api/v1.0/todo/%s' % created_todo['id'], data='{"title": "Renamed todo", "answer": 42, "id": 55}', content_type='application/json', headers=self.headers_user1)
        self.assertEqual(201, response.status_code)
        data = json.loads(response.data)
        self.assertEqual(created_todo['id'], data['id'])
        self.assertEqual('Renamed todo', data['title'])
        self.assertEqual(False, 'answer' in data)

    def test_update_with_invalid_json(self):
        response = self.server.post('/api/v1.0/todo', data='{jovemnerd.com.br}', headers=self.headers_user1)
        self.assertEqual(400, response.status_code)
        data = json.loads(response.data)
        self.assertEqual('No JSON found', data['error'])

    def test_update_todo_from_another_user(self):
        created_todo = database.create_todo(self.user2, {"title": "Test todo"})
        response = self.server.put('/api/v1.0/todo/%s' % created_todo['id'], data='{"title": "Renamed todo", "done": true}', content_type='application/json', headers=self.headers_user1)
        self.assertEqual(404, response.status_code)
        data = json.loads(response.data)
        self.assertEqual('Todo %s not found' % created_todo['id'], data['error'])

    def test_delete_todo(self):
        created_todo = database.create_todo(self.user1, {"title": "Test todo"})
        response = self.server.delete('/api/v1.0/todo/%s' % created_todo['id'], headers=self.headers_user1)
        self.assertEqual(201, response.status_code)
        data = json.loads(response.data)
        self.assertEqual(created_todo['id'], data['id'])
        self.assertEqual('Test todo', data['title'])
        self.assertEqual(False, data['done'])

        todo = database.get_todo(self.user1, created_todo['id'])
        self.assertEqual(True, todo is None)

    def test_delete_todo_with_invalid_id(self):
        response = self.server.delete('/api/v1.0/todo/555', headers=self.headers_user1)
        self.assertEqual(404, response.status_code)
        data = json.loads(response.data)
        self.assertEqual('Todo 555 not found', data['error'])

    def test_delete_todo_from_another_user(self):
        created_todo = database.create_todo(self.user2, {"title": "Test todo"})
        response = self.server.delete('/api/v1.0/todo/%s' % created_todo['id'], headers=self.headers_user1)
        self.assertEqual(404, response.status_code)
        data = json.loads(response.data)
        self.assertEqual('Todo %s not found' % created_todo['id'], data['error'])

    def test_create_user(self):
        response = self.server.post('/api/v1.0/user', data='{"name": "new user"}', content_type='application/json')
        self.assertEqual(201, response.status_code)
        user = json.loads(response.data)
        self.assertEqual('new user', user['name'])

        response = self.server.post('/api/v1.0/todo?token=%s' % user['token'], data='{"title": "Test todo"}', content_type='application/json')
        self.assertEqual(201, response.status_code)
        data = json.loads(response.data)

        response = self.server.get('/api/v1.0/todo?token=%s' % user['token'])
        self.assertEqual(200, response.status_code)
        todos = json.loads(response.data)
        self.assertEqual(1, len(todos))

    def test_calls_to_invalid_routes(self):
        response = self.server.get('/api/v1.0/banana', headers=self.headers_user1)
        self.assertEqual(404, response.status_code)
        data = json.loads(response.data)
        self.assertEqual('Not found', data['error'])

        response = self.server.post('/api/v1.0/banana', data='{"title": "Test"}', headers=self.headers_user1)
        self.assertEqual(404, response.status_code)
        data = json.loads(response.data)
        self.assertEqual('Not found', data['error'])

        response = self.server.put('/api/v1.0/banana/1', data='{"title": "Test"}', headers=self.headers_user1)
        self.assertEqual(404, response.status_code)
        data = json.loads(response.data)
        self.assertEqual('Not found', data['error'])

        response = self.server.delete('/api/v1.0/banana/1', headers=self.headers_user1)
        self.assertEqual(404, response.status_code)
        data = json.loads(response.data)
        self.assertEqual('Not found', data['error'])

    def test_without_token(self):
        created_todo = database.create_todo(self.user1, {"title": "Test todo"})
        response = self.server.get('/api/v1.0/todo')
        self.assertEqual(401, response.status_code)

        response = self.server.get('/api/v1.0/todo/%s' % created_todo['id'])
        self.assertEqual(401, response.status_code)

        response = self.server.post('/api/v1.0/todo', data='{"title": "Test todo"}', content_type='application/json')
        self.assertEqual(401, response.status_code)

        response = self.server.put('/api/v1.0/todo/%s' % created_todo['id'], data='{"title": "Renamed todo", "done": true}', content_type='application/json')
        self.assertEqual(401, response.status_code)

        response = self.server.delete('/api/v1.0/todo/%s' % created_todo['id'])
        self.assertEqual(401, response.status_code)

    def test_calls_with_invalid_token(self):
        headers = {'Authorization' : 'token not-a-valid-token'}

        created_todo = database.create_todo(self.user1, {"title": "Test todo"})
        response = self.server.get('/api/v1.0/todo', headers=headers)
        self.assertEqual(401, response.status_code)

        response = self.server.get('/api/v1.0/todo/%s' % created_todo['id'], headers=headers)
        self.assertEqual(401, response.status_code)

        response = self.server.post('/api/v1.0/todo', data='{"title": "Test todo"}', content_type='application/json', headers=headers)
        self.assertEqual(401, response.status_code)

        response = self.server.put('/api/v1.0/todo/%s' % created_todo['id'], data='{"title": "Renamed todo", "done": true}', content_type='application/json', headers=headers)
        self.assertEqual(401, response.status_code)

        response = self.server.delete('/api/v1.0/todo/%s' % created_todo['id'], headers=headers)
        self.assertEqual(401, response.status_code)

    def test_calls_with_user_token_as_url_param(self):
        response = self.server.post('/api/v1.0/todo?token=%s' % self.user1['token'], data='{"title": "Test todo"}', content_type='application/json')
        self.assertEqual(201, response.status_code)
        created_todo = data = json.loads(response.data)

        response = self.server.get('/api/v1.0/todo/%s?token=%s' % (created_todo['id'], self.user1['token']))
        self.assertEqual(200, response.status_code)

        response = self.server.put('/api/v1.0/todo/%s?token=%s' % (created_todo['id'], self.user1['token']), data='{"title": "Renamed test todo"}', content_type='application/json')
        self.assertEqual(201, response.status_code)

        response = self.server.delete('/api/v1.0/todo/%s?token=%s' % (created_todo['id'], self.user1['token']))
        self.assertEqual(201, response.status_code)


if __name__ == '__main__':
    unittest.main()
