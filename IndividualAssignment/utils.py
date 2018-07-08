import pandas as pd

from properties import get_BA_theo_properties, read_graph_from_csv

CSV_NAME = ""

def remove_last_char():
    PATH = "data/dbgen/"
    filenames = ["customer.csv", "lineitem.csv", "nation.csv", "orders.csv", "part.csv", "partsupp.csv", "region.csv", "supplier.csv"]
    for filename in filenames:
        filepath = PATH+filename
        with open(filepath, 'r') as infile:
            data = infile.readlines()
            for i in range(len(data)):
                data[i] = data[i][:len(data[i])-2] + data[i][len(data[i])-1:]
            
        with open(filepath, 'w') as outfile:
            outfile.writelines(data)
    
    
def remove_header(data):
    data.to_csv(CSV_NAME+".csv", header=False, index=False)
    
def remove_column(data):
    data = data.drop(data.columns[0],axis=1)
    return data

def shrink_network(data, min_no, max_no):
    print(data.shape)
    data = data.drop(data[data._start < min_no].index)
    data = data.drop(data[data._start > max_no].index)
    data = data.drop(data[data._end > max_no].index)
    data = data.drop(data[data._end < min_no].index)
    print(data.shape)
    return data
    
def get_network_hub(data, min_no, max_no):
    data1 = data.drop(data[data.iloc[:,0] != min_no].index)   
    data2 = data.drop(data[data.iloc[:,1] != max_no].index)
    data = pd.concat([data1,data2])
    return data

if __name__ == '__main__':
    data = pd.read_csv("network.csv")
    #G = read_graph_from_csv("network")
    data =  get_network_hubs(data, 150026,150026)
    data = remove_column(data)
    remove_header(data)

'''
hubs are    no of connected nodes 
150027.0    6566
150024.0    6502
150037.0    6498
150040.0    6479
150026.0    6457
150021.0    6432
150036.0
'''