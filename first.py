from datetime import datetime
from dateutil.relativedelta import relativedelta
from pprint import pprint
import requests


d = datetime.now()
new = d - relativedelta(days=30)

first = new.strftime("%Y-%m-%d")
second = d.strftime("%Y-%m-%d")
t = rf"https://fioapi.fio.cz/v1/rest/periods/{API}/{first}/{second}/transactions.html"

response = requests.get(t)

pprint(response.text)
