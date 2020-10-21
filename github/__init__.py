#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from auxillary.test_github_api import get_github_repo, get_github_file


class Repository:
    GH_URL = 'https://api.github.com'
    def __init__(self, owner, name):
        self.owner = owner
        self.name = name
        self.files = []
        self.fetch()


    def fetch(self):
        """Update list of files in a repository"""
        content = get_github_repo(self.owner, self.name)
        for file in content:
            if file["size"] and file["path"] not in self.files:
                self.files.append(file["path"])


    def get_file_content(self, path):
        """Return utf-8 encoded file content"""
        if path not in self.files:
            raise Exception("No such file in a repository")
        return get_github_file(self.owner, self.name, path)
