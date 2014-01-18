__author__ = 'robert'

import json
from odict import odict
import re
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
    edge_labels = dict()
    if labels is None:
        for edge in graph:
            G.add_edge(edge[0], edge[1])
    else:
        for edge in graph:
            G.add_edge(edge[0], edge[1])
            edge_labels[(edge[0], edge[1])] = labels[edge[0] + "_" + edge[1]]

#    if labels is None:
#        labels = range(len(graph))
#    edge_labels = dict(zip(graph, labels))

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
    nx.draw_networkx_nodes(G, graph_pos, node_size=node_size, alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G, graph_pos, width=edge_tickness, alpha=edge_alpha, edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos, font_size=node_text_size, font_family=text_font)

    if labels is None:
        nx.draw_networkx_edge_labels(G, graph_pos)
    else:
        nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels)

    # show graph
    plt.show()

def examples():
    graph = [(20, 21),(21, 22),(22, 23), (23, 24),(24, 25), (25, 20)]
    draw_graph1(graph)
    draw_graph(graph)

    graph = [(0, 1), (1, 5), (1, 7), (4, 5), (4, 8), (1, 6), (3, 7), (5, 9),
             (2, 4), (0, 4), (2, 5), (3, 6), (8, 9)]
    labels = map(chr, range(65, 65+len(graph)))
    draw_graph(graph, labels)

    graph = [('A', 'B'),('B', 'C'),('C', 'B'), ('C', 'D'),('D', 'A')]
    draw_graph(graph)


#{u'tsemple': 1, u'Thaddeus': 1, None: 12}
def pull_name(name_part):
    n = name_part.replace('u\'','').replace('\'','')
    return n.replace(' ', '')

def get_names(json_line):
    names = odict()
    regex = '{(.*)}'
    matches = re.match(regex, json_line)
    if matches is None:
        return names

    groups = matches.groups()
    name_list = groups[0]
    parts = name_list.split(',')
    for p in parts:
        name_count = p.split(':')
        name = pull_name(name_count[0])
        if name != "None":
            count = int(name_count[1])
            if name in names:
                names[name] += count
            else:
                names[name] = count
    return names

def read_user_file(fName):
    f = open(fName, 'r')
    pairs = []
    for line in f:
        if line[0] == '{':
            names = get_names(line)
            for name1_idx in range(0, len(names)):
                for name2_idx in range(name1_idx+1, len(names)):
                    name1 = names.keys()[name1_idx]
                    count1 = names.values()[name1_idx]
                    name2 = names.keys()[name2_idx]
                    count2 = names.values()[name2_idx]
                    pairs.append((name1, count1, name2, count2))
    return pairs


def remove_dups_and_assign_weights(list_of_pairs):
    unique_pairs = []
    unique_pair_hash = {}
    for pair in list_of_pairs:
        (n1, c1, n2, c2) = pair
        s1 = n1 + "_" + n2
        s2 = n2 + "_" + n1
        weight = c1*c2
        if s1 in unique_pair_hash:
            unique_pair_hash[s1] += weight
        elif s2 in unique_pair_hash:
            unique_pair_hash[s2] += weight
        else:
            unique_pair_hash[s1] = weight
            unique_pairs.append((n1,n2))

    return unique_pairs, unique_pair_hash

def test1():
    fileName = "UserByURL_Test"
    name_pairs = read_user_file(fileName)
    assert len(name_pairs) == 3
    (unique_pairs, pair_hash) = remove_dups_and_assign_weights(name_pairs)
    assert len(unique_pairs) == 2
    assert pair_hash["user1_user2"] == 2
    assert pair_hash["user1_user3"] == 1
    assert len(pair_hash) == 2
    print "PASS1"
    draw_graph(unique_pairs, graph_layout="spring", node_size=500, labels=pair_hash)

def test2():
    fileName = "UserByURL_Test2"
    name_pairs = read_user_file(fileName)
    assert len(name_pairs) == 6
    (unique_pairs, pair_hash) = remove_dups_and_assign_weights(name_pairs)
    assert len(unique_pairs) == 3
    assert pair_hash["user1_user2"] == 20
    assert pair_hash["user1_user3"] == 56
    assert pair_hash["user2_user3"] == 65
    assert len(pair_hash) == 3
    print "PASS2"
    draw_graph(unique_pairs, graph_layout="spring", node_size=500, labels=pair_hash)

def draw_user_graph():
    fileName = "UserByURL"  # Generated by stats.user_stats()
    # The Orig has all the data, this file has only some since the graph is too big
    name_pairs = read_user_file(fileName)
    print "Number of pairs %d" % (len(name_pairs))
    (unique_pairs, pair_hash) = remove_dups_and_assign_weights(name_pairs)
    print "Number of unique pairs %d" % (len(unique_pairs))
    draw_graph(unique_pairs, graph_layout="spring", node_size=500, labels=pair_hash)

if __name__ == "__main__":
    test1()
    test2()
    draw_user_graph()