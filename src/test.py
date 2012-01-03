from gen_sub_graph import *;
from util import *;
import networkx as nx;
from networkx import *;
#from networkx.readwrite import *;

def main():
    dataSrc = sys.argv[1];
    numOfNodes = int(sys.argv[2]);
    numNodeHidden = int(sys.argv[3]);

    [relMatrix, subgraph] = genFullSubgraph(dataSrc, numOfNodes, numNodeHidden);

    stats(subgraph);
    print relMatrix;


    [relMatrix, subgraph] = genPartialSubgraph(dataSrc, numOfNodes, numNodeHidden);
    stats(subgraph);
    #print subgraph.nodes(True);
    print relMatrix;

    '''trying to write it out.... no success yet
    f = open('sample.adjdata', 'w');
    f.write(networkx.readwrite.json_graph.adjacency_data(subgraph));
    f.close();
    
    [nodeTypeCount, edgeTypeCount] = stats(newgraph);
    relMatrix = gen_full_rel_matrix(subgraph, nodeTypeCount, edgeTypeCount);
    '''
    

if __name__ == '__main__':
    sys.exit(main())
