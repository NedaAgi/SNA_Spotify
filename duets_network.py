import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

duet_artists = pd.read_csv(r'duets.csv', usecols=['Track', 'Artist_1', 'Artist_2', 'Popularity', 'Year', 'Genre'])

edges = [(x, y, {'Track': t, 'Popularity': z, 'Year': v, 'Genre': w}) for x, y, t, z, v, w in
         zip(duet_artists['Artist_1'], duet_artists['Artist_2'], duet_artists['Track'], duet_artists['Popularity'],
             duet_artists['Year'], duet_artists['Genre'])]
G = nx.MultiGraph()
G.add_edges_from(edges)

to_be_removed = [x for x in G.nodes() if G.degree(x) < 10]
for x in to_be_removed:
    G.remove_node(x)

Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
G = G.subgraph(Gcc[0])

N = len(G)
L = G.size()

print("N = ", N)
print("L = ", L)

degrees = [G.degree[node] for node in G]

kmax = np.max(degrees)

kavg = np.mean(degrees)
print("max degree = ", kmax)
print("avg degree = ", kavg)

df = nx.to_pandas_edgelist(G)
df.to_csv("duets_final.csv", index=False, encoding='utf-8-sig')

nx.write_gexf(G, "duets.gexf")
