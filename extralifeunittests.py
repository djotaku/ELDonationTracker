import unittest
import json
import time
import unicodedata
import urllib.request
import extralifedonations

class regressionTestCase(unittest.TestCase):
    #this uses my JSON from the end of 2018 as a check to make sure it can at least handle that
    def setUp(self):
        f = open('/home/ermesa/bin/python/extralife/testJSON/endof2018_participant.json')
        self.participantJSON = json.load(f)
        f.closed
        f = open('/home/ermesa/bin/python/extralife/testJSON/endof2018_donations.json')
        self.donationsJSON = json.load(f)
        f.closed
    
    def test_totalraised(self):
        self.assertEqual(extralifedonations.ParticpantTotalRaised(self.participantJSON)[0],'$380.00')
        
    def test_participantgoal(self):
        self.assertEqual(extralifedonations.ParticipantGoal(self.participantJSON)[0],"$750.00")
        
    def test_ParticipantLastDonorNameAmnt(self):
        self.assertEqual(extralifedonations.ParticipantLastDonorNameAmnt(self.donationsJSON)[0],"Eric Mesa - $2.00")
    
    def tearDown(self):
        print("tearing up")
    
if __name__ == '__main__':
    unittest.main(verbosity=2)

#things to test:
#for ParticipantLastDonorNameAmnt and any function that reads in names - can the names have characters outside ascii? what about emojis?
#for ParticipantLastDonorNameAmnt and any functions that deal with donations amounts - can they deal with a hidden donation amount? (it will be None in the JSON)
#in any of the functions that print messages - can they deal with emojis and characters outside ascii?
