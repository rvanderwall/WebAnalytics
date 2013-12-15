__author__ = 'robert'

import json
import networkx as nx
import matplotlib.pyplot as plt

def draw_graph1(graph):

    # extract nodes from graph
    nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

    # create networkx graph
    G=nx.Graph()

    # add nodes
    for node in nodes:
        G.add_node(node)

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    # draw graph
    pos = nx.shell_layout(G)
    nx.draw(G, pos)

    # show graph
    plt.show()


def draw_graph(graph, labels=None, graph_layout='shell',
               node_size=1600, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):

    # create networkx graph
    G=nx.Graph()

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    # these are different layouts for the network you may try
    # shell seems to work best
    if graph_layout == 'spring':
        graph_pos=nx.spring_layout(G)
    elif graph_layout == 'spectral':
        graph_pos=nx.spectral_layout(G)
    elif graph_layout == 'random':
        graph_pos=nx.random_layout(G)
    else:
        graph_pos=nx.shell_layout(G)

    # draw graph
    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size,
                           alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,
                           alpha=edge_alpha,edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
                            font_family=text_font)

#    if labels is None:
#        labels = range(len(graph))

#    edge_labels = dict(zip(graph, labels))
#    nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels,
    nx.draw_networkx_edge_labels(G, graph_pos)

    # show graph
    plt.show()

# draw example
#graph = [(20, 21),(21, 22),(22, 23), (23, 24),(24, 25), (25, 20)]
#draw_graph1(graph)
#draw_graph(graph)

#graph = [(0, 1), (1, 5), (1, 7), (4, 5), (4, 8), (1, 6), (3, 7), (5, 9),
#         (2, 4), (0, 4), (2, 5), (3, 6), (8, 9)]
#labels = map(chr, range(65, 65+len(graph)))
#draw_graph(graph, labels)

#graph = [('A', 'B'),('B', 'C'),('C', 'B'), ('C', 'D'),('D', 'A')]
#draw_graph(graph)

#{u'tsemple': 1, u'Thaddeus': 1, None: 12}
def pull_name(name_part):
    n = name_part.replace('u\'','').replace('\'','')
    return n.replace('{','').replace(' ', '')

def get_names(json_line):
    names = []
    parts = json_line.split(',')
    for p in parts:
        name_count = p.split(':')
        name = pull_name(name_count[0])
        if name != "None":
            names.append(name)
    return names

def read_user_file():
    f = open("UserByURL", 'r')
    pairs = []
    for line in f:
        if line[0] == '{':
            names = get_names(line)
            for name in names:
                for name2 in names:
                    if name != name2:
                        pairs.append((name, name2))
    return pairs

def remove_dups(list_of_pairs):
    unique_pairs = []
    unique_pair_hash = {}
    for pair in list_of_pairs:
        (n1, n2) = pair
        s1 = n1 + "_" + n2
        s2 = n2 + "_" + n1
        if s1 not in unique_pair_hash and s2 not in unique_pair_hash:
            unique_pair_hash[s1] = 1
            unique_pairs.append((n1,n2))
    return unique_pairs

name_pairs = read_user_file()
print len(name_pairs)
unique_pairs = remove_dups(name_pairs)
print len(unique_pairs)
draw_graph(name_pairs, graph_layout="spring", node_size=500)