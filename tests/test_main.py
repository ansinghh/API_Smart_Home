# Asked Chatgpt to provide me test data such as Alice or John Doe
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_and_get_user():
    user_data = {
        "name": "Alice",
        "email": "alice@example.com",
        "password": "password123"
    }
    response = client.post("/api/users", json=user_data)
    assert response.status_code == 200
    user = response.json()
    assert "id" in user
    assert user["name"] == "Alice"
    assert user["email"] == "alice@example.com"
    user_id = user["id"]

    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    fetched_user = response.json()
    assert fetched_user["id"] == user_id
    assert fetched_user["name"] == "Alice"
    assert fetched_user["email"] == "alice@example.com"

def test_create_house_and_get_house():
    user_data = {
        "name": "Bob",
        "email": "bob@example.com",
        "password": "password123"
    }
    response = client.post("/api/users", json=user_data)
    user = response.json()
    user_id = user["id"]

    house_data = {
        "user_id": user_id,
        "name": "Bob's House",
        "address": "123 Main St"
    }
    response = client.post("/api/houses", json=house_data)
    assert response.status_code == 200
    house = response.json()
    assert "id" in house
    assert house["name"] == "Bob's House"
    assert house["address"] == "123 Main St"
    assert house["user_id"] == user_id
    house_id = house["id"]

    response = client.get(f"/api/houses/{house_id}")
    assert response.status_code == 200
    fetched_house = response.json()
    assert fetched_house["id"] == house_id
    assert fetched_house["name"] == "Bob's House"

def test_create_room_and_get_rooms():
    user_data = {
        "name": "Charlie",
        "email": "charlie@example.com",
        "password": "password123"
    }
    response = client.post("/api/users", json=user_data)
    user = response.json()
    user_id = user["id"]

    house_data = {
        "user_id": user_id,
        "name": "Charlie's House",
        "address": "456 Elm St"
    }
    response = client.post("/api/houses", json=house_data)
    house = response.json()
    house_id = house["id"]

    room_data = {
        "house_id": house_id,
        "name": "Living Room",
        "room_type": "common"
    }
    response = client.post(f"/api/houses/{house_id}/rooms", json=room_data)
    assert response.status_code == 200
    room = response.json()
    assert "id" in room
    assert room["name"] == "Living Room"
    room_id = room["id"]

    response = client.get(f"/api/houses/{house_id}/rooms")
    assert response.status_code == 200
    rooms = response.json()["rooms"]
    assert any(r["id"] == room_id for r in rooms)

def test_create_device_and_control_device():
    user_data = {
        "name": "David",
        "email": "david@example.com",
        "password": "password123"
    }
    response = client.post("/api/users", json=user_data)
    user = response.json()
    user_id = user["id"]

    house_data = {
        "user_id": user_id,
        "name": "David's House",
        "address": "789 Oak St"
    }
    response = client.post("/api/houses", json=house_data)
    house = response.json()
    house_id = house["id"]

    room_data = {
        "house_id": house_id,
        "name": "Bedroom",
        "room_type": "private"
    }
    response = client.post(f"/api/houses/{house_id}/rooms", json=room_data)
    room = response.json()
    room_id = room["id"]

    device_data = {
        "room_id": room_id,
        "device_name": "Lamp",
        "device_type": "light",
        "status": "off"
    }
    response = client.post(f"/api/rooms/{room_id}/devices", json=device_data)
    assert response.status_code == 200
    device = response.json()
    assert "id" in device
    assert device["device_name"] == "Lamp"
    device_id = device["id"]
    
    response = client.get(f"/api/rooms/{room_id}/devices")
    assert response.status_code == 200
    devices = response.json()["devices"]
    assert any(d["id"] == device_id for d in devices)

    control_data = {"status": "on"}
    response = client.post(f"/api/devices/{device_id}/control", json=control_data)
    assert response.status_code == 200
    message = response.json()["message"]
    assert f"Device {device_id} turned on" in message

    response = client.get(f"/api/rooms/{room_id}/devices")
    devices = response.json()["devices"]
    for d in devices:
        if d["id"] == device_id:
            assert d["status"] == "on"
