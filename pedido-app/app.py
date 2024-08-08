from flask import Flask,jsonify,request
import mysql.connector
import os
import sys
from src.avaliacao import avaliacao_bp
from src.pedido import pedido_bp
from src.produto import produto_bp
from functools import wraps
from db import db_mysql_class




#Criar uma instância do Flask
app = Flask(__name__)


app.register_blueprint(produto_bp)
app.register_blueprint(pedido_bp)
app.register_blueprint(avaliacao_bp)




#Iniciar o aplicativo se este arquivo for executado diretamente
if __name__ == '__main__':
    app.run()



