import sys
sys.path.insert(1, 'C:/DeepFun_v2/DeepFaceLab_NVIDIA')
import subprocess
from DFM_SET_CELEBApi import runWithChosenCeleb

def doURL (celeb, vidUrl) :
    print ('>>> doURL! ' + celeb + ' ' + vidUrl)

def doURLTime (celeb, vidUrl, cutStartMin, cutStartSec, cutEndMin, cutEndSec) :
    print ('>>> doURLTime! ' + celeb + ' ' + vidUrl)
    print('>> cut between> {} : {} and {} : {}'.format (cutStartMin, cutStartSec, cutEndMin, cutEndSec))

def doFile (celeb) :
    print ('>>> doFile! ' + celeb )
    #subprocess.Popen("C:/Users/rober/Desktop/pythonapi/pythonapi/3.bat",creationflags=subprocess.CREATE_NEW_CONSOLE)
    runWithChosenCeleb(celeb)

def doFileTime (celeb, cutStartMin, cutStartSec, cutEndMin, cutEndSec) :
    print ('>>> doFileTime! ' + celeb )
    print('>> cut between> {} : {} and {} : {}'.format (cutStartMin, cutStartSec, cutEndMin, cutEndSec))
