def test_post_game(client):
    query = """
        mutation CreateGame($data: GameInput!) {
            createGame(data: $data) {
                name
                genre
                releasedYear
                platform
                allowMultiplayer
            }
        }
        """

    variables = {
        "data": {
            "name": "The Witcher 3",
            "genre": "RPG",
            "releasedYear": 2015,
            "platform": "PC",
            "allowMultiplayer": False,
        }
    }

    response = client.post(
        "/graphql/games/", json={"query": query, "variables": variables}
    )

    assert response.status_code == 200

    result = response.json()

    assert "errors" not in response.json()
    assert result["data"] is not None

    data = result["data"]["createGame"]
    assert data["name"] == "The Witcher 3"
    assert data["releasedYear"] == 2015
    assert data["platform"] == "PC"
    assert data["genre"] == "RPG"
    assert data["allowMultiplayer"] is False


def test_create_game_missing_required_field(client):
    query = """
    mutation CreateGame($data: GameInput!) {
        createGame(data: $data) {
            name
        }
    }
    """

    variables = {
        "data": {
            "genre": "RPG",
            "releasedYear": 2015,
            "platform": "PC",
            "allowMultiplayer": False,
        }
    }

    response = client.post(
        "/graphql/games",
        json={"query": query, "variables": variables},
    )

    body = response.json()

    assert response.status_code == 200
    assert "errors" in body
    assert body["data"] is None


def test_create_game_invalid_type(client):
    query = """
    mutation CreateGame($data: GameInput!) {
        createGame(data: $data) {
            name
        }
    }
    """

    variables = {
        "data": {
            "name": "The Witcher 3",
            "genre": "RPG",
            "releasedYear": "INVALID",
            "platform": "PC",
            "allowMultiplayer": False,
        }
    }

    response = client.post(
        "/graphql/games",
        json={"query": query, "variables": variables},
    )

    body = response.json()

    assert "errors" in body
    assert body["data"] is None


def test_create_game_unknown_field(client):
    query = """
    mutation CreateGame($data: GameInput!) {
        createGame(data: $data) {
            name
        }
    }
    """

    variables = {
        "data": {
            "name": "The Witcher 3",
            "genre": "RPG",
            "releasedYear": 2015,
            "platform": "PC",
            "allowMultiplayer": False,
            "invalidField": "something",
        }
    }

    response = client.post(
        "/graphql/games",
        json={"query": query, "variables": variables},
    )

    assert "errors" in response.json()
