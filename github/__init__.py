#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tempfile
import git


GH_URL = 'https://github.com'


class Repository:
    def __init__(self, owner, repo_name):
        self.owner = owner
        self.repo_name = repo_name
        self.url = GH_URL + "/{owner}/{repo_name}.git".format(
            owner=self.owner,
            repo_name=self.repo_name)
        self.dir = None
        self.clone()

    def clone(self):
        """Clone github repository to a temporary dir"""
        if self.dir:
            pass
            # TODO update repo
        else:
            self.dir = tempfile.mkdtemp()
            git.Git(self.dir).clone(self.url, "--bare")
            self.dir = os.path.join(self.dir, self.repo_name + ".git")

    def get_file_content(self, filepath, branch="master"):
        """Return file content"""
        try:
            content = git.Git(
                self.dir).show(
                "{branch}:{filepath}".format(
                    branch=branch,
                    filepath=filepath))

        except BaseException:
            pass
            # TODO idk how to handle this exception
        return content


if __name__ == "__main__":
    rep = Repository("keder", "todogit")
    print(rep.dir)
    print(rep.get_file_content("README.md"))
