import pytest
from unittest.mock import patch, MagicMock
from src.entregador.entregador_rotas import entregador_bp, create_entregador, get_entregador, update_entregador, delete_entregador, get_entregador_all, get_entregador_disponivel, update_entregador_disponivel, update_entregador_indisponivel, seleciona_entregador
from flask import Flask
import sys,os
sys.path.insert(0, os.path.abspath('/home/runner/.local/lib/python3.10/site-packages')) 
from flask_testing import TestCase


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(entregador_bp)
    app.config['TESTING'] = True
    client = app.test_client()
    
    yield client

@patch('src.db.db_mysql_class.get_db_connection')
def test_create_entregador(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    response = client.post('/entregador/cria_entregador', json={
        'nome': 'Teste', 'cpf': '12345678900', 'telefone': '999999999', 'email': 'teste@teste.com', 'placa': 'ABC1234', 'tipo_veiculo': 'carro', 'disponivel': True
    })
    
    assert response.status_code == 201
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('src.db.db_mysql_class.get_db_connection')
def test_get_entregador(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {'id_entregador': 1, 'nome': 'Teste'}
    
    response = client.get('/entregador/consulta_entregador/1')
    
    assert response.status_code == 200
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('src.db.db_mysql_class.get_db_connection')
def test_get_entregador_not_found(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    
    response = client.get('/entregador/consulta_entregador/999')
    
    assert response.status_code == 404
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('src.db.db_mysql_class.get_db_connection')
def test_update_entregador(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    response = client.put('/entregador/atualiza_entregador/1', json={
        'nome': 'Teste Atualizado', 'cpf': '12345678900', 'telefone': '999999999', 'email': 'teste@teste.com', 'placa': 'ABC1234', 'tipo_veiculo': 'carro', 'disponivel': True
    })
    
    assert response.status_code == 200
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('src.db.db_mysql_class.get_db_connection')
def test_delete_entregador(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    response = client.delete('/entregador/deleta_entregador/1')
    
    assert response.status_code == 200
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('src.db.db_mysql_class.get_db_connection')
def test_get_entregador_all(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [{'id_entregador': 1, 'nome': 'Teste'}]
    
    response = client.get('/entregador/consulta_all/')
    
    assert response.status_code == 200
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('src.db.db_mysql_class.get_db_connection')
def test_get_entregador_all_empty(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []
    
    response = client.get('/entregador/consulta_all/')
    
    assert response.status_code == 404
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('src.db.db_mysql_class.get_db_connection')
def test_get_entregador_disponivel(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [{'id_entregador': 1, 'nome': 'Teste', 'disponivel': 1}]
    
    response = client.get('/entregador/consulta_entregador_disponivel/')
    
    assert response.status_code == 200
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('src.db.db_mysql_class.get_db_connection')
def test_get_entregador_disponivel_empty(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []
    
    response = client.get('/entregador/consulta_entregador_disponivel/')
    
    assert response.status_code == 404
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('src.db.db_mysql_class.get_db_connection')
def test_update_entregador_disponivel(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    response = client.put('/entregador/atualiza_entregador_disponivel/1')
    
    assert response.status_code == 200
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('src.db.db_mysql_class.get_db_connection')
def test_update_entregador_indisponivel(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    response = client.put('/entregador/atualiza_entregador_indisponivel/1')
    
    assert response.status_code == 200
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('src.db.db_mysql_class.get_db_connection')
def test_seleciona_entregador(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {'id_entregador': 1, 'nome': 'Teste', 'disponivel': 1}
    
    response = client.get('/entregador/seleciona_entregador/')
    
    assert response.status_code == 200
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('src.db.db_mysql_class.get_db_connection')
def test_seleciona_entregador_not_found(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    
    response = client.get('/entregador/seleciona_entregador/')
    
    assert response.status_code == 404
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch('src.db.db_mysql_class.get_db_connection')
def test_update_entregador_success(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    response = client.put('/entregador/atualiza_entregador/1', json={
        'nome': 'Teste Atualizado', 'cpf': '12345678900', 'telefone': '999999999', 'email': 'teste@teste.com', 'placa': 'ABC1234', 'tipo_veiculo': 'carro', 'disponivel': True
    })
    
    assert response.status_code == 200
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('src.db.db_mysql_class.get_db_connection')
def test_update_entregador_fail(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Database error")
    
    response = client.put('/entregador/atualiza_entregador/1', json={
        'nome': 'Teste Atualizado', 'cpf': '12345678900', 'telefone': '999999999', 'email': 'teste@teste.com', 'placa': 'ABC1234', 'tipo_veiculo': 'carro', 'disponivel': True
    })
    
    assert response.status_code == 400
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch('src.db.db_mysql_class.get_db_connection')
def test_create_entregador_success(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    response = client.post('/entregador/cria_entregador', json={
        'nome': 'Teste', 'cpf': '12345678900', 'telefone': '999999999', 'email': 'teste@teste.com', 'placa': 'ABC1234', 'tipo_veiculo': 'carro', 'disponivel': True
    })
    
    assert response.status_code == 201
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('src.db.db_mysql_class.get_db_connection')
def test_create_entregador_fail(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Database error")
    
    response = client.post('/entregador/cria_entregador', json={
        'nome': 'Teste', 'cpf': '12345678900', 'telefone': '999999999', 'email': 'teste@teste.com', 'placa': 'ABC1234', 'tipo_veiculo': 'carro', 'disponivel': True
    })
    
    assert response.status_code == 400
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('src.db.db_mysql_class.get_db_connection')
def test_delete_entregador_success(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    response = client.delete('/entregador/deleta_entregador/1')
    
    assert response.status_code == 200
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('src.db.db_mysql_class.get_db_connection')
def test_delete_entregador_fail(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Database error")
    
    response = client.delete('/entregador/deleta_entregador/1')
    
    assert response.status_code == 400
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('src.db.db_mysql_class.get_db_connection')
def test_seleciona_entregador_success(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {'id_entregador': 1, 'nome': 'Teste', 'disponivel': 1}
    
    response = client.get('/entregador/seleciona_entregador/')
    
    assert response.status_code == 200
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('src.db.db_mysql_class.get_db_connection')
def test_seleciona_entregador_not_found(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    
    response = client.get('/entregador/seleciona_entregador/')
    
    assert response.status_code == 404
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('src.db.db_mysql_class.get_db_connection')
def test_seleciona_entregador_fail(mock_get_db_connection, client):
    # Given: Uma conexão de banco de dados que lançará uma exceção
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Erro no banco de dados")
    
    # When: O cliente solicita selecionar um entregador disponível
    response = client.get('/entregador/seleciona_entregador/')
    
    # Then: A resposta deve ser um erro 400
    assert response.status_code == 400
    
    # And: O método execute deve ser chamado uma vez
    mock_cursor.execute.assert_called_once()
    
    # And: O cursor deve ser fechado uma vez
    mock_cursor.close.assert_called_once()
    
    # And: A conexão deve ser fechada uma vez
    mock_conn.close.assert_called_once()



if __name__ == '__main__':
    pytest.main()
