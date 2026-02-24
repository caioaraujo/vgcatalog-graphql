def test_create_game(client):
    payload = {
        "name": "Super Metroid",
        "released_year": 1991,
        "platform": "Super Nintendo",
        "genre": "Action/Adventure",
        "allow_multiplayer": False,
    }

    response = client.post("/games/", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Super Metroid"
    assert data["released_year"] == 1991
    assert data["platform"] == "Super Nintendo"
    assert data["genre"] == "Action/Adventure"
    assert data["allow_multiplayer"] is False
