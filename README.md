# fiap-3SOAT-tech-challenge-fase-5
 

## **Instruções para Executar**
Os nossos microsserviços estão sendo executados utilizando containers Docker no Kubernetes na Cloud DigitalOcean. **Para executá-los basta fazer o build e deploy das imagens a partir dos Dockerfiles nos diretórios pedido-app, fatura-app e entregador-app.**

   <div align="center">
   <img src="imgs\Desenho_Arquitetura_FIAPFOOD.png" alt="Estrutura Kubernetes">
   </div>


Também é necessário ajustar as variáveis de ambiente de acesso ao MySQL e as urls dos serviços fatura e entregador no arquivo config.py do pedido-app:

   <div align="center">
   <img src="imgs\urls.png" alt="urls">
   </div>

## **Padrão SAGA**
O padrão SAGA escolhido foi a **Orquestração**. Escolhemos este padrão devido à complexidade do fluxo e quantidade interações dos outros microsserviços com o microsserviço Pedido. Assim sendo, elegemos o serviço de pedido como o orquestrador de todo o fluxo.

Escolhemos o RabbitMQ para ser o nosso gerenciador de mensageria. Criamos as filas referentes à criação de pedidos, geração e cobrança de faturas, confirmação e cancelamento de pedidos, solicitação e confirmação de entregadores, e confirmação de entrega.

   <div align="center">
   <img src="imgs\fluxo saga 3.drawio.png" alt="Fluxo SAGA">
   </div>

## **OWASP ZAP**
Geramos os relatórios de OWASP ZAP para os endpoints: 

**/produto/consulta_restaurante/5** (Cardápio)

**/pedido/cria_pedido** (Checkout)

**/fatura/cria_fatura** (Geração de Pagamento)



   <div align="center">
   <img src="imgs\fluxo saga 3.drawio.png" alt="Fluxo SAGA">
   </div>