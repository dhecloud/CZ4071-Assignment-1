import random
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import csv
from networkx.generators.classic import empty_graph
from collections import Counter
import numpy as np
import math
import time
import sys


def read_graph_from_csv(name):
    G = nx.read_edgelist(name, delimiter = ",", data = False, create_using=nx.Graph())
    return G

    
def get_network_hub(data, min_no, max_no):
    data1 = data.drop(data[data.iloc[:,0] != min_no].index)   
    data2 = data.drop(data[data.iloc[:,1] != max_no].index)
    data = pd.concat([data1,data2])
    return data
    
def create_subgraph(csv, nodeno):
    data = pd.read_csv(CSV_NAME,header=None)
    if CSV_NAME == "networkmine.csv":        
        nodeno = float(nodeno)
    data = get_network_hub(data, nodeno, nodeno)
    data.to_csv("data/subgraph.csv", header=False, index=False)
    
def plot_largest_hub(nodeno):
    create_subgraph(CSV_NAME, nodeno)
    G = read_graph_from_csv("data/subgraph.csv")
    pos = nx.spectral_layout(G)
    nx.draw_networkx_nodes(G,pos,node_size = 1, node_color = "blue")
    nx.draw_networkx_edges(G,pos)
    plt.savefig("graph/subgraph.png")
    
def get_model_clustering_coeff(G, node=False):
    if (node):
        cluscoeff = nx.clustering(G, node)
    else:
        cluscoeff = nx.clustering(G)
    #print(set(cluscoeff.values()))
    return cluscoeff

    
def get_model_avg_clustering_coeff(G):
    cluscoeff = get_model_clustering_coeff(G)
    cluscoeff = list(cluscoeff.values())
    cluscoeff = np.mean(cluscoeff)
    print("model average clustering coefficient is " + str(cluscoeff))
    return cluscoeff

def get_model_average_path_length(G):
    stime = time.time()
    nodeslist = G.nodes()
    dislist = []
    for node in nodeslist[:10]:
        spl = nx.shortest_path_length(G, target = node)
        dislist.append(np.mean(list(spl.values())))
    dia = np.mean(dislist)
    print("model average path length is " + str(dia))
    return dia



def plot_model_deg_dist(G, plot=True):
    degrees = nx.degree(G)
    totaldeg = sum(float(v) for k,v in degrees.items())
    
    degree_seq = sorted(degrees.values(),reverse=True)
    dmax = max(degree_seq)
    totalnodes = G.number_of_nodes()
    avgdeg = totaldeg/totalnodes
    count = dict(Counter(degree_seq))
    largestnode = list(degrees.keys())[list(degrees.values()).index(dmax)]
    plot_largest_hub(largestnode)
    print("The size of the model's largest hub is " + str(dmax))
    
    count= {k: v/totalnodes for k, v in count.items()}
    kin = (list(count.keys()))
    pkin  = (list(count.values()))
    if (plot):
        print("plotting degree distribution..")
        plt.clf()
        plt.cla()
        plt.close()
        if CSV_NAME == "networkmine":
            plt.plot((kin)[:15], (pkin)[:15], 'b-', marker = 'o')
        else:
            plt.plot((kin), (pkin), 'b-', marker = 'o')
        plt.title("Degree distribution for model")
        plt.ylabel("P(k)in")
        plt.xlabel("kin")   
        plt.savefig("graph/degree_his_model.png")
        plt.clf()
        plt.cla()
        plt.close()
        
    print("model pk-in for k-in = " + str((kin[::-1])[:4]) + " is " + str((pkin[::-1])[:4]) + " respectively.")

    return avgdeg, dmax, list((kin[::-1])[:4]), list((pkin[::-1])[:4])
    

def get_model_properties(G):
    numnodes = G.number_of_nodes()
    avgdeg, dmax, kin, pk  = plot_model_deg_dist(G, plot=True)
    apl = get_model_average_path_length(G)
    acc = get_model_avg_clustering_coeff(G)
    print('===\n')
    return [dmax, kin, pk, numnodes, acc, apl, avgdeg]
    
    
def compute_BA_deg_dist(N):
    pklist = []
    kin = range(1,N)
    for k in kin:
        pk = k ** -3
        pklist.append(pk)
        if k < 5:
            print("BA degree distribution for k = " + str(k) + " is expected to be " + str(pk))
    
    print("plotting degree distribution..")
    plt.clf()
    plt.cla()
    plt.close()
    if CSV_NAME == "networkmine":
        plt.plot((kin)[:15], (pklist)[:15], 'b-', marker = 'o')
    else:
        plt.plot((kin[:15]), (pklist[:15]), 'b-', marker = 'o')

    plt.title("Degree distribution for BA")
    plt.ylabel("p(k)in")
    plt.xlabel("kin")   
    plt.savefig("graph/degree_his_BA.png")
    plt.clf()
    plt.cla()
    plt.close()
    
    return pklist[:4]

def compute_BA_avg_path_length(N):
    num = np.log(N)
    denom = np.log(np.log(N))
    answer = num/denom
    print("BA path length for N = " + str(N) + " is expected to be " + str(answer))
    return answer

def compute_BA_avg_clustering_coeff(N):
    m = 1
    C = (m/8) * ((np.log(N)**2)/N)
    print("BA average clustering coefficient for N = " + str(N) + " is expected to be " + str(C))
    return C
    
