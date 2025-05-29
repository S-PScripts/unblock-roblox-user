import requests

roblosecurity = 'ENTER IT HERE'
user_to_unblock = (ENTER IT HERE)

session = requests.Session()
session.headers.update({
    'Cookie': (
        f'.ROBLOSECURITY={roblosecurity}; '
        'RBXEventTrackerV2=ENTER IT HERE; '
        'RBXSessionTracker=ENTER IT HERE;'
    ),
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Origin': 'https://www.roblox.com',
    'Referer': 'https://www.roblox.com/',
})

unblock_url = f'https://apis.roblox.com/user-blocking-api/v1/users/{user_to_unblock}/unblock-user'

# Try to unblock
response = session.post(unblock_url)

# If 403, get CSRF token and retry
if response.status_code == 403:
    token = response.headers.get('x-csrf-token')
    if token:
        session.headers.update({'X-CSRF-Token': token})
        response = session.post(unblock_url)

print('Status:', response.status_code)
print('Response:', response.text)
