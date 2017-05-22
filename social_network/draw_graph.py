from math import ceil

from igraph import Graph, plot, layout

table = list()
with open(r"../data/forward_map.txt", 'r', encoding="utf-8") as in_f:
    lines = in_f.readlines()
    table = [[int(x) for x in line.split(' ')] for line in lines]

vertices = set()
edges = list()
forward_att = list()
for i in range(len(table)):
    for j in range(i):
        if table[j][i] > 0 and table[i][j] > 0:
            edges.append((str(i), str(j)))
            vertices.add(str(i))
            vertices.add(str(j))
            forward_att.append(table[i][j] + table[j][i])

g = Graph()
g.add_vertices(list(vertices))
g.add_edges(edges)
g.es["forward"] = forward_att
sgcom = g.community_spinglass()
g.vs['community'] = sgcom.membership

print(g)
print()
print(sgcom)

g.vs["label"] = g.vs["name"]
g.es["width"] = [ceil(x / 10) for x in forward_att]
for v in g.vs:
    if v["community"] == 0:
        v['color'] = 'gold'
    elif v["community"] == 1:
        v['color'] = 'green'
    elif v["community"] == 2:
        v['color'] = 'red'

layout = g.layout("tree")
plot(g, "../data/forward_map.png", bbox=(800, 800))
