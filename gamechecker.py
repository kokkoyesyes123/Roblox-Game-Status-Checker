import requests
import time

def get_csrf_token(cookie):
    url = "https://auth.roblox.com/v2/login"
    headers = {
        "Cookie": f".ROBLOSECURITY={cookie}"
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 403:
        csrf_token = response.headers.get("x-csrf-token")
        return csrf_token
    else:
        raise Exception("Failed to retrieve CSRF token.")

def check_game_status(game_id, cookie, csrf_token):
    try:
        url = f"https://games.roblox.com/v1/games/multiget-place-details?placeIds={game_id}"
        headers = {
            "Cookie": f".ROBLOSECURITY={cookie}",
            "X-CSRF-Token": csrf_token
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            game_data = response.json()
            game_name = game_data[0]["name"]
            is_playable = game_data[0]["isPlayable"]

            if not is_playable:
                return f"❌ Status Check: '{game_name}' is not currently playable. kok is sad. 😭😭😭"
            else:
                return f"✅ Status Check: '{game_name}' is still up and playable. kok is happy! 👍😁😁😁"
        elif response.status_code == 404:
            return f"❌ Game with ID {game_id} has been deleted or is unavailable. Please wait for kok to reupload the game. 😭😭😭"
        else:
            return f"❗ Unexpected status code ({response.status_code})."
    except Exception as e:
        return f"❗ Error checking game status: {e}"

def send_to_discord_webhook(webhook_url, message, role_ping=None):
    if webhook_url:
        payload = {"content": message}
        if role_ping:
            payload["content"] = f"{role_ping} {message}"
        requests.post(webhook_url, json=payload)
    else:
        print(f"Webhook URL not provided. Skipping Discord notification: {message}")

if __name__ == "__main__":
    roblox_cookie = input("Enter your Roblox .ROBLOSECURITY cookie: ")
    user_game_id = input("Enter the game ID: ")
    interval_seconds = int(input("Enter the time interval in seconds: "))
    discord_webhook_url = input("Enter your Discord webhook URL (leave empty if not using): ")

    csrf_token = get_csrf_token(roblox_cookie)
    
    while True:
        status = check_game_status(user_game_id, roblox_cookie, csrf_token)
        print(status)
        send_to_discord_webhook(discord_webhook_url, status)  # Send status to Discord with role ping
        print(f"Checking again in {interval_seconds} seconds...")
        time.sleep(interval_seconds)
