# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 18:13:49 2015

@author: smostafa
"""

"""This file contains code for use with "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2010 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

import sys
import gzip
import os

class Record(object):
    """Represents a record."""

class Respondent(Record): 
    """Represents a respondent."""

class Pregnancy(Record):
    """Represents a pregnancy."""

class Table(object):
    """Represents a table as a list of objects"""
    #print ("object--------",object)

    def __init__(self):
        self.records = []
        #print ("RECords", self.records )
        
    def __len__(self):
        return len(self.records)

    def ReadFile(self, data_dir, filename, fields, constructor, n=None):
        """Reads a compressed data file builds one object per record.

        Args:
            data_dir: string directory name
            filename: string name of the file to read

            fields: sequence of (name, start, end, case) tuples specifying 
            the fields to extract

            constructor: what kind of object to create
        """
        filename = os.path.join(data_dir, filename)
        print ("directory name ---------:",data_dir)

        if filename.endswith('gz'):
            fp = gzip.open(filename)
            #print (fp)
        else:
            fp = open(filename)
            print ("hellooo   :",fp)

        for i, line in enumerate(fp):
            if i == n:
                break
            #print (i)
           # print ("-------------------------------------------------")      
            #print (line) 
            #print ("-------------------------------------------------")             
            record = self.MakeRecord(line, fields, constructor)
            self.AddRecord(record)
        fp.close()

    def MakeRecord(self, line, fields, constructor):
        """Scans a line and returns an object with the appropriate fields.

        Args:
            line: string line from a data file

            fields: sequence of (name, start, end, cast) tuples specifying 
            the fields to extract

            constructor: callable that makes an object for the record.

        Returns:
            Record with appropriate fields.
        """
        obj = constructor()
        for (field, start, end, cast) in fields:
            try:
                s = line[start-1:end]
                val = cast(s)
            except ValueError:
                # If you are using Visual Studio, you might see an
                # "error" at this point, but it is not really an error;
                # I am just using try...except to handle not-available (NA)
                # data.  You should be able to tell Visual Studio to
                # ignore this non-error.
                val = 'NA'
            setattr(obj, field, val)
        return obj

    def AddRecord(self, record):
        """Adds a record to this table.

        Args:
            record: an object of one of the record types.
        """
        self.records.append(record)

    def ExtendRecords(self, records):
        """Adds records to this table.

        Args:
            records: a sequence of record object
        """
        self.records.extend(records)

    def Recode(self):
        """Child classes can override this to recode values."""
        pass


class Respondents(Table):
    """Represents the respondent table."""

    def ReadRecords(self, data_dir='.', n=None):
        filename = self.GetFilename()
        self.ReadFile(data_dir, filename, self.GetFields(), Respondents, n)
        self.Recode()

    def GetFilename(self):
        return '2002FemResp.dat'

    def GetFields(self):
        """Returns a tuple specifying the fields to extract.

        The elements of the tuple are field, start, end, case.

                field is the name of the variable
                start and end are the indices as specified in the NSFG docs
                cast is a callable that converts the result to int, float, etc.
        """
        return [
            ('caseid', 1, 12, int),
            ]

class Pregnancies(Table):
    """Contains survey data about a Pregnancy."""

    def ReadRecords(self, data_dir='.', n=None):
        filename = self.GetFilename()
        self.ReadFile(data_dir, filename, self.GetFields(), Pregnancy, n)
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


def main(name, data_dir='.'):
    resp = Respondents()
    resp.ReadRecords(data_dir)
    print ('Number of respondents', len(resp.records))

    preg = Pregnancies()
    preg.ReadRecords(data_dir)
    print ('Number of pregnancies', len(preg.records))

    
if __name__ == '__main__':

    main(*sys.argv)
    
    
    
