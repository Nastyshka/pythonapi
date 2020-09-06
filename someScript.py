def doURL (celeb, vidUrl) :
    print ('>>> doURL! ' + celeb + ' ' + vidUrl)

def doURLTime (celeb, vidUrl, cutStartMin, cutStartSec, cutEndMin, cutEndSec) :
    print ('>>> doURLTime! ' + celeb + ' ' + vidUrl)
    print('>> cut between> {} : {} and {} : {}'.format (cutStartMin, cutStartSec, cutEndMin, cutEndSec))

def doFile (celeb) :
    print ('>>> doFile! ' + celeb )

def doFileTime (celeb, cutStartMin, cutStartSec, cutEndMin, cutEndSec) :
    print ('>>> doFileTime! ' + celeb )
    print('>> cut between> {} : {} and {} : {}'.format (cutStartMin, cutStartSec, cutEndMin, cutEndSec))
