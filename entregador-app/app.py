from flask import Flask,jsonify,request

from src.entregador import entregador_bp

from functools import wraps
from src.db import db_mysql_class

   
# def token_required(f):
#     token = None 

#     if 'Authorization' in request.headers:
#         if request.headers['Authorization']:
#             token = request.headers['Authorization'].split(" ")[1]

#     if not token:
#         return jsonify({'message': 'Token is missing!'}), 403

#     try:
#         db_objt = db_mysql_class()
#         connection = db_objt.get_db_connection()
#         cursor = connection.cursor()

#         cursor.execute("SELECT user FROM bearer_token WHERE bearer_token = %s", (token,))
#         user = cursor.fetchone()

#         if not user:

#             return jsonify({'message': 'Token is invalid!'}), 403
#     finally:
#         cursor.close()
#         connection.close()

#     return


#Criar uma instância do Flask
app = Flask(__name__)


# @app.before_request
# def before_request():
#     token_func = token_required(lambda: None)
#     return token_func


app.register_blueprint(entregador_bp)


#Iniciar o aplicativo se este arquivo for executado diretamente
if __name__ == '__main__':
    app.run()



