#!/usr/bin/env python
"""Operations with github API"""

import json
import requests


GH_URL = 'https://api.github.com'


def get_github_repo(user, repo):
    """Return user/repo content in a python list of dictionaries."""

    url = GH_URL+"/repos/%s/%s/contents" % (user,repo)
    try:
        req = requests.get(url)
        req.raise_for_status()    # raise HTTPError on non 200 code
    except requests.exceptions.RequestException as err:
        #TODO correct error handling
        print(err)
        return []
    return req.json()

if __name__ == "__main__":
    repo_content = get_github_repo("keder", "todogit")
    for file in repo_content:
        print (json.dumps(file, indent=4))
