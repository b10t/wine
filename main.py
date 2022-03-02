import datetime
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from environs import Env
from jinja2 import Environment, FileSystemLoader, select_autoescape

WINERY_OPENING_YEAR = 1920

if __name__ == '__main__':
    env = Env()
    env.read_env()
    data_file = env.str('DATA_FILE', 'sample_data.xlsx')

    wines = pandas.read_excel(data_file,
                              na_values=['N/A', 'NA'],
                              keep_default_na=False) \
        .to_dict(orient='records')

    grouped_drinks = defaultdict(list)

    for wine in wines:
        grouped_drinks[wine['Категория']].append(wine)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    winery_age = datetime.datetime.now().year - WINERY_OPENING_YEAR

    template = env.get_template('template.html')

    rendered_page = template.render(
        grouped_drinks=grouped_drinks,
        winery_age=winery_age
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
