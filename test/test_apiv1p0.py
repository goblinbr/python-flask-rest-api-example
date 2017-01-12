import unittest

from run import app
from app import database
import json


class TestApiv1p0(unittest.TestCase):

    def setUp(self):
        self.server = app.test_client()
        database.clear()

    def test_get_todo_list(self):
        database.create_todo({'title': 'Buy ice cream'})
        database.create_todo({'title': 'Visit grandpa'})
        response = self.server.get('/api/v1.0/todo')
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
        database.create_todo({'title': 'Buy ice cream'})
        response = self.server.get('/api/v1.0/todo/1')
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data)
        self.assertEqual(1, data['id'])
        self.assertEqual('Buy ice cream', data['title'])
        self.assertEqual(False, data['done'])

    def test_get_todo_with_invalid_id(self):
        response = self.server.get('/api/v1.0/todo/12154')
        self.assertEqual(404, response.status_code)
        data = json.loads(response.data)
        self.assertEqual('Not found', data['error'])

    def test_create_todo(self):
        response = self.server.post('/api/v1.0/todo', data='{"title": "Test todo"}', content_type='application/json')
        self.assertEqual(201, response.status_code)
        data = json.loads(response.data)
        self.assertEqual(1, data['id'])
        self.assertEqual('Test todo', data['title'])
        self.assertEqual(False, data['done'])

        response = self.server.post('/api/v1.0/todo', data='{"title": "Test todo 2"}', content_type='application/json')
        self.assertEqual(201, response.status_code)
        data = json.loads(response.data)
        self.assertEqual(2, data['id'])
        self.assertEqual('Test todo 2', data['title'])
        self.assertEqual(False, data['done'])

    def test_create_todo_without_title(self):
        response = self.server.post('/api/v1.0/todo', data='{"titlex": "Test todo"}', content_type='application/json')
        self.assertEqual(400, response.status_code)
        data = json.loads(response.data)
        self.assertEqual('Title is a required field', data['error'])

    def test_create_todo_with_other_fields(self):
        response = self.server.post('/api/v1.0/todo', data='{"title": "Test todo", "answer": 42, "id": 5}', content_type='application/json')
        self.assertEqual(201, response.status_code)
        data = json.loads(response.data)
        self.assertEqual(1, data['id'])
        self.assertEqual('Test todo', data['title'])
        self.assertEqual(False, 'answer' in data)

if __name__ == '__main__':
    unittest.main()