# fiap-3SOAT-tech-challenge-fase-5
 

# Arquitetura
## **Padrão SAGA**
O padrão SAGA escolhido foi a **Orquestração**. Escolhemos este padrão devido à complexidade do fluxo e quantidade interações dos outros microsserviços com o microsserviço Pedido. Assim sendo, elegemos o serviço de pedido como o orquestrador de todo o fluxo.

Escolhemos o RabbitMQ para ser o nosso gerenciador de mensageria. Criamos as filas referentes à criação de pedidos, geração e cobrança de faturas, confirmação e cancelamento de pedidos, solicitação e confirmação de entregadores, e confirmação de entrega.

   <div align="center">
   <img src="imgs\fluxo saga 3.drawio.png" alt="Fluxo SAGA">
   </div>