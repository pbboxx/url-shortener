
import unittest
from app import app, db



class BasicTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/urls.db'
        db.drop_all()
        db.create_all()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass


    def test_home_page(self):
        """
        Test the accessbility of the home page
        :return:  200
        """
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_encodage(self):
        """
        Test the encodage when an url is submitted :return 200
        Test the decodage when a url shortening is submit :return 302
        Test non existant  url :return 404
        """
        url = 'https://moneypark.ch/'
        response = self.app.post('/',data=url, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_2 = self.app.get('/cjFl_Q',)
        self.assertEqual(response_2.status_code, 302)

        response_3 = self.app.get('/cjFl',)
        self.assertEqual(response_3.status_code, 404)




if __name__ == "__main__":
    unittest.main()