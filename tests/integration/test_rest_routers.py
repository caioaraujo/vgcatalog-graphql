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


def test_update_game_when_not_found(client):
    payload = {
        "name": "Super Metroid",
        "released_year": 1991,
        "platform": "Super Nintendo",
        "genre": "Action/Adventure",
        "allow_multiplayer": False,
    }

    response = client.put("/games/1", json=payload)

    assert response.status_code == 404


def test_update_game_when_game_exists(client, game_factory):
    game_factory()

    payload = {
        "name": "TMNT IV: Turtles in Time",
        "released_year": 1991,
        "platform": "Arcade",
        "genre": "Beat em Up",
        "allow_multiplayer": False,
    }

    response = client.put("/games/2", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 2
    assert data["name"] == "TMNT IV: Turtles in Time"
    assert data["released_year"] == 1991
    assert data["platform"] == "Arcade"
    assert data["genre"] == "Beat em Up"
    assert data["allow_multiplayer"] is False


def test_get_game_by_id_when_game_not_found(client):
    response = client.get("/games/1")

    assert response.status_code == 404


def test_get_game_by_id_when_game_exists(client, game_factory):
    game_factory()

    response = client.get("/games/2")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 2
    assert data["name"] == "Teenage Mutant Ninja Turtles: Turtles in Time"
