import requests
from django.conf import settings

def getmotinfo(registration):

    # Get the Oauth token 
    oauthtokenattempt = requests.post(
        "https://login.microsoftonline.com/a455b827-244f-4c97-b5b4-ce5d13b4d00c/oauth2/v2.0/token",
        data={'grant_type': 'client_credentials','client_id': settings.DVLA_MOT_ID,'client_secret': settings.DVLA_MOT_SECRET,'scope': 'https://tapi.dvsa.gov.uk/.default',}
    )
    oauthtokenattempt.raise_for_status()
    accesstoken = oauthtokenattempt.json().get('access_token')

    # get mot data and return out the json 
    motdataattempt = requests.get(
        f"https://history.mot.api.gov.uk/v1/trade/vehicles/registration/{registration}",
        headers={'accept': 'application/json','Authorization': f'Bearer {accesstoken}','x-api-key': settings.DVLA_MOT_KEY}
    )
    motdataattempt.raise_for_status()
    return motdataattempt.json()
