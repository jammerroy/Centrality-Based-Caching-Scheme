import networkx as nx
import matplotlib.pyplot as plt
import random
import pprint

n1=2									#CONTENT REQUEST FROM NODE 1 FOR CONTENT SERVER N2
n2=5									#REQUIRED CONTENT SERVER
cont_server=999 								#NUMBER OF CONTENT SERVERS
cont_server_no=0							#COUNT OF THE NUMBER OF CONTENT SERVERS
servers={}								#SERVER LIST DENOTING WHICH NODE CONTAINS WHICH SERVER

G=nx.Graph()								#GRAPH CREATED USING NETWORKX MODULE
G=nx.read_edgelist('facebook_combined.txt',nodetype=int)				#NODES AND EDGES INSERTED INTO GRAPH FROM FILE, NODES ARE OF TYPE INT AND INDICATED AS '0','1'...

#print G.number_of_edges()
#print G.number_of_nodes()

dic = nx.betweenness_centrality(G)
print dic
for key in dic:
	G.node[key]['cb_value'] = dic[key]

nodes=G.number_of_nodes()

for node in range(nodes):						#ASSIGNING THE ATTRIBUTE OF BETWEENESS CENTRALITY VALUE OF EACH NODE,INITIALIZED TO ZERO
	G.node[node]['no_of_requests'] = 0				#ASSIGNING THE ATTRIBUTE OF NUMBER OF CONTENT REQUEST PATH TRAVELLING ALONG THE NODE
	G.node[node]['cache_server'] = []

for i in range(0,cont_server):						#CONTENT SERVERS FROM 0 TO S BEING ADDED TO THE GRAPH AS ADJACENT TO RANDOM NODES
    	cont_server_no+=1
	count=random.randrange(0, 4000)
	
	servers.setdefault(count,[])
	servers[count].append(cont_server_no)
	
	G.add_edge(count,nodes+1)
	G.node[nodes+1]['cont_server'] = 1
	nodes=G.number_of_nodes()
	

#print G.number_of_nodes()

pprint.pprint(servers)							#A SERVER LIST DENOTING WHICH NODES CONNECT TO WHICH SERVER

for key in servers:							#FINDING THE END NODE OF THE PATH CONNECTED TO THE CONTENT SERVER REQUIRED
	content=servers[key]
	if n2 in content:
		n3=key		

path = (nx.shortest_path(G,source=n1,target=n3))			#SHORTEST PATH FROM NODE 1 to END NODE CONNECTED TO THE CONTENT SERVER
print path

size=len(path)

cb_value_max=0
cou=0


while(cou<2):
	cb_value_max=0	
	for node in path:
		if cou == 0:
			G.node[node]['cb_value']=0
			cb_value_max=0
		else:			
			dic_new = nx.betweenness_centrality(G)
			G.node[node]['cb_value']=dic_new[node]	
			if cb_value_max < G.node[node]['cb_value']:
				cb_value_max = G.node[node]['cb_value']
			
	
	for node in reversed(path):
		if cou == 0:
			if G.node[node]['cb_value'] == cb_value_max:
				print "CACHE HERE AT",node
				G.node[node]['no_of_requests']+=1				
				G.node[node]['cache_server'].append(n2)				
				break
		else:			
			dic_new2 = nx.betweenness_centrality(G)
			cb_val=dic_new2[node]
			G.node[node]['no_of_requests']+=1			
			if n2 not in G.node[node]['cache_server']:
				if cb_val == G.node[node]['cb_value']:
					print "CACHE HERE AT",node
					break

	cou+=1


#nx.draw(G,with_labels=True,node_size=500)
#plt.show()

