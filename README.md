## Tech Challenge #3
Repositório criado para atender aos requisitos do Tech Challenge da fase atual do curso de Machine Learning Engineering da FIAP. Este projeto engloba a construção de uma API para coleta de dados, armazenamento em banco de dados e aplicação de um modelo de Machine Learning.

## Integrantes
- Eduardo Dias
- Felipe Langoni

## Tecnologias utilizadas
- Python
- FastAPI
- Swagger
- Docker

## Proposta do Desafio
O objetivo deste projeto é construir uma API que colete dados, armazene essas informações em um banco de dados relacional e treine um modelo de Machine Learning utilizando essa base de dados. O modelo treinado deve ser utilizado para alimentar uma aplicação ou dashboard, apresentando visualmente os resultados do processo.


## Soluções Implementadas

### Dados Coletados
Utilizamos como dataset dados fornecidos pela globo através [deste endpoint](https://drive.google.com/file/d/13rvnyK5PJADJQgYe-VbdXb7PpLPj7lPr/view).

Com tais dados, precisamos fazer a distribuição em grupo das empresas que mais possuem maior correlação entre elas, seja por indíce de participação 
Após coletados e armazenados, iniciamos o processo a sanitização dos dados. Este processo garante que a análise não considere dados inconsistentes ou nullos.



## Iniciando a aplicação
**Subir containers docker**
```
sudo docker build -t meu-app .
sudo docker run -it -p 80:80 meu-app
```


**Limpar cache**
```
rm -rf __pycache__
```


## Recursos da API
- POST /recommend - Recomenda noticias com base no histórico do usuário e a recencia das notícias, considerando o cold start, recomenda as notícias mais populares do momento caso não exista histórico.


Como fazer uma requisição:

```
curl -X POST "http://localhost:80/recommend"      -H "Content-Type: application/json"      -d '{
           "history": ["13db0ab1-eea2-4603-84c4-f40a876c7400"],
           "timestampHistory_new": [1708473600],
           "top_n": 3
         }'
```
Output:
```
{"recommendations":[{"page":"d6620ce8-945f-4924-9b67-8bd3bffcdb7f","title":"Caso Vitória Gabrielly: STJ rejeita pedido da defesa para anulação de julgamento"},{"page":"59ea1631-5702-4b66-9aae-703ce1ee9e56","title":"PF prende mais três suspeitos de envolvimento na ocultação dos corpos de Bruno e Dom "},{"page":"9aa5e6c8-f7a9-46b4-839a-61a140210209","title":"PF faz operação contra..}]}
```