import networkx as nx;
from networkx import *;
from matrix import *;
from networkx.readwrite import json_graph;
import json;

def read_adj_data(path):
    newgraph = nx.DiGraph()
    d = json.load(open(path))

    newgraph = networkx.readwrite.json_graph.adjacency_graph(d, True);

    if not ('nodeTypeCount' in newgraph.graph):
        [nodeTypeCount, edgeTypeCount] = stats(newgraph);
    else:
        nodeTypeCount = newgraph.graph['nodeTypeCount'];
        edgeTypeCount = newgraph.graph['edgeTypeCount'];
        
    relMatrix = gen_full_rel_matrix(newgraph, nodeTypeCount, edgeTypeCount);

    return [newgraph, relMatrix];

def write_adj_data(graph, path):
    f = open(path, 'w');
    data = networkx.readwrite.json_graph.adjacency_data(graph)
    s = json.dumps(data);    
    f.write(s);
    f.close();

def addNodeAndRelEdges(graph, subgraph, nextNode):
    subgraph.add_node(nextNode);
    subgraph.node[nextNode]['type'] = graph.node[nextNode]['type'];

    for start, end in graph.out_edges_iter(nextNode):
        if end in subgraph.nodes_iter():
            subgraph.add_edge(start, end);
            subgraph.edge[start][end]['type'] = graph.edge[start][end]['type'];


    for start, end in graph.in_edges_iter(nextNode):
        if start in subgraph.nodes_iter():
            subgraph.add_edge(start, end);
            subgraph.edge[start][end]['type'] = graph.edge[start][end]['type'];


def read_data(path):
    
    graph = nx.DiGraph();    

    nTypes = [];
    eTypes = [];
    
    f = file(path, 'r');

    while(True):
        line = f.readline();
        if line == '':
            break;

        line = line.rstrip();

        line = line.split(",");

        if (len(line) == 3):
            
            node1 = int(line[0]);
            node2 = int(line[1]);
            edgeType = int(line[2]);
            #print "edge";
            graph.add_node(node1);
            graph.add_node(node2);
            graph.add_edge(node1, node2);

            graph.edge[node1][node2]['type'] = edgeType;

            if not (edgeType in eTypes):
                eTypes.append(edgeType);
        else:
            node = int(line[0]);
            nodeType = int(line[1]);

            if not (node in graph.nodes()):
                continue;

            graph.node[node]['type'] = nodeType;

            if not (nodeType in nTypes):
                nTypes.append(nodeType);
            #print "type";
        
    f.close();
    graph.graph['edgeTypeCount'] = len(eTypes);
    graph.graph['nodeTypeCount'] = len(nTypes);
    return [graph, nTypes, eTypes];

def getAllNeighbors(graph, subgraph):
    neighbors = [];
    for node in subgraph.nodes_iter():
        neighbor = graph.successors_iter(node);

        for nei in neighbor:
            if not nei in subgraph.nodes_iter():
                neighbors.append(nei);

        neighbor = graph.predecessors_iter(node);

        for nei in neighbor:
            if not nei in subgraph.nodes_iter():
                neighbors.append(nei);

    return neighbors;

def stats(graph):
    edgeTypeCount = {};
    nodeTypeCount = {};

    hiddenNodeCount = 0;
    hiddenEdgeCount = 0;

    for node in graph.nodes_iter():
        if 'type' in graph.node[node]:
            nodeType = graph.node[node]['type'];
            if nodeType in nodeTypeCount:
                nodeTypeCount[nodeType] +=1;
            else:
                nodeTypeCount[nodeType] = 1;
        else:
            hiddenNodeCount += 1;

    for startNode, endNode in graph.edges_iter():
        if 'type' in graph.edge[startNode][endNode]:
            edgeType = graph.edge[startNode][endNode]['type'];
            if edgeType in edgeTypeCount:
                edgeTypeCount[edgeType] +=1;
            else:
                edgeTypeCount[edgeType] = 1;
        else:
            hiddenEdgeCount+=1;

    print "Num of edges: %d" % graph.number_of_edges();
    print "Num of nodes: %d" % graph.number_of_nodes();
    print "Hidden node count: %d" % hiddenNodeCount;
    print "Hidden edge count: %d" % hiddenEdgeCount;

    print "Edge count by type:";
    print edgeTypeCount;
    print "Node count by type:";
    print nodeTypeCount;
    
    print "";

    return [len(nodeTypeCount), len(edgeTypeCount)];

