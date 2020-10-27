#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from tempfile import mkdtemp
from git import Git


GH_URL = 'https://github.com'


class Repository:
    def __init__(self, owner, repo_name):
        self.owner = owner
        self.repo_name = repo_name
        self.dir = None
        self._repo = None
        self.clone()

    @property
    def url(self):
        return GH_URL + "/{0.owner}/{0.repo_name}.git".format(self)

    @property
    def git_dir(self):
        if self._repo is None:
            self._repo = Git(self.dir)
        return self._repo

    def clone(self):
        """Clone github repository to a temporary dir"""
        if self.dir:
            pass
            # TODO update repo
        else:
            tmp_dir = mkdtemp()
            Git(tmp_dir).clone(self.url, "--bare")  # It's not a _repo !!!
            self.dir = os.path.join(tmp_dir, self.repo_name+".git")

    def get_file_content(self, filepath, branch="master"):
        """Return file content"""
        try:
            filename = "{}:{}".format(branch, filepath)
            content = self.git_dir.show(filename)
        except BaseException:
            pass
            # TODO idk how to handle this exception
        return content


if __name__ == "__main__":
    rep = Repository("keder", "todogit")
    print(rep.dir)
    print(rep.url)
    print(rep.get_file_content("README.md"))