def compute_BA_diameter(N):
    num = np.log10(N)
    denom = np.log10(np.log10(N))
    answer = num/denom
    print("BA diameter for N = " + str(N) + " is expected to be " + str(answer))
    return answer

def get_BA_theo_properties(G):
    numnodes = G.number_of_nodes()
    degdist = compute_BA_deg_dist(numnodes)
    apl = compute_BA_avg_path_length(numnodes)
    acc = compute_BA_avg_clustering_coeff(numnodes)
    dia = compute_BA_diameter(numnodes)
    print('===\n')
    return [numnodes, degdist, apl, acc, dia]
    

def compute_RN_deg_dist(N):
    pklist = []  
    p = 0.5
    avgk = p*(N-1)
    kin = range(0,N)
    kinfinal = []
    for k in kin:
        try:
            answer = (math.exp(-avgk))  * (np.power(avgk,k)) / math.factorial(k)
            pklist.append(answer)
            kinfinal.append(k)
            if k < 5:
                print("RN degree distribution for N = " + str(N) + ", k = " + str(k) + ", p = " + str(p) + " is expected to be " + str(answer)) 
        except OverflowError or RunetimeWarning:
            break
    
    #using static image for RN
    
    return pklist[:4], avgk
    
def compute_RN_avg_path_length(N):
    p = 0.5
    avgk = p*(N-1)
    num = np.log(N)
    denom = np.log(avgk)
    answer = num/denom
    print("RN path length for N = " + str(N) + " is expected to be " + str(answer))
    return answer

def compute_RN_avg_clustering_coeff(N):
    p = 0.5
    avgk = p*(N-1)
    C = avgk / N
    print("RN average clustering coefficient for N = " + str(N) + " is expected to be " + str(C))
    return C    
        
def get_RN_theo_properties(G):
    numnodes = G.number_of_nodes()
    degdist, avgk = compute_RN_deg_dist(numnodes)
    apl = compute_RN_avg_path_length(numnodes)
    acc = compute_RN_avg_clustering_coeff(numnodes)
    print('===\n')
    return [numnodes, degdist, apl, acc, avgk]

def compute_SF_deg_dist(N, kmin, gamma):
    pklist = []    
    p = 0.5
    avgk = p*(N-1)
    kin = range(1,N)
    for k  in kin:
        answer = (gamma -1) * np.power(kmin, gamma-1) * (k ** - gamma)
        pklist.append(answer)
        if k < 5:
            print("SF degree distribution for N = " + str(N) + ", k = " + str(k) + ", p = " + str(p) + " is expected to be " + str(answer)) 
            
    print("plotting degree distribution..")
    plt.clf()
    plt.cla()
    plt.close()
    if CSV_NAME == "networkmine":
        plt.plot((kin)[:15], (pklist)[:15], 'b-', marker = 'o')
    else:
        plt.plot((kin[:15]), (pklist[:15]), 'b-', marker = 'o')
    plt.title("Degree distribution for SF")
    plt.ylabel("P(k)in")
    plt.xlabel("kin")   
    plt.savefig("graph/degree_his_SF.png")
    plt.clf()
    plt.cla()
    plt.close()
    
    return pklist[:4], avgk
    
def compute_SF_largest_hub(N, kmin, gamma):
    kmax = kmin * np.power(N, (1/(gamma-1)))
    print("SF size of largest hub for N = " + str(N) + ", kmin = " + str(kmin) + " is expected to be " + str(kmax))
    return kmax
    
def compute_SF_avg_path_length(N, gamma):
    if gamma == 2:
        answer = 1
    elif gamma > 2 and gamma < 3 :
        numer = np.log(np.log(N))
        denom = np.log(gamma-1)
        answer = numer /denom
    elif gamma == 3:
        numer = np.log(N)
        denom = np.log(np.log(N))
        answer = numer / denom
    elif gamma > 3:
        answer = np.log(N)
    else:
        answer = 0
    print("SF path length for N = " + str(N) + " and gamma = " + str(gamma) + " is expected to be " + str(answer))
    return answer

        
def get_SF_theo_properties(G):
    numnodes = G.number_of_nodes()
    gamma = 2.5
    kmin = 1
    degdist, avgk = compute_SF_deg_dist(numnodes, kmin, gamma)
    apl = compute_SF_avg_path_length(numnodes, gamma)
    hub = compute_SF_largest_hub(numnodes, kmin, gamma)
    print('===\n')
    return [numnodes, degdist, apl, hub, avgk]


if __name__ == '__main__':
    
    if (sys.argv[1]):
        CSV_NAME = sys.argv[1]
        if "networkmine.csv" in CSV_NAME:
            CSV_NAME = "networkmine.csv"
    else:
        #default
        CSV_NAME = "networkmine.csv"
    G = read_graph_from_csv(CSV_NAME)
    
    model = get_model_properties(G)
    RN = get_RN_theo_properties(G)
    BA = get_BA_theo_properties(G)
    SF = get_SF_theo_properties(G)
    with open('analysis/model.txt','w') as f:
        f.write(str(model))
    f.close()
    
    with open('analysis/RN.txt','w') as f:
        f.write(str(RN))
    f.close()
    with open('analysis/BA.txt','w') as f:
        f.write(str(BA))
    f.close()
    with open('analysis/SF.txt','w') as f:
        f.write(str(SF))
    f.close()
