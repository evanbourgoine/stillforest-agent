import requests
from dotenv import load_dotenv
load_dotenv()

app_id = '1202883444954046'
app_secret = '9c51652f08d993d3f34e5704897a7432'
short_token = 'EAARGBCBxU74BQ9HIuTZCr0B2LmluAw92yhD3tAz2i3o6si2RA1IO9AFqCyf3ZCKoQjZCCtgEN5esk30wMxpjUeZBS2eczm4CG1rWHxBtxS1SKkdwukU40jmeQbcLZBEYdZAsoKg1CJTynVgNpNrjB5amOkZBYyh3nRMI46eRuaxzIy4Vd8XAsJ0bpiEhZBGQQIBYwl6TaZBsnKkmIvr6ZANDPlvFnzoDBtbf8x1zwa2AFZArnMPBonErANPxXS2TM9weVyfIjiCbmqMBCFTtgHS5Lfsud13TgZDZD'

response = requests.get(
    'https://graph.facebook.com/oauth/access_token',
    params={
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': short_token
    }
)

data = response.json()

if 'access_token' in data:
    print('SUCCESS!')
    print('Token length:', len(data['access_token']))
    print('Expires in:', data.get('expires_in', 'N/A'), 'seconds')
    print('\nYour long-lived token:')
    print(data['access_token'])
else:
    print('ERROR:', data)