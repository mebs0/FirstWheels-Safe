from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import CarsInGarage, SavedChecklist
from rest_framework.test import APITestCase

testusername = "sammyjj"
testpassword = "TestP4ssword123!"
testregnum = "YC09UGY"

loginurl = "/user/login/"
garageurl = "/vehicle/garage/"
checklisturl = "/vehicle/checklists/"
anprurl = "/vehicle/scananpr/"

class vehiclesTest(APITestCase):
    def setUp(self):
        # here we make up a user and log in so we can get a token for the restricted tests
        self.tester = APIClient()
        self.loggedinuser = User.objects.create_user(username=testusername, password=testpassword)
        self.baretoken = self.tester.post(loginurl, {"username": testusername, "password": testpassword}).data["token"]
        #need to format the token in the http expected format
        self.loggedinusertoken = {"HTTP_AUTHORIZATION": f"Token {self.baretoken}"}


    def test_lookupfunctionality(self):
        # tests to make sure the lookup works with a correct reg number
        testcall = self.tester.post("/vehicle/lookup/", {"registrationNumber": "YC09UGY"}, format="json")
        self.assertEqual(testcall.status_code, 200)


    def test_addingtogarage(self):
        # here we test to make sure the garage lets us add a car
        self.tester.post(garageurl, {"registration_number": testregnum}, **self.loggedinusertoken)
        self.assertTrue(CarsInGarage.objects.filter(linkeduser=self.loggedinuser, regnum=testregnum).exists())


    def test_gettinggaragecars(self):
        # here we test to make sure we can get cars from the garage
        CarsInGarage.objects.create(linkeduser=self.loggedinuser, regnum=testregnum)
        testcall = self.tester.get(garageurl, **self.loggedinusertoken)
        self.assertEqual(testcall.data[0]["registration_number"], testregnum)

    def test_removingcarfromgarage(self):
        # here we test to make sure we can remove a car from the garage
        CarsInGarage.objects.create(linkeduser=self.loggedinuser, regnum=testregnum)
        testcall = self.tester.delete(garageurl, {"registration_number": testregnum}, **self.loggedinusertoken)
        self.assertEqual(testcall.data["status"], "Been Deleted")

    def test_savingcheckllist(self):
        # here we test to make sure we can save a checklist
        self.tester.post(checklisturl, {"registration_number": testregnum,"checklist": {"Engine Oil Between Min and Max": True}}, format="json", **self.loggedinusertoken)
        self.assertTrue(SavedChecklist.objects.filter(linkeduser=self.loggedinuser, regnum=testregnum).exists())


    def test_gettingchecklist(self):
        # here we test we cab get a checklist for a user
        SavedChecklist.objects.create(linkeduser=self.loggedinuser, regnum=testregnum, carchecklist={"Engine Oil Between Min and Max": True})
        testcall = self.tester.get(checklisturl, **self.loggedinusertoken)
        self.assertEqual(testcall.data[0]["registration_number"], testregnum)


    def test_anprwithoutimage(self):
        # here we test that the anpr fails correctly with no image
        testcall = self.tester.post(anprurl, {})
        self.assertEqual(testcall.status_code, 500)


