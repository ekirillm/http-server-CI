import json
import requests
import unittest


class TestSet(unittest.TestCase):

    def test_simple_put(self):
        msg = {"message":"aaa"}
        r = requests.post('http://127.0.0.1:2000/1', data=json.dumps(msg), headers={'Content-Type': 'application/json'})
        self.assertTrue(r.text == 'Created' or r.text == 'Ok')

    def test_simple_get(self):
        msg = {"message":"bbb"}
        r = requests.post('http://127.0.0.1:2000/1', data=json.dumps(msg), headers={'Content-Type': 'application/json'})
        r = requests.get('http://127.0.0.1:2000/1')
        self.assertEqual(r.json(), msg)

    def test_simple_delete(self):
        msg = {"message":"bbb"}
        r = requests.post('http://127.0.0.1:2000/1', data=json.dumps(msg), headers={'Content-Type': 'application/json'})
        r = requests.delete('http://127.0.0.1:2000/1')
        self.assertEqual(r.text, 'Ok')


if __name__ == '__main__':
    unittest.main()

