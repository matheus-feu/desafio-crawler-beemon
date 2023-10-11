import os
import time

from celery import shared_task
from django.core.mail import send_mail
from dotenv import load_dotenv
from urllib3.exceptions import MaxRetryError

from app.helpers.scrapy_imdb import IMDbScraper
from app.helpers.setup_logger import logger

load_dotenv()


@shared_task(name="scrapy_task")
def scrapy_task(url, file_type):
    """
    Tarefa que é agendada para ser executada periodicamente, a cada 15 minutos.
    """
    try:
        logger.info('Scrapy task started')
        imdb_scraper = IMDbScraper(url)
        imdb_scraper.scrape()
        imdb_scraper.save_type_info(file_type)
        imdb_scraper.save_in_db()
        logger.info('Scrapy task finished successfully')
    except MaxRetryError as e:
        logger.error(f'Máximo conexão: {e}')
    except Exception as e:
        logger.error(f'Error: {e}')


@shared_task(name="send_feedback_email_task")
def send_feedback_email_task(name, email, message):
    """
    Tarefa que é executada quando um usuário envia um feedback e então envia um email para o destinatário.
    """
    time.sleep(10)

    subject = "Your Feedback"
    from_email = os.getenv('EMAIL_HOST_USER')
    recipient_list = [email]

    email_message = f"Hi {name}! Obrigado pelo seu feedback. Iremos revisá-lo em breve,.\n\nMessage: {message}"
    send_mail(subject, email_message, from_email, recipient_list, fail_silently=False)
