import os



# variaveis de banco de dados
db_host     = os.getenv('MYSQL_HOST')
db_user     = os.getenv('MYSQL_USER')
db_password = os.getenv('MYSQL_PASSWORD')
db_port     = 25060
db_database = 'FIAP-FOOD'




# # variaveis de banco de dados
# db_host     = ${{ secrets.MYSQL_HOST }}
# db_user     = ${{ secrets.MYSQL_PASSWORD }}
# db_password = ${{ secrets.MYSQL_USER }}
# db_port     = 25060
# db_database = 'FIAP-FOOD'

