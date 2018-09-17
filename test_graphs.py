from graphviz import Graph
import os

os.environ["PATH"] += os.pathsep + 'D:/graphviz-2.38/release/bin'

graph = Graph('FSM', filename='fsm.gv', engine='sfdp')

graph.node("A", shape="circle", start="true")
graph.node("B", shape="circle")
graph.node("C", shape="circle")
graph.node("D", shape="circle")
graph.node("E", shape="circle")
graph.node("F", shape="doublecircle")
graph.node("G", shape="doublecircle")
graph.node("H", shape="circle")

graph.edge("A", "B", label="1")
graph.edge("A", "H", label="0")
graph.edge("B", "A", label="1")
graph.edge("B", "H", label="0")
graph.edge("C", "G", label="1")
graph.edge("C", "E", label="0")
graph.edge("D", "G", label="1")
graph.edge("D", "E", label="0")
graph.edge("E", "F", label="1")
graph.edge("E", "G", label="0")
graph.edge("F", "F", label="1")
graph.edge("F", "F", label="0")
graph.edge("G", "F", label="1")
graph.edge("G", "G", label="0")
graph.edge("H", "C", label="1")
graph.edge("H", "C", label="0")

graph.render("test_graph1.gv")

graph = Graph('FSM1', filename='fsm1.gv', engine='sfdp')

graph.node("A", shape="circle", start="true")
graph.node("B", shape="circle")
graph.node("C", shape="circle")
graph.node("D", shape="circle")
graph.node("E", shape="circle")
graph.node("F", shape="doublecircle")
graph.node("G", shape="doublecircle")

graph.edge("A", "B", label="1")
graph.edge("A", "C", label="0")
graph.edge("B", "A", label="1")
graph.edge("B", "C", label="0")
graph.edge("C", "D", label="1")
graph.edge("C", "D", label="0")
graph.edge("D", "F", label="1")
graph.edge("D", "E", label="0")
graph.edge("E", "G", label="1")
graph.edge("E", "F", label="0")
graph.edge("F", "F", label="1")
graph.edge("F", "F", label="0")
graph.edge("G", "F", label="1")
graph.edge("G", "G", label="0")

graph.render("test_graph2.gv")