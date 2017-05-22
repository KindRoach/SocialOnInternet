from igraph import Graph, plot

# g = Graph(directed=True)
#
# g.add_vertices(["Tom", "John", "Gary"])
# g.add_edges([('Tom', 'John'), ('Gary', 'John')])
#
# age_att = [18, 20, 18]
# g.vs["age"] = age_att
#
# strength_att = [5, 1]
# g.es["strength"] = strength_att

g = Graph.Tree(130, 3, "Tree_OUT")

print(g.summary())

print(g.degree())

print(g.degree())  ## 每个节点的度(出入度一起算)
print(g.betweenness())  ## betweeness
print(g.closeness())  ## closeness


sgcom = g.community_spinglass()
print(sgcom.summary()) ## summary of the community structure
print(sgcom.membership)

for v in g.vs:
    if v.degree() >= 3:
        v['color'] = 'Gold'
        v['frame_color'] = 'Gold'
    else:
        v['color'] = 'blue'
        v['frame_color'] = 'blue'

for e in g.es:
    e['color'] = g.vs[e.target]['color']

plot(g, "../data/fine_tune_network_graph_0.png")
