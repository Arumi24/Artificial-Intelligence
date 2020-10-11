###################################################################
# @Author: Aymen Rumi                                             #
# @Date: 10-10-2020 (Friday October 10th, 2020)                   #
# @Email: aymen.rumi@mail.mcgill.ca                               #
# @Last Modified: 10-11-2020 (Saturday October 11th, 2020)        #
###################################################################

"""
This file contains code for a data processing object used for Mistplay Data Engineering Challenge
Object will be called to process data according to Mistplay requirements

This object may be used to process any dataset that adhere to proper file format. Futher methods may be added to deal with future data processing needs


Documentation:

    class DataPrepocessor:
        
        def __init__()              -initializes object 
                                
        def importData()            -import data into object

        def printColumnNames()      -print data columns
                                
        def countDuplicates()       -count duplicate data entries in given column
                                
        def removeDuplicates()      -remove duplicate entries in given column
                                
        def addRank()               -add rank of numerical column

        def anonymizeColumn()       -encrypt a column

        def decryptColumn()         -decrypt encrypted column

        def decryptEntry()          -decrypt encrypted data entry

        def invertedIndex()         -create inverted index table

        def saveData()              -save dataset 

        def JSONtoParquet()         -convert JSON to parquet

        def getEncryptionKeys()     -return encryption keys for encrypted column

        def getData()               -return data


"""



# imported packages
# Requirements: Python Data Structure, Regex, Encryption, JSON reader, Parquet reader, JSONtoParquet converter

import snappy
import re
import json
import fastparquet
import pandas as pd  """ PySpark  dataframe may be used if data being processed is considered Big Data"""
from cryptography.fernet import Fernet
from json2parquet import convert_json


# User must call object and use necessary methods to process/transform data as user desires

# Object contains methods that give user information about dataset, methods that help process/transform data according
# according to Mistplay requirements

class DataPrepocessor(object):
    
    # Object initialization, import JSON data as through File Path or URL, or import Parquet data
    # Data is saved into pandas dataframe for easier processing
    # User needs to import data for preprocessing

    def __init__(self,filePath=None,url=None,parquet=False):

        if parquet==False:
            if filePath!=None:
                self.df=pd.read_json(filePath, lines=True) 
            elif url!=None:
                self.df = pd.read_json(url,lines=True)
            else: 
                print("Please Initialize Object with JSON Data (filePath or URL)")
        else:
            self.df=pd.read_parquet(file, engine='fastparquet')

        self.encrypted=[]
        self.encryptionKeys=dict()
            
    
    # Method to import dataset into object if user did not do so in object initialization or needs to import new dataset

    def importData(self,filePath=None,url=None,parquet=False):
        
        if parquet==False:
            if filePath!=None:
                self.df=pd.read_json(filePath, lines=True) 
            elif url!=None:
                self.df = pd.read_json(url,lines=True)
            else: 
                self.df=None
                print("Please Insert JSON Data (filePath or URL)")
        else:
            self.df=pd.read_parquet(file, engine='fastparquet')
            
        
    # Method to print colummn names (information for user)
    
    def printColumnNames(self):
        
        if self.df is None:
            print("No Data Available")
        else:
            print(list(self.df.columns)) 
    
    
    # Method to count duplicates by column (information for user)
    
    def countDuplicates(self, colName):
        
        if self.df is None:
            print("No Data Available")
        else:
            try:
                print(sum(self.df[colName].duplicated().tolist()))
            except:
                print("Column Name {} does not exist".format(colName))

    
    # Method to remove duplicates by column name
        
    def removeDuplicates(self, columnName):
        
        if self.df is None:
            print("No Data Available")
        else:
            try:
                self.df=(self.df[~self.df[columnName].duplicated()])
            except:
                print("Column Name {} does not exist".format(columnName))
                    
    
    # Method to add rank column to data, -input column must contain numeric values-
    # User has option to group rank by another column
    
    def addRank(self,columnName, newColName,group_by=None):
        
        if self.df is None:
            print("No Data Available")
        else:
            if group_by==None:
                self.df[newColName] = self.df[columnName].rank(ascending=False).astype(int)
            else: 
                self.df[newColName] = self.df.groupby(group_by)[columnName].rank("dense", ascending=False).astype(int)
            
          
    # Method to anonymize column with key provided by user, key is saved in dictionary for future use 
    # User has option to save a file with the key
    
    def anonymizeColumn(self,columnName,saveToFile=False,keyName=None):
        
        if columnName not in self.encrypted:
            key = Fernet.generate_key()
            if saveToFile==True:
                fileName=keyName+".key"
                with open(fileName, "wb") as key_file:
                    key_file.write(key)

            f = Fernet(key)

            for i in range(len(self.df[columnName])):
                self.df[columnName][i]=(f.encrypt(self.df[columnName][i].encode()))

            self.encrypted.append(columnName)
            self.encryptionKeys[columnName] = key
            self.df=self.df.rename(columns = {columnName:columnName+"_anon"})
        else:
            print("Column is already encrypted")
        
        
    # Decrypting a column

    def decryptColumn(self,columnName):
        
        col_name=re.sub('_anon', '', columnName)
        key=self.encryptionKeys[col_name]

        f = Fernet(key)
        
        for i in range(len(self.df[columnName])):
                self.df[columnName][i]=(f.decrypt(self.df[columnName][i])).decode("utf-8")

        self.encrypted.remove(col_name)
        self.df=self.df.rename(columns = {columnName:re.sub('_anon', '', columnName)})

        del self.encryptionKeys[col_name]
    

    # Decrypting an encrypted entry for a certain column

    def decryptEntry(self,entry,columnName):
        
        col_name=re.sub('_anon', '', columnName)
        key=self.encryptionKeys[col_name]

        f = Fernet(key)

        return f.decrypt(entry).decode("utf-8")
        
    
    # Method to create inverted index table, for given key and value. Table saved as JSON file, user has option to save as Parquet file
    
    def invertedIndex(self,keyColumn, valueColumn, fileName,parquet=True):
        
        
        if self.df is None:
            print("No Data Available")
        else:
            inverted_index= dict()
            for index,row in self.df.iterrows():
                if row[keyColumn] in inverted_index:
                    inverted_index[row[keyColumn]].append(row[valueColumn])
                else:
                    inverted_index[row[keyColumn]]=[row[valueColumn]]
            JSONfileName=fileName+".json"

            with open(JSONfileName, 'w') as outfile:
                json.dump(inverted_index, outfile)

            if parquet==True:
                convert_json(JSONfileName,fileName+"parquet")
        
        
    # Method to save processed data file
    # User can save file as either
    #                               1. JSON
    #                               2. CSV
    #                               3. Parquet
     
    def saveData(self,fileName,JSON=True,CSV=False,parquet=False):
        
        if JSON==True:
            fileName=fileName+".json"
            self.df.to_json(fileName, orient='records',date_format='iso' , lines=True)
            
        if CSV==True:
            fileName=fileName+".csv"
            self.df.to_csv(fileName, orient='records',date_format='iso' , lines=True)
            
        if parquet==True:
            fileName=fileName+".parquet"
            self.df.to_parquet(fileName)


    # Method to convert JSON file to Parquet file

    def JSONtoParquet(jsonFile,fileName):
        convert_json(jsonFile,fileName+".parquet")
    
    
    # Method to return encryption keys  

    def getEncryptionKeys(self):
        return self.encryptionKeys

    # Method to return data beinf processed on

    def getData(self):
        return self.df


"""
This code follows object oriented design standard

"""