import requests
from graphviz import Digraph
import module_commiters
import module_projects

f = open('input.txt')
str = f.read()
f.close()
users = str.split(' ')

dot = Digraph(comment='Collaborations', format='png')

for user in users:
	dot.node(user, user)

for user in users:
	user_repos = module_projects.user_projects(user)
	for repo in user_repos:
		dot.node(repo, repo)
		commiters = module_commiters.project_commiters(repo)
		result = list(set(commiters) & set(users))
		for commiter in result:
			dot.edge(commiter, repo)
dot.render('github.gv')
