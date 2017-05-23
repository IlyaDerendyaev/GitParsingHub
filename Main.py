
import requests
from bs4 import BeautifulSoup as bs
from graphviz import Digraph


def user_projects(user):
	r = requests.get("https://api.github.com/users/" + user + "/repos")
	list = r.json()
	projects = []
	for element in list:
		if element['watchers'] > 4:
			projects.append(element['full_name'])
	return projects


def project_commiters(project):
	r = requests.get("https://api.github.com/repos/" + project + '/commits')
	list = r.json()
	commiters = []
	for element in list:
		if element['author'] != None:
			seen = 0
			for commiter in commiters:
				if commiter == element['author']['login']:
					seen = 1
			if seen == 0:
				commiters.append(element['author']['login'])
	return commiters



f = open('input.txt')
str = f.read()
f.close()
users = str.split(' ')

'''
users = project_commiters('r1chardj0n3s/parse')
print(users)
'''

dot = Digraph(comment='Collaborations', format='png')

for user in users:
	dot.node(user, user)



for user in users:
	user_repos = user_projects(user)
	i = 0
	n = min(len(user_repos), 5)
	while i < n:
		repo = user_repos[i]
		i = i + 1
		dot.node(repo, repo)
		commiters = project_commiters(repo)
		result = list(set(commiters) & set(users))
		for commiter in result:
			dot.edge(commiter, repo)
dot.render('github.gv')
