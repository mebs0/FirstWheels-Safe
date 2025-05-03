from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


testusername = "sammyjkj"
testusername2 = "sammyjj"
testpassword = "TestP4ssword123!"
passtooshort = "TP123"
testregnum = "YC09UGY"

signupurl = "/user/signup/"
loginurl = "/user/login/"

class usersTest(APITestCase):

    # this test makes up a user that is used later on
    def setUp(self):
        self.premadeuser = User.objects.create_user(username=testusername, password=testpassword)

    # FOR SIGNUP
    def test_goodsignup(self):
        # this test tests is the signup works with correct fields
        testcall = self.client.post(signupurl, {"username": testusername2,"password": testpassword,"password2": testpassword})
        self.assertEqual(testcall.status_code, 201)
        self.assertTrue(User.objects.filter(username=testusername).exists())

    def test_badsignupMissingfields(self):
        # this tests to make sure that a missing field is picked up and errored
        testcall = self.client.post(signupurl, {"username": testusername})
        self.assertEqual(testcall.data["signuperror"], "Username or Password missing")

    def test_badsignupShortpass(self):
        # this tests makes sure that a short pass is rejected
        testcall = self.client.post(signupurl, {"username":testusername,"password":passtooshort,"password2":passtooshort})
        self.assertEqual(testcall.data["signuperror"], "Password Needs To Be 8 Characters")

    def test_badsignupPassmismatch(self):
        # this test makes sure that a differrent pass2 is rejected
        testcall = self.client.post(signupurl, {"username": testusername,"password": testpassword,"password2": passtooshort})
        self.assertEqual(testcall.data["signuperror"], "Passwords Do Not Match")

    def test_badsignupUsertaken(self):
        # this test makes sure that a username that already exists is rejected
        testcall = self.client.post(signupurl, {"username": testusername,"password": testpassword,"password2": testpassword})
        self.assertEqual(testcall.data["signuperror"], "Username Exists")

    # FOR LOGIN
    def test_goodlogin(self):
        # this test a good login with correct deatils
        testcall = self.client.post(loginurl, {"username": testusername,"password": testpassword})
        self.assertEqual(testcall.status_code, 200)

    def test_badlogin(self):
        # this test makes sure an incorrect login is rejected
        testcall = self.client.post(loginurl, {"username": testusername,"password": passtooshort})
        self.assertEqual(testcall.data["loginerror"], "Username or Password Is Wrong")

    # FOR DELETE
    def test_testdelete(self):
        # this test makes sure a user is deleted 
        token = Token.objects.create(user=self.premadeuser)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        self.client.delete("/user/del/")
        self.assertFalse(User.objects.filter(username=testusername).exists())
