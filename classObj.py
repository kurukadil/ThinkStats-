# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 14:07:28 2015

@author: smostafa
"""

# Product Structure
#
# SKU
# Product Name
# Brand
# Manufacturer
# As a list [width, depth, height, units]
# Weight
# Units

#%% Define the Product class

class Product:
    
    Version = "Ver 3.4 Rev 6"
    
    def __init__(self,sku,name,brand,manu,dims,wt,wtunits):
        self.SKU = sku
        self.Name = name
        self.Brand = brand
        self.Manufacturer = manu
        self.Dimensions = dims
        self.Weight = wt           # Should have been Weight
        self.WtUnits = wtunits
    
    def Print(self):
        out = "\nName:\t\t"+self.Name+"\nSKU:\t\t"+self.SKU+"\n"+ \
            "Brand:\t\t"+self.Brand+"\nManufacturer:\t"+self.Manufacturer+"\n\n"+ \
            "Dimensions\n"+ \
            "\tWidth:\t"+str(self.Dimensions[0])+self.Dimensions[3]+"\n"+ \
            "\tDepth:\t"+str(self.Dimensions[1])+self.Dimensions[3]+"\n"+ \
            "\tHeight:\t"+str(self.Dimensions[2])+self.Dimensions[3]+"\n\n"+ \
            "\tWeight:\t"+str(self.Weight)+self.WtUnits+"\n"
        print (out)
    
    def SetPhone(self,PhoneNum):
        # Phone number format is XXX-XXX-XXXX
    
        dgts="0123456789"
    
        BadFmt=False
        if type(PhoneNum)!=type("abc") or len(PhoneNum)!=12:
            BadFmt=True
        
        if PhoneNum[3]!="-" or PhoneNum[7]!="-":
            BadFmt=True
        
        if not ( PhoneNum[0] in dgts and PhoneNum[1] in dgts and \
                    PhoneNum[2] in dgts and PhoneNum[4] in dgts and \
                    PhoneNum[5] in dgts and PhoneNum[6] in dgts and\
                    PhoneNum[8] in dgts and PhoneNum[9] in dgts and \
                    PhoneNum[10] in dgts and PhoneNum[11] in dgts):
            BadFmt=True
        
        if BadFmt:
            print ("Wrong phone number format. Use \"xxx-xxx-xxxx\"\n")
            return False
        
        self.__PhoneNumber = PhoneNum
        
        return True
    
    def GetPhone(self):
        return self.__PhoneNumber
    
    def PrintShelfVolume(self):
        volume = self.Dimensions[0]*self.Dimensions[1]*self.Dimensions[2]
        out = "Shelf Volume = " + str(volume) + " " + \
                self.Dimensions[3] + " cubed\n"
        print (out)
        return volume
    
    def FootprintArea(self):
        return self.Dimensions[0]*self.Dimensions[1]

#%%   Create two instances           

Milk23 = Product("DAR023","VG Skim Milk","Very Good Brands","Georgia Dairy",[8,8,10,"in"],2.2,"lbs")
Cer12 = Product("CER012","VG Corn Flakes","Very Good Brands","House Products, Inc.",[9,3,11,"in"],18,"oz")

#%%    Define the MilkProduct class




class MilkProduct(Product):
    
    Category = "Dairy"
    Storage = "Refrigerated"
    
    def __init__(self,sku,name,brand=None,manu=None,dims=None,wt=None, \
        wtunits=None,vol=None,fatcat="Whole",expir=None,servsize=None, \
        numserve=None,cals=None,fatgrams=None,fatcals=None,phone=None):
        
        Product.__init__(self,sku,name,brand,manu,dims,wt,wtunits)
        
        self.Volume = vol
        self.FatCategory = fatcat
        self.ExpirationDate = expir
        self.ServingSize = servsize
        self.NumberServings = numserve
        self.Calories = cals
        self.FatGrams = fatgrams
        self.FatCalories = fatcals
        
        if phone!=None:
            self.SetPhone(phone)
       
#%%    Define the LaundreyDetergentProduct class   
    
class LaundryDetergentProduct(Product):
    
    Category = "Laundry"

    def __init__(self,sku,name,brand=None,manu=None,dims=None,wt=None, \
        wtunits=None,numloads=None,sudslevel="Not HE",form="Powder", \
        scent=None,phone=None):
        
        Product.__init__(self,sku,name,brand,manu,dims,wt,wtunits)
        
        self.NumberLoads = numloads
        self.SudsingLevel = sudslevel
        self.PhysicalForm = form
        self.Scent = scent
        
        if phone!=None:
            self.SetPhone(phone)

#%%   Create two instances     

Milk23 = MilkProduct("DAR023","VG Skim Milk","Very Good Brands", \
        "Georgia Dairy",[8,8,10,"in"],2.2,"lbs","1Gal","Skim","2014-09-27", \
        8,16,90,0,0,"305-735-4353")
        
Det16 = LaundryDetergentProduct("LAU016","VG Laundry Detergent", \
        "Very Good Brands",dims=[9,3,11,"in"],wt=18,wtunits="oz", \
        numloads=72,sudslevel="HE",form="Liquid")
    