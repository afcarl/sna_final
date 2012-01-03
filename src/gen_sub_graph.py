import networkx as nx;
from networkx import *;
import sys;
import random;
from util import *;

def main():

    if (len(sys.argv) < 5):
        print "python genSubgraph.py dataFile numOfNodes numNodeHidden type(full or partial)";
        return;

    dataSrc = sys.argv[1];
    numOfNodes = int(sys.argv[2]);
    numNodeHidden = int(sys.argv[3]);
    graphType = sys.argv[4];

    if (graphType == 'full'):
        genFullSubgraph(dataSrc, numOfNodes, numNodeHidden);
    else:
        genPartialSubgraph(dataSrc, numOfNodes, numNodeHidden);

def genPartialSubgraph(dataSrc, numOfNodes, numNodeHidden):
    [graph, e_type, n_type, nTypes, eTypes] = read_data(dataSrc);
    
    [subgraph, sub_e_type, sub_n_type] = randomSampling(graph, e_type, n_type, numOfNodes, 0);
        
    hiddenCount = 0;

    nodes = subgraph.nodes();

    #relMatrix = gen_full_rel_matrix(subgraph, sub_e_type, sub_n_type,len(nTypes), len(eTypes));

    #print relMatrix;

    while hiddenCount < numNodeHidden:
        randInt = random.randint(0, len(nodes)-1);

        randNode = nodes[randInt];

        del(sub_n_type[randNode]);
        nodes.remove(randNode);

        #stats(subgraph, sub_e_type, sub_n_type);

        hiddenCount+=1;

    relMatrix = gen_full_rel_matrix(subgraph, sub_e_type, sub_n_type,len(nTypes), len(eTypes));    

    stats(subgraph, sub_e_type, sub_n_type);
    print relMatrix
    
    return [relMatrix, subgraph, sub_e_type, sub_n_type];

def genFullSubgraph(dataSrc, numOfNodes, numNodeHidden):
    [graph, e_type, n_type, nTypes, eTypes] = read_data(dataSrc);
    
    [subgraph, sub_e_type, sub_n_type] = randomSampling(graph, e_type, n_type, numOfNodes, numNodeHidden);
    path = '../data/sample_random_acad';
    stats(subgraph, sub_e_type, sub_n_type);
    relMatrix = gen_full_rel_matrix(subgraph, sub_e_type, sub_n_type,len(nTypes), len(eTypes)); 
    write_edgelist(subgraph, path+'.dat');
    write_dict(path+'.edgetype', subgraph, e_type, 1);
    write_dict(path+'.nodetype', subgraph, n_type, 0);   
    print relMatrix;
    return [relMatrix, subgraph, sub_e_type, sub_n_type];
        
def randomSampling(graph, e_type, n_type, numOfNodes, numHiddenNodes):   

    sub_e_type = {};
    sub_n_type = {};

    subgraph = nx.DiGraph();

    randInt = random.randint(0, graph.number_of_nodes()-1);

    randomNode = graph.nodes()[randInt];

    subgraph.add_node(randomNode);
    sub_n_type[randomNode] = n_type[randomNode];
    nextNodeCand = [];
    isHidden = False;

    while (subgraph.number_of_nodes() < numOfNodes):        

        if (not isHidden) and (subgraph.number_of_nodes() >= (numOfNodes  - numHiddenNodes)):
            isHidden = True;
            #print "Hidden!";
            #stats(subgraph, sub_e_type, sub_n_type);

        if len(nextNodeCand) == 0:
            #print "Find neighbors";
            for node in subgraph.nodes_iter():
                existingNodes = subgraph.nodes();
                neighbor = graph.successors(node);

                for nei in neighbor:
                    if not nei in existingNodes:
                        nextNodeCand.append(nei);

                neighbor = graph.predecessors(node);

                for nei in neighbor:
                    if not nei in existingNodes:
                        nextNodeCand.append(nei);
            #print len(nextNodeCand);

        #randomly select a node from neighboring nodes and add to subgraph
        randInt = random.randint(0, len(nextNodeCand)-1);
        nextNode = nextNodeCand[randInt];
        nextNodeCand.remove(nextNode);
        subgraph.add_node(nextNode);

        if not isHidden:
            sub_n_type[nextNode] = n_type[nextNode];

        #add out and in edges for the new node if another vertex is already in graph
        outEdges = graph.out_edges(nextNode);

        for start, end in outEdges:
            if end in existingNodes:
                subgraph.add_edge(start, end);
                key = str(start) + "," + str(end);
                sub_e_type[key] = e_type[key];


        inEdges = graph.in_edges(nextNode);

        for start, end in inEdges:
            if start in existingNodes:
                subgraph.add_edge(start, end);
                key = str(start) + "," + str(end);
                sub_e_type[key] = e_type[key];    
    
    return [subgraph, sub_e_type, sub_n_type];

if __name__ == '__main__':
    sys.exit(main())
