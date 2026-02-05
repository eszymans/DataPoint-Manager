import unittest
import requests
import threading
import time
import os
from app import app, db
from app.models import DataPoint


class TestAPISpecification(unittest.TestCase):
    PORT = 5002
    BASE_URL = f"http://127.0.0.1:5002/api/data"

    TEST_DB_FILE = 'test_api.db'

    @classmethod
    def setUpClass(cls):

        basedir = os.path.abspath(os.path.dirname(__file__))
        cls.db_path = os.path.join(basedir, cls.TEST_DB_FILE)

        app.config[
            'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + cls.db_path
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        with app.app_context():
            db.create_all()

        cls.server_thread = threading.Thread(
            target=app.run,
            kwargs={'port': cls.PORT, 'use_reloader': False}
        )
        cls.server_thread.daemon = True
        cls.server_thread.start()

        time.sleep(1.5)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.db_path):
            try:
                os.remove(cls.db_path)
            except PermissionError:
                pass

    def setUp(self):
        with app.app_context():
            db.session.query(DataPoint).delete()
            db.session.commit()

    def test_get_all_data(self):
        with app.app_context():
            p = DataPoint(weight=60.5, height=170.0, category=1)
            db.session.add(p)
            db.session.commit()

        response = requests.get(self.BASE_URL)

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertIsInstance(data, list, "Response must be a list")
        self.assertGreater(len(data), 0, "List should not be empty")
        self.assertIsInstance(data[0], dict,
                              "List elements must be dictionaries")
        self.assertEqual(data[0]['weight'], 60.5)

    def test_post_data_success(self):

        payload = {
            "weight": 80.0,
            "height": 180.0,
            "category": 2
        }

        response = requests.post(self.BASE_URL, json=payload)

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertIsInstance(data, dict)
        self.assertIn('id', data,
                      "Response must contain 'id' key (primary key)")
        self.assertIsInstance(data['id'], int)

    def test_post_data_validation_failure(self):
        invalid_payload = {
            "weight": 80.0,
            "height": 180.0
        }

        response = requests.post(self.BASE_URL, json=invalid_payload)

        self.assertEqual(response.status_code, 400)
        data = response.json()

        self.assertIsInstance(data, dict)
        self.assertIn('error', data,
                      "Error response must contain 'error' key")

    def test_delete_data_success(self):
        with app.app_context():
            p = DataPoint(weight=90.0, height=190.0, category=3)
            db.session.add(p)
            db.session.commit()
            record_id = p.id

        delete_url = f"{self.BASE_URL}/{record_id}"
        response = requests.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertIsInstance(data, dict)
        self.assertIn('deleted_id', data)
        self.assertEqual(data['deleted_id'], record_id)

    def test_delete_data_not_found(self):
        non_existent_id = 999999
        delete_url = f"{self.BASE_URL}/{non_existent_id}"

        response = requests.delete(delete_url)

        self.assertEqual(response.status_code, 404)
        data = response.json()

        self.assertIsInstance(data, dict)
        self.assertIn('error', data)
        self.assertEqual(data['error'], "Record not found")


if __name__ == '__main__':
    unittest.main()
