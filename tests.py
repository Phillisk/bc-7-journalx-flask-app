import os
from app.mod_auth import controllers
import unittest
import tempfile

class JournalxTestCase(unittest.TestCase):

    def setUp(self):
    	#creates a new test client and initializes a new database
        self.db_fd, controllers.app.config['DATABASE'] = tempfile.mkstemp()
        controllers.app.config['TESTING'] = True
        self.app = controllers.app.test_client()
        controllers.init_db()

    def tearDown(self):
    	#delete the database after the test, we close the file and remove it from the filesystem
        os.close(self.db_fd)
        os.unlink(controllers.app.config['DATABASE'])

    def test_empty_db(self):
    	#Tests empty database
        rv = self.app.get('/')
        assert 'No entries here so far' in rv.data

    def login(self, username, password):
    	return self.app.post('/login', data=dict(
        					username=username,
        					password=password
    						), follow_redirects=True)

	def logout(self):
		return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
	    rv = self.login('admin', 'default')
	    assert 'You were logged in' in rv.data
	    rv = self.logout()
	    assert 'You were logged out' in rv.data
	    rv = self.login('adminx', 'default')
	    assert 'Invalid username' in rv.data
	    rv = self.login('admin', 'defaultx')
	    assert 'Invalid password' in rv.data


if __name__ == '__main__':
    unittest.main()