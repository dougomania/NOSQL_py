# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 16:35:50 2016

@author: Doug
"""


import pandas as pd
import pprint
import numpy as np


def load_data():
    dataframe = pd.read_pickle('percentage.p')
    return dataframe

def load_test():
    dataframe= pd.read_pickle('test_data.p')  
    return dataframe

def smaller_dataset(df):
    df = df[:150000]
    df.to_pickle('test_data.p')
    
    
def clean_data(df):
    pass
    
def get_percentage(df):
    cindex = df.columns
    gen1 = []
    gen2 = []
    gen3 = []
    #print cindex    
    print df
    
    for i in range(len(df)):
        if df[cindex[1]][i] != "(null)" :
            gen1.append( float(df[cindex[1]][i])/float(1253)*100)
        else:
            gen1.append("(null)")
        if df[cindex[2]][i] != "(null)":  
            gen2.append(float(df[cindex[2]][i])/float(1253)*100)
        else:
            gen2.append("(null)")
        if df[cindex[3]][i] != "(null)":  
            gen3.append(float(df[cindex[3]][i])/float(1253)*100)
        else:
            gen3.append("(null)")
                
    df["gen1 %"] = gen1
    df["gen2 %"] = gen2
    df["gen3 %"] = gen3
    
    df.to_pickle('percentage.p')
    


def get_bins(df):
    g1_bin = (pd.cut(df["gen1 %"], np.arange(0, 110, 10)))
    g2_bin = (pd.cut(df["gen2 %"], np.arange(0, 110, 10)))
    g3_bin = (pd.cut(df["gen3 %"], np.arange(0, 110, 10)))
    
    g1_count = pd.value_counts(g1_bin)
    g2_count = pd.value_counts(g2_bin)
    g3_count = pd.value_counts(g3_bin)    
    
    g1_count = g1_count.divide(2)
    g2_count = g2_count.divide(2)
    g3_count = g3_count.divide(2)
    
    g1 = g1_count.reindex(g1_bin.cat.categories)
    g2 = g2_count.reindex(g2_bin.cat.categories)
    g3 = g3_count.reindex(g3_bin.cat.categories)
    
    g1g2 = g1.add(g2)
    g1_3 = g1g2.add(g3)
    
    
    return g1, g2, g3, g1_3
    
def save_data(g1,g2,g3,g1_3):
    g1= g1.to_frame()
    g2 = g2.to_frame()
    g3 = g3.to_frame()
    g1_3 = g1_3.to_frame()
    
    g1.to_pickle('g1_histo.p')
    g2.to_pickle('g2_histo.p')
    g3.to_pickle('g3_histo.p')
    g1_3.to_pickle('gall_histo.p')    

def print_histo():
    g1 = pd.read_pickle('g1_histo.p')
    g2= pd.read_pickle('g2_histo.p')
    g3= pd.read_pickle('g3_histo.p')
    gall= pd.read_pickle('gall_histo.p')
    
    print g1
    print g2
    print g3
    print gall

df = load_data() 
a,b,c,d = get_bins(df)
save_data(a,b,c,d)
print_histo()  
#print(len(df))


