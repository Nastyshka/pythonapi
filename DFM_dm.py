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

chrome_path = "C:/Users/rober/Desktop/chromedriver.exe"

celebs = ["daisy ridley", "emma stone", "gal gadot", "K AOA CHANMI", "emma watson"] # list of celebs (another one)
CELEB_CHOISES = [('daisy ridley','Daisy Ridley'), ('emma stone', 'emma stone'),
 ('gal gadot','Gal Gadot'), ('K AOA CHANMI', 'K AOA CHANMI'), ('emma watson', 'Emma Watson')] #Add celebrities here

STATE_CHOISES = [('REVIEW','REVIEW'), ('APPROVED', 'APPROVED'),
 ('WORKING','WORKING'), ('DONE', 'DONE')] #Add states here



# retrieving data
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('adfdfm-bf958f34c7c0.json', scope)
client = gspread.authorize(creds)

sheet = client.open('ADFDFMQueue').get_worksheet(1)

def test(user,videoName,celebrityNum):
    sheet.delete_row(1)
    titles = sheet.col_values(1)
    
    sheet.update('H1', len(titles))
    
    sheet.update('A'+str(len(titles)+1), user)
    sheet.update('B'+str(len(titles)+1), videoName)
    # sheet.update('C'+str(len(titles)+1), celebs[celebrityNum-1])
    sheet.update('C'+str(len(titles)+1), celebrityNum)

def saveInQueue(title, videoName, celebrityNum, usr):
    qSize = sheet.row_count
    print ( qSize)
    print ('>>> saveInQueue  > ' + title + ' > ' + videoName + ' > ' + usr + ' > ' + celebrityNum) 
    row = [title, videoName, celebrityNum, usr, 'REVIEW']
    sheet.append_row(row)

def deleteFromQueue(index):
    qSize = sheet.row_count
    print ( qSize)
    print ('>>> delete from Queue  > ' + str(index))
    sheet.delete_row(index)

def findUsrInQueue (usr): 
    try :
        cell = sheet.find(usr)
        print('>>>> found  > ' + str(cell.row))
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

def setVidState (vid, state) : 
    print (">>> I set state here")
    cell = sheet.find(vid)
    sheet.update_cell(cell.row, 5, state.upper())

def setDoneWithUrl (vid, url) : 
    cell = sheet.find(vid)
    print('>>>> I set done here  > ' + str(cell.row))
    sheet.update_cell(cell.row, 5, 'DONE')
    sheet.update_cell(cell.row, 6, url)