import networkx as nx;
from networkx import *;
import sys;
from matrix import *;
import random;
from util import *;
path = '../data/sample_poga_hepth_';
def main():

    if (len(sys.argv) < 4):
        print "python gen_rel_matrix.py dataFile sampleSize sampleType(dms or dps)";
        return;
    
    dataSrc = sys.argv[1];
    k = int(sys.argv[2]);
    sampleType = sys.argv[3];

    [graph, e_type, n_type, nTypes, eTypes] = read_data(dataSrc);

    #stats(graph, e_type, n_type, nTypes, eTypes);
    
    #fullRelMatrix = gen_full_rel_matrix(graph, e_type, n_type, len(nTypes), len(eTypes));

    
    print "Node types: %d" % len(nTypes);
    print "Edge types: %d" % len(eTypes);
    
    print "Node Count: %d" % graph.number_of_nodes();
    print "Edge Count: %d" % graph.number_of_edges();
   
    #print fullRelMatrix;

    subgraph = sampling(graph, e_type, n_type, nTypes, eTypes, k, sampleType);
    #path = '../data/sample_poga_acad_';
    #write_edgelist('../data/sample_poga_acad_1.dat', subgraph);    
    #write_dict('../data/sample_poga_acad_1.edgetype', subgraph, e_type, 1);
    #write_dict('../data/sample_poga_acad_1.nodetype', subgraph, n_type, 1);
    
    subRelMatrix = gen_full_rel_matrix(subgraph, e_type, n_type, len(nTypes), len(eTypes));

    print subRelMatrix;

def sampling(graph, e_type, n_type, nTypes, eTypes, k, sampleType):
    fullRelMatrix = gen_full_rel_matrix(graph, e_type, n_type, len(nTypes), len(eTypes));

    sampleRelMatrix = Matrix(len(nTypes)+len(eTypes), len(nTypes) + len(eTypes));

    subgraph = nx.DiGraph();

    randInt = random.randint(0, graph.number_of_nodes()-1);

    randomNode = graph.nodes()[randInt];

    subgraph.add_node(randomNode);

    print "Start node: %d" % randomNode;
    if (sampleType == 'dms'):
        print "Running DMS";        
    elif (sampleType == 'dps'):
        print "Running DPS";
   
    while (subgraph.number_of_nodes() < k):
        #print "-------------------Run %d" % k;
        #print subgraph.nodes();
        #print subgraph.edges();
        nextNodeCand = [];
        existingNodes = subgraph.nodes();
        origRelMatrix = gen_full_rel_matrix(subgraph, e_type, n_type, len(nTypes), len(eTypes));

        if (sampleType == 'dms'):            
            maxDiff = -1;
            nextNode = -1;            
        elif (sampleType == 'dps'):            
            nextNodeRMSE = {};
        else:
            print "Error! what sampling type you want????";
            exit();                   

        if len(nextNodeCand) == 0:
            for node in subgraph.nodes_iter():
                neighbor = graph.successors(node);

                for nei in neighbor:
                    if not nei in existingNodes:
                        nextNodeCand.append(nei);

                neighbor = graph.predecessors(node);

                for nei in neighbor:
                    if not nei in existingNodes:
                        nextNodeCand.append(nei);


        for nodeCand in nextNodeCand:            
            subgraph.add_node(nodeCand);

            outEdges = graph.out_edges(nodeCand);

            for start, end in outEdges:
                if end in existingNodes:
                    subgraph.add_edge(start, end);


            inEdges = graph.in_edges(nodeCand);

            for start, end in inEdges:
                if start in existingNodes:
                    subgraph.add_edge(start, end);

            newRelMatrix = gen_full_rel_matrix(subgraph, e_type, n_type, len(nTypes), len(eTypes));

            diff = rmseDiff(origRelMatrix, newRelMatrix);

            #print "Max diff: %.2f, diff: %.2f, edge: %d, %d" % (maxDiff, diff, edgeCand[0], edgeCand[1]);


            if (sampleType == 'dms'):
                if (diff > maxDiff):
                    nextNode = nodeCand;
                    maxDiff = diff;
            elif (sampleType == 'dps'):
                nextNodeRMSE[nodeCand] = diff;


            subgraph.remove_node(nodeCand);

            
        #now add the node and edges
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
        subgraph.add_node(nextNode);
        outEdges = graph.out_edges(nextNode);

        for start, end in outEdges:
            if end in existingNodes:
                subgraph.add_edge(start, end);


        inEdges = graph.in_edges(nextNode);

        for start, end in inEdges:
            if start in existingNodes:
                subgraph.add_edge(start, end);


        if (subgraph.number_of_nodes() % 10 == 0):            
            subRelMatrix = gen_full_rel_matrix(subgraph, e_type, n_type, len(nTypes), len(eTypes));

            diff = rmseDiff(fullRelMatrix, subRelMatrix);

            print "Nodes: %d, Edges: %d, RMSE: %.2f" % (subgraph.number_of_nodes(), subgraph.number_of_edges(), diff);
            if subgraph.number_of_nodes()%40==0:
                write_edgelist(subgraph, path+str(subgraph.number_of_nodes()/40)+'.dat');    
                write_dict(path+str(subgraph.number_of_nodes()/40)+'.edgetype', subgraph, e_type, 1);
                write_dict(path+str(subgraph.number_of_nodes()/40)+'.nodetype', subgraph, n_type, 0);

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
