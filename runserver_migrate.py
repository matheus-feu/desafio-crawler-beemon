import os
import sys

from django.core.management import execute_from_command_line

if __name__ == "__main__":
    """
    Função para ser utilizada na linha de comando, para executar o makemigrations e o migrate.
    """

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

    execute_from_command_line([sys.argv[0], "makemigrations"])
    execute_from_command_line([sys.argv[0], "migrate"])
    execute_from_command_line([sys.argv[0], "runserver"])
