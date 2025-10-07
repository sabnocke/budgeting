import os
from dotenv import load_dotenv
from datetime import datetime
from pprint import pprint
import requests


def get_all():
    start = datetime.now().strftime('%Y-%m-%d')
    api = os.environ.get("API_KEY")
    link = rf"https://fioapi.fio.cz/v1/rest/periods/{api}/{start}/2010-01-01/transactions.json"

    r = requests.get(link)

    pprint(r)


if __name__ == "__main__":
    load_dotenv()
    get_all()