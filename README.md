# Datathon Fase 5

Este repositório foi criado para atender aos requisitos do **Datathon** da Fase 5 do curso de **Machine Learning Engineering** da FIAP. O desafio envolve a criação de um sistema de recomendação para a Globo, visando prever quais notícias os usuários do G1 irão consumir a seguir, com foco em técnicas de aprendizado de máquina.

## Integrantes
- **Eduardo Dias**
- **Felipe Langoni**

## Tecnologias Utilizadas
- **Python**
- **FastAPI**
- **Swagger**
- **Docker**

## Descrição do Desafio

O objetivo deste Datathon é desenvolver um modelo de **sistema de recomendação** para prever qual será a próxima notícia que um usuário do G1 lerá, considerando:
1. A recência dos conteúdos.
2. O desafio do **cold-start**, quando novos usuários ou itens não possuem informações suficientes para alimentar o sistema de recomendação.

O modelo deve ser treinado com dados sobre os usuários e seus históricos de leitura, criando uma API para fornecer recomendações personalizadas. Após isso, o modelo será empacotado em um container Docker e disponibilizado em um ambiente de produção (AWS, GCP).

## Soluções Implementadas

### Coleta e Armazenamento de Dados
Utilizamos um conjunto de dados fornecido pela Globo, que inclui informações sobre os usuários e seu histórico de acesso a notícias. O armazenamento e pré-processamento desses dados são feitos de forma eficiente para treinar o modelo de recomendação.

### Abordagens de Recomendação
O modelo de recomendação considera diferentes abordagens, como:
- **Content-Based Filtering**: Recomendar notícias com base nas características dos próprios itens.
- **Previsão do Próximo Item**: Usar o histórico do usuário para prever o próximo item.
- **Cold-Start**: Resolver o problema do cold-start, oferecendo recomendações para usuários novos ou conteúdos sem histórico.

### Processo de Treinamento
O modelo foi treinado com base no histórico de dados de usuários, considerando a recência das notícias e a relevância dos itens.

### Criação da API
Desenvolvemos uma API com **FastAPI** para fornecer previsões e recomendações personalizadas aos usuários.

### Empacotamento com Docker
O projeto foi empacotado em um container Docker para facilitar o deployment e a escalabilidade da aplicação.

## Como Rodar a Aplicação

### Subir os Containers Docker
1. **Build do container Docker:**
```bash
docker-compose up -d --build
```

## Recursos da API

### POST /recommend
Este endpoint fornece recomendações de notícias com base no histórico do usuário e na recência das notícias. Em casos de **cold-start**, ele recomenda as notícias mais populares.

#### Como Fazer uma Requisição:
Use o comando `curl` para testar a API localmente:

```bash
curl -X POST "http://localhost:8000/recommend" \
-H "Content-Type: application/json" \
-d '{
    "history": ["13db0ab1-eea2-4603-84c4-f40a876c7400"],
    "timestampHistory_new": [1708473600],
    "top_n": 3
}'
```

### Exemplo de Resposta

```json
{
  "recommendations": [
    {
      "page": "d6620ce8-945f-4924-9b67-8bd3bffcdb7f",
      "title": "Caso Vitória Gabrielly: STJ rejeita pedido da defesa para anulação de julgamento"
    },
    {
      "page": "59ea1631-5702-4b66-9aae-703ce1ee9e56",
      "title": "PF prende mais três suspeitos de envolvimento na ocultação dos corpos de Bruno e Dom"
    },
    {
      "page": "9aa5e6c8-f7a9-46b4-839a-61a140210209",
      "title": "PF faz operação contra..."
    }
  ]
}
```

