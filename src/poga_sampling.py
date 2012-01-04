import networkx as nx;
from networkx import *;
import sys;
from matrix import *;
import random;
from util import *;

def main():

    if (len(sys.argv) < 4):
        print "python poga_sampling.py dataFile sampleSize hiddenNodeCount sampleType(dms or dps) type(full or partial) outputFile";
        return;
    
    dataSrc = sys.argv[1];
    k = int(sys.argv[2]);
    hiddenCount = int(sys.argv[3]);
    sampleType = sys.argv[4];
    graphType = sys.argv[5];
    outputFile = sys.argv[6];

    #[graph, nTypes, eTypes] = read_data(dataSrc);
    [graph, fullRelMatrix] = read_adj_data(dataSrc);

    
    #stats(graph, e_type, n_type, nTypes, eTypes);
    
    #fullRelMatrix = gen_full_rel_matrix(graph, e_type, n_type, len(nTypes), len(eTypes));

    '''
    print "Node types: %d" % len(nTypes);
    print "Edge types: %d" % len(eTypes);
    
    print "Node Count: %d" % graph.number_of_nodes();
    print "Edge Count: %d" % graph.number_of_edges();
    '''
    #print fullRelMatrix;

    if (graphType == 'full'):
        subgraph = sampling(graph, k-hiddenCount, sampleType);  

        subRelMatrix = gen_full_rel_matrix(subgraph, graph.graph['nodeTypeCount'], graph.graph['edgeTypeCount']);
        stats(subgraph);
        print subRelMatrix;

        neighbors = getAllNeighbors(graph, subgraph);

        hiddenNodeCount = 0;
        
        while hiddenNodeCount < hiddenCount:

            if len(neighbors) == 0:
                neighbors = getAllNeighbors(graph, subgraph);

            node = neighbors.pop();
            addNodeAndRelEdges(graph, subgraph, node);
            del(subgraph.node[node]['type']);
            hiddenNodeCount+=1;

        subRelMatrix = gen_full_rel_matrix(subgraph, graph.graph['nodeTypeCount'], graph.graph['edgeTypeCount']);
        stats(subgraph);
        print subRelMatrix;
    else:
        subgraph = sampling(graph, k, sampleType);
        nodes = subgraph.nodes();
        relMatrix = gen_full_rel_matrix(subgraph, graph.graph['nodeTypeCount'], graph.graph['edgeTypeCount']);
        stats(subgraph);
        print relMatrix;

        numHiddenCount = 0;
        while numHiddenCount < hiddenCount:
            randInt = random.randint(0, len(nodes)-1);

            randNode = nodes[randInt];

            del(subgraph.node[randNode]['type']);
            nodes.remove(randNode);

            #stats(subgraph, sub_e_type, sub_n_type);

            numHiddenCount+=1;

        stats(subgraph);
        relMatrix = gen_full_rel_matrix(subgraph, graph.graph['nodeTypeCount'], graph.graph['edgeTypeCount']);    
        print relMatrix;

    write_adj_data(subgraph, outputFile);

def sampling(graph, k, sampleType):

    nodeTypeCount = graph.graph['nodeTypeCount'];
    edgeTypeCount = graph.graph['edgeTypeCount'];

    
    fullRelMatrix = gen_full_rel_matrix(graph, nodeTypeCount, edgeTypeCount);

    sampleRelMatrix = Matrix(nodeTypeCount + edgeTypeCount, nodeTypeCount + edgeTypeCount);

    subgraph = nx.DiGraph();
    subgraph.graph['nodeTypeCount'] = nodeTypeCount;
    subgraph.graph['edgeTypeCount'] = edgeTypeCount;

    randInt = random.randint(0, graph.number_of_nodes()-1);

    randomNode = graph.nodes()[randInt];

    subgraph.add_node(randomNode);
    subgraph.node[randomNode]['type'] = graph.node[randomNode]['type'];

    print "Start node: %d" % randomNode;
    if (sampleType == 'dms'):
        print "Running DMS";        
    elif (sampleType == 'dps'):
        print "Running DPS";

    maxDiff = -1;
    nextNode = -1;        
    while (subgraph.number_of_nodes() < k):
        #print "-------------------Run %d" % k;
        #print subgraph.nodes();
        #print subgraph.edges();
        nextNodeCand = [];
        if maxDiff == -1:
            origRelMatrix = gen_full_rel_matrix(subgraph, nodeTypeCount, edgeTypeCount);
        else:
            origRelMatrix = maxRelMatrix;
            
        if (sampleType == 'dms'):            
            maxDiff = -1;
            nextNode = -1;            
        elif (sampleType == 'dps'):            
            nextNodeRMSE = {};
        else:
            print "Error! what sampling type you want????";
            exit();                   

        if len(nextNodeCand) == 0:
            nextNodeCand = getAllNeighbors(graph, subgraph);

        for nodeCand in nextNodeCand:            
            addNodeAndRelEdges(graph, subgraph, nodeCand);
            newRelMatrix = gen_full_rel_matrix(subgraph, nodeTypeCount, edgeTypeCount);

            diff = rmseDiff(origRelMatrix, newRelMatrix);

            #print "Max diff: %.2f, diff: %.2f, edge: %d, %d" % (maxDiff, diff, edgeCand[0], edgeCand[1]);


            if (sampleType == 'dms'):
                if (diff > maxDiff):
                    nextNode = nodeCand;
                    maxDiff = diff;
                    maxRelMatrix = newRelMatrix;
            elif (sampleType == 'dps'):
                nextNodeRMSE[nodeCand] = diff;

            subgraph.remove_node(nodeCand);

        if (sampleType == 'dps'):
            #print nextNodeRMSE;
            rmseSum = 0.0;
            for node in nextNodeRMSE:
                rmse = nextNodeRMSE[node];
                rmseSum += rmse;

            randomDec = random.uniform(0.0, rmseSum);

            #print "sum: %.2f, random: %.2f" % (rmseSum, randomDec);

            rmseSum = 0.0;
            for node in nextNodeRMSE:
                rmse = nextNodeRMSE[node];
                rmseSum += rmse;
                if randomDec < rmseSum:
                    nextNode = node;
                    break;               
        
        #print "Choose %d" % nextNode;               
        addNodeAndRelEdges(graph, subgraph, nextNode);

        if (subgraph.number_of_nodes() % 10 == 0):            
            subRelMatrix = gen_full_rel_matrix(subgraph, nodeTypeCount, edgeTypeCount);

            diff = rmseDiff(fullRelMatrix, subRelMatrix);

            print "Nodes: %d, Edges: %d, RMSE: %.2f" % (subgraph.number_of_nodes(), subgraph.number_of_edges(), diff);

    return subgraph;

def rmseDiff(origRelMatrix, newRelMatrix):
    diff = 0.0;

    for rowIndex in range(origRelMatrix.row_count()):
        for colIndex in range(origRelMatrix.col_count()):
            cellDiff = origRelMatrix.get_item(rowIndex, colIndex) - newRelMatrix.get_item(rowIndex, colIndex);

            diff += cellDiff*cellDiff;

    diff /= (origRelMatrix.row_count() * origRelMatrix.col_count());

    return diff ** 0.5;
            

    

if __name__ == '__main__':
    sys.exit(main())
