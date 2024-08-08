import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, json
from src.fatura import fatura_bp

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(fatura_bp)
    client = app.test_client()
    yield client

@patch('src.fatura.db_mongo_class')
def test_create_fatura_success(mock_db_mongo_class, client):
    mock_collection = MagicMock()
    mock_db_instance = MagicMock()
    mock_db_instance.get_collection.return_value = mock_collection
    mock_collection.find.return_value.sort.return_value.limit.return_value = [{"id_fatura": 1}]
    mock_db_mongo_class.return_value = mock_db_instance

    data = {
        "id_pedido": 1,
        "id_cliente": 1,
        "valor": 100,
        "status": 0
    }
    response = client.post('/fatura/cria_fatura/', json=data)

    assert response.status_code == 201
    assert response.json == {"message": "Fatura criado com sucesso"}

@patch('src.fatura.db_mongo_class')
def test_create_fatura_error(mock_db_mongo_class, client):
    mock_db_instance = MagicMock()
    mock_db_instance.get_collection.side_effect = Exception("Erro de conexão")
    mock_db_mongo_class.return_value = mock_db_instance

    data = {
        "id_pedido": 1,
        "id_cliente": 1,
        "valor": 100,
        "status": 0
    }
    response = client.post('/fatura/cria_fatura/', json=data)

    assert response.status_code == 400
    assert "error" in response.json

@patch('src.fatura.db_mongo_class')
def test_get_fatura_success(mock_db_mongo_class, client):
    mock_collection = MagicMock()
    mock_db_instance = MagicMock()
    mock_db_instance.get_collection.return_value = mock_collection
    mock_collection.find_one.return_value = {"id_fatura": 1, "id_pedido": 1}
    mock_db_mongo_class.return_value = mock_db_instance

    response = client.get('/fatura/consulta_fatura/1')

    assert response.status_code == 200
    assert json.loads(response.data) == {"id_fatura": 1, "id_pedido": 1}

@patch('src.fatura.db_mongo_class')
def test_get_fatura_not_found(mock_db_mongo_class, client):
    mock_collection = MagicMock()
    mock_db_instance = MagicMock()
    mock_db_instance.get_collection.return_value = mock_collection
    mock_collection.find_one.return_value = None
    mock_db_mongo_class.return_value = mock_db_instance

    response = client.get('/fatura/consulta_fatura/1')

    assert response.status_code == 404
    assert response.json == {"message": "fatura não encontrada"}

@patch('src.fatura.db_mongo_class')
def test_update_fatura_status_success(mock_db_mongo_class, client):
    mock_collection = MagicMock()
    mock_db_instance = MagicMock()
    mock_db_instance.get_collection.return_value = mock_collection
    mock_db_mongo_class.return_value = mock_db_instance

    data = {"status": 1}
    response = client.put('/fatura/atualiza_fatura/1', json=data)

    assert response.status_code == 200
    assert response.json == {"message": "Fatura atualizada com sucesso"}

@patch('src.fatura.db_mongo_class')
def test_update_fatura_status_error(mock_db_mongo_class, client):
    mock_db_instance = MagicMock()
    mock_db_instance.get_collection.side_effect = Exception("Erro de conexão")
    mock_db_mongo_class.return_value = mock_db_instance

    data = {"status": 1}
    response = client.put('/fatura/atualiza_fatura/1', json=data)

    assert response.status_code == 400
    assert "error" in response.json

# Testes para rotas adicionais de atualização de status
@patch('src.fatura.db_mongo_class')
def test_update_fatura_status_pago(mock_db_mongo_class, client):
    mock_collection = MagicMock()
    mock_db_instance = MagicMock()
    mock_db_instance.get_collection.return_value = mock_collection
    mock_db_mongo_class.return_value = mock_db_instance

    response = client.put('/fatura/atualiza_fatura_pago/1')

    assert response.status_code == 200
    assert response.json == {"message": "Fatura atualizada com sucesso"}

@patch('src.fatura.db_mongo_class')
def test_update_fatura_status_nao_pago(mock_db_mongo_class, client):
    mock_collection = MagicMock()
    mock_db_instance = MagicMock()
    mock_db_instance.get_collection.return_value = mock_collection
    mock_db_mongo_class.return_value = mock_db_instance

    response = client.put('/fatura/atualiza_fatura_nao_pago/1')

    assert response.status_code == 200
    assert response.json == {"message": "Fatura atualizada com sucesso"}

@patch('src.fatura.db_mongo_class')
def test_update_fatura_status_cancelado(mock_db_mongo_class, client):
    mock_collection = MagicMock()
    mock_db_instance = MagicMock()
    mock_db_instance.get_collection.return_value = mock_collection
    mock_db_mongo_class.return_value = mock_db_instance

    response = client.put('/fatura/atualiza_fatura_cancelado/1')

    assert response.status_code == 200
    assert response.json == {"message": "Fatura cancelada com sucesso"}

@patch('src.fatura.db_mongo_class')
def test_consulta_all_fatura(mock_db_mongo_class, client):
    # Given: Configurando os mocks
    mock_collection = MagicMock()
    mock_db_instance = MagicMock()
    mock_db_instance.get_collection.return_value = mock_collection
    mock_collection.find.return_value = [{"id_fatura": 1}, {"id_fatura": 2}]
    mock_db_mongo_class.return_value = mock_db_instance

    # When: Fazendo a requisição para a rota '/fatura/consulta_all/'
    response = client.get('/fatura/consulta_all/')

    # Then: Verificando se a resposta é 200 (OK)
    assert response.status_code == 200
    # Verificando se a quantidade de faturas retornadas é 2
    assert len(json.loads(response.data)) == 2
