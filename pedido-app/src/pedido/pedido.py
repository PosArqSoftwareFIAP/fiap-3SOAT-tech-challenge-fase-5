from flask import Blueprint, jsonify,request
import sys
from db import db_mysql_class
from src.produto import get_produto as gp
from src.produto import get_produto_lote
from itertools import groupby
from datetime import datetime
import traceback
import requests

pedido_bp = Blueprint('pedido', __name__)



def check(list):
    check = all(i == list[0] for i in list)
    if check:
        return list[0],check
    return 'Erro', check 



# Rota para criar um novo pedido
@pedido_bp.route('/pedido/cria_pedido', methods=['POST'])
def create_pedido():
    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    cursor = conn.cursor()
    #create pedido
    #lista de dict produto [{id_produto:2,descricao:'xablau'},{id_produto:2,descricao:'xablau'},{id_produto:2,descricao:'sem_bacon'}]
    #cliente
    #endereço do cliente
    #seleciona entregador
    #forma de pagamento
    #
    try:
        print("Passou : Inicio do try",file=sys.stderr)
        data = request.json
        print("Passou : data",file=sys.stderr)
        print(data['produtos'],file=sys.stderr)
        print(type(data['produtos']),file=sys.stderr)


        produtos_list = list(get_produto_lote( [produto['id_produto'] for produto in data['produtos']]))
        print("Passou : get_produto_lote",file=sys.stderr)
        print(produtos_list,file=sys.stderr)



        # for produto in data['produtos']:
        #     produto_info = gp(produto['id_produto'])
        #     produtos_list.append(produto_info)

        disponivel_check = next((item for item in produtos_list if item['disponivel'] == 0), None)
        print("Passou : disponivel_check",file=sys.stderr)



        id_restaurante, id_check = check([x['id_restaurante'] for x in  produtos_list])
        print("Passou : id_restaurante",file=sys.stderr)

        if id_check and disponivel_check == None:
            valor_lista = [float(x['valor']) for x in produtos_list]
            valor_total = sum(valor_lista)
            
            produtos_texto_lista = []

            for produto in data['produtos']:
                
                produto_selecionado = next((item for item in produtos_list if item['id_produto'] == produto['id_produto']), None)
                produto_selecionado['descricao'] = produto['descricao']

                produtos_texto_lista.append(produto_selecionado)

            produtos_texto_string = str(produtos_texto_lista)
            print(produtos_texto_string,file=sys.stderr)


            current_datetime = datetime.now()

            query = "INSERT INTO pedido (id_cliente, id_restaurante, id_entregador, id_endereco_cliente, forma_pagamento, produtos, status_pedido, valor, data_hora_pedido) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (data['id_cliente'], id_restaurante, None, data['id_endereco_cliente'], data['forma_pagamento'], produtos_texto_string, 1, valor_total, current_datetime)
            # arrumar ali no DATA[entregador] para pegar sem o data 
            cursor.execute(query, values)
            conn.commit()


            query_pedido = "SELECT * FROM pedido WHERE id_pedido = (SELECT MAX(id_pedido) FROM pedido WHERE id_cliente = %s AND data_hora_pedido >= NOW() - INTERVAL 3 DAY)"
            values_pedido =(data['id_cliente'],)
            cursor.execute(query_pedido, values_pedido)
            pedido = cursor.fetchone()
            print("Passou: Pedido, query do pedido",file=sys.stderr)
            print(pedido,"\n",file=sys.stderr)

            dados = {
                    "id_pedido": pedido[0],
                    "id_cliente": data.get('id_cliente'),
                    "valor": valor_total,
                    "status": 1
                }
            
            headers = {
                "Content-Type": "application/json"
            }





            response = requests.post("https://octopus-app-865nn.ondigitalocean.app/fatura/cria_fatura/",headers=headers,json=dados,verify=False, allow_redirects=False)
            print(response.status_code)
            print(response.headers) 
            if response.status_code == 301:
                new_url = response.headers['Location']
                response = requests.post(new_url, json=dados, headers=headers)
                print(response.status_code)
                print(response.json())

            return jsonify({"message": "pedido criado com sucesso","id pedido":pedido[0]}), 201
        else:
           return jsonify({"message": "Pedido invalido, produtos de mais de um restaurante no pedido"}), 400
        
    
    except Exception as e:
        error_info = traceback.format_exc()
        print("Ocorreu um erro!")
        print("Mensagem:", str(e))
        print("Informações completas do erro:\n", error_info)
        return jsonify({"error": str(e),  "Informações completas do erro:": error_info}), 400
    finally:
        cursor.close()
        conn.close()




