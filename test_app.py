import unittest
import json
from app import app

class WellnessAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SESSION_TYPE'] = 'filesystem'
        self.app = app.test_client()
        self.app.secret_key = 'test-secret'

    def test_login_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_registration(self):
        response = self.app.post('/register', data={
            'name': 'Test User',
            'age': '25',
            'screen_time': '2.5',
            'avatar_id': '1'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'WELLNESS QUEST', response.data)

    def test_complete_task(self):
        # First register
        self.app.post('/register', data={
            'name': 'Test User',
            'age': '25',
            'screen_time': '2.5',
            'avatar_id': '1'
        })
        
        # Complete task
        response = self.app.post('/complete_task', 
                                data=json.dumps({'task_id': 1, 'duration': 30}),
                                content_type='application/json')
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['points'], 60) # 30 * 2

    def test_avatar_unlock(self):
        self.app.post('/register', data={
            'name': 'Test User',
            'age': '25',
            'screen_time': '2.5',
            'avatar_id': '1'
        })
        
        # Earn enough points to unlock next avatar (50 points)
        self.app.post('/complete_task', 
                      data=json.dumps({'task_id': 1, 'duration': 25}),
                      content_type='application/json')
        
        # Check if avatar 4 is unlocked via /change_avatar
        response = self.app.post('/change_avatar',
                                data=json.dumps({'avatar_id': 4}),
                                content_type='application/json')
        data = json.loads(response.data)
        self.assertTrue(data['success'])

if __name__ == '__main__':
    unittest.main()
