import networkx as nx
import json
import array
from collections import deque


proplayer = []			# this array store all users data that collect from Twitter.
nodeFirstUser = []				# this array store all following user data from firt node.


def ltm(G,start):
	TH = 0.6		#	threshold
	b = 0			#	Bw,v
	active = []
	visit = []
	nb = []
	count = 0
	inDg = 0
	q = deque()
	active.append(start)
	visit.append(start)
	q.append(start)
	while q:
		node = q.popleft()
		for nb_active in G.neighbors(node):
			if nb_active not in visit:
				inDg = G.in_degree(nb_active)
				for act_node in active:
					if nb_active in G.neighbors(act_node):
						b += 1/inDg
				if b >= TH:
					active.append(nb_active)
					visit.append(nb_active)
					q.append(nb_active)
				inDg = 0
				b = 0
	return active


def get_node_inter(list_data):		# get node intersection
	node = []
	for data in list_data:
		if data['user'] not in node:
			node.append(data['user'])
		if data['user'] not in proplayer:
			proplayer.append(data['user'])
		for name in data['following']:
			if name not in node:
				# print(name)
				node.append(name)
		if data['user'] == 139169385:
			for name in data['following']:
					nodeFirstUser.append(name)
	return node



def get_array(node,list_data):		# array store
	try:
		arr = []
		for data in list_data:
			if node == data['user']:
				for name in data['following']:
					arr.append(name)
		return arr
	except:
		pass


def inter(start,list,nodeInit):		# Intersection between first node and all following user
	new = []
	max = -1;
	q = deque()
	q.append(start)
	print('Start node : Arteezy')
	print('Find intersection set . . .')
	print('Who is Proplayer Dota ! ! !\n')
	while q:
		node = q.popleft()
		for nb in G.neighbors(node):
			node_follow = get_array(nb,list)
			if len(node_follow) != 0:
				new = set(nodeInit).intersection(node_follow)
				if max < len(new):
					max = len(new)
					tmp = new
				else:
						new = tmp
		nodeInit = new
	return new


def get_data(path):			# get data from json
	tweets = []
	with open(path) as tweet_data:
	    for line in tweet_data:
	        data = line[:-2]
	        try:
	            json_acceptable_string = data.replace("'", "\"")
	            data_json = json.loads(json_acceptable_string)
	            tweets.append(data_json)
	        except:
	            pass
	return tweets

def get_node(list_data):	# Create node
	node = []
	for data in list_data:
		if data['user'] not in node:
			node.append(data['user'])

		if data['user'] not in proplayer:		# Create array store all user that collected from Twiiter.
			proplayer.append(data['user'])

		if data['user'] == 139169385:			# Create array store following user of first node.
			for name in data['following']:
					nodeFirstUser.append(name)
		for name in data['following']:
			if name not in node:
				node.append(name)
	return node


if __name__ == "__main__":
	G = nx.DiGraph() 								#create directed graph
	path = '/Users/khathawut/Documents/My works/Project/Data_Mining/data.json'
	list_data = get_data(path) 						#get data from json file
	node = get_node(list_data) 						#get node's name

	#add node
	for n in node:
	    G.add_node(n)

	#add edge with order (user --> following)
	for data in list_data:
	    name_user = data['user']
	    for name_following in data['following']:
	        G.add_edge(name_user,name_following)

	nodeInit = nodeFirstUser
	print(len(G))
	#Arteezy
	interNodePro = inter(139169385,list_data,nodeInit)
	interNodePro.add(139169385)
	print(interNodePro)
	print('\n##################################   Result : ',len(interNodePro) ,'   ##################################')
	print('\n== Find Activated node ! ! ! ==\n')

	for pro in interNodePro:	# find activated node in n array
		active_final = ltm(G,pro);
		print('Player :',pro,'			active count :  ',len(active_final),' 	node')

	# print(type(n))
	# print(len(n))
	# print(n)
	# print(proplayer)