# Rota para recuperar o pedido
@pedido_bp.route('/pedido/consulta_pedido/<int:id>', methods=['GET'])
def get_pedido(id):
    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM pedido WHERE id_pedido = %s"
        cursor.execute(query, (id,))
        pedido = cursor.fetchone()
        if pedido:
            return jsonify(pedido), 200
        else:
            return jsonify({"message": "pedido não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()








# Rota para recuperar o pedido
@pedido_bp.route('/pedido/consulta_pedido_status/<int:id>', methods=['GET'])
def get_pedido_status(id):
    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT pd.*, sp.status_pedido as status_pedido FROM `FIAP-FOOD`.pedido as pd JOIN `FIAP-FOOD`.pedido_status as sp ON pd.status_pedido = sp.id_pedido_status WHERE pd.status_pedido = %s"
        cursor.execute(query, (id,))
        pedido = cursor.fetchall()
        if pedido:
            return jsonify(pedido), 200
        else:
            return jsonify({"message": "pedido não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()







# Rota para atualizar um pedido pelo ID
@pedido_bp.route('/pedido/atualiza_pedido/<int:id>', methods=['PUT'])
def update_pedido(id):
    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    cursor = conn.cursor()
    try:
        data = request.json
        query = "UPDATE pedido SET id_cliente = %s, id_restaurante = %s, id_entregador = %s, id_endereco_cliente = %s, forma_pagamento = %s, produtos = %s, status_pedido = %s, valor = %s, data_hora_pedido = %s WHERE id_pedido = %s"
        values = (data.get('id_cliente'), data.get('id_restaurante'), data.get('id_entregador'), data.get('id_endereco_cliente'), data.get('forma_pagamento'), data.get('produtos'), data.get('status_pedido'), data.get('valor'), data.get('data_hora_pedido'), id)
        cursor.execute(query, values)
        conn.commit()
        return jsonify({"message": "Pedido atualizado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()





# Rota para excluir um pedido pelo ID
@pedido_bp.route('/pedido/deleta_pedido/<int:id>', methods=['DELETE'])
def delete_pedido(id):
    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    cursor = conn.cursor()
    try:
        query = "DELETE FROM pedido WHERE id_pedido = %s"
        cursor.execute(query, (id,))
        conn.commit()
        return jsonify({"message": "pedido excluído com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()



# Rota para atualizar um pedido pelo ID
@pedido_bp.route('/pedido/atualiza_pedido_aguardando/<int:id>', methods=['PUT'])
def update_pedido_aguardando(id):
    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    cursor = conn.cursor()
    try:
        query = "UPDATE pedido SET status_pedido = 1 WHERE id_pedido = %s"
        values = (id,)
        cursor.execute(query, values)
        conn.commit()
        return jsonify({"message": "Pedido atualizado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()







# Rota para atualizar um pedido pelo ID para preparacao
@pedido_bp.route('/pedido/atualiza_pedido_preparacao/<int:id>', methods=['PUT'])
def update_pedido_preparacao(id):
    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    cursor = conn.cursor()
    try:

        query_fatura = "SELECT * FROM fatura WHERE id_pedido = %s"
        values_fatura =(id,)
        cursor.execute(query_fatura, values_fatura)
        fatura = cursor.fetchone()
        print("Passou: query_fatura, ",file=sys.stderr)
        print(fatura,"\n",file=sys.stderr)
        if fatura[4] == 2:
            entregador = requests.get('https://oyster-app-pov9e.ondigitalocean.app/entregador/seleciona_entregador/').json()

            print(entregador,file=sys.stderr)
            
            query = "UPDATE pedido SET id_entregador = %s, status_pedido = 2 WHERE id_pedido = %s"
            values = (entregador['id_entregador'], id)
            cursor.execute(query, values)
            conn.commit()
            return jsonify({"message": "Pedido atualizado com sucesso"}), 200
        else:
         return jsonify({"message": "Erro ao atualizar pedido (Fatura não paga)"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()





# Rota para atualizar um pedido pelo ID
@pedido_bp.route('/pedido/atualiza_pedido_a_caminho/<int:id>', methods=['PUT'])
def update_pedido_a_caminho(id):
    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    cursor = conn.cursor()
    try:
        query = "UPDATE pedido SET status_pedido = 3 WHERE id_pedido = %s"
        values = (id,)
        cursor.execute(query, values)
        conn.commit()
        return jsonify({"message": "Pedido atualizado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()








# Rota para atualizar um pedido pelo ID
@pedido_bp.route('/pedido/atualiza_pedido_pago_entregue/<int:id>', methods=['PUT'])
def update_pedido_entregue(id):
    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    cursor = conn.cursor()
    try:
        query_pedido = "SELECT * FROM pedido WHERE id_pedido =  %s "
        values_pedido =(id,)
        cursor.execute(query_pedido, values_pedido)
        pedido = cursor.fetchone()
        print("Passou: Pedido, query do pedido",file=sys.stderr)
        print(pedido,"\n",file=sys.stderr)


        entregador = requests.put(f"https://oyster-app-pov9e.ondigitalocean.app/entregador/atualiza_entregador_disponivel/{pedido[3]}").json()

        print(entregador,file=sys.stderr)
        
        query = "UPDATE pedido SET status_pedido = 4 WHERE id_pedido = %s"
        values = (id,)
        cursor.execute(query, values)
        conn.commit()
        return jsonify({"message": "Pedido atualizado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()





# Rota para recuperar o pedido
@pedido_bp.route('/pedido/consulta_all_pedido_status/', methods=['GET'])
def get_all_pedido_status():
    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM pedido as pd where pd.status_pedido <> 5 ORDER BY CASE pd.status_pedido WHEN 4 THEN 1 WHEN 3 THEN 2 WHEN 2 THEN 3 WHEN 1  THEN 4 END, pd.data_hora_pedido ASC;"
        cursor.execute(query)
        pedido = cursor.fetchall()
        if pedido:
            return jsonify(pedido), 200
        else:
            return jsonify({"message": "pedido não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()





# Rota para atualizar um pedido pelo ID
@pedido_bp.route('/pedido/atualiza_pedido_cancelado/<int:id>', methods=['PUT'])
def update_pedido_cancelado(id):
    db_objt = db_mysql_class()
    conn = db_objt.get_db_connection()
    cursor = conn.cursor()
    try:
        query = "UPDATE pedido SET status_pedido = 6 WHERE id_pedido = %s"
        values = (id,)
        cursor.execute(query, values)
        conn.commit()
        return jsonify({"message": "Pedido atualizado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


