#!/usr/bin/env python
"""Operations with github API"""

import base64
import json
import requests


GH_URL = 'https://api.github.com'


def get_github_repo(user, repo):
    """Return user/repo content in a python list of dictionaries."""

    url = GH_URL+"/repos/{user}/{repo}/contents".format(user=user, repo=repo)
    try:
        req = requests.get(url)
        req.raise_for_status()    # raise HTTPError on non 200 code
    except requests.exceptions.RequestException as err:
        #TODO correct error handling
        print(err)
        return []
    return req.json()

def get_github_file(user,repo,path):
    """Return user/repo/file content."""
    url = GH_URL+"/repos/{user}/{repo}/contents/{path}".format(
            user=user, repo=repo, path=path)
    try:
        req = requests.get(url)
        req.raise_for_status()    # raise HTTPError on non 200 code
    except requests.exceptions.RequestException as err:
        #TODO correct error handling
        print(err)
        return ""
    return base64.b64decode(req.json()['content'] )



if __name__ == "__main__":
    repo_content = get_github_repo("keder", "todogit")
    for file in repo_content:
        print (json.dumps(file, indent=4))
        print ("Content of file:")
        if file["size"]:
            print (get_github_file("keder","todogit",file["path"]))

