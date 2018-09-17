import argparse
from graphviz import Graph
import pydot
from collections import deque

parser = argparse.ArgumentParser()
parser.add_argument("file", help="dot file with graph")
args = parser.parse_args()

(graph,) = pydot.graph_from_dot_file(args.file)

terminals = [0]
char_to_matrix = {}
matrix_to_char = {}
number = 0
E = set()
for node in graph.get_node_list():
    if node.get_attributes().get("shape") == "circle":
        terminals.append(0)
    else:
        terminals.append(1)
    char_to_matrix.update({node.get_name(): number})
    matrix_to_char.update({number: node.get_name()})
    number += 1

matrix_adjacency = [[[] for i in range(len(graph.get_node_list()) + 1)] for i in range(len(graph.get_node_list()) + 1)]

for edge in graph.get_edge_list():
    label = edge.get_attributes().get('label')
    matrix_adjacency[char_to_matrix.get(edge.get_source()) + 1][char_to_matrix.get(edge.get_destination()) + 1].append(
        label)
    E.add(label)

for k in range(1, len(matrix_adjacency)):
    sub_e = set()
    for i in range(1, len(matrix_adjacency[k])):
        for char in matrix_adjacency[k][i]:
            sub_e.add(char)
    dif_e = E.difference(sub_e)
    for char in dif_e:
        matrix_adjacency[k][0].append(char)


def reachable_nodes(matrix):
    queue = deque()
    queue.append(1)
    used = set()
    used.add(1)
    while queue:
        next_node = queue.popleft()
        for column in range(1, len(matrix)):
            if matrix[next_node][column] and column not in used:
                queue.append(column)
                used.add(column)
    return used


def revert(matrix):
    for i in range(0, len(matrix)):
        for j in range(i, len(matrix)):
            tmp = matrix[i][j]
            matrix[i][j] = matrix[j][i]
            matrix[j][i] = tmp

    return matrix


def edges(matrix, n, char):
    edges_with_char = []
    for i in range(len(matrix)):
        if char in matrix[n][i]:
            edges_with_char.append(i)
    return edges_with_char


def build_table(matrix, terminals):
    queue = deque()
    step_number = 0
    n = len(matrix)
    marked = [[-1 for i in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if marked[i][j] == -1 and terminals[i] != terminals[j]:
                marked[i][j] = marked[j][i] = step_number
                queue.append([i, j])

    while queue:
        step_number += 1
        pair = queue.popleft()
        for c in E:
            r_c = edges(matrix, pair[0], c)
            for r in r_c:
                s_c = edges(matrix, pair[1], c)
                for s in s_c:
                    if marked[r][s] == -1:
                        marked[r][s] = marked[s][r] = step_number
                        queue.append([r, s])
    return marked


reachable = reachable_nodes(matrix_adjacency)

matrix = revert(matrix_adjacency)

marked = build_table(matrix, terminals)

component = [-1 for i in range(len(matrix))]

for i in range(len(matrix)):
    if marked[0][i] != -1:
        component[i] = 0

components_count = 0
for i in range(1, len(matrix)):
    if i not in reachable:
        continue
    if component[i] == -1:
        components_count += 1
        component[i] = components_count
        for j in range(i + 1, len(matrix)):
            if marked[i][j] == -1:
                component[j] = components_count
                if j not in reachable:
                    component[j] = -1

map_equivalence = {}
new_nodes = [pydot.Node() for i in range(components_count + 1)]
new_edges = []

for i in range(len(component)):
    class_equivalence = component[i]
    if class_equivalence != -1:
        class_equivalence_node = new_nodes[class_equivalence]
        map_equivalence.update({i: class_equivalence_node})
        if class_equivalence_node.get_name():
            class_equivalence_node.set_name(class_equivalence_node.get_name() + ',' + matrix_to_char.get(i - 1))
        else:
            class_equivalence_node.set_name(matrix_to_char.get(i - 1))

for edge in graph.get_edge_list():
    source = map_equivalence.get(char_to_matrix.get(edge.get_source()) + 1)
    destination = map_equivalence.get(char_to_matrix.get(edge.get_destination()) + 1)
    label = edge.get_attributes().get('label')

    if not source or not destination:
        continue

    is_existed_edge = False
    for new_edge in new_edges:
        if new_edge.get_source() == source.get_name() and new_edge.get_destination() == destination.get_name():
            new_label = set(new_edge.get_attributes().get('label').split(","))
            new_label.add(label)
            new_label = ",".join(new_label)
            new_edge.get_attributes().update({'label': new_label})
            is_existed_edge = True
    if not is_existed_edge:
        new_edges.append(pydot.Edge(source, destination, label=label))

g = Graph('G', filename='answer.gv', engine='sfdp')

for node in new_nodes:
    g.node(node.get_name())

for edge in new_edges:
    g.edge(edge.get_source(), edge.get_destination(), edge.get_attributes().get('label'))

g.view()

g.render()
