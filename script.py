import requests

roblosecurity = 'YOUR_ROBLOSECURITY_COOKIE_HERE'
session = requests.Session()
session.headers.update({
    'Cookie': (
        f'.ROBLOSECURITY={roblosecurity}; '
        'RBXEventTrackerV2=INSERT IT HERE; '
        'RBXSessionTracker=INSERT IT HERE;'
    ),
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Origin': 'https://www.roblox.com',
    'Referer': 'https://www.roblox.com/',
})

# Step 1: Get authenticated user ID
auth_resp = session.get('https://users.roblox.com/v1/users/authenticated')
auth_user_id = auth_resp.json().get('id')
print('Authenticated user ID:', auth_user_id)

# Step 2: Get your blocklist
blocklist_url = f'https://apis.roblox.com/user-blocking-api/v1/users/{auth_user_id}/blocked-users'
blocklist_resp = session.get(blocklist_url)
print('Blocked users:', blocklist_resp.status_code, blocklist_resp.json())

user_to_unblock = 4035560999
blocked_users = blocklist_resp.json() if blocklist_resp.status_code == 200 else []

# Step 3: Check if user is blocked
if any(user['blockedUser']['id'] == user_to_unblock for user in blocked_users):
    print(f'User {user_to_unblock} is blocked. Attempting to unblock...')
    unblock_url = f'https://apis.roblox.com/user-blocking-api/v1/users/{user_to_unblock}/unblock-user'
    response = session.post(unblock_url)
    if response.status_code == 403:
        token = response.headers.get('x-csrf-token')
        if token:
            session.headers.update({'X-CSRF-Token': token})
            response = session.post(unblock_url)
    print('Unblock status:', response.status_code)
    print('Unblock response:', response.text)
else:
    print(f'User {user_to_unblock} is NOT in your blocked users list. Cannot unblock.')
