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
    [graph, nTypes, eTypes] = read_data(dataSrc);
    
    subgraph = randomSampling(graph, numOfNodes, 0);
        
    hiddenCount = 0;

    nodes = subgraph.nodes();

    #relMatrix = gen_full_rel_matrix(subgraph, sub_e_type, sub_n_type,len(nTypes), len(eTypes));

    #print relMatrix;

    while hiddenCount < numNodeHidden:
        randInt = random.randint(0, len(nodes)-1);

        randNode = nodes[randInt];

        del(subgraph.node[randNode]['type']);
        nodes.remove(randNode);

        #stats(subgraph, sub_e_type, sub_n_type);

        hiddenCount+=1;

    relMatrix = gen_full_rel_matrix(subgraph, len(nTypes), len(eTypes));    

    #stats(subgraph, sub_e_type, sub_n_type);
    #print relMatrix
    
    return [relMatrix, subgraph];

def genFullSubgraph(dataSrc, numOfNodes, numNodeHidden):
    [graph, nTypes, eTypes] = read_data(dataSrc);
    
    subgraph = randomSampling(graph, numOfNodes, numNodeHidden);
    
    #stats(subgraph, sub_e_type, sub_n_type);
    relMatrix = gen_full_rel_matrix(subgraph, len(nTypes), len(eTypes));    
    #print relMatrix;
    return [relMatrix, subgraph];
        
def randomSampling(graph, numOfNodes, numHiddenNodes):   
   
    subgraph = nx.DiGraph();

    randInt = random.randint(0, graph.number_of_nodes()-1);

    randomNode = graph.nodes()[randInt];

    subgraph.add_node(randomNode);
    subgraph.node[randomNode]['type'] = graph.node[randomNode]['type'];
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
            subgraph.node[nextNode]['type'] = graph.node[nextNode]['type'];

        #add out and in edges for the new node if another vertex is already in graph
        outEdges = graph.out_edges(nextNode);

        for start, end in outEdges:
            if end in existingNodes:
                subgraph.add_edge(start, end);                
                subgraph.edge[start][end]['type'] = graph.edge[start][end]['type'];


        inEdges = graph.in_edges(nextNode);

        for start, end in inEdges:
            if start in existingNodes:
                subgraph.add_edge(start, end);
                subgraph.edge[start][end]['type'] = graph.edge[start][end]['type'];
    
    return subgraph;

if __name__ == '__main__':
    sys.exit(main())
