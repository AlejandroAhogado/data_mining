import json
import requests
from pandas.io.json import json_normalize
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, engine, text, types, MetaData, Table, String
from datetime import datetime
import config
import os 

# API URL
github_api = "https://api.github.com"
github_repo = ""

# Create a session
github_session = requests.Session()
github_session.auth = (config.gh_user, config.gh_token)

# Get the branches
def branches_of_repo(repo, owner, api):
    branches = []
    next = True
    i = 0
    while next == True:
        url = api + '/repos/{}/{}/branches?page={}&per_page=100'.format(owner, repo, i)
        branch_pg =  github_session.get(url = url)
        branch_pg_list = [dict(item, **{'repo_name':'{}'.format(repo)}) for item in branch_pg.json()]    
        branch_pg_list = [dict(item, **{'owner':'{}'.format(owner)}) for item in branch_pg_list]
        branches = branches + branch_pg_list
        if 'Link' in branch_pg.headers:
            if 'rel="next"' not in branch_pg.headers['Link']:
                next = False
        i = i + 1
    return branches

branches = json_normalize(branches_of_repo('DeepSpeed', 'microsoft', github_api))
branches.to_csv('data/branches.csv')

# Get the commits
def commits_of_repo(repo, owner, api):
    commits = []
    next = True
    i = 0
    while next == True:
        url = api + '/repos/{}/{}/commits?page={}&per_page=100'.format(owner, repo, i)
        commit_pg =  github_session.get(url = url)
        commit_pg_list = [dict(item, **{'repo_name':'{}'.format(repo)}) for item in commit_pg.json()]    
        commit_pg_list = [dict(item, **{'owner':'{}'.format(owner)}) for item in commit_pg_list]
        commits = commits + commit_pg_list
        if 'Link' in commit_pg.headers:
            if 'rel="next"' not in commit_pg.headers['Link']:
                next = False
        i = i + 1
    return commits


commits = json_normalize(commits_of_repo('DeepSpeed', 'microsoft', github_api))
commits.to_csv('data/commits.csv')

commits2 = json_normalize(commits_of_repo('DeepSpeed', 'microsoft', github_api))
# To DF
commits_df = pd.DataFrame(commits2)
commits_df.describe()

# Get the issues
#issues_url = f"{repo_url}/issues"
#issues = github_session.get(issues_url).json()

# Get the pull requests
#pulls_url = f"{repo_url}/pulls"
#pulls = github_session.get(pulls_url).json()

# Get the commits
#commits_url = f"{repo_url}/commits"
#commits = github_session.get(commits_url).json()

# Get the contributors
#contributors_url = f"{repo_url}/contributors"
#contributors = github_session.get(contributors_url).json()
# convert json to CSV



