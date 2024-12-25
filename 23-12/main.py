import networkx as nx

with open("data.txt") as f:
    ls = f.read().strip().split("\n")

G = nx.Graph(l.split("-") for l in ls)
cliques = list(nx.enumerate_all_cliques(G))

print(sum(len(c) == 3 and any(x[0] == 't' for x in c) for c in cliques))

print(",".join(sorted(cliques[-1])))