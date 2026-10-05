import requests

def main():
    # Prompt user for inputs
    roblosecurity = input("Enter your .ROBLOSECURITY cookie: ").strip()
    user_to_block = input("Enter the user ID you want to block: ").strip()
    
    # Optional: You can prompt or leave blank for these trackers if needed
    rbx_event_tracker = input("Enter RBXEventTrackerV2 cookie value (or leave blank): ").strip()
    rbx_session_tracker = input("Enter RBXSessionTracker cookie value (or leave blank): ").strip()
    
    # Build cookie header string
    cookie = f'.ROBLOSECURITY={roblosecurity};'
    if rbx_event_tracker:
        cookie += f' RBXEventTrackerV2={rbx_event_tracker};'
    if rbx_session_tracker:
        cookie += f' RBXSessionTracker={rbx_session_tracker};'
    
    session = requests.Session()
    session.headers.update({
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Origin': 'https://www.roblox.com',
        'Referer': 'https://www.roblox.com/',
    })
    
    block_url = f'https://apis.roblox.com/user-blocking-api/v1/users/{user_to_block}/block-user'
    
    response = session.post(block_url)
    
    # If CSRF token needed, retry with token
    if response.status_code == 403:
        token = response.headers.get('x-csrf-token')
        if token:
            session.headers.update({'X-CSRF-Token': token})
            response = session.post(block_url)
    
    print('Status:', response.status_code)
    print('Response:', response.text)

if __name__ == "__main__":
    main()
