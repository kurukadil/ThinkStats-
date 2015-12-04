# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 21:27:27 2015

@author: Akter
"""
"""
    Respondents Class collect All the information required to call 'ReadFile'
    of the Table class which actually read every single line from the data file
    and make a table. 
"""

import Table


#table= Table.Table

class Respondents(Table.Table):
    """
      Represent the respond table by creating respondent table
    """
    def ReadRecords(self, data_dir='.', n=None):
        filename= self.GetFilename()
        self.ReadFile (data_dir, filename, self.GetFields(), Respondents, n)
        
    def GetFilename(self):
        return '2002FemResp.dat'
        
    def GetFields (self) :
        """
           Returns tuple specifying the field to extract. 
           
           The elements of the tuple are field, start,end, case.
           field is the name of the variable
           start and end are the indices as specified in the NSFG (data source) docs
           cast is a callable that converts the result to int, float, etc
        """
        return [
                ('caseid', 1, 12, int),
               ]
    