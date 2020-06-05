#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 11:57:07 2018

@author: Austin
"""

import json
import matplotlib
import string

# Read in JSON dataset as a dict
filepath_aggregateDataSet = '_dataSets/aggregateDataSet_01.json'
def read_JSON_dataset(filepath):
    with open(filepath, 'r') as openFile:
        aggregateDataSet = json.load(openFile)
    return aggregateDataSet
# aggregateDataSet = read_JSON_dataset(filepath_aggregateDataSet)   # <––––––– Uncomment to import json data


def readCsvAsDict(csvPath):
    tableList = []
    with open(csvPath, 'r') as openFile:
        readFile = openFile.read()
    rowSplit = readFile.split('\n')
    for row in rowSplit:
        tableList.append(row.split(','))
    for y in range(len(tableList)):
        for x in range(len(tableList[y])):
            tableList[y][x] = tableList[y][x].replace(';',',')
    dictKeys = []
    caseKeys = tableList.pop(0)
    for row in tableList:
        dictKeys.append(row[0])
    csvDict = {}
    '''for key in dictKeys:
        csvDict[key] = {}
        for x in caseKeys:
            csvDict[key][x] = None'''
    for row in tableList:
        tempDict = {}
        for i, col in enumerate(row):
            if i != 0:
                tempDict[caseKeys[i]] = col
        csvDict[row[0]] = tempDict
    return csvDict

def saveDictToJSON(dct, filename):
    import os
    if not os.path.exists(filename):
        with open(filename, 'w') as writeFile:
            json.dump(dct, writeFile)
    else:
        print("File already exists.")
    return

# Functions for JSON to CSV
def dictEntryToString(dctKey, dct, columnList):
    """Turns one dict entry (who's value is also a dict) into a csv line."""
    stringEntry = ''
    entryList = []
    entryList.append(dctKey)
    for i, col in enumerate(columnList):
        if i == 0:
            continue
        else:
            if col not in dct:
                continue
            elif col == 'AppearanceDate':
                entryVal = '(' + '/'.join(map(str, dct[col])) + ')'
            elif isinstance(dct[col], list):
                entryVal = ' | '.join(map(str, dct[col]))
            elif col == 'Judge/Part':
                entryVal = dct[col]
                entryVal = entryVal.replace('\n\n', ' | ')
            else:
                entryVal = dct[col]
            entryList.append(entryVal)
    try:
        stringEntry = ';'.join(entryList)
    except:
        print('Error:', entryList)
    return stringEntry

def fullDictToCSV(dct):
    """Calls previous function for each entry in a dict. Returns full CSV."""
    rows = []
    for key in dct.keys():
        rows.append(key)
    columns = []
    for x in dct[rows[0]].keys():
        columns.append(x)
    columns[0] = 'Case ID'
    
    csvFile = ''
    csvCols = ';'.join(columns)
    csvFile += (csvCols + '\n')
    for entry in rows:
        csvLine = ''
        csvLine += dictEntryToString(entry, dct[entry], columns)
        csvFile += (csvLine + '\n')
    
    return csvFile


def normalizeFirmName(firmName):
    '''Takes a firm name as input and returns a normalized list of words, for comparison.'''
    normName = ''
    for char in firmName:
        if char not in string.punctuation:
            normName += char
        else:
            normName += ' '
    normName = normName.lower().split()
    return normName


def compareWords(s1, s2):
    """How similar are s1 and s2. (Assume single words)"""
    similarity = 0
    if len(s1) > len(s2):
        iterWord = s2
        compWord = s1
    else:
        iterWord = s1
        compWord = s2
        
    i = 0   # Index for iterWord
    j = 0   # Index for compWord
    while i < len(iterWord) and j < len(compWord):
        if iterWord[i] in compWord:
            
            i += 1
            j += 1
        else:
            
            i += 1
    
    pctSimilar = int((similarity/len(iterWord) * 100))
    return pctSimilar


def compareFirmNames(f1, f2):
    """Compares two firm names. (Assumes they're lists of words.)"""
    return

def findAcronyms(dct):
    """Look for possible acronyms. (len < 3/4/5)"""
    return


def stringCompareTest(s1, s2):
    
    sameString = ''
    if len(s1) > len(s2):
        iterWord = s2 
    else:
        iterWord = s1
    lastSameLetter = 0
    while lastSameLetter < len(iterWord):
        i = lastSameLetter
        while i < len(iterWord):
            if s1[i] == s2[i]:
                sameString += s1[i]
            else:
                sameString += '_'
            i += 1
        lastSameLetter = len(iterWord)
    return sameString