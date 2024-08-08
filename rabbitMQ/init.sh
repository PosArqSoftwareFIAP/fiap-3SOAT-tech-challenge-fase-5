#!/bin/bash
set -e

# Aguardar o RabbitMQ iniciar
sleep 10

# Configurar variáveis de ambiente
RABBITMQ_USER=${RABBITMQ_DEFAULT_USER:-user}
RABBITMQ_PASSWORD=${RABBITMQ_DEFAULT_PASS:-password}

# Configurar usuário e senha
rabbitmqctl add_user $RABBITMQ_USER $RABBITMQ_PASSWORD
rabbitmqctl set_user_tags $RABBITMQ_USER administrator
rabbitmqctl set_permissions -p / $RABBITMQ_USER ".*" ".*" ".*"

# Criar filas
rabbitmqadmin declare queue name=canal_cria_pedido durable=true
rabbitmqadmin declare queue name=canal_gera_fatura durable=true
rabbitmqadmin declare queue name=canal_cobranca durable=true
rabbitmqadmin declare queue name=canal_confirma_pedido durable=true
rabbitmqadmin declare queue name=canal_cancela_pedido durable=true
rabbitmqadmin declare queue name=canal_solicita_entregador durable=true
rabbitmqadmin declare queue name=canal_confirma_entregador durable=true
rabbitmqadmin declare queue name=canal_confirma_entrega durable=true

# Iniciar o RabbitMQ Server
rabbitmq-server