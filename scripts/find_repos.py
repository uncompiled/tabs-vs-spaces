import os
import json
import requests

from collections import defaultdict

GITHUB_API = "https://api.github.com/search/repositories" \
             "?q=language:{}&sort=stars&order=desc&per_page=100"

# export GITHUB_ACCESS_TOKEN=<your github token>
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN", None)
if GITHUB_ACCESS_TOKEN:
    GITHUB_API += "&access_token={}".format(GITHUB_ACCESS_TOKEN)

# Languages that we're inspecting.
LANGUAGES = ["javascript", "java", "php", "python", "ruby", "go"]


def find_repos(language):
    """
    Fetches the top starred repos for a given language.
    :param language: string containing the programming language to be queried
    :return: list of repos for a given language.
    """
    try:
        response = requests.get(GITHUB_API.format(language))
    except requests.RequestException:
        # GitHub is a sad panda.
        return []
    else:
        try:
            repos = [{'id': item['id'],
                      'name': item['name'],
                      'full_name': item['full_name'],
                      'description': item['description'],
                      'html_url': item['html_url'],
                      'clone_url': item['clone_url'],
                      'stargazers_count': item['stargazers_count'],
                      'language': item['language']
                      } for item in response.json()["items"]]
        except (ValueError, KeyError):
            # In case GitHub is down, don't barf?  ¯\_(ツ)_/¯
            repos = []

    return repos


if __name__ == "__main__":
    top_repos = defaultdict(lambda: None)
    for language in LANGUAGES:
        top_repos[language] = find_repos(language)
    print(json.dumps(top_repos))
