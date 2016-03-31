# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 09:34:14 2016

@author: ajohnson
"""

##############
# import

import os
import csv
import glob
from os.path import basename

##############
# variables

inDir = 'C:/Users/ajohnson/Desktop/mktg625 data/orig/'
outDir = 'C:/Users/ajohnson/Desktop/mktg625 data/split/'
extList1 = ('TRX','TSX','SSX')          # already comma-delimited
extList2 = ('DSX','DSX2','WSX','WSX2')  # tab-delimited, modify to csv

##############
# subroutines

def parseFile(file):
    fileName, fileExt = os.path.splitext(file)
    baseFile = basename(fileName)
    f = open(file, 'r')
    for line in f:
        a = line.split(',')
        outName = outDir + baseFile + fileExt + '.' + a[0]
        if fileExt == '.TRX' and a[0] == '02':  #further split TRX files 
            if a[2] in ('GS','PC','PS','SC','SS'):  
                outName = outName + '.prod'
            elif a[2] == 'TX':
                outName = outName + '.tax'
            elif a[2] == 'TM':
                outName = outName + '.time'
        outFile = open(outName,'a')
        outFile.write(baseFile + ',' + line)
        
def convertToCSV(file):
    csvFile = file + '.csv'
    txtFile = csv.reader(open(file, "rb"), delimiter = '\t')
    outCsv = csv.writer(open(csvFile, 'wb'))
    outCsv.writerows(txtFile)
    return csvFile
       
##############         
# main                

for file in os.listdir(inDir):
    # parse files     
    if file.endswith(extList1):
        parseFile(inDir + file)
    # convert tab-delimited to csv then parse files
    if file.endswith(extList2):
        newFile = convertToCSV(inDir + file)
        parseFile(newFile)
        
# get unique list of file extensions in outDir   
extList = list()     
for file in os.listdir(outDir):
    fileExt = file.split('.',1)[-1]
    extList.append(fileExt)
extList = list(set(extList)) 

# concat files with like extensions into one main "all" file
for ext in extList:
    read_files = glob.glob(outDir + '*.' + ext)
    with open(outDir + 'all.' + ext, 'wb') as outfile:
        for f in read_files:
            with open(f, 'rb') as infile:
                outfile.write(infile.read())

            
