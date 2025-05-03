import numpy as numpyy
import requests
import easyocr
from PIL import Image
from ultralytics import YOLO
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import (api_view, permission_classes)
from .models import CarsInGarage, SavedChecklist
from .apis.getmotdata import getmotinfo
from datetime import datetime
import cv2

@api_view(["POST"])
def getvehicledata(request):
    searchedreg = request.data.get("registrationNumber")
    try:
        # try getting the info from dvlas primary api
        vehicledata = requests.post("https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles",json={"registrationNumber": searchedreg},
            headers={"x-api-key": settings.DVLA_KEY,"Content-Type": "application/json",})
        vehicledatajson = vehicledata.json() # save it as a json for vue compatibility

        vehicledatajson["score"] = getscore(vehicledatajson) # call the score calc method and add it to the json
        vehicledatajson["advice"] = getinsights(vehicledatajson) # call the advice calc method and add it to the json

        try:
            vehiclemotdata = getmotinfo(searchedreg) # now try to get the mot data from dvla secondary api
            vehicledatajson["mot_data"] = vehiclemotdata # add it to the json
            
            # this appends extra data to the main json structure if we get it from the mot api
            if vehiclemotdata.get("model"): vehicledatajson["model"] = vehiclemotdata["model"]
            if vehiclemotdata.get("engineSize"): vehicledatajson["engineCapacity"] = vehiclemotdata["engineSize"]
            if vehiclemotdata.get("hasOutstandingRecall"): vehicledatajson["hasOutstandingRecall"] = vehiclemotdata["hasOutstandingRecall"]

        except Exception as motapierror: vehicledatajson["mot_data"] = {} # if theres a mot error just add the mot as empty so vue can still work

        return Response(vehicledatajson, status=vehicledata.status_code)
    except Exception as apierror: return Response(apierror) # returns a error if the api fails

    


def getscore(vehicleapidata):
    yearpoints = 100 # this is the start score of 100 

    # checks the age of the car, if too old reduce points if very new add points
    vehicleyear = vehicleapidata.get("yearOfManufacture")
    if vehicleyear:
        vehicleage = 2025 - int(vehicleyear)
        if vehicleage > 15: yearpoints -= 25
        elif vehicleage > 10: yearpoints -= 15
        elif vehicleage > 5: yearpoints -= 8
        else: yearpoints += 2

    # has mot means more points, no mot means less points
    hasmot = vehicleapidata.get("motStatus", "").lower()
    if hasmot != "valid": yearpoints -= 15
    else: yearpoints += 5

    # if we have long life on the mot then add points
    motexpirydate = vehicleapidata.get("motExpiryDate")
    if motexpirydate:
        try:
            daystillmotrenew = (datetime.strptime(motexpirydate, "%Y-%m-%d") - datetime.now()).days # gets the amount of days till mot expires
            if daystillmotrenew > 180: yearpoints += 5
        except: pass

    # if taxed get some points as its expected, if none lose points
    if vehicleapidata.get("taxStatus", "").lower() != "taxed": yearpoints -= 10
    else: yearpoints += 2

    # depedning of fuel type add or remove points 
    fuletype = vehicleapidata.get("fuelType", "").lower()
    if fuletype == "diesel": yearpoints -= 5
    elif fuletype == "electric": yearpoints += 10
    elif fuletype == "petrol": yearpoints += 2

    # check emmisions if they are too high remove points, if low add points
    carbonemmisions = int(vehicleapidata.get("co2Emissions", 0))
    if carbonemmisions > 200: yearpoints -= 10
    elif carbonemmisions < 120: yearpoints += 5

    # check engine size, to big is very bad, smaller is better
    engineccsize = vehicleapidata.get("engineCapacity", 0)
    if engineccsize > 2900: yearpoints -= 25
    elif engineccsize >= 2000: yearpoints -= 10
    elif engineccsize < 1400: yearpoints += 5

    # if car has any recalls remove points
    if vehicleapidata.get("hasOutstandingRecall"): yearpoints -= 10

    # if cars marked for export remove alot of points as its not legal in the uk
    if vehicleapidata.get("markedForExport", False): yearpoints -= 25

    return max(min(yearpoints, 100), 0) # return points and make sure its 0-100


