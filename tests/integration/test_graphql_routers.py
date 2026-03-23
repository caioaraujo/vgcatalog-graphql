def test_create_game(client):
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


def test_create_game_that_already_exists(client, game_factory):
    game_factory()
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
            "name": "Teenage Mutant Ninja Turtles: Turtles in Time",
            "genre": "Beat em up",
            "releasedYear": 1991,
            "platform": "Super Nintendo",
            "allowMultiplayer": False,
        }
    }

    response = client.post(
        "/graphql/games",
        json={"query": query, "variables": variables},
    )

    assert "errors" in response.json()


def test_update_game(client, game_factory):
    game_factory()
    query = """
    mutation UpdateGame($gameId: Int!, $data: GameInput!) {
        updateGame(gameId: $gameId, data: $data) {
            id
            name
            genre
            releasedYear
            platform
            allowMultiplayer
        }
    }
    """

    variables = {
        "gameId": 2,
        "data": {
            "name": "The Witcher 3",
            "genre": "RPG",
            "releasedYear": 2015,
            "platform": "PC",
            "allowMultiplayer": False,
        },
    }

    response = client.post(
        "/graphql/games", json={"query": query, "variables": variables}
    )

    assert response.status_code == 200

    result = response.json()

    assert "errors" not in response.json()
    assert result["data"] is not None

    data = result["data"]["updateGame"]
    assert data["id"] == 2
    assert data["name"] == "The Witcher 3"
    assert data["releasedYear"] == 2015
    assert data["platform"] == "PC"
    assert data["genre"] == "RPG"
    assert data["allowMultiplayer"] is False


def test_update_game_that_not_exists(client):
    query = """
    mutation UpdateGame($gameId: Int!, $data: GameInput!) {
        updateGame(gameId: $gameId, data: $data) {
            id
            name
            genre
            releasedYear
            platform
            allowMultiplayer
        }
    }
    """

    variables = {
        "gameId": 2,
        "data": {
            "name": "The Witcher 3",
            "genre": "RPG",
            "releasedYear": 2015,
            "platform": "PC",
            "allowMultiplayer": False,
        },
    }

    response = client.post(
        "/graphql/games", json={"query": query, "variables": variables}
    )

    assert "errors" in response.json()


def test_query_game_by_id(client, game_factory):
    game_factory()
    query = """
        query GetGame($id: Int!) {
            game(gameId: $id) {
                id
                name
                genre
                platform
                releasedYear
                allowMultiplayer
            }
        }
    """

    response = client.post(
        "/graphql/games",
        json={"query": query, "variables": {"id": 2}},
    )

    data = response.json()

    assert "errors" not in data
    assert data["data"]["game"] == {
        "id": 2,
        "name": "Teenage Mutant Ninja Turtles: Turtles in Time",
        "genre": "BeatEm Up",
        "platform": "Super Nintendo",
        "releasedYear": 1991,
        "allowMultiplayer": True,
    }


def test_query_game_by_id_when_not_found(client, game_factory):
    game_factory()
    query = """
        query GetGame($id: Int!) {
            game(gameId: $id) {
                id
                name
                genre
                platform
                releasedYear
                allowMultiplayer
            }
        }
    """

    response = client.post(
        "/graphql/games",
        json={"query": query, "variables": {"id": 99}},
    )

    data = response.json()

    assert "errors" in data


def test_list_games_by_platform(client, games_factory):
    games_factory.create_batch(5)
    query = """
        query GetGames($filters: GameFilterInput!) {
            games(data: $filters) {
                id
                name
                genre
                platform
                releasedYear
                allowMultiplayer
            }
        }
    """

    response = client.post(
        "/graphql/games",
        json={
            "query": query,
            "variables": {"filters": {"platform": {"eq": "Super Nintendo"}}},
        },
    )

    data = response.json()

    assert "errors" not in data
    assert len(data["data"]["games"]) == 5
    assert all(("Super Nintendo" == g["platform"] for g in data["data"]["games"]))


def test_list_games_by_name_contains(client, games_factory):
    games_factory.create_batch(5)
    query = """
        query GetGames($filters: GameFilterInput!) {
            games(data: $filters) {
                id
                name
                genre
                platform
                releasedYear
                allowMultiplayer
            }
        }
    """

    response = client.post(
        "/graphql/games",
        json={"query": query, "variables": {"filters": {"name": {"contains": "game"}}}},
    )

    data = response.json()

    assert "errors" not in data
    assert len(data["data"]["games"]) == 5
    assert all(("Game" in g["name"] for g in data["data"]["games"]))
