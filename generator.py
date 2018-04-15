# -*- coding: utf-8 -*-

import itertools
import os.path
import random
import string
import subprocess
import sys


class Repository(object):

    def __init__(self, repo_name):
        self.repo_name = repo_name
        self.branches = {}
        self.__next_commit_number = itertools.count(1)
        subprocess.call('git init {}'.format(repo_name), shell=True)

    def new_branch(self, branch_name):
        self.branches[branch_name] = Branch(self, branch_name, self.repo_name)

    def next_commit_number(self):
        return next(self.__next_commit_number)


class Branch(object):

    def __init__(self, parent_repository, name, wd):
        self.name = name
        self.wd = wd
        self.parent_repository = parent_repository

    def create(self):
        subprocess.call('git --git-dir {wd}/.git --work-tree {wd} branch {name}'.format(
            wd=self.wd, name=self.name), shell=True)

    def checkout(self):
        subprocess.call('git --git-dir {wd}/.git --work-tree {wd} checkout {name}'.format(
            wd=self.wd, name=self.name), shell=True)

    def commit(self):
        subprocess.call('git --git-dir {wd}/.git --work-tree {wd} add -A'.format(
            wd=self.wd), shell=True)
        subprocess.call('git --git-dir {wd}/.git --work-tree {wd} commit -m "{name} generator commit {id}"'.format(
            wd=self.wd, name=self.name, id=self.parent_repository.next_commit_number()), shell=True)


class FilesAndDirectories(object):

    def __init__(self, wd):
        self.wd = wd

    def create_file(self):
        with open(os.path.join(self.wd, self.generate_name()), 'w') as f:
            f.write(self.generate_words())

    def create_directory(self):
        pass

    def generate_name(self):
        return ''.join(random.choice(string.ascii_letters) for _ in range(10))

    def generate_words(self):
        return ' '.join([self.generate_name() for _ in range(random.randint(20, 30))])


if __name__ == '__main__':

    files = 3
    directories = 1
    commits = 6

    if '--files' in sys.argv:
        files = sys.argv[sys.argv.index('--files')+1]

    if '--directories' in sys.argv:
        directories = sys.argv[sys.argv.index('--directories')+1]

#    if '--branches' in sys.argv:
#        branches = sys.argv[sys.argv.index('--branches')+1]

    fad = FilesAndDirectories(sys.argv[1])
    repo = Repository(sys.argv[1])
    repo.new_branch('master')
    print(repo.branches)
    repo.branches['master'].create()

    for x in range(commits):
        fad.create_file()
        repo.branches['master'].commit()