def getinsights(vehicleapidata):
    # make 3 arrays so we can store the pros cons and tips
    vehiclepros = []
    vehiclecons = []
    vehicletips = []

    # get all the data from the api and puts it into some variables to use easily
    fueltype = vehicleapidata.get("fuelType", "").lower()
    engineccsize = vehicleapidata.get("engineCapacity")
    carbonemmisions = vehicleapidata.get("co2Emissions")
    regyear = int(vehicleapidata.get("yearOfManufacture") or 0)
    hasmot = vehicleapidata.get("motStatus").lower()
    beenexported = vehicleapidata.get("markedForExport", False)
    pendingrecalls = vehicleapidata.get("hasOutstandingRecall", False)
    hastax = vehicleapidata.get("taxStatus", "").lower()
    motexpirydate = vehicleapidata.get("motExpiryDate")
    dateoflastvc5 = vehicleapidata.get("dateOfLastV5CIssued")

    age = 2025 - regyear # calc the cars age

    # add some insights on what fuel types mean
    if fueltype == "diesel": vehiclecons.append("Diesal Engines Are Known To Increase Insurance And Have Pollution Issues.")
    elif fueltype == "petrol": vehiclepros.append("Petrol Engines Are Cheaper To Maintain And Have Lower Insurance.")
    elif fueltype == "electric": vehiclepros.append("Electric Cars Are The Best, Cheap To Run And Very Low insurance.")

    if fueltype == "diesel" and regyear < 2016: vehiclecons.append("This Vehicle Is Not ULEZ Complaint, Expect Extra Charges In London")
    elif fueltype == "petrol" and regyear < 2006: vehiclecons.append("This Vehicle Is Not ULEZ Complaint, Expect Extra Charges In London")
    else: vehiclepros.append("This Vehicle Is ULEZ Complaint, No Extra Charges In London")

    # adds insights into engine sizes and their costs
    if engineccsize:
        if engineccsize > 2000: vehiclecons.append("Larger Engines Drink More Fuel, Increasing Costs And Also Have Higher Insurance.")
        elif engineccsize < 1400: vehiclepros.append("Smaller Enginer Drink Less Fuel, Lower Costs And Insurance.")

    # adds insights into road tax
    if carbonemmisions:
        if carbonemmisions > 180: vehiclecons.append("High Carbon Emmisions Result In Higher Road Tax.")
        elif carbonemmisions < 100: vehiclepros.append("Low Carbon Emmissions Result In Lower Road Tax.")
        
    # adds insights into what the age of the car means for the user    
    if age:
        if age < 5: vehiclepros.append("Relatively modern vehicle, may have better safety and reliability.")
        elif age > 12: vehiclecons.append("Older vehicles may require more frequent maintenance.")
        elif 5 <= age <= 10: vehiclepros.append("Reasonable age, likely to be affordable yet still reliable.")

    # just reitetates the mot status and tells the user to check its expiry again as its a legal need
    if "not valid" in hasmot: vehiclecons.append("Vehicle does not have a valid MOT, which could indicate hidden issues.")
    else: vehiclepros.append("Vehicle has a valid MOT.")

    if motexpirydate: vehicletips.append(f"MOT valid until {motexpirydate} - plan your inspection before expiry.")
    
    # tells user exported cars are illegal in the uk
    if beenexported: vehiclecons.append("Vehicle is marked for export - may not be legal for UK roads.")
    # tells the user that the vehicle has recalls
    if pendingrecalls: vehiclecons.append("This vehicle has outstanding manufacturer recalls.")

    # tells user the car istaxed and if not its illegality in the uk
    if "taxed" in hastax: vehiclepros.append("The vehicle is currently taxed.")
    else: vehiclecons.append("Vehicle is not taxed, which could mean extra upfront costs.")

    # tells the user to double check the sellers vc5 matches up with the apis date
    if dateoflastvc5: vehicletips.append(f"Last V5C issued on {dateoflastvc5}. Ensure the seller's document matches.")

    if not vehiclepros:vehiclepros.append("None")
    if not vehiclecons:vehiclecons.append("None")

    return { "selectedvehiclepros": vehiclepros, "selectedvehiclecons": vehiclecons, "selectedvehicletips": vehicletips}


