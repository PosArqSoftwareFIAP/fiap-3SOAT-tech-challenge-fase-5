import pytest

import sys,os
sys.path.insert(0, os.path.abspath('/home/runner/.local/lib/python3.10/site-packages')) 
from flask_testing import TestCase

import sys,os

# Adiciona o diretório raiz ao caminho do sistema
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class TestApp(TestCase):
    def create_app(self):
        # Configura a aplicação para o modo de testes
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        return app

    def test_consulta_entregador(self):
        response = self.client.get('/entregador/consulta_entregador/3')
        self.assertEqual(response.status_code, 200)

    def test_consulta_todos_entregadores(self):
        response = self.client.get('/entregador/consulta_all/')
        self.assertEqual(response.status_code, 200)

    def test_consulta_entregador_disponivel(self):
        response = self.client.get('/entregador/consulta_entregador_disponivel/')
        self.assertEqual(response.status_code, 200)

    def test_update_entregador_indisponivel(self):
        response = self.client.put('/entregador/atualiza_entregador_indisponivel/3')
        self.assertEqual(response.status_code, 200)

    def test_update_entregador_disponivel(self):
        response = self.client.put('/entregador/atualiza_entregador_disponivel/3')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    pytest.main()

