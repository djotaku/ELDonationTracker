import extralifedonations

#run with command: py.test-3 extralifeunittests.py

#Tests for class Donor
def test_Donor_lt():
    donor1 = extralifedonations.Donor("donor1","message",45)
    donor2 = extralifedonations.Donor("donor2","message",30)
    assert donor2 < donor1

#Tests for class Participant
