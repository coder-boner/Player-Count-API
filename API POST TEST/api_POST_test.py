import requests

API_URL = "http://127.0.0.1:8080/scp_sl/plr_count/"
API_KEY = "API_KEY"


def update_player_count(new_count):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {"player_count": new_count}
    response = requests.put(API_URL, json=data, headers=headers)

    if response.status_code == 200:
        print("Player count updated successfully")
        print(response.json())
    else:
        print("Failed to update player count")
        print(response.json())


# Example usage
update_player_count(43)

sigma = requests.get("https://api.scpslgame.com/serverinfo.php?id=30017&key=wojRclHhzLFl3xMy6hXhGTge&key=wojRclHhzLFl3xMy6hXhGTge")
print(sigma.text)