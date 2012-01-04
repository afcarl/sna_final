import networkx as nx;
from networkx import *;
import sys;
import random;
from util import *;

def main():

    if (len(sys.argv) < 5):
        print "python genSubgraph.py dataFile numOfNodes numNodeHidden type(full or partial) outputFile";
        return;

    dataSrc = sys.argv[1];
    numOfNodes = int(sys.argv[2]);
    numNodeHidden = int(sys.argv[3]);
    graphType = sys.argv[4];
    outputFile = sys.argv[5];

    if (graphType == 'full'):
        [relMatrix, subgraph] = genFullSubgraph(dataSrc, numOfNodes, numNodeHidden);
        write_adj_data(subgraph, outputFile);
    else:
        [relMatrix, subgraph] = genPartialSubgraph(dataSrc, numOfNodes, numNodeHidden);
        write_adj_data(subgraph, outputFile);

def genPartialSubgraph(dataSrc, numOfNodes, numNodeHidden):
    [graph, nTypes, eTypes] = read_data(dataSrc);
    
    subgraph = randomSampling(graph, numOfNodes);
        
    hiddenCount = 0;

    nodes = subgraph.nodes();

    stats(subgraph);
    relMatrix = gen_full_rel_matrix(subgraph, len(nTypes), len(eTypes));

    print relMatrix;

    while hiddenCount < numNodeHidden:
        randInt = random.randint(0, len(nodes)-1);

        randNode = nodes[randInt];

        del(subgraph.node[randNode]['type']);
        nodes.remove(randNode);

        #stats(subgraph, sub_e_type, sub_n_type);

        hiddenCount+=1;

    relMatrix = gen_full_rel_matrix(subgraph, len(nTypes), len(eTypes));    

    stats(subgraph);
    print relMatrix
    
    return [relMatrix, subgraph];

def genFullSubgraph(dataSrc, numOfNodes, numNodeHidden):
    [graph, nTypes, eTypes] = read_data(dataSrc);
    
    subgraph = randomSampling(graph, numOfNodes-numNodeHidden);
    
    subRelMatrix = gen_full_rel_matrix(subgraph, len(nTypes), len(eTypes));
    stats(subgraph);
    print subRelMatrix;

    neighbors = getAllNeighbors(graph, subgraph);

    hiddenNodeCount = 0;
        
    while hiddenNodeCount < numNodeHidden:

        if len(neighbors) == 0:
            neighbors = getAllNeighbors(graph, subgraph);

        node = neighbors.pop();
        addNodeAndRelEdges(graph, subgraph, node);
        del(subgraph.node[node]['type']);
        hiddenNodeCount+=1;

    subRelMatrix = gen_full_rel_matrix(subgraph, len(nTypes), len(eTypes));
    stats(subgraph);
    print subRelMatrix;
        
    return [subRelMatrix, subgraph];
        
def randomSampling(graph, numOfNodes):   
   
    subgraph = nx.DiGraph();
    subgraph.graph['edgeTypeCount'] = graph.graph['edgeTypeCount'];
    subgraph.graph['nodeTypeCount'] = graph.graph['nodeTypeCount'];

    randInt = random.randint(0, graph.number_of_nodes()-1);

    randomNode = graph.nodes()[randInt];

    subgraph.add_node(randomNode);
    subgraph.node[randomNode]['type'] = graph.node[randomNode]['type'];
    nextNodeCand = [];

    while (subgraph.number_of_nodes() < numOfNodes):        
      

        if len(nextNodeCand) == 0:
            nextNodeCand = getAllNeighbors(graph, subgraph);
            #print len(nextNodeCand);

        #randomly select a node from neighboring nodes and add to subgraph
        randInt = random.randint(0, len(nextNodeCand)-1);
        nextNode = nextNodeCand[randInt];
        nextNodeCand.remove(nextNode);

        addNodeAndRelEdges(graph, subgraph, nextNode);        
              
    
    return subgraph;

if __name__ == '__main__':
    sys.exit(main())
