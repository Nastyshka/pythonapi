import sys
#sys.path.insert(1, 'C:/DeepFun_v2/DeepFaceLab_NVIDIA')
import subprocess
from DFM_dm import saveInQueue

def doURL (celeb, vidUrl) :
    print ('>>> doURL! ' + celeb + ' ' + vidUrl)

def doURLTime (celeb, vidUrl, cutStartMin, cutStartSec, cutEndMin, cutEndSec) :
    print ('>>> doURLTime! ' + celeb + ' ' + vidUrl)
    print('>> cut between> {} : {} and {} : {}'.format (cutStartMin, cutStartSec, cutEndMin, cutEndSec))

def doFile (title, celeb, videoFileName, usr, tags) :
    print ('>>> doFile! ' + celeb )
    #subprocess.Popen("C:/Users/rober/Desktop/pythonapi/pythonapi/3.bat",creationflags=subprocess.CREATE_NEW_CONSOLE)
    # test("TEST", videoFileName, int(celeb))
    saveInQueue(title, videoFileName, celeb, usr, tags)

def doFileTime (celeb, cutStartMin, cutStartSec, cutEndMin, cutEndSec) :
    print ('>>> doFileTime! ' + celeb )
    print('>> cut between> {} : {} and {} : {}'.format (cutStartMin, cutStartSec, cutEndMin, cutEndSec))
