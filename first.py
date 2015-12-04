# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 16:30:24 2015

@author: Akter
"""

import Pregnancies
import numpy

def Mean(t):
    """Computes the mean of a sequence of numbers.

    Args:
        t: sequence of numbers

    Returns:
        float
    """
    return float(sum(t)) / len(t)

def CountLiveAndNonLiveChildren (table):
    
    NonLive=0
    FirstChildPrglength=[]
    OtherChildPrglength=[]
    
    FirstChild=Pregnancies.Pregnancies()
    OtherChild=Pregnancies.Pregnancies()
    
    for p in table.records:
        
        #print ("length of pregnancy: ", (p.prglength))
        #prglength.append(p.prglength)
        # skip non-live births
        if p.outcome!=1:
            NonLive=NonLive+1
            continue 
        
        if p.birthord==1:
            FirstChild.AddRecord(p)
            FirstChildPrglength.append(p.prglength)
        else:
            OtherChild.AddRecord(p)
            OtherChildPrglength.append(p.prglength)
            
    return FirstChildPrglength,OtherChildPrglength,FirstChild, OtherChild, NonLive

def Process(table):
    """Runs analysis on the given table.
    
    Args:
        table: table object
    """
    table.lengths = [p.prglength for p in table.records]
    table.n = len(table.lengths)
    table.mu = Mean(table.lengths)
            
def MakeTables(data_dir='.'):
    """Reads survey data and returns tables for first babies and others."""
    table = Pregnancies.Pregnancies()
    table.ReadRecords(data_dir)

    FirstChildPrglength,OtherChildPrglength,FirstChild, OtherChild, NonLive = CountLiveAndNonLiveChildren(table)
    
    return table, FirstChild, OtherChild


def ProcessTables(*tables):
    """Processes a list of tables
    
    Args:
        tables: gathered argument tuple of Tuples
    """
    for table in tables:
        Process(table)
        
        
def Summarize(data_dir):
    """Prints summary statistics for first babies and others.
    
    Returns:
        tuple of Tables
    """
    table, firsts, others = MakeTables(data_dir)
    ProcessTables(FirstChild, OtherChild)
        
    print ("Number of first babies", FirstChild.n)
    print ("Number of others", OtherChild.n)

    mu1, mu2 = FirstChild.mu, OtherChild.mu

    print ("Mean gestation in weeks:") 
    print ("First babies", mu1) 
    print ("Others", mu2)
    
    print ("Difference in days", (mu1 - mu2) * 7.0)


def main(name, data_dir='.'):
    Summarize(data_dir)
    

if __name__ == '__main__':
    import sys
    main(*sys.argv)            

table= Pregnancies.Pregnancies()
table.ReadRecords()
print("*******************************************************\n")
print ("total number of pregnancies: ", len(table.records))
FirstChildPrglength,OtherChildPrglength, FirstChild, OtherChild, NonLive=CountLiveAndNonLiveChildren(table)
print ("non live:- ",NonLive)
print ("First Child:-",len(FirstChild) )
print ("Other than first Child:-", len(OtherChild))
print(FirstChildPrglength)
print(OtherChildPrglength)


print("Average Pregnancy period for first Child (in weeks):- ", numpy.mean(FirstChildPrglength))
print("Average Pregnancy period for Other Child (in weeks):- ", numpy.mean(OtherChildPrglength))
print("On an average First child came ",24*7*(numpy.mean(FirstChildPrglength)- numpy.mean(OtherChildPrglength)),"hours late")
