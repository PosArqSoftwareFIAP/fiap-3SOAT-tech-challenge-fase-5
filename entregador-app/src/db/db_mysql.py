import config as config
import mysql.connector
import os
import sys

class db_mysql_class:
    def __init__(self):

        # Configurações do banco de dados
        self.db_config = {
            'host':     config.db_host,
            'user':     config.db_user,
            'password': config.db_password,
            'port' :    config.db_port,
            'database': config.db_database
        }


    def get_db_connection(self):
        return mysql.connector.connect(**self.db_config)


