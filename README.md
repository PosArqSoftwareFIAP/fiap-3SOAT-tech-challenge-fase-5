# fiap-3SOAT-tech-challenge-fase-5
 

# Arquitetura
## **Padrão SAGA**
O padrão SAGA escolhido foi a **Orquestração**. Escolhemos este padrão devido à complexidade do fluxo e quantidade interações dos outros microsserviços com o microsserviço Pedido. Assim sendo, elegemos o serviço de pedido como o orquestrador de todo o fluxo.

   <div align="center">
   <img src="imgs\fluxo saga 3.drawio.png" alt="Fluxo SAGA">
   </div>