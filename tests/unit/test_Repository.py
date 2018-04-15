
import unittest
import unittest.mock
import generator


class TestRepository(unittest.TestCase):

    @unittest.mock.patch('subprocess.call')
    def test_repo_name(self, subprocess_call):

        generator.Repository('test_repo_name')

        subprocess_call.assert_called_with('git init test_repo_name')
