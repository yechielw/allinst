#!/bin/python
import sys
import os
import requests
import re
repo = sys.argv[1]

def validate_repo(repo):
   
    if repo.startswith("http"):
        return repo
    elif not repo.startswith('git') and not repo.startswith('bitbuck'):
        if repo.startswith('/'):
            repo = "github.com" + repo
        else:
            repo = "github.com/" + repo


    repo = "https://" + repo
    return repo

print(validate_repo(repo))

# https://api.github.com//repos/RhinoSecurityLabs/pacu/languages | jq 'to_entries | max_by(.value) | .key'
# stript https:// from begining of string
stripted = repo.replace("https://github.com","")

language = "https://api.github.com/repos" + stripted + "/languages"

print(language)
languages = requests.get(language).json()
mainLangKey = max(languages, key=languages.get)
mainLanguage = languages[mainLangKey]
print(mainLangKey)

if mainLangKey == "Rust":
    os.system("cargo install --git " + repo)
if mainLangKey == "Python":
    os.system("pipx install git+" + repo)
if mainLangKey == "Go":
    # mainVersion = "https://api.github.com/repos/" + stripted 
    repodetails = "https://api.github.com/repos" + stripted
    #print(repodetails)
    defaultBranch = requests.get(repodetails).json()
    #print(defaultBranch['default_branch'])
    mod = requests.get("https://raw.githubusercontent.com" + stripted + '/' + defaultBranch['default_branch'] + "/go.mod").text
    os.system("go install -v " + re.findall(r'module.*',mod)[0].split()[1] + '@' + defaultBranch['default_branch'])

