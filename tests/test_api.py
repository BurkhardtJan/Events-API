import requests
import time

BASE_URL = "http://localhost:5000"


def test_health_endpoint_returns_healthy():
    "Tests that the api endpoint returns 200 OK"
    url = f"{BASE_URL}/api/health"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_user_creates_new_user():
    "Tests that the user is created"
    url = f"{BASE_URL}/api/auth/register"
    username = f"testuser_{int(time.time() * 1000)}"
    user_data = {"username": username, "password": "testpassword"}
    response = requests.post(url, json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["user"]["username"] == username


def test_login_returns_jwt_token():
    "Tests that the jwt token is returned"
    url = f"{BASE_URL}/api/auth/login"
    usedata = {
        "username": "john_doe",
        "password": "securepassword123"
    }
    response = requests.post(url, json=usedata)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def register_login_return_token():
    "A helper function to register a user, log in and returns the token"
    register_url = f"{BASE_URL}/api/auth/register"
    login_url = f"{BASE_URL}/api/auth/login"
    username = f"testuser_{int(time.time() * 1000)}"
    user_data = {"username": username, "password": "testpassword"}
    requests.post(register_url, json=user_data)
    response = requests.post(login_url, json=user_data)
    return response.json()["access_token"]


def test_create_public_event_requires_auth_and_succeeds_with_token():
    "Create public event with auth"
    url = f"{BASE_URL}/api/events"
    test_data = {
        "title": "Python Meetup",
        "description": "Monthly Python developer meetup",
        "date": "2026-01-15T18:00:00",
        "location": "Tech Hub, Room 101",
        "capacity": 50,
        "is_public": True,
        "requires_admin": False
    }
    token = register_login_return_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, json=test_data, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Python Meetup"
    assert data["description"] == "Monthly Python developer meetup"
    assert data["date"] == "2026-01-15T18:00:00"
    assert data["location"] == "Tech Hub, Room 101"
    assert data["capacity"] == 50
    assert data["is_public"] == True


def test_rsvp_to_public_event_succeeds_without_auth():
    "Create public event without auth"
    url = f"{BASE_URL}/api/events"
    test_data = {
        "title": "Python Meetup",
        "description": "Monthly Python developer meetup",
        "date": "2026-01-15T18:00:00",
        "location": "Tech Hub, Room 101",
        "capacity": 50,
        "is_public": True,
        "requires_admin": False
    }
    token = register_login_return_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, json=test_data, headers=headers)
    event_id = response.json()["id"]
    rsvp_url = f"{BASE_URL}/api/rsvps/event/{event_id}"
    rsvp_data = {
        "attending": True
    }
    rsvp_response = requests.post(rsvp_url, json=rsvp_data)
    assert rsvp_response.status_code == 201
    assert rsvp_response.json()["event_id"] == event_id


def test_register_user_duplicate():
    "Tests of Duplicate username registration"
    url = f"{BASE_URL}/api/auth/register"
    username = f"testuser_{int(time.time() * 1000)}"
    user_data = {"username": username, "password": "testpassword"}
    response = requests.post(url, json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["user"]["username"] == username
    second_response = requests.post(url, json=user_data)
    assert second_response.status_code == 400


def test_create_public_event_without_token():
    "Create public event without token"
    url = f"{BASE_URL}/api/events"
    test_data = {
        "title": "Python Meetup",
        "description": "Monthly Python developer meetup",
        "date": "2026-01-15T18:00:00",
        "location": "Tech Hub, Room 101",
        "capacity": 50,
        "is_public": True,
        "requires_admin": False
    }
    response = requests.post(url, json=test_data)
    assert response.status_code == 401


def test_rsvp_to_private_event_fails_without_auth():
    "Create public event without auth"
    url = f"{BASE_URL}/api/events"
    test_data = {
        "title": "Python Meetup",
        "description": "Monthly Python developer meetup",
        "date": "2026-01-15T18:00:00",
        "location": "Tech Hub, Room 101",
        "capacity": 50,
        "is_public": False,
        "requires_admin": False
    }
    token = register_login_return_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, json=test_data, headers=headers)
    event_id = response.json()["id"]
    rsvp_url = f"{BASE_URL}/api/rsvps/event/{event_id}"
    rsvp_data = {
        "attending": True
    }
    rsvp_response = requests.post(rsvp_url, json=rsvp_data)
    assert rsvp_response.status_code == 401