@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAuthenticated])
def usergarageapi(request):
    loggedinuser = request.user

    # gets the garage cars for a user
    if request.method == "GET":
        allcars = CarsInGarage.objects.filter(linkeduser=loggedinuser)
        return Response([ {"registration_number": singlecar.regnum} for singlecar in allcars])

    # adds a car to the users garage
    elif request.method == "POST":
        selectedreg = request.data.get("registration_number", "").upper().strip()
        notneeded, created = CarsInGarage.objects.get_or_create(linkeduser=loggedinuser, regnum=selectedreg)
        return Response({"status": "Added" if created else "Already In garage"}, status=201)

    # deletes a car from the users garage
    elif request.method == "DELETE":
        selectedreg = request.data.get("registration_number", "").upper().strip()
        hasbeendeleted = CarsInGarage.objects.filter(linkeduser=loggedinuser, regnum=selectedreg).delete()
        return Response({"status": "Been Deleted" if hasbeendeleted[0] else "Car not in your garage"})


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def userchecklistapi(request):
    loggedinuser = request.user
    # gets the users checklist for a car
    if request.method == "GET":
        userschecklist = SavedChecklist.objects.filter(linkeduser=loggedinuser)
        formattedchecklist = [{"registration_number": listperreg.regnum,"checklist": listperreg.carchecklist} for listperreg in userschecklist]
        return Response(formattedchecklist)

    # adds the new checklist of a car to the users db entry
    elif request.method == "POST":
        selectedreg = request.data.get("registration_number")
        filledoutchecklist = request.data.get("checklist")
        notneeded, created = SavedChecklist.objects.update_or_create(linkeduser=loggedinuser,regnum=selectedreg,defaults={"carchecklist": filledoutchecklist})
        return Response({"status": "Saved" if created else "Updated"})


loadedmodel = YOLO("best.pt") # the trained model for yolo
easyocrr = easyocr.Reader(["en"], gpu=True)  # easyocr reader set in english mode

@api_view(["POST"])
def anprscanner(request):
    sentimage = request.FILES.get("imagetocheck") # gets the image from frontend
    try:
        # convert to numpy array and run yolo against it
        imagenumpy = numpyy.array(Image.open(sentimage).convert("RGB"))
        yoloresult = loadedmodel(imagenumpy) # YOLO

        # if that image has no box then try the next
        if not yoloresult or len(yoloresult[0].boxes) == 0: return Response({"gotplate": False})

        # go through the boxes yolo has found        
        for foundbox in yoloresult[0].boxes:
            # get the edges of the plate and make up the aspect ratio
            left, top, right, bottom = map(int, foundbox.xyxy[0].cpu().numpy())
            boxratio = (right - left) / (bottom - top)
            # if the ratio is around what uk plates are then attempt to read
            if 4 < boxratio < 6:
                # Convert the image to BGR so openCV can use it
                # crop the image then get easyocr to pull text from it
                opencvimage = cv2.cvtColor(imagenumpy, cv2.COLOR_RGB2BGR) # OPENCV
                imagecropped = opencvimage[top:bottom, left:right]
                extractedtext = easyocrr.readtext(imagecropped, detail=0) # EASYOCR
                # make sure we get a text back
                if extractedtext:
                    formattedplate = extractedtext[0].strip().upper().replace(" ", "")
                    # do more manual correction as easyocr finds it hard for "I" and we can use the plate structure to help
                    if len(formattedplate) > 3:
                        formattedplate = list(formattedplate)
                        if formattedplate[2] == "I": formattedplate[2] = "1"
                        if formattedplate[3] == "I": formattedplate[3] = "1"
                        if formattedplate[2] == "O": formattedplate[2] = "0"
                        if formattedplate[3] == "O": formattedplate[3] = "0"
                        if formattedplate[2] == "S": formattedplate[2] = "5"
                        if formattedplate[3] == "S": formattedplate[3] = "5"
                        if formattedplate[2] == "B": formattedplate[2] = "8"
                        if formattedplate[3] == "B": formattedplate[3] = "8"
                        formattedplate = "".join(formattedplate)
                    #  make sure its the right length and its alphanumeric (nums and letters) and give it to the frontend
                    if 6 <= len(formattedplate) <= 8 and formattedplate.isalnum(): return Response({"gotplate": True, "plate": formattedplate})

        return Response({"gotplate": False}) # if the try fails then just say we didnt get a plate

    except Exception as e: return Response({"error": str(e)}, status=500) # error handling
