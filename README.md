## Tech Challenge #3
Repositório criado para atender aos requisitos do Tech Challenge da fase atual do curso de Machine Learning Engineering da FIAP. Este projeto engloba a construção de uma API para coleta de dados, armazenamento em banco de dados e aplicação de um modelo de Machine Learning.

## Integrantes
- Eduardo Dias
- Felipe Langoni
- Maxuel Pereira de Oliveira
- Rodrigo de Souza Francisco

## Tecnologias utilizadas
- Python
- FastAPI
- Streamlit
- Swagger
- Docker
- Postgresql

## Proposta do Desafio
O objetivo deste projeto é construir uma API que colete dados, armazene essas informações em um banco de dados relacional e treine um modelo de Machine Learning utilizando essa base de dados. O modelo treinado deve ser utilizado para alimentar uma aplicação ou dashboard, apresentando visualmente os resultados do processo.


## Soluções Implementadas

### Dados Coletados
Utilizamos como dataset dados fornecidos pela B3 através [deste endpoint](https://sistemaswebb3-listados.b3.com.br/indexProxy/indexCall/GetPortfolioDay/eyJsYW5ndWFnZSI6InB0LWJyIiwicGFnZU51bWJlciI6MSwicGFnZVNpemUiOjEyMCwiaW5kZXgiOiJJQk9WIiwic2VnbWVudCI6IjIifQ==) e, com isso, obtermos dados como: Empresas listadas na bolsa de valores, sua participação percentual da ação na carteira teórica da BOVESPA e demais informações.

Com tais dados, precisamos fazer a distribuição em grupo das empresas que mais possuem maior correlação entre elas, seja por indíce de participação 
Após coletados e armazenados, iniciamos o processo a sanitização dos dados. Este processo garante que a análise não considere dados inconsistentes ou nullos.

### Algoritmo K-means
- Utilizamos o Algoritmo K-means para fazer a distribuição da porcentagem de participação pela quantidade teórica
- Separamos os dados em 2 clusters, considerando o resultado obtido com o Elbow Method

### Elbow Method

![](https://raw.githubusercontent.com/edurodriguesdias/tech-challenge-3/refs/heads/main/images/elbow_method.png)

### Dashboard Visualização
Para facilitar a visualização da distribuição feita pelo algoritmo K-means, utilizamos o `streamlit` onde é apresentado o resultado da análise de forma visual/

Para acessar o dashboard, basta abrir o link http://localhost:8501 em seu navegador.

<img width="1064" alt="image" src="https://github.com/user-attachments/assets/a202d9bc-b097-4562-a935-0d80514a4d09">

### Fluxos da Aplicação
![novo drawio](https://github.com/user-attachments/assets/adde7e1c-9b51-470f-82d9-b7fd2fe6ebb4)

## Iniciando a aplicação
**Subir containers docker**
```
docker-compose up -d
```

**Instalar dependências do projeto**
```
docker-compose exec web pip install -r ./requirements/requirements.txt
```

**Limpar cache**
```
rm -rf __pycache__
```

## Banco de Dados
Este projeto utiliza PostgreSQL como banco de dados. Certifique-se de que o container correspondente esteja em status `running` para o correto funcionamento da API.

## Documentação
A API está documentada usando Swagger. Com a aplicação rodando localmente, você pode acessar a documentação no seguinte endereço:
http://localhost:8000/docs
****

## Recursos da API
- GET /extract-data: Coleta os dados da fonte e os armazena no banco de dados.
- GET /optimal-centroid-number: Analisa as informações e indica a melhor quantidade de Clusters usando o Elbow Method.
- POST /training-model: Inicia o processo de treinamento do modelo de Machine Learning com os dados armazenados.
