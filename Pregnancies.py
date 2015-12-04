# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 18:57:48 2015

@author: smostafa
"""
import Table

class Pregnancies(Table.Table):
    """Contains survey data about a Pregnancy."""

    def ReadRecords(self, data_dir='.', n=None):
        filename = self.GetFilename()
        self.ReadFile(data_dir, filename, self.GetFields(), Pregnancies, n)
        self.Recode()

    def GetFilename(self):
        return '2002FemPreg.dat'

    def GetFields(self):
        """Gets information about the fields to extract from the survey data.

        Documentation of the fields for Cycle 6 is at
        http://nsfg.icpsr.umich.edu/cocoon/WebDocs/NSFG/public/index.htm

        Returns:
            sequence of (name, start, end, type) tuples
        """
        return [
            ('caseid', 1, 12, int),
            ('nbrnaliv', 22, 22, int),
            ('babysex', 56, 56, int),
            ('birthwgt_lb', 57, 58, int),
            ('birthwgt_oz', 59, 60, int),
            ('prglength', 275, 276, int),
            ('outcome', 277, 277, int),
            ('birthord', 278, 279, int),
            ('agepreg', 284, 287, int),
            ('finalwgt', 423, 440, float),
            ]

    def Recode(self):
        for rec in self.records:

            # divide mother's age by 100
            try:
                if rec.agepreg != 'NA':
                    rec.agepreg /= 100.0
            except AttributeError:
                pass

            # convert weight at birth from lbs/oz to total ounces
            # note: there are some very low birthweights
            # that are almost certainly errors, but for now I am not
            # filtering
            try:
                if (rec.birthwgt_lb != 'NA' and rec.birthwgt_lb < 20 and
                    rec.birthwgt_oz != 'NA' and rec.birthwgt_oz <= 16):
                    rec.totalwgt_oz = rec.birthwgt_lb * 16 + rec.birthwgt_oz
                else:
                    rec.totalwgt_oz = 'NA'
            except AttributeError:
                pass