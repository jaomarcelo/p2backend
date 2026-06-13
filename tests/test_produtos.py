import pytest


def test_listar_produtos_vazio(client):
    response = client.get("/produtos")

    assert response.status_code == 200
    assert response.json() == []


def test_criar_produto(client):
    response = client.post(
        "/produtos",
        json={
            "nome": "Mouse",
            "preco": 100,
            "estoque": 20
        }
    )

    assert response.status_code == 201
    assert response.json()["nome"] == "Mouse"


def test_produto_aparece_na_listagem(client):
    client.post(
        "/produtos",
        json={
            "nome": "Teclado",
            "preco": 150
        }
    )

    response = client.get("/produtos")

    assert len(response.json()) == 1


def test_buscar_produto_sucesso(
    client,
    produto_existente
):
    response = client.get(
        f"/produtos/{produto_existente['id']}"
    )

    assert response.status_code == 200


def test_buscar_produto_inexistente(client):
    response = client.get("/produtos/999")

    assert response.status_code == 404


def test_deletar_produto(
    client,
    produto_existente
):
    response = client.delete(
        f"/produtos/{produto_existente['id']}"
    )

    assert response.status_code == 204


def test_deletar_e_confirmar_remocao(
    client,
    produto_existente
):
    client.delete(
        f"/produtos/{produto_existente['id']}"
    )

    response = client.get(
        f"/produtos/{produto_existente['id']}"
    )

    assert response.status_code == 404


def test_deletar_inexistente(client):
    response = client.delete("/produtos/999")

    assert response.status_code == 404


@pytest.mark.parametrize(
    "payload",
    [
        {"nome": "", "preco": 10},
        {"nome": "Teste", "preco": 0},
        {"nome": "Teste", "preco": -5}
    ]
)
def test_payloads_invalidos(client, payload):
    response = client.post(
        "/produtos",
        json=payload
    )

    assert response.status_code == 422


def test_banco_isolado(client):
    response = client.get("/produtos")

    assert response.json() == []