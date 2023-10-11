import os

import psycopg2
from dotenv import load_dotenv

from app.helpers.setup_logger import logger
from app.models import MoviesModels

load_dotenv()


class PostgreSQLPipeline(object):

    def create_connection(self):
        """
        Criar conexão com o banco de dados PostgreSQL.
        """
        db_settings = {
            'dbname': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'),
        }
        self.conn = psycopg2.connect(**db_settings)

    def close_connection(self):
        """
        Fecha a conexão com o banco de dados.
        """
        self.conn.close()

    def process_item(self, item):
        """
        Durante a extração de dados, o item é inserido dentro da tabela.
        :param item: Item a ser inserido.
        :return:
        """
        self.insert_data(item)
        return item

    def insert_data(self, data_list):
        """
        Insere dados em uma tabela no banco de dados.
        :param data_list: Lista de dicionários contendo os dados a serem inseridos.
        """
        try:
            created_count = 0
            updated_count = 0

            for data in data_list:
                movie, created = MoviesModels.objects.update_or_create(
                    title=data['title'],
                    defaults={
                        'year': data['year'],
                        'duration': data['duration'],
                        'rating': data['rating'],
                        'votes': data['votes'],
                        'img_url': data['img_url']
                    }
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1

            logger.info(
                f"Inserção de {created_count} registros e atualização de {updated_count} registros concluída com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao inserir/atualizar dados: {e}")
