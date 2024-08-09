import os



# variaveis de banco de dados
db_host     = os.getenv('MYSQL_HOST')
db_user     = os.getenv('MYSQL_USER')
db_password = os.getenv('MYSQL_PASSWORD')
db_port     = 25060
db_database = 'FIAP-FOOD'


# url outros microsserviços
url_entregador = 'https://oyster-app-pov9e.ondigitalocean.app'
url_fatura = 'https://octopus-app-865nn.ondigitalocean.app'