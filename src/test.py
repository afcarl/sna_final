from gen_sub_graph import *;
from util import *;
import networkx as nx;
from networkx import *;
from networkx.readwrite import json_graph;
import json;

def main():
    dataSrc = sys.argv[1];
    numOfNodes = int(sys.argv[2]);
    numNodeHidden = int(sys.argv[3]);

    [relMatrix, subgraph] = genFullSubgraph(dataSrc, numOfNodes, numNodeHidden);

    stats(subgraph);
    print relMatrix;


    [relMatrix, subgraph] = genPartialSubgraph(dataSrc, numOfNodes, numNodeHidden);
    stats(subgraph);
    
    print relMatrix;

    '''read and write to file
    write_adj_data(subgraph, 'test.adj');

    [newgraph, newRelMatrix] = read_adj_data('test.adj');

    stats(newgraph);
    print newRelMatrix;
    '''
    

if __name__ == '__main__':
    sys.exit(main())
