import os

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from app.forms import URLScrappyForm, FeedbackForm
from app.helpers.scrapy_imdb import IMDbScraper
from app.helpers.validate_url import is_valid_url
from app.tasks import send_feedback_email_task


def feedback(request):
    """
    Visualização que renderiza o formulário de feedback e envia um email com os dados inseridos no formulário para
    a conta de email do desenvolvedor, utilizando o Celery.
    """
    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            send_feedback_email_task.delay(name, email, message)
            return redirect('success')
    else:
        form = FeedbackForm()

    return render(request, 'feedback/feedback.html', {'form': form})


def success(request):
    """Visualização que renderiza a página de sucesso após o envio do feedback."""
    return render(request, 'feedback/success.html')


def home(request):
    """Pagina inicial da aplicação, aonde o usuário pode inserir a URL do IMDB.
    A URL é validada e se for válida, o scraper é executado e os dados são retornados."""

    form = URLScrappyForm()
    data_html = None
    data_json = None

    if request.method == 'POST':
        form = URLScrappyForm(request.POST)
        arquivo = request.POST.get('arquivo')

        if form.is_valid():
            url = form.cleaned_data['url']

            if not is_valid_url(url):
                messages.error(request, 'URL inválida ou inacessível.')
            elif 'imdb.com' not in url:
                messages.error(request, 'URL não é do IMDB.')
            else:
                try:
                    imdb_scraper = IMDbScraper(url)
                    if arquivo == 'csv':
                        imdb_scraper.scrape()
                        data_html = imdb_scraper.save_type_info(arquivo)
                        imdb_scraper.save_in_db()
                    elif arquivo == 'json':
                        imdb_scraper.scrape()
                        data_json = imdb_scraper.save_type_info(arquivo)
                        imdb_scraper.save_in_db()
                    else:
                        messages.error(request, 'Tipo de arquivo inválido.')

                except Exception as e:
                    messages.error(request, f'Ocorreu um erro inesperado: {str(e)}')

    return render(request, 'home.html',
                  {'form': form, 'data_html': data_html, 'data_json': data_json, 'error_message': messages.error})


@csrf_exempt
def download_csv(request):
    """Visualização que retorna o arquivo CSV como um download."""

    csv_path = os.path.join('media', 'imdb_data.csv')

    if os.path.exists(csv_path):
        with open(csv_path, 'rb') as csv_file:
            response = HttpResponse(csv_file.read(), content_type='text/csv')

        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(csv_path)}"'
        return response
    else:
        messages.error(request, 'Arquivo CSV não encontrado.')
        return redirect('home')


@csrf_exempt
def download_json(request):
    """Visualização que retorna o arquivo JSON como um download."""

    json_path = os.path.join('media', 'imdb_data.json')

    if json_path:
        with open(json_path, 'rb') as json_file:
            response = HttpResponse(json_file.read(), content_type='text/json')

        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(json_path)}"'
        return response
    else:
        messages.error(request, 'Arquivo JSON não encontrado.')
        return redirect('home')
