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

# retrieving data
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('adfdfm-bf958f34c7c0.json', scope)
client = gspread.authorize(creds)

sheet = client.open('ADFDFMQueue').sheet1

def test(user,videoName,celebrityNum):
    sheet.delete_row(1)
    titles = sheet.col_values(1)
    
    sheet.update('H1', len(titles))
    
    sheet.update('A'+str(len(titles)+1), user)
    sheet.update('B'+str(len(titles)+1), videoName)
    sheet.update('C'+str(len(titles)+1), celebs[celebrityNum-1])
