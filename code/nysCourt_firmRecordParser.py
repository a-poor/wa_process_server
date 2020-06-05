#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 18:29:45 2018

@author: Austin
"""

import os
from bs4 import BeautifulSoup
from bs4 import Comment
import json


testRecordsPath = 'testrecords.html'


def soupFromFile(filename):
    """Reads file at filename and returns soup (If no file, returns None)"""
    if not os.path.exists(filename):
        return None
    with open(filename) as openFile:
        readFile = openFile.read()
    soup = BeautifulSoup(readFile, 'html.parser')
    return soup


def createTableFromSoup(soup):
    table = []
    
    # Find table starting point comment
    listStartComment = ' header row '
    commentList = soup.find_all(string=lambda text:isinstance(text, Comment))
    listStart = commentList[commentList.index(listStartComment)].next_element.next_element
    #print('List start:', listStart.prettify())
    
    # Find column headers
    soupHeaders = listStart.find_all('th')
    tableHeaders = []
    for x in soupHeaders:
        tableHeaders.append(x.get_text().strip())
    tableHeaders[0] = 'Entry Number'
    tableHeaders[-1] = 'Motion Decision'
    table.append(tableHeaders)
    
    # Create a list of soup table rows
    soupTableRows = listStart.find_all('tr')
    #print('len soupTableRows', len(soupTableRows))
    for i in range(1, len(soupTableRows)):
        currentRow = soupTableRows[i]
        soupRow = currentRow.find_all('td')
        rowHolder = []
        for j in range(len(soupRow)):
            currentVal = soupRow[j].get_text().strip()
            #print(currentVal)
            if j == 0:
                rowHolder.append(int(currentVal))
            elif j == 3:
                rowHolder.append(separateCaseStatus(currentVal))
            elif j == 8:
                rowHolder.append(reformatDate(currentVal))
            else:
                rowHolder.append(currentVal)
        table.append(rowHolder)
        
    return table


def tableToDict(table):
    """Creates a dictionary version of the table."""
    caseRecords = {}
    backupDictSave = []    # Place to put case dicts if they're going to be overwritten
    keys = table[0]
    #tableLength = len(keys)
    for rowNum, row in enumerate(table):
        if rowNum > 0:
            tempDict = {}
            for colNum, val in enumerate(row):
                tempDict[keys[colNum]] = val
            if not tempDict['Index Number'] in caseRecords:
                caseRecords[tempDict['Index Number']] = tempDict
                del caseRecords[tempDict['Index Number']]['Index Number']
            else:
                backupDictSave.append(tempDict)
    if len(backupDictSave) > 0: print(backupDictSave)
    return caseRecords



def separateJudgePart(caseRecordsDict):
    """Modifies caseRecordsDict to make 'Judge' and 'Part' separate elements."""
    
    return


def reformatDate(dateString):
    """Converts the table date string 'mm/dd/yyyy' to a tuple of ints: (mm, dd, yyyy)"""
    m, d, y = dateString.split('/')
    return (int(m), int(d), int(y))


def separateCaseStatus(inStatus):
    """Separates inputed case status to tuple of statuses."""
    outStatus = ()
    statusList = inStatus.split('-')
    for i in range(len(statusList)):
        statusList[i] = statusList[i].strip()
        outStatus += (statusList[i],)
    return outStatus


def htmlTableToDict(filepath):
    """Converts saved html table to dictionary (using previous functions)."""
    soup = soupFromFile(filepath)
    table = createTableFromSoup(soup)
    tableDict = tableToDict(table)
    return tableDict


def combineDictionaries(dicts):
    """Combine multiple dictionaries"""
    combinedDict = {}
    backup = []
    for dictionary in dicts:
        for k, v in dictionary.items():
            if k not in combinedDict:
                combinedDict[k] = v
            else:
                backup.append((dicts.index(dictionary), k, v))
    if len(backup) > 0: 
        print('Num duplicate dict entries: {}'.format(len(backup)))
        print('Format: (dict key, entry key, entry value)')
        for x in backup:
            print(x)
    return combinedDict


def allHtmlPathLists(directory = '.', prependDir=True):
    """Creates a list of filepaths for HTML files in directory."""
    pathList = []
    dirContents = os.listdir(directory)
    for x in dirContents:
        name, xtnsn = os.path.splitext(x)
        if xtnsn == '.html':
            filename = name + xtnsn
            pathList.append(filename)
    pathList.sort()
    if prependDir:
        for i, x in enumerate(pathList):
            pathList[i] = directory + '/' + x
    return pathList


def saveDataAsJSON(saveDict, filename):
    """Saves the dictionary as a json file"""
    if not os.path.exists(filename):
        # Check to see if it's a JSON file
        filename, extension = os.path.splitext(filename)
        if extension == '':
            extension = '.json'
            
        elif extension != '.json':
            while True:    # <––– Start REPL loop
                print('You aren\'t using a .json extension to save your file.')
                userReply = input('Are you sure you want to use "{}" as the file extension? Y/N '.format(extension)).lower().strip()
                
                if userReply == 'y' or userReply == 'yes':
                    print('Okay. Saving file…')
                    savePath = filename + extension
                    break    # <––– Stop the loop
                    
                elif userReply == 'n' or userReply == 'no':
                    print('Do you want to (r)eplace "{}" with ".json" or'.format(extension))
                    userFollowupReply = input('(a)ppend ".json" to the end? r/a ').lower().strip()
                    if userFollowupReply == 'r':
                        print('Replacing extension with ".json"…')
                        savePath = filename + '.json'
                        
                    elif userFollowupReply == 'a':
                        print('Appending ".json"…')
                        savePath = filename + extension + '.json'
                        
                    else:
                        print('I coulnt\'t understand your reply.')
                        print('Appending ".json"…')
                        savePath = filename + extension + '.json'
                        
                    break    # <––– Stop the loop
                    
                elif userReply == 'q':
                    print('Quitting function w/o saving…')
                    return None
                
                else:
                    print('Sorry, I couldn\'t understand that.\n')
        else:
            savePath = filename + extension
        
        print('dict len:', len(saveDict))
        with open(savePath, 'w') as openFile:
            json.dump(saveDict, openFile)
    
    else:
        print('Sorry, that filename is already taken.')
    
    return None
    

def fullDataSetFromFolder(filepath='.', savepath=None, returnDataSet=False):
    list_of_file_paths = allHtmlPathLists(filepath)
    #print(list_of_file_paths)
    dictList = []
    for path in list_of_file_paths:
        try:
            tmpDict = htmlTableToDict(path)
        except:
            print('Error with path:', path)
        else:
            dictList.append(tmpDict)
    fullDict = combineDictionaries(dictList)
    if savepath is None: savepath = filepath + '.json'
    saveDataAsJSON(fullDict, savepath)
    
    if returnDataSet is True:
        returnStatement = fullDict
    else:
        returnStatement = None
    return returnStatement


def createDataSets(filepath='.'):
    """Call on firm folder containing 'HTML' folder."""
    returnStatement = None
    if filepath[-1] == '/': filepath = filepath[:-1]
    if not os.path.exists(filepath):
        print('Can\'t find path: "{}"'.format(filepath))
    elif 'HTML' not in os.listdir(filepath):
        print('No folder called "HTML" in this directory.')
    else:
        rawSavePath = os.path.split(filepath)
        if rawSavePath[1] == '':
            saveFilename = os.path.split(rawSavePath[0])
        else:
            saveFilename = rawSavePath[1]
        #saveFilename += '_2018.json'
        saveFilepath = (rawSavePath[0] + '/' + rawSavePath[1] + '/JSON/', saveFilename, '.json')
        
        while os.path.exists(saveFilepath):
            a, b = os.path.splitext(saveFilepath)
            saveFilepath = a + '_01' + b
            
        htmlFolders = os.listdir(filepath+'/HTML')
        for folder in htmlFolders:
            if folder[0] == '.':
                continue # Skip hidden folders
            folderPath = filepath + '/HTML/' + folder
            directory, filename, extension = saveFilepath
            filename += folder
            saveFilepath = (directory, filename, extension)
            formattedSavePath = ''.join(saveFilepath)
            while os.path.exists(formattedSavePath):
                directory, filename, extension = saveFilepath
                if filename[-3] != '_':
                    filename += '_01'
                else:
                    version = int(filename[-2:])
                    version += 1
                    filename = filename[:-2] + str(version).zfill(2)
                saveFilepath = (directory, filename, extension)
                formattedSavePath = ''.join(saveFilepath)
            fullDataSetFromFolder(folderPath, ''.join(saveFilepath))
    return returnStatement


def run():
    # Not quite working yet…
    createDataSets('GoodFirms/BelkinBurdenWenigGoldmanLLP')
    
    
    
def readJsonToDict(filename):
    dataSet = None
    with open(filename, 'r') as readFile:
        dataSet = json.load(readFile)
    return dataSet


def importAndCombineJSON(dataSetList):
    setList = []
    aggregateSet = {}
    for file in dataSetList:
        setList.append(readJsonToDict(file))
    aggregateSet = combineDictionaries(setList)
    saveDataAsJSON(aggregateSet, '_dataSets/aggregateDataSet_01.json')
    return None

focusDirectory = '_dataSets'
dataSetList = os.listdir(focusDirectory)
for i in range(len(dataSetList)):
    dataSetList[i] = focusDirectory + '/' + dataSetList[i]
print('\n'.join(dataSetList))