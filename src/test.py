from gen_sub_graph import *;
from util import *;

def main():
    dataSrc = sys.argv[1];
    numOfNodes = int(sys.argv[2]);
    numNodeHidden = int(sys.argv[3]);

    [relMatrix, subgraph, sub_e_type, sub_n_type] = genFullSubgraph(dataSrc, numOfNodes, numNodeHidden);

    stats(subgraph, sub_e_type, sub_n_type);
    print relMatrix;


    [relMatrix, subgraph, sub_e_type, sub_n_type] = genPartialSubgraph(dataSrc, numOfNodes, numNodeHidden);
    stats(subgraph, sub_e_type, sub_n_type);
    print relMatrix;    

if __name__ == '__main__':
    sys.exit(main())
