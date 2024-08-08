FROM rabbitmq:3-management

# Copiar o script de inicialização
COPY init.sh /init.sh

# Dar permissão de execução ao script
RUN chmod +x /init.sh

EXPOSE 5672 15672
# Definir o script como ponto de entrada
ENTRYPOINT ["/init.sh"]
