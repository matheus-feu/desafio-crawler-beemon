[![wakatime](https://wakatime.com/badge/user/3bd24664-869f-460a-94e1-b98da8136504/project/018b0553-2e4f-452e-8f1c-50e5d4c05dee.svg)](https://wakatime.com/@Feu/projects/jdeiczpjnu?start=2023-10-03&end=2023-10-09) 

<h2 align="center">Crawler - IMDb</h2>

## Índice

- [Sobre](#-sobre)
- [Interface Web](#-interface-web)
- [Tecnologias utilizadas](#-tecnologias-utilizadas)
- [Como baixar o projeto](#-como-baixar-o-projeto)
- [Como executar o projeto](#-como-executar-o-projeto)
- [Autor](#-autor)

## 📖 Sobre

Este é um projeto Python/Django projetado para coletar informações dos 250 filmes mais bem avaliados
no [IMDb](https://www.imdb.com/chart/top/). O projeto executa a coleta de dados, armazena as informações em arquivos
CSV/JSON sendo possíveis realizar o download na interface e exibe um DataFrame do Pandas ao final da execução.

Além disso, os dados também são armazenados em um banco de dados PostgreSQL hospedado no [Render](https://render.com) e
o broker [Redis](https://redis.io/) hospedado na [AWS](https://aws.amazon.com/pt/).

### Principais Características

- **Coleta de Dados**: O projeto coleta detalhes sobre os 250 filmes mais bem avaliados no IMDb, incluindo título, ano
  de lançamento, duração, classificação e número de votos.


- **Armazenamento em Arquivos**: Os dados podem ser salvos em formato CSV ou JSON, proporcionando flexibilidade na
  utilização futura desses dados.


- **Banco de Dados PostgreSQL**: Os dados também são armazenados em um banco de dados PostgreSQL, que está hospedado no
  Render. Note que, devido à hospedagem no Render, as operações de escrita no banco de dados podem ser um pouco lentas.

    - Se você quiser executar o projeto localmente, você pode simplesmente alterar as configurações do banco de dados
      para um banco de dados local ou hospedado remotamente, basta mudar as configurações no arquivo `.env`.

      ```bash
      # .env
      DB_NAME=postgres
      DB_USER=postgres
      DB_PASSWORD=postgres
      DB_HOST=db
      DB_PORT=5432
      ```

- **Execução Assíncrona com Celery e Redis**: O projeto utiliza o Celery em conjunto com o Redis hospedado na AWS como
  broker para executar a tarefa de coleta de dados de forma assíncrona a cada 20 minutos. Isso mantém os dados
  atualizados automaticamente.

- **Formulário de Feedback**: O projeto inclui um formulário de feedback, que permite aos usuários enviar comentários e
  mensagens. O envio de e-mails é tratado de forma assíncrona pelo Celery, com a função `send_email` do Django sendo
  utilizada para o envio de e-mails.

### Configuração do Agendamento (Schedules)

Você pode ajustar o agendamento da tarefa de coleta de dados no [Django Admin](http://localhost:8000/admin)
em `Period Tasks` ou diretamente no arquivo `core.celery.py`.

[![Django Admin](https://imgur.com/vkJrYSI.png)](http://localhost:8000/admin)

Abaixo está um exemplo de configuração no arquivo `celery.py` em `schedule`, conforme a documentação
do [Celery Schedule](https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html#crontab-schedules).

```python
app.conf.beat_schedule = {
    'scrapy_task': {
        'task': 'scrapy_task',
        'schedule': crontab(hour='*', minute='*/20', day_of_week='*'),
        'args': ('https://www.imdb.com/chart/top/', 'csv'),
    }
}
```

### Logs do sistema

Os logs do sistema são armazenados no arquivo `crawler.log` na raiz do projeto, vale ressaltar que o sistema de logs
estará sempre imprimindo todo o processo de execução no terminal.

Abaixo simula a execução do sistema ao enviar a URL `https://www.imdb.com/chart/top/`, informar o tipo de arquivo `csv',
nesta etapa o sistema irá coletar os dados, retornar para a interface, salvar os arquivos e enviar os dados para o banco
de dados.

Devido ao uso do Render, o processo de escrita no banco de dados pode ser um pouco lento, justo
logs `Sending data to database...` e `Data sent to database.` é quando o processo está quase finalizando.

```bash
2023-10-09 13:12:19 django       | 2023-10-09 13:12:19,402 - INFO - app.helpers.setup_logger - Initializing Selenium...
2023-10-09 13:12:20 django       | 2023-10-09 13:12:20,418 - INFO - app.helpers.setup_logger - Selenium initialized 
2023-10-09 13:12:29 django       | 2023-10-09 13:12:29,076 - INFO - app.helpers.setup_logger - Getting https://www.imdb.com/chart/top/...
2023-10-09 13:12:35 django       | 2023-10-09 13:12:35,045 - INFO - app.helpers.setup_logger - Getting movie data and validation...
2023-10-09 13:12:35 django       | 2023-10-09 13:12:35,163 - INFO - app.helpers.setup_logger - Closing Selenium...
2023-10-09 13:12:35 django       | 2023-10-09 13:12:35,300 - INFO - app.helpers.setup_logger - Movie data collected.
2023-10-09 13:12:35 django       | 2023-10-09 13:12:35,301 - INFO - app.helpers.setup_logger - Saving files...
2023-10-09 13:12:35 django       | 2023-10-09 13:12:35,307 - INFO - app.helpers.setup_logger - Saving CSV file in media/imdb_data.csv...
2023-10-09 13:12:35 django       | 2023-10-09 13:12:35,354 - INFO - app.helpers.setup_logger - Files saved.
2023-10-09 13:12:40 django       | 2023-10-09 13:12:40,387 - INFO - app.helpers.setup_logger - Create connection with database.
2023-10-09 13:12:40 django       | 2023-10-09 13:12:40,388 - INFO - app.helpers.setup_logger - Sending data to database...
```

## 🌐 Interface Web

A interface web é construída com o Django e Bootstrap, e permite que os usuários coletem dados através da URL informada,
permitindo download dados em arquivos CSV ou JSON e visualização dos dados em um DataFrame do Pandas.

[![Interface Web](https://imgur.com/3nCvD5E.png)](http://localhost:8000/)

Envio de feedbacks e mensagens através do formulário de contato.

[![Formulário de Contato](https://imgur.com/ZVR5ykC.png)](http://localhost:8000/)

---

## 🚀 Tecnologias utilizadas

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/-Django-092E20?style=flat-square&logo=django&logoColor=white)
![Celery](https://img.shields.io/badge/-Celery-37814A?style=flat-square&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/-Redis-DC382D?style=flat-square&logo=redis&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![GitHub](https://img.shields.io/badge/-GitHub-181717?style=flat-square&logo=github&logoColor=white)
![PyCharm](https://img.shields.io/badge/-PyCharm-000000?style=flat-square&logo=pycharm&logoColor=white)
![Selelium](https://img.shields.io/badge/-Selelium-43B02A?style=flat-square&logo=selelium&logoColor=white)

## 🎯 Como baixar o projeto

#### 📁 Clonar o repositório

```bash
# Clone este repositório
git clone https://github.com/matheus-feu/desafio-crawler-beemon.git

# Acesse a pasta do projeto no terminal/cmd
cd desafio-crawler-beemon
```

#### 🐳 Docker

```bash
# Execute o comando para criar o container
docker-compose up -d --build
```

#### 🐍 Python

```bash
# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Execute as migrações
python manage.py migrate

# Execute o projeto
python manage.py runserver
```

Ou se preferir basta executar uma script que já está pronto para executar os comandos do django.

```bash
# Execute o script
python runserver_migrate.py
```

## ⚙️ Como executar o projeto

#### 💻 Pré-requisitos

Antes de começar, é necessário ter instalado em sua máquina as seguintes ferramentas:

- Precisa ter instalado o [Python](https://www.python.org/downloads/).
- Precisa ter instalado o [Docker](https://www.docker.com/products/docker-desktop).
- Ter instalado o  [Git](https://git-scm.com/downloads).
- Possuir um editor de código, eu utilizo o [PyCharm](https://www.jetbrains.com/pt-br/pycharm/download/#section=windows)
  ou o [VSCode](https://code.visualstudio.com/download).
- Ter um terminal para executar os comandos, como o [Git Bash](https://gitforwindows.org/) ou
  o [CMD](https://docs.microsoft.com/pt-br/windows-server/administration/windows-commands/cmd).

Com tudo em mãos e devidamente instalado, você poderá seguir o próximo tópico.


### 🎲 Executando o projeto hospedado no Render

Para melhor experiência sem a necessidade de executar o projeto localmente, você pode acessar o projeto hospedado no
Render.

- [Crawler - IMDb](https://crawler-imdb.onrender.com)

No site você pode informar a URL `https://www.imdb.com/chart/top/` e o tipo de arquivo `csv` ou `json` e clicar em enviar,
o processo é um pouco lento devido a hospedagem ser gratuita, mas logo os dados serão retornados para a interface web. 

Qualquer dúvida utilize o formulário de contato para enviar o feedback.

[![Crawler - IMDb](https://imgur.com/8Og8bqj.png)](https://crawler-imdb.onrender.com)

### 🎲 Executando o projeto no Github Code Spaces

Para melhor experiência sem a necessidade de executar o projeto localmente, você pode acessar o projeto utilizando
o [Code Spaces](https://github.com/features/codespaces) do Github.

No arquivo `settings.py` é possível configurar o `ALLOWED_HOSTS`  e `CSRF_TRUSTED_ORIGINS` para o domínio do Code
Spaces.

## 👨‍💻 Autor

- [Email](mailto:matheusfeu@gmail.com)
- [Linkedin](https://www.linkedin.com/in/matheus-feu-558558186/)
- [Github](https://github.com/matheus-feu)
- [Instagram](https://www.instagram.com/math_feu/)
