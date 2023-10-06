import json
import requests
from pandas import json_normalize
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

# Get repository information
def repo_info(repo, owner, api):
    url = api + '/repos/{}/{}'.format(owner, repo)
    repo_info = github_session.get(url=url)
    repo_info_list = repo_info.json()
    # Get id of the repository
    id_repo = repo_info_list['id']
    return id_repo
# Id of the repository
id_general_repo = repo_info('DeepSpeed', 'microsoft', github_api)

# Get the commits
def commits_of_repo(repo, owner, api):
    commits = []
    next = True
    i = 1
    while next == True:
        url = api + '/repos/{}/{}/commits?page={}&per_page=100'.format(owner, repo, i)
        commit_pg = github_session.get(url=url)
        commit_pg_list = commit_pg.json()

        # Procesar y guardar la información de los commits
        for commit_data in commit_pg_list:
            sha = commit_data["sha"]
            author_name = commit_data["commit"]["author"]["name"]
            creation_date = commit_data["commit"]["author"]["date"]
            # Verificar si "author" es None y si contiene "id"
            if commit_data.get("author") is not None and "id" in commit_data["author"]:
                author_id = commit_data["author"]["id"]
            else:
                author_id = "ID Desconocido"
            id_repository = id_general_repo

            # Agregar la información a la lista
            commits.append({
                "SHA del commit": sha,
                "Nombre del autor": author_name,
                "Fecha de creación": creation_date,
                "ID del author": author_id,
                "ID repositorio": id_repository
            })

        if 'Link' in commit_pg.headers:
            if 'rel="next"' not in commit_pg.headers['Link']:
                next = False
        i = i + 1
    return commits

commits = json_normalize(commits_of_repo('DeepSpeed', 'microsoft', github_api))
commits.to_csv('data/commits.csv')

# Get the closed pulls
def closed_pulls_of_repo(repo, owner, api):
    closed_pulls = []
    next = True
    i = 1
    while next == True:
        url = api + '/repos/{}/{}/pulls?state=closed&page={}&per_page=100'.format(owner, repo, i)
        pull_pg = github_session.get(url=url)
        pull_pg_list = pull_pg.json()

        # Procesar y guardar la información de los pulls
        for closed_pull_data in pull_pg_list:
            id_pull = closed_pull_data["id"]
            name = closed_pull_data["title"]
            id_user = closed_pull_data["user"]["id"]
            status = closed_pull_data["state"]
            created_at = closed_pull_data["created_at"]
            closed_at = closed_pull_data["closed_at"]
            id_commit = closed_pull_data["merge_commit_sha"]
            id_repository = id_general_repo
            

            # Agregar la información a la lista
            closed_pulls.append({
                "ID pull": id_pull,
                "Name": name,
                "ID Usuario": id_user,
                "Estado": status,
                "Fecha de creación": created_at,
                "Fecha de cierre": closed_at,
                "ID commit": id_commit,
                "ID repositorio": id_repository
            })

        if 'Link' in pull_pg.headers:
            if 'rel="next"' not in pull_pg.headers['Link']:
                next = False
        i = i + 1
    return closed_pulls

# Get the open pulls
def open_pulls_of_repo(repo, owner, api):
    open_pulls = []
    next = True
    i = 1
    while next == True:
        url = api + '/repos/{}/{}/pulls?state=open&page={}&per_page=100'.format(owner, repo, i)
        pull_pg = github_session.get(url=url)
        pull_pg_list = pull_pg.json()

        # Procesar y guardar la información de los pulls
        for pull_data in pull_pg_list:
            id_pull = pull_data["id"]
            name = pull_data["title"]
            id_user = pull_data["user"]["id"]
            status = pull_data["state"]
            created_at = pull_data["created_at"]
            closed_at = pull_data["closed_at"]
            id_commit = pull_data["merge_commit_sha"]
            id_repository = id_general_repo
          
            

            # Agregar la información a la lista
            open_pulls.append({
                "ID pull": id_pull,
                "Name": name,
                "ID Usuario": id_user,
                "Estado": status,
                "Fecha de creación": created_at,
                "Fecha de cierre": closed_at,
                "ID commit": id_commit,
                "ID repositorio": id_repository
            })

        if 'Link' in pull_pg.headers:
            if 'rel="next"' not in pull_pg.headers['Link']:
                next = False
        i = i + 1
    return open_pulls

# Combine open_pulls and closed_pulls
pulls = json_normalize( closed_pulls_of_repo('DeepSpeed', 'microsoft', github_api) + open_pulls_of_repo('DeepSpeed', 'microsoft', github_api))
pulls.to_csv('data/pulls.csv')

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



