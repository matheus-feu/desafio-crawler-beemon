import os

import pandas as pd
from django.conf import settings


def convert_to_csv(data, csv_filename='imdb_data.csv'):
    """Converte um DataFrame do Pandas em um arquivo CSV e retorna o caminho do arquivo."""

    media_path = settings.MEDIA_ROOT
    df = pd.DataFrame(data)
    csv_path = os.path.join(media_path, csv_filename)
    df.to_csv(csv_path, index=False)

    return csv_path


def convert_to_json(data, json_filename='imdb_data.json'):
    """Converte um DataFrame do Pandas em um arquivo JSON e retorna o caminho do arquivo."""

    media_path = settings.MEDIA_ROOT
    df = pd.DataFrame(data)
    json_path = os.path.join(media_path, json_filename)
    df.to_json(json_path, orient='records', indent=4)

    return json_path
