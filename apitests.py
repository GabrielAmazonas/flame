from api import app
import unittest
import random
import string

class TestRegister(unittest.TestCase):

    def test_register(self):
        tester = app.test_client(self)
        
        login = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + '@gmail.com'
        password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

        response = tester.post('/register',json={ 'Email' : login, 'Password' : password})

        self.assertEquals(response.data, b'User registered.')

if __name__ == '__main__':
    unittest.main()