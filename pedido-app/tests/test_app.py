import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask.testing import FlaskClient

import sys,os
sys.path.insert(0, os.path.abspath('/home/runner/.local/lib/python3.10/site-packages')) 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Importar a aplicação Flask
from app import app as flask_app

@pytest.fixture
def app() -> Flask:
    flask_app.testing = True
    return flask_app

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

@patch('app.db_mysql_class')
@patch('app.requests')
@patch('app.get_produto_lote')
def test_create_pedido_success(mock_get_produto_lote, mock_requests, mock_db_mysql_class, client):
    mock_db_instance = MagicMock()
    mock_db_mysql_class.return_value = mock_db_instance
    mock_conn = MagicMock()
    mock_db_instance.get_db_connection.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mock_get_produto_lote.return_value = [{'id_produto': 2, 'disponivel': 1, 'id_restaurante': 1, 'valor': 10.0}]
    mock_requests.post.return_value.status_code = 200
    
    response = client.post('/pedido/cria_pedido', json={
        'id_cliente': 1,
        'produtos': [{'id_produto': 2, 'descricao': 'xablau'}],
        'id_endereco_cliente': 1,
        'forma_pagamento': 'dinheiro'
    })
    
    assert response.status_code == 201
    assert 'pedido criado com sucesso' in response.json['message']

@patch('app.db_mysql_class')
@patch('app.requests')
@patch('app.get_produto_lote')
def test_create_pedido_fail_unavailable_product(mock_get_produto_lote, mock_requests, mock_db_mysql_class, client):
    mock_db_instance = MagicMock()
    mock_db_mysql_class.return_value = mock_db_instance
    mock_conn = MagicMock()
    mock_db_instance.get_db_connection.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mock_get_produto_lote.return_value = [{'id_produto': 2, 'disponivel': 0, 'id_restaurante': 1, 'valor': 10.0}]
    
    response = client.post('/pedido/cria_pedido', json={
        'id_cliente': 1,
        'produtos': [{'id_produto': 2, 'descricao': 'xablau'}],
        'id_endereco_cliente': 1,
        'forma_pagamento': 'dinheiro'
    })
    
    assert response.status_code == 400
    assert 'Pedido invalido' in response.json['message']

@patch('app.db_mysql_class')
def test_get_pedido_success(mock_db_mysql_class, client):
    mock_db_instance = MagicMock()
    mock_db_mysql_class.return_value = mock_db_instance
    mock_conn = MagicMock()
    mock_db_instance.get_db_connection.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchone.return_value = {
        'id_pedido': 1,
        'id_cliente': 1,
        'valor': 10.0,
        'status_pedido': 1
    }
    
    response = client.get('/pedido/consulta_pedido/1')
    
    assert response.status_code == 200
    assert 'id_pedido' in response.json

@patch('app.db_mysql_class')
def test_get_pedido_not_found(mock_db_mysql_class, client):
    mock_db_instance = MagicMock()
    mock_db_mysql_class.return_value = mock_db_instance
    mock_conn = MagicMock()
    mock_db_instance.get_db_connection.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchone.return_value = None
    
    response = client.get('/pedido/consulta_pedido/999')
    
    assert response.status_code == 404
    assert 'pedido não encontrado' in response.json['message']

@patch('app.db_mysql_class')
def test_delete_pedido_success(mock_db_mysql_class, client):
    mock_db_instance = MagicMock()
    mock_db_mysql_class.return_value = mock_db_instance
    mock_conn = MagicMock()
    mock_db_instance.get_db_connection.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    response = client.delete('/pedido/deleta_pedido/1')
    
    assert response.status_code == 200
    assert 'pedido excluído com sucesso' in response.json['message']

@patch('app.db_mysql_class')
def test_delete_pedido_fail(mock_db_mysql_class, client):
    mock_db_instance = MagicMock()
    mock_db_mysql_class.return_value = mock_db_instance
    mock_conn = MagicMock()
    mock_db_instance.get_db_connection.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception('DB error')
    
    response = client.delete('/pedido/deleta_pedido/1')
    
    assert response.status_code == 400
    assert 'error' in response.json

if __name__ == '__main__':
    pytest.main()
