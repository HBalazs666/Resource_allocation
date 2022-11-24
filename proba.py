from graph_gen import graph_gen, dijkstra


fog_num=2
starting_point = 2

graph = graph_gen(fog_num)
graph.print_adj_list()

dijkstra(graph, fog_num, starting_point)
