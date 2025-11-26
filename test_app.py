import pytest
from unittest.mock import patch, MagicMock
from app import app  # importa seu Flask

@pytest.fixture
def client():
    """Cria cliente de teste do Flask"""
    app.testing = True
    return app.test_client()


# -------------------------------
# Teste da rota principal "/"
# -------------------------------
def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<html" in response.data.lower()   # deve retornar HTML


# -------------------------------
# Teste enviando mensagem vazia
# -------------------------------
def test_chat_empty_message(client):
    response = client.post("/chat", json={"message": ""})
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["response"] == "Mensagem vazia."


# -------------------------------
# Teste com mock da LLM (OpenAI)
# -------------------------------
@patch("app.llm")
def test_chat_valid_message(mock_llm, client):
    # simula o retorno da LLM
    fake_ai_msg = MagicMock()
    fake_ai_msg.content = "Resposta mockada"
    mock_llm.invoke.return_value = fake_ai_msg

    response = client.post("/chat", json={"message": "Olá!"})
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["response"] == "Resposta mockada"

    # verifica se o modelo foi realmente chamado
    mock_llm.invoke.assert_called_once()
