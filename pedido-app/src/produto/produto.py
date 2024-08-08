from flask import Blueprint, jsonify,request
import sys
from db import db_mysql_class


produto_bp = Blueprint('produto', __name__)







@produto_bp.route('/produto/cria_produto', methods=['POST'])
@produto_bp.route('/produto/cria_produto/', methods=['POST'])
def criar_produto():
    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    cursor = conn.cursor()
    try:

        id_restaurante = request.json['id_restaurante']
        nome_produto = request.json['nome_produto']
        descricao = request.json['descricao']
        valor = request.json['valor']
        disponivel = request.json['disponivel']

        query = "INSERT INTO produto (id_restaurante, nome_produto, descricao, valor, disponivel) VALUES (%s, %s, %s, %s, %s)"
        values = (id_restaurante, nome_produto, descricao, valor, disponivel)

        cursor.execute(query, values)
        conn.commit()

        cursor.close()
        return jsonify({"message": "Produto criado com sucesso"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    






# Rota para recuperar o produto
@produto_bp.route('/produto/consulta_produto/<int:id>', methods=['GET'])
@produto_bp.route('/produto/consulta_produto/<int:id>/', methods=['GET'])
def get_produto(id):
    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM produto WHERE id_produto = %s"
        cursor.execute(query, (id,))
        produto = cursor.fetchone()
        if produto:
            return jsonify(produto), 200
        else:
            return jsonify({"message": "produto não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()






@produto_bp.route('/produto/atualiza_produto/<int:id>', methods=['PUT'])
@produto_bp.route('/produto/atualiza_produto/<int:id>/', methods=['PUT'])
def atualizar_produto(id):
    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:

        id_restaurante = request.json['id_restaurante']
        nome_produto = request.json['nome_produto']
        descricao = request.json['descricao']
        valor = request.json['valor']
        disponivel = request.json['disponivel']

        query = "UPDATE produto SET id_restaurante=%s, nome_produto=%s, descricao=%s, valor=%s, disponivel=%s WHERE id_produto=%s"
        values = (id_restaurante, nome_produto, descricao, valor, disponivel, id)

        cursor.execute(query, values)
        conn.commit()

        cursor.close()
        return jsonify({"message": "Produto atualizado com sucesso"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    






@produto_bp.route('/produto/deleta_produto/<int:id>', methods=['DELETE'])
@produto_bp.route('/produto/deleta_produto/<int:id>/', methods=['DELETE'])
def excluir_produto(id):
    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "DELETE FROM produto WHERE id_produto = %s"
        cursor.execute(query, (id,))
        conn.commit()
        cursor.close()
        return jsonify({"message": "Produto excluído com sucesso"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400






@produto_bp.route('/produto/consulta_produto_categoria/<string:categoria>/', methods=['GET'])
def get_produto_categoria(categoria):
    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM produto WHERE categoria = %s"
        cursor.execute(query, (categoria,))
        produto = cursor.fetchone()
        if produto:
            return jsonify(produto), 200
        else:
            return jsonify({"message": "produto não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()














# Rota para recuperar todos os produtos
@produto_bp.route('/produto/consulta_all/', methods=['GET'])
def get_produto_all():
    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM produto"
        cursor.execute(query)
        produto = cursor.fetchall()
        if produto:
            return jsonify(produto), 200
        else:
            return jsonify({"message": "produto não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()









# Rota para recuperar todos os produtos
@produto_bp.route('/produto/consulta_restaurante/<int:id_restaurante>', methods=['GET'])
def get_produto_restaurante(id_restaurante):
    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM produto WHERE id_restaurante = %s and disponivel > 0"
        cursor.execute(query , (id_restaurante,))
        produto = cursor.fetchall()
        if produto:
            return jsonify(produto), 200
        else:
            return jsonify({"message": "produto não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()











# Rota para recuperar o produto
# @produto_bp.route('/produto/produto_lote/', methods=['GET'])
# @swag_from('../swagger_yaml/get_produto_lote.yaml')
def get_produto_lote(produtos_lista):
    print("Passou : Get_prduto",file=sys.stderr)

    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        print("Passou : COMEÇO",file=sys.stderr)

        produtos_string = ','.join(map(str,produtos_lista))
        print("Passou : produtos_string",file=sys.stderr)


        query = f"SELECT * FROM produto WHERE id_produto in ({produtos_string})"
        cursor.execute(query)
        produto = cursor.fetchall()
        if produto:
            return produto
        else:
            print("prdutos não encontrados")
            return [] 
    except Exception as e:
        print(e)
        return [] 
    finally:
        cursor.close()
        conn.close()













# # Rota para recuperar o produto
# @produto_bp.route('/produto/consulta_produto_preco/<int:id>', methods=['GET'])
# @produto_bp.route('/produto/consulta_produto_preco/<int:id>/', methods=['GET'])
# def get_produto_preco(id):
#     db_objt = db_mysql_class()
#     conn = db_objt.get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     try:
#         query = "SELECT valor FROM produto WHERE id_produto = %s"
#         cursor.execute(query, (id,))
#         produto = cursor.fetchone()
#         if produto:
#             return jsonify(produto), 200
#         else:
#             return jsonify({"message": "produto não encontrado"}), 404
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400
#     finally:
#         cursor.close()
#         conn.close()




