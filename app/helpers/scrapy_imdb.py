import os
import time

import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver

from app.helpers.setup_logger import logger
from app.pipelines import PostgreSQLPipeline

load_dotenv()


class IMDbScraper:
    def __init__(self, url):
        self.url = url
        self.data = []
        self.driver = None
        self.soup = None

    def initialize_selenium(self):
        """
        Inicializa o Selenium com as configurações necessárias.
        :return: Instância do Selenium.
        """
        logger.info('Initializing Selenium...')
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument('--headless')
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(
            options=options
        )
        self.driver.implicitly_wait(10)
        logger.info(f'Selenium initialized {self.driver.title}')

        return self.driver

    @classmethod
    def handle_movie(cls, text):
        """
        Trata o nome do filme, juntando todas as informações que estão após o '.'
        """
        return ''.join(text.split('.')[1:]).strip().replace("'", "")

    def find_movie_elements(self):
        return self.soup.find_all('li', class_='ipc-metadata-list-summary-item sc-59b6048d-0 jemTre cli-parent')

    def get_movie_data(self, movie_element):
        title_element = movie_element.find('h3', class_='ipc-title__text')
        img_element = movie_element.find('img', class_='ipc-image')
        metadata_element = movie_element.find('div', class_='sc-c7e5f54-7 brlapf cli-title-metadata')
        ratings_element = movie_element.find('div',
                                             class_='sc-e3e7b191-0 iKUUVe sc-c7e5f54-2 hCiLPi cli-ratings-container')

        if metadata_element and ratings_element:
            year_element = metadata_element.find_all('span', class_='sc-c7e5f54-8 hgjcbi cli-title-metadata-item')[0]
            duration_element = metadata_element.find_all('span', class_='sc-c7e5f54-8 hgjcbi cli-title-metadata-item')[1]
            rating_element = ratings_element.find('span',
                                                  class_='ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating')
            votes_element = ratings_element.find('span', class_='ipc-rating-star--voteCount')

            title = self.handle_movie(title_element.text.strip())
            year = year_element.text.strip()
            duration = duration_element.text.strip()
            img_url = img_element['src'].split(',')[0]
            rating = rating_element.text.strip()[0:3]
            votes = votes_element.text.strip().replace('(', '').replace(')', '')

            return {
                'title': title,
                'year': int(year),
                'duration': duration,
                'rating': rating,
                'votes': votes,
                'img_url': img_url
            }

        return None

    def save_type_info(self, file_type: str, data=None):
        """
        Salva as informações em um arquivo, conforme tipo definido e retorna o conteúdo do arquivo.
        :param data: Dados a serem salvos.
        :param file_type: Tipo do arquivo a ser salvo.
        :return:
        """
        logger.info('Saving files...')
        df = pd.DataFrame(data=self.data)

        path = os.path.join('media', f'imdb_data.{file_type}')

        if file_type == 'csv':
            logger.info(f'Saving CSV file in {path}...')

            df.to_csv(path, index=False)
            df['img_html'] = df['img_url'].apply(lambda x: f'<img src="{x}" width="140px">')
            df = df.reset_index(drop=True).reset_index()
            df['index'] = df['index'] + 1

            df = df.rename(
                columns={
                    'index': 'ID',
                    'title': 'Título',
                    'year': 'Ano',
                    'duration': 'Duração',
                    'rating': 'Avaliação',
                    'votes': 'Votos',
                    'img_url': 'URL Imagem',
                    'img_html': 'Imagem'
                }
            )
            data = df.to_html(
                classes='table table-bordered table-striped',
                escape=False,
                index=False,
                justify='center'
            )

        elif file_type == 'json':
            logger.info(f'Saving JSON file in {path}...')

            df.to_json(path, orient="records", indent=4)
            with open(path, 'r', encoding='utf-8') as json_file:
                data = json_file.read()

        logger.info('Files saved.')

        return data

    def save_in_db(self):
        """
        Enviar os dados para a classe de pipeline para salvar no banco de dados.
        """
        pipeline = PostgreSQLPipeline()
        pipeline.create_connection()

        logger.info('Create connection with database.')
        try:
            logger.info('Sending data to database...')
            pipeline.process_item(self.data)
            logger.info('Data sent to database.')
        except Exception as e:
            logger.error(f'Error while sending data to database: {str(e)}')
        finally:
            pipeline.close_connection()

    def scrape(self):
        self.driver = self.initialize_selenium()
        self.driver.get(self.url)
        logger.info(f'Getting {self.url}...')
        time.sleep(10)

        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        self.driver.save_screenshot('screenshot.png')

        try:
            movie_elements = self.find_movie_elements()

            logger.info('Getting movie data and validation...')
            for movie_element in movie_elements:
                movie_data = self.get_movie_data(movie_element)
                if movie_data:
                    self.data.append(movie_data)

        except Exception as e:
            logger.error(e)
            logger.error('Error while getting movie data.')

        finally:
            logger.info('Closing Selenium...')
            self.driver.quit()

        logger.info('Movie data collected.')

        return self.data
