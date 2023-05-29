#!/usr/bin/env python

from os import environ
import yaml
import requests

def main():
    pre_commit_config_path = "../../.pre-commit-config.yaml"

    with open(pre_commit_config_path, "r") as pre_commit:
        try:
            pre_commit_config = yaml.safe_load(pre_commit)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)
    
    for repo in pre_commit_config['repos']:
        repo_url = repo['repo'].replace('.git','') if '.git' in repo['repo'] else repo['repo']
        release = repo['rev']
        headers = {'Accept': 'application/json'}
        resp = requests.get(f"{repo_url}/refs?type=tag", headers=headers)
        if resp.status_code == requests.codes.ok:
            latest_release = resp.json()['refs'][0]
            if release != latest_release:
                print(f'{repo_url} needs to be updated to {latest_release}, currently at {release}')
                repo['rev'] = latest_release
        
    with open(pre_commit_config_path, 'w') as pre_commit:
        yaml.dump(pre_commit_config, pre_commit, default_flow_style=False)


if __name__== "__main__":
    main()