def gen_full_rel_matrix(graph, nodeTypeCount, edgeTypeCount):    
    nodeToNodeMatrix = gen_node_to_node_rel_matrix(graph, nodeTypeCount, edgeTypeCount);
    nodeToEdgeMatrix = gen_node_to_edge_rel_matrix(graph, nodeTypeCount, edgeTypeCount);
    edgeToNodeMatrix = gen_edge_to_node_rel_matrix(graph, nodeTypeCount, edgeTypeCount);
    edgeToEdgeMatrix = gen_edge_to_edge_rel_matrix(graph, nodeTypeCount, edgeTypeCount);

    '''
    print "Node to node";
    print nodeToNodeMatrix;
    print "Node to edge";
    print nodeToEdgeMatrix;
    print "Edge to node";
    print edgeToNodeMatrix;
    print "Edge to edge";
    print edgeToEdgeMatrix;
    '''
        
    fullRelMatrix = Matrix(nodeTypeCount+edgeTypeCount, nodeTypeCount+edgeTypeCount);
    
    for rowIndex in range(fullRelMatrix.row_count()):
        for colIndex in range(fullRelMatrix.col_count()):            
            if (rowIndex < nodeTypeCount and colIndex < nodeTypeCount):
                fullRelMatrix.set_item(rowIndex, colIndex, nodeToNodeMatrix.get_item(rowIndex, colIndex));
            elif (rowIndex >= nodeTypeCount and colIndex >= nodeTypeCount):
                fullRelMatrix.set_item(rowIndex, colIndex, edgeToEdgeMatrix.get_item(rowIndex-nodeTypeCount, colIndex-nodeTypeCount));
            elif (rowIndex >= nodeTypeCount):
                fullRelMatrix.set_item(rowIndex, colIndex, edgeToNodeMatrix.get_item(rowIndex-nodeTypeCount, colIndex));
            elif (colIndex >= nodeTypeCount):
                fullRelMatrix.set_item(rowIndex, colIndex, nodeToEdgeMatrix.get_item(rowIndex, colIndex-nodeTypeCount));

    #print fullRelMatrix;
    return fullRelMatrix;


def gen_node_to_edge_rel_matrix(graph, nodeTypeCount, edgeTypeCount):
    nodeToEdgeMatrix = Matrix(nodeTypeCount, edgeTypeCount);

    for node in graph.nodes_iter():
        if not ('type' in graph.node[node]):
            #node type not observed, continue;
            continue;
        nodeType = graph.node[node]['type'];

        for startNode, endNode in graph.edges_iter(node):
            if not ('type' in graph.edge[startNode][endNode]):
                #edge type not observed, continue;
                continue;
            
            edgeType = graph.edge[startNode][endNode]['type'];

            nodeToEdgeMatrix.set_item(nodeType, edgeType, nodeToEdgeMatrix.get_item(nodeType, edgeType) + 1);

    #print nodeToEdgeMatrix;

    for rowIndex in range(nodeToEdgeMatrix.row_count()):        
        row = nodeToEdgeMatrix.get_row(rowIndex);

        edgeCount = 0;
        for colIndex in range(0, nodeToEdgeMatrix.col_count()):            
            edgeCount += row[colIndex];
                        
        for colIndex in range(0, nodeToEdgeMatrix.col_count()):
            if edgeCount == 0:
                nodeToEdgeMatrix.set_item(rowIndex, colIndex, 0);
            else:
                nodeToEdgeMatrix.set_item(rowIndex, colIndex, round(nodeToEdgeMatrix.get_item(rowIndex, colIndex)/float(edgeCount), 3));

    #print "Node To Edge:";    
    #print nodeToEdgeMatrix;
    return nodeToEdgeMatrix;

