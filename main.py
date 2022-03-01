import datetime
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

excel_data_df = pandas.read_excel(
    'wine3.xlsx',
    na_values=['N/A', 'NA'],
    keep_default_na=False
)
wines = excel_data_df.to_dict(orient='records')

drinks = defaultdict(list)

for wine in wines:
    drinks[wine['Категория']].append(wine)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

service_years = datetime.datetime.now().year - 1920

template = env.get_template('template.html')

rendered_page = template.render(drinks=drinks)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
