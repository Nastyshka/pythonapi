from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import urllib, os, urllib.request
import time
import re
import subprocess

import gspread

from oauth2client.service_account import ServiceAccountCredentials
import pprint
from operator import itemgetter

chrome_path = "C:/Users/rober/Desktop/chromedriver.exe"

celebs = ["daisy ridley", "emma stone", "gal gadot", "K AOA CHANMI", "emma watson"] # list of celebs (another one)
# CELEB_CHOISES = [('K APINK NAEUN','K APINK NAEUN'), ('K BLACKPINK JENNIE', 'K BLACKPINK JENNIE'),
#  ('K IU','K IU'), ('K MISS A SUZY', 'K MISS A SUZY'), ('K RED VELVET IRENE', 'K RED VELVET IRENE'), ('K RED VELVET WENDY', 'K RED VELVET WENDY')
#  , ('K TWICE MOMO', 'K TWICE MOMO'), ('K TWICE TZUYU', 'K TWICE TZUYU')] #Add celebrities here

STATE_CHOISES = [('3 REVIEW','REVIEW'), ('2 APPROVED', 'APPROVED'),
 ('1 WORKING','WORKING'), ('4 DONE', 'DONE')] #Add states here


# retrieving data
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('adfdfm-bf958f34c7c0.json', scope)
client = gspread.authorize(creds)

sheet = client.open('ADFDFMQueue').get_worksheet(2)
sheetCeleb = client.open('ADFDFMQueue').get_worksheet(1)
sheetTags = client.open('ADFDFMQueue').get_worksheet(3)

# def test(user,videoName,celebrityNum):
#     sheet.delete_row(1)
#     titles = sheet.col_values(1)
    
#     sheet.update('H1', len(titles))
    
#     sheet.update('A'+str(len(titles)+1), user)
#     sheet.update('B'+str(len(titles)+1), videoName)
#     # sheet.update('C'+str(len(titles)+1), celebs[celebrityNum-1])
#     sheet.update('C'+str(len(titles)+1), celebrityNum)

def saveInQueue(title, videoName, celebrityNum, usr, tags):
    qSize = sheet.row_count
    print ( qSize)
    print ('>>> saveInQueue  > ' + title + ' > ' + videoName + ' > ' + usr + ' > ' + celebrityNum) 
    row = [title, videoName, celebrityNum, usr, '3 REVIEW', tags]
    sheet.append_row(row)
    print ('>>> saveInQueue  > ' + str(qSize) + ' > ' + str(sheet.row_count))
    sortSheetData()

def deleteFromQueue(index):
    qSize = sheet.row_count
    print ( qSize)
    print ('>>> delete from Queue  > ' + str(index))
    sheet.delete_row(index)

def findUsrInQueue (usr): 
    try :
        cell = sheet.find(usr)
        print('>>>> found  > ' + str(cell))
        return cell.row
    except gspread.exceptions.CellNotFound:
        print('>>>> not found  > ' + usr)
        return -1

def getAllInQueue():
    return sheet.get_all_values()

def editQueueLine (data, ind): 
    print('>>> edit line ' + str(ind) + ' > ' + str(data))  
    sheet.update_cell(ind, 1, data[0])
    sheet.update_cell(ind, 3, data[2])
    sheet.update_cell(ind, 5, data[4])
    sortSheetData()

def setVidState (vid, state) : 
    print (">>> I set state here")
    cell = sheet.find(vid)
    sheet.update_cell(cell.row, 5, state.upper())
    sortSheetData()

def setDoneWithUrl (vid, url) : 
    cell = sheet.find(vid)
    print('>>>> I set done here  > ' + str(cell.row))
    sheet.update_cell(cell.row, 5, 'DONE')
    sheet.update_cell(cell.row, 6, url)
    sortSheetData()

def sortSheetData () :
    allOld = sheet.get_all_values()

    print ('>>> sort   > ' + str(sheet.row_count))
    allSorted  = sorted(allOld, key=itemgetter(4))
    i = 1
    while i < len(allOld):
       print (' > ' + str(allSorted[i]))
       i+=1
    sheet.clear()
    sheet.append_rows(allSorted)   
    return allSorted

def getCelebs ():
    allcelebs = sheetCeleb.get_all_values()
    celbCoises = []
    i=0
    while i < len(allcelebs):
        val = allcelebs[i]
        celbCoises.append((val[0], val[0]))
        i+=1
    return celbCoises

def getTags ():
    allTags = sheetTags.get_all_values()
    tagCoises = []
    i=0
    while i < len(allTags):
        val = allTags[i]
        tagCoises.append((val[0], val[0]))
        i+=1
    return tagCoises