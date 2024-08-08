from flask import Flask,jsonify,request
import mysql.connector
import os
import sys

from fatura import fatura_bp

from functools import wraps
from db import db_mysql_class



#Criar uma instância do Flask
app = Flask(__name__)

app.register_blueprint(fatura_bp)





#Iniciar o aplicativo se este arquivo for executado diretamente
if __name__ == '__main__':
    app.run()