###########################################################################
#    
#   #Pmf.py
#    
#
#import logging
#import math
#import random
#
#class _DictWrapper(object):
#    """ private. An object that contains a dictionary."""
#
#    def __init__(self, d=None, name=''):
#        # if d is provided, use it; otherwise make a new dict
#        if d == None:
#            d = {}
#        self.d = d
#        self.name = name
#
#    def GetDict(self):
#        """Gets the dictionary."""
#        return self.d
#
#    def Values(self):
#        """Gets an unsorted sequence of values.
#
#        Note: one source of confusion is that the keys in this
#        dictionaries are the values of the Hist/Pmf, and the
#        values are frequencies/probabilities.
#        """
#        return self.d.keys()
#
#    def Items(self):
#        """Gets an unsorted sequence of (value, freq/prob) pairs."""
#        return self.d.items()
#
#    def Render(self):
#        """Generates a sequence of points suitable for plotting.
#
#        Returns:
#            tuple of (sorted value sequence, freq/prob sequence)
#        """
#        return zip(*sorted(self.Items()))
#
#    def Print(self):
#        """Prints the values and freqs/probs in ascending order."""
#        for val, prob in sorted(self.d.iteritems()):
#            print (val, prob)
#
#    def Set(self, x, y=0):
#        """Sets the freq/prob associated with the value x.
#
#        Args:
#            x: number value
#            y: number freq or prob
#        """
#        self.d[x] = y
#
#    def Incr(self, x, term=1):
#        """Increments the freq/prob associated with the value x.
#
#        Args:
#            x: number value
#            term: how much to increment by
#        """
#        self.d[x] = self.d.get(x, 0) + term
#
#    def Mult(self, x, factor):
#        """Scales the freq/prob associated with the value x.
#
#        Args:
#            x: number value
#            factor: how much to multiply by
#        """
#        self.d[x] = self.d.get(x, 0) * factor
#
#    def Remove(self, x):
#        """Removes a value.
#
#        Throws an exception if the value is not there.
#
#        Args:
#            x: value to remove
#        """
#        del self.d[x]
#
#    def Total(self):
#        """Returns the total of the frequencies/probabilities in the map."""
#        total = sum(self.d.itervalues())
#        return total
#
#    def MaxLike(self):
#        """Returns the largest frequency/probability in the map."""
#        return max(self.d.itervalues())
#
#
#class Hist(_DictWrapper):
#    """Represents a histogram, which is a map from values to frequencies.
#
#    Values can be any hashable type; frequencies are integer counters.
#    """
#
#    def Copy(self, name=None):
#        """Returns a copy of this Hist.
#
#        Args:
#            name: string name for the new Hist
#        """
#        if name is None:
#            name = self.name
#        return Hist(dict(self.d), name)
#
#    def Freq(self, x):
#        """Gets the frequency associated with the value x.
#
#        Args:
#            x: number value
#
#        Returns:
#            int frequency
#        """
#        return self.d.get(x, 0)
#
#    def Freqs(self):
#        """Gets an unsorted sequence of frequencies."""
#        return self.d.values()
#
#    def IsSubset(self, other):
#        """Checks whether the values in this histogram are a subset of
#        the values in the given histogram."""
#        for val, freq in self.Items():
#            if freq > other.Freq(val):
#                return False
#        return True
#
#    def Subtract(self, other):
#        """Subtracts the values in the given histogram from this histogram."""
#        for val, freq in other.Items():
#            self.Incr(val, -freq)
#
#
#class Pmf(_DictWrapper):
#    """Represents a probability mass function.
#    
#    Values can be any hashable type; probabilities are floating-point.
#    Pmfs are not necessarily normalized.
#    """
#
#    def Copy(self, name=None):
#        """Returns a copy of this Pmf.
#
#        Args:
#            name: string name for the new Pmf
#        """
#        if name is None:
#            name = self.name
#        return Pmf(dict(self.d), name)
#
#    def Prob(self, x, default=0):
#        """Gets the probability associated with the value x.
#
#        Args:
#            x: number value
#            default: value to return if the key is not there
#
#        Returns:
#            float probability
#        """
#        return self.d.get(x, default)
#
#    def Probs(self):
#        """Gets an unsorted sequence of probabilities."""
#        return self.d.values()
#
#    def Normalize(self, fraction=1.0):
#        """Normalizes this PMF so the sum of all probs is 1.
#
#        Args:
#            fraction: what the total should be after normalization
#        """
#        total = self.Total()
#        if total == 0.0:
#            raise ValueError('total probability is zero.')
#            logging.warning('Normalize: total probability is zero.')
#            return
#        
#        factor = float(fraction) / total
#        for x in self.d:
#            self.d[x] *= factor
#    
#    def Random(self):
#        """Chooses a random element from this PMF.
#
#        Returns:
#            float value from the Pmf
#        """
#        if len(self.d) == 0:
#            raise ValueError('Pmf contains no values.')
#            
#        target = random.random()
#        total = 0.0
#        for x, p in self.d.iteritems():
#            total += p
#            if total >= target:
#                return x
#
#        # we shouldn't get here
#        assert False
#
#    def Mean(self):
#        """Computes the mean of a PMF.
#
#        Returns:
#            float mean
#        """
#        mu = 0.0
#        for x, p in self.d.iteritems():
#            mu += p * x
#        return mu
#
#    def Var(self, mu=None):
#        """Computes the variance of a PMF.
#
#        Args:
#            mu: the point around which the variance is computed;
#                if omitted, computes the mean
#
#        Returns:
#            float variance
#        """
#        if mu is None:
#            mu = self.Mean()
#            
#        var = 0.0
#        for x, p in self.d.iteritems():
#            var += p * (x - mu)**2
#        return var
#
#    def Log(self):
#        """Log transforms the probabilities."""
#        m = self.MaxLike()
#        for x, p in self.d.iteritems():
#            self.Set(x, math.log(p/m))
#
#    def Exp(self):
#        """Exponentiates the probabilities."""
#        m = self.MaxLike()
#        for x, p in self.d.iteritems():
#            self.Set(x, math.exp(p-m))
#
#
#def MakeHistFromList(t, name=''):
#    """Makes a histogram from an unsorted sequence of values.
#
#    Args:
#        t: sequence of numbers
#        name: string name for this histogram
#
#    Returns:
#        Hist object
#    """
#    hist = Hist(name=name)
#    [hist.Incr(x) for x in t]
#    return hist
#
#
#def MakeHistFromDict(d, name=''):
#    """Makes a histogram from a map from values to frequencies.
#
#    Args:
#        d: dictionary that maps values to frequencies
#        name: string name for this histogram
#
#    Returns:
#        Hist object
#    """
#    return Hist(d, name)
#
#
#def MakePmfFromList(t, name=''):
#    """Makes a PMF from an unsorted sequence of values.
#
#    Args:
#        t: sequence of numbers
#        name: string name for this PMF
#
#    Returns:
#        Pmf object
#    """
#    hist = MakeHistFromList(t, name)
#    return MakePmfFromHist(hist)
#
#
#def MakePmfFromDict(d, name=''):
#    """Makes a PMF from a map from values to probabilities.
#
#    Args:
#        d: dictionary that maps values to probabilities
#        name: string name for this PMF
#
#    Returns:
#        Pmf object
#    """
#    pmf = Pmf(d, name)
#    pmf.Normalize()
#    return pmf
#
#
#def MakePmfFromHist(hist, name=None):
#    """Makes a normalized PMF from a Hist object.
#
#    Args:
#        hist: Hist object
#        name: string name
#
#    Returns:
#        Pmf object
#    """
#    if name is None:
#        name = hist.name
#
#    # make a copy of the dictionary
#    d = dict(hist.GetDict())
#    pmf = Pmf(d, name)
#    pmf.Normalize()
#    return pmf
#
#
#def MakePmfFromCdf(cdf, name=None):
#    """Makes a normalized Pmf from a Cdf object.
#
#    Args:
#        cdf: Cdf object
#        name: string name for the new Pmf
#
#    Returns:
#        Pmf object
#    """
#    if name is None:
#        name = cdf.name
#
#    pmf = Pmf(name=name)
#
#    prev = 0.0
#    for val, prob in cdf.Items():
#        pmf.Incr(val, prob-prev)
#        prev = prob
#
#    return pmf
#
#
#def MakeMixture(pmfs, name='mix'):
#    """Make a mixture distribution.
#
#    Args:
#      pmfs: Pmf that maps from Pmfs to probs.
#      name: string name for the new Pmf.
#
#    Returns: Pmf object.
#    """
#    mix = Pmf(name=name)
#    for pmf, prob in pmfs.Items():
#        for x, p in pmf.Items():
#            mix.Incr(x, p * prob)
#    return mix
#    
#    
    
    
    
    