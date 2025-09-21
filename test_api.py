# test_api.py

import requests

BASE = "http://127.0.0.1:5000"

def main():
    # Register user
    r = requests.post(BASE + "/auth/register", json={"username":"user1","password":"password"})
    print("register:", r.status_code, r.json())

    # Login
    r = requests.post(BASE + "/auth/login", json={"username":"user1","password":"password"})
    print("login:", r.status_code, r.json())
    if r.status_code != 200:
        return
    token = r.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # Create task
    payload = {
        "title":"Finish project",
        "description":"Complete REST API by deadline",
        "due_date":"2025-09-22T18:00:00",
        "priority":2,
        "recurrence": "daily"
    }
    r2 = requests.post(BASE + "/tasks", json=payload, headers=headers)
    print("create task:", r2.status_code, r2.json())

    # List tasks
    r3 = requests.get(BASE + "/tasks", headers=headers)
    print("list tasks:", r3.status_code, r3.json())

    # Recommend
    r4 = requests.get(BASE + "/tasks/recommend", headers=headers)
    print("recommend:", r4.status_code, r4.json())

if __name__ == "__main__":
    main()
