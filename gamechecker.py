import requests
import time

def check_game_status(game_id):
    try:
        url = f"https://www.roblox.com/games/{game_id}"
        response = requests.get(url)

        if response.status_code == 200:
            if "[ Content Deleted ]" in response.text:
                return "Game has been deleted."
            elif "Sorry, this place is currently under review." in response.text:
                return "Game is under review."
            else:
                return "Game is still up."
        elif response.status_code == 404:
            return "Game has been deleted or is unavailable."
        else:
            return f"Unexpected status code: {response.status_code}"
    except Exception as e:
        return f"Error checking game status: {e}"

if __name__ == "__main__":
    user_game_id = input("Enter the game ID: ")
    interval_seconds = int(input("Enter the time to check again in seconds: "))
    
    while True:
        status = check_game_status(user_game_id)
        print(status)
        print(f"Checking again in {interval_seconds} seconds...")
        time.sleep(interval_seconds)
