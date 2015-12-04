# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 17:18:34 2015

@author: Akter
"""
"""
   The Table class of the python file, Given the
   directory of the data file, Read each line from 
   the data file and and make a record or data table
   Each line of data is consider as a record and store in table as an object
   This oparation start with Calling the function "ReadFile"
"""
import os
import gzip


class Table (object):
    """present a table as a list of objects (each line is a record, and each
    record is stored as an object in the table class)"""
    def __init__(self):
        self.records = []
        
    def __len__(self):
        return len(self.records)
        
    def ReadFile(self,data_dir,filename,fields, constructor, n=None):
        """ given all the above args (info) it reads a compressed data file and 
            build one object per record
            
            Args: 
            data_dir: string directory name (complete directory: i.e '.' for current directory)
            filename: string name of the file to read (i.e "./2002FemPreg.dat")
            Fields: sequence of (name, start,end,case)
                explanation: a line in data file appears like: 1234045678
                and there is a field called 'case-id' now imagine:
                first 5 digit of the line is under case_id field; you can defind that using: Field ('case-id',0,3,int)
                next 5 digit of the line is under children_weight field; define that using ('children_weight',4,9,int)
                Then the table will look like: 
                   
                    case-id  children_weight
                    12340     45678
                that will become one record object 
            constructor : what kind of object to create     
            
            """
        filename= os.path.join(data_dir, filename)  # gives filename 
        if filename.endswith('gz'):
            # for windows after downloading the data file it store as .dat.gz
            fp=gzip.open(filename)
        else:
            fp = open(filename)
            
        for i, line in enumerate (fp) : # line represents left and to right end of a line of a doc
            if i== n : # i represents indices of each line ie. 0 1 2 3 .... 
                break
            record = self.MakeRecord (line, fields, constructor)
            self.AddRecord (record)
            
        fp.close()
        return self.records
        
    def MakeRecord(self, line, fields, constructor):
        """ scans a line and returns and object with appropriate fields.
            Args: 
            line : string line from a data file
            fields: sequence of (name, start,end,cast) tuple specifying the fields to extract see in 'Readfile' function
            constructor : what kind of object(record as a boject) to make: Respondents or Pregnancies    
            Returns :
            Record with appropriate fields. 
       """     
        record_obj = constructor() # create and object of the value of the arg constructor passed by the calling
        for (field,start,end,cast) in fields : 
            """
             fields tuple comes as [('caseid',1,12,int)]
             field- represent first item in the tuple- caseid'
             star - represents second item in the tuple - 1
             end - represents third item in the tuple - 12. and so on
            """
            try:
                s = line [start-1:end]
                val = cast(s) # line will be cast appropriately as instructed by calling
                
            except ValueError:
                val= 'NA'
            
            setattr(record_obj,field,val)  
                
        return record_obj
        
    def AddRecord(self,record): 
        # A record consist of record_object; either Respondent object or Pregnancies object (all the properties of the object including fields tuple)
        # meaning each time the calling sends one line of data and its keeps on adding in table format (logically)
        # 
        """ Adds a record to this table.
            args: 
                record : an object of one of the record types 
        """
        self.records.append(record)
        
        
    
         
          
        
      
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
         