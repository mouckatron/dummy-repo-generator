
import itertools
import unittest
import unittest.mock
import generator


class TestBranch(unittest.TestCase):

    def setUp(self):
        self.subject = generator.Branch(None, 'branch1', 'testwd')

    def test_init(self):
        assert self.subject.name == 'branch1'

    @unittest.mock.patch('subprocess.call')
    def test_create(self, subprocess_call):
        self.subject.create()

        subprocess_call.assert_called_with('git --git-dir testwd/.git --work-tree testwd branch branch1')

    @unittest.mock.patch('subprocess.call')
    def test_checkout(self, subprocess_call):
        self.subject.checkout()

        subprocess_call.assert_called_with('git --git-dir testwd/.git --work-tree testwd checkout branch1')


class TestBranchWithParentRepository(unittest.TestCase):

    def setUp(self):
        mock_parent_repository = unittest.mock.Mock()
        mock_parent_repository.next_commit_number = unittest.mock.Mock(side_effect=itertools.count(1))
        self.subject = generator.Branch(mock_parent_repository, 'branch1', 'testwd')

    @unittest.mock.patch('subprocess.call')
    def test_commit(self, subprocess_call):
        self.subject.commit()

        subprocess_call.assert_called_with('git --git-dir testwd/.git --work-tree testwd commit -m "branch1 generator commit 1"')

    @unittest.mock.patch('subprocess.call')
    def test_incrementing_commit_number(self, subprocess_call):

        self.subject.commit()
        self.subject.commit()

        subprocess_call.assert_called_with('git --git-dir testwd/.git --work-tree testwd commit -m "branch1 generator commit 2"')
