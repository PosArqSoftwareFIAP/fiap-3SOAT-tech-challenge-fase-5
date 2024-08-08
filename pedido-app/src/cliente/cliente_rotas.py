from flask import Blueprint, jsonify,request
import sys
from db import db_mysql_class
from flasgger import swag_from


cliente_bp = Blueprint('cliente', __name__)




@cliente_bp.route('/cliente/cria_cliente', methods=['POST'])
@swag_from('../swagger_yaml/create_cliente.yaml')
def create_cliente():
    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    cursor = conn.cursor()
    try:
        data = request.json
        query = "INSERT INTO cliente (nome, cpf, telefone, email, data_nascimento, data_cadastro) VALUES (%s, %s, %s, %s, %s, NOW())"
        values = (data['nome'], data['cpf'], data['telefone'], data['email'], data['data_nascimento'])
        cursor.execute(query, values)
        conn.commit()
        return jsonify({"message": "Cliente criado com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()



# Rota para consultar um cliente pelo ID
@cliente_bp.route('/cliente/consulta_cliente/<int:id>', methods=['GET'])
@swag_from('../swagger_yaml/get_cliente.yaml')
def get_cliente(id):
    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM cliente WHERE id_cliente = %s"
        cursor.execute(query, (id,))
        cliente = cursor.fetchone()
        if cliente:
            return jsonify(cliente), 200
        else:
            return jsonify({"message": "Cliente não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()






# Rota para atualizar um cliente pelo ID
@cliente_bp.route('/cliente/atualiza_cliente/<int:id>', methods=['PUT'])
@swag_from('../swagger_yaml/update_cliente.yaml')
def update_cliente(id):
    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    cursor = conn.cursor()
    try:
        data = request.json
        query = "UPDATE cliente SET nome = %s, cpf = %s, telefone = %s, email = %s, data_nascimento = %s WHERE id_cliente = %s"
        values = (data['nome'], data['cpf'], data['telefone'], data['email'], data['data_nascimento'], id)
        cursor.execute(query, values)
        conn.commit()
        return jsonify({"message": "Cliente atualizado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()




# Rota para excluir um cliente pelo ID
@cliente_bp.route('/cliente/deleta_cliente/<int:id>', methods=['DELETE'])
@swag_from('../swagger_yaml/delete_cliente.yaml')
def delete_cliente(id):
    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    cursor = conn.cursor()
    try:
        query = "DELETE FROM cliente WHERE id_cliente = %s"
        cursor.execute(query, (id,))
        conn.commit()
        return jsonify({"message": "Cliente excluído com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()










# Rota de cria endereco_cliente 
@cliente_bp.route('/cliente/cria_endereco_cliente', methods=['POST'])
@swag_from('../swagger_yaml/criar_endereco_cliente.yaml')
def criar_endereco_cliente():
    
    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    try:
        cursor = conn.cursor()

        rua = request.json['rua']
        numero = request.json['numero']
        bairro = request.json['bairro']
        cep = request.json['cep']
        estado = request.json['estado']
        cidade = request.json['cidade']
        complemento = request.json['complemento']
        id_cliente = request.json['id_cliente']

        query = "INSERT INTO endereco_cliente (rua, numero, bairro, cep, estado, cidade, complemento, id_cliente) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (rua, numero, bairro, cep, estado, cidade, complemento, id_cliente)

        cursor.execute(query, values)
        conn.commit()

        cursor.close()
        return jsonify({"message": "Endereço para cliente criado com sucesso"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400






# Rota para consultar todos os endereco_cliente pelo ID do cliente
@cliente_bp.route('/cliente/consulta_endereco_cliente/<int:id>', methods=['GET'])
@swag_from('../swagger_yaml/obter_endereco_cliente.yaml')
def obter_endereco_cliente(id):

    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM endereco_cliente WHERE id_cliente = %s"
        cursor.execute(query, (id,))
        endereco = cursor.fetchall()
        cursor.close()

        if endereco:
            return jsonify(endereco), 200
        else:
            return jsonify({"message": "Endereço para cliente não encontrado"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 400






# Rota para atualizar um cliente pelo ID
@cliente_bp.route('/cliente/atualiza_endereco_cliente/<int:id>', methods=['PUT'])
@swag_from('../swagger_yaml/atualizar_endereco_cliente.yaml')
def atualizar_endereco_cliente(id):

    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    try:
        cursor = conn.cursor()

        rua = request.json['rua']
        numero = request.json['numero']
        bairro = request.json['bairro']
        cep = request.json['cep']
        estado = request.json['estado']
        cidade = request.json['cidade']
        complemento = request.json['complemento']
        id_cliente = request.json['id_cliente']

        query = "UPDATE endereco_cliente SET rua=%s, numero=%s, bairro=%s, cep=%s, estado=%s, cidade=%s, complemento=%s, id_cliente=%s WHERE id_endereco_cliente=%s"
        values = (rua, numero, bairro, cep, estado, cidade, complemento, id_cliente, id)

        cursor.execute(query, values)
        conn.commit()

        cursor.close()
        return jsonify({"message": "Endereço para cliente atualizado com sucesso"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400







# Rota para excluir um cliente pelo ID
@cliente_bp.route('/cliente/deleta_endereco_cliente/<int:id>', methods=['DELETE'])
@swag_from('../swagger_yaml/excluir_endereco_cliente.yaml')
def excluir_endereco_cliente(id):

    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    try:
        cursor = conn.cursor()
        query = "DELETE FROM endereco_cliente WHERE id_endereco_cliente = %s"
        cursor.execute(query, (id,))
        conn.commit()
        cursor.close()
        return jsonify({"message": "Endereço para cliente excluído com sucesso"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400









# Rota para consultar um cliente pelo CPF
@cliente_bp.route('/cliente/consulta_cliente_cpf/<string:cpf>', methods=['GET'])
@swag_from('../swagger_yaml/get_cliente_cpf.yaml')
def get_cliente_cpf(cpf):
    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM cliente WHERE cpf = %s"
        cursor.execute(query, (cpf,))
        cliente = cursor.fetchone()
        if cliente:
            return jsonify(cliente), 200
        else:
            return jsonify({"message": "Cliente não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


