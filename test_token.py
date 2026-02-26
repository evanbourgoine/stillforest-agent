import requests
from dotenv import load_dotenv
load_dotenv()

app_id = '....'
app_secret = '....'
short_token = '....'

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
