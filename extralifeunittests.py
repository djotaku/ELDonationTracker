#import unittest
#import json
#import time
#import unicodedata
#import urllib.request
import extralifedonations

#run with command: py.test-3 extralifeunittests.py

def test_answer():
    assert 3 == 5


#class regressionTestCase(unittest.TestCase):
#    #this uses my JSON from the end of 2018 as a check to make sure it can at least handle that
    #def setUp(self):
        #f = open('/home/ermesa/bin/python/extralife/testJSON/endof2018_participant.json')
        #self.participantJSON = json.load(f)
        #f.close()
        #f = open('/home/ermesa/bin/python/extralife/testJSON/endof2018_donations.json')
        #self.donationsJSON = json.load(f)
        #f.close()
    
    #def test_totalraised(self):
        #self.assertEqual(extralifedonations.ParticpantTotalRaised(self.participantJSON)[0],'$380.00')
        
    #def test_participantgoal(self):
     #   self.assertEqual(extralifedonations.ParticipantGoal(self.participantJSON)[0],"$750.00")
        
    #def test_ParticipantLastDonorNameAmnt(self):
     #   self.assertEqual(extralifedonations.ParticipantLastDonorNameAmnt(self.donationsJSON)[0],"Eric Mesa - $2.00")
    
    #def test_ParticipantTopDonor(self):
     #   self.assertEqual(extralifedonations.ParticipantTopDonor(self.donationsJSON)[0], "Katie and Dan - $126.00")
        
    #def test_Participantlast5DonorNameAmts(self):
     #   self.assertEqual(extralifedonations.Participantlast5DonorNameAmts(self.donationsJSON)[0],'''Eric Mesa - $2.00\nEric Mesa - $50.00\nDavid Mesa - $2.00\nKatie and Dan - $126.00\nDavid Mesa - $100.00\n''')
        
    #def test_Participantlast5DonorNameAmtsMessage(self):
     #   self.maxDiff = None
      #  self.assertEqual(extralifedonations.Participantlast5DonorNameAmtsMessage(self.donationsJSON)[0],'''Eric Mesa - $2.00 - b'"trying to fix a bug in my code"'\nEric Mesa - $50.00 - b'"Matching for $50 of Dave\\\'s $100"'\nDavid Mesa - $2.00 - b"It's not pretty, but I'll admit it.  I'm a one-upper."\nKatie and Dan - $126.00 - \nDavid Mesa - $100.00 - \n''')
    
    #def test_Participantlast5DonorNameAmtsMessageHorizontal(self):
     #   self.maxDiff = None
     #   self.assertEqual(extralifedonations.Participantlast5DonorNameAmtsMessageHorizontal(self.donationsJSON)[0],'''Eric Mesa - $2.00 - b'"trying to fix a bug in my code"' | Eric Mesa - $50.00 - b'"Matching for $50 of Dave\\\'s $100"' | David Mesa - $2.00 - b"It's not pretty, but I'll admit it.  I'm a one-upper." | Katie and Dan - $126.00 -  | David Mesa - $100.00 -  | ''')
    
    #def tearDown(self):
     #   print("tearing up")
    

#class emptyfieldsTestCase(unittest.TestCase):
    #this will use custom JSONs to test various cases where a field is empty - names, donation amounts, or donation messages
 #   def setUp(self):
  #      f = open('/home/ermesa/bin/python/extralife/testJSON/donations_noname1.json')
   #     self.donationsJSON_noname = json.load(f)
    #    f.close()
        
     #   self.donationJSON_noamount = None
      #  self.donationJSON_nomsg = None
    
   # def test_NoName_ParticipantLastDonorNameAmnt(self):
    #    self.assertEqual(extralifedonations.ParticipantLastDonorNameAmnt(self.donationsJSON_noname)[0],"None - $2.00")
        
    #def test_NoName_ParticipantTopDonor(self):
     #   self.assertEqual(extralifedonations.ParticipantTopDonor(self.donationsJSON_noname)[0],"None - $2.00")
    
    #def test_NoName_Participantlast5DonorNameAmts(self):
     #   self.assertEqual(extralifedonations.Participantlast5DonorNameAmts(self.donationsJSON_noname)[0],"None - $2.00\n")
        
    #def test_NoName_Participantlast5DonorNameAmtsMessage(self):
     #   self.assertEqual(extralifedonations.Participantlast5DonorNameAmtsMessage(self.donationsJSON_noname)[0],'''None - $2.00 - b\'"trying to fix a bug in my code"\'\n''')
    
    
#class specialcharactersTestCase(unittest.TestCase):
    #this will test special characters in names or donation messages. Should test: spanish punctuation, asian characters, emojis
 #   print('test case')

#class sortingTestCase(unittest.TestCase):
    #this will test that the largest donation can be found. Should test the basic case of integers as well as testing when the difference is in the decimals
 #   print('test case')


#if __name__ == '__main__':
#    unittest.main(verbosity=2)

#things to test:
#for ParticipantLastDonorNameAmnt and any function that reads in names - can the names have characters outside ascii? what about emojis?
#for ParticipantLastDonorNameAmnt and any functions that deal with donations amounts - can they deal with a hidden donation amount? (it will be None in the JSON)
#in any of the functions that print messages - can they deal with emojis and characters outside ascii?

#for generic tests, same as above; does it order the names correctly if the difference is in the decimal places; dealing with lots of donations