def gen_node_to_node_rel_matrix(graph, nodeTypeCount, edgeTypeCount):

    nodeToNodeMatrix = Matrix(nodeTypeCount, nodeTypeCount);
    
    for node in graph.nodes_iter():
        if not ('type' in graph.node[node]):
            continue;

        nodeType = graph.node[node]['type'];
                
        for nei in graph.successors_iter(node):
            if not ('type' in graph.node[nei]):
                continue;
            
            neiType = graph.node[nei]['type'];

            nodeToNodeMatrix.set_item(nodeType, neiType, nodeToNodeMatrix.get_item(nodeType, neiType) + 1);

    for rowIndex in range(nodeToNodeMatrix.row_count()):        
        row = nodeToNodeMatrix.get_row(rowIndex);

        neiCount = 0;
        for colIndex in range(0, nodeToNodeMatrix.col_count()):            
            neiCount += row[colIndex];
                        
        for colIndex in range(0, nodeToNodeMatrix.col_count()):
            if neiCount == 0:
                nodeToNodeMatrix.set_item(rowIndex, colIndex, 0);
            else:
                nodeToNodeMatrix.set_item(rowIndex, colIndex, round(nodeToNodeMatrix.get_item(rowIndex, colIndex)/float(neiCount), 3));

    #print "Node to Node:";
    #print nodeToNodeMatrix;
    return nodeToNodeMatrix;


def gen_edge_to_edge_rel_matrix(graph, nodeTypeCount, edgeTypeCount):

    edgeToEdgeMatrix = Matrix(edgeTypeCount, edgeTypeCount);
    
    for startNode, endNode in graph.edges_iter():
        if not ('type' in graph.edge[startNode][endNode]):
            continue;
        
        edgeType = graph.edge[startNode][endNode]['type'];
                               
        for neiStart, neiEnd in graph.edges_iter(endNode):
            if not ('type' in graph.edge[neiStart][neiEnd]):
                continue;

            neiEdgeType = graph.edge[neiStart][neiEnd]['type'];

            edgeToEdgeMatrix.set_item(edgeType, neiEdgeType, edgeToEdgeMatrix.get_item(edgeType, neiEdgeType) + 1);
        
    #print edgeToEdgeMatrix;

    for rowIndex in range(edgeToEdgeMatrix.row_count()):        
        row = edgeToEdgeMatrix.get_row(rowIndex);

        neiEdgeCount = 0;
        for colIndex in range(0, edgeToEdgeMatrix.col_count()):            
            neiEdgeCount += row[colIndex];
                        
        for colIndex in range(0, edgeToEdgeMatrix.col_count()):
            if neiEdgeCount == 0:
                edgeToEdgeMatrix.set_item(rowIndex, colIndex, 0);
            else:
                edgeToEdgeMatrix.set_item(rowIndex, colIndex, round(edgeToEdgeMatrix.get_item(rowIndex, colIndex)/float(neiEdgeCount), 3));

        
    
    #print "Edge to Edge:"
    #print edgeToEdgeMatrix;
    return edgeToEdgeMatrix;

def gen_edge_to_node_rel_matrix(graph, nodeTypeCount, edgeTypeCount):

    edgeToNodeMatrix = Matrix(edgeTypeCount, nodeTypeCount);
    
    for startNode, endNode in graph.edges_iter():
        if not ('type' in graph.edge[startNode][endNode]) or not ('type' in graph.node[endNode]):
            continue;

        edgeType = graph.edge[startNode][endNode]['type'];
                               
        nodeType = graph.node[endNode]['type'];

        edgeToNodeMatrix.set_item(edgeType, nodeType, edgeToNodeMatrix.get_item(edgeType, nodeType) + 1);
        
    #print edgeToNodeMatrix;

    for rowIndex in range(edgeToNodeMatrix.row_count()):        
        row = edgeToNodeMatrix.get_row(rowIndex);

        nodeCount = 0;
        for colIndex in range(0, edgeToNodeMatrix.col_count()):            
            nodeCount += row[colIndex];
                        
        for colIndex in range(0, edgeToNodeMatrix.col_count()):
            if nodeCount == 0:
                edgeToNodeMatrix.set_item(rowIndex, colIndex, 0);
            else:
                edgeToNodeMatrix.set_item(rowIndex, colIndex, round(edgeToNodeMatrix.get_item(rowIndex, colIndex)/float(nodeCount), 3));


    #print "Edge To Node:";
    #print edgeToNodeMatrix;
    return edgeToNodeMatrix;
