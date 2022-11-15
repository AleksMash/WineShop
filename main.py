from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime as dt
import pandas as pnd
import configargparse
from jinja2 import Environment, FileSystemLoader, select_autoescape


def main():
    parser = configargparse.ArgParser(default_config_files=['settings.conf'])
    parser.add('-c', '--config_file', required=False, is_config_file=True, help='config file path')
    parser.add('-d','--data_file', required=True, help='data file path')
    parser.add('--on_sale_phrase', required=False, default='Выгодное предложение', help='On sale phrase')
    options=parser.parse_args()
    env=Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')
    delta_years = dt.datetime.now().year-1920
    wine_data = pnd.read_excel(options.data_file, sheet_name='Лист1',
                          keep_default_na=False)
    categories = sorted(set(wine_data['Категория'].tolist()))
    wine_data = wine_data.to_dict(orient='records')
    wines_by_categories = {}
    for cat in categories:
        drinks = list(filter(lambda item: item['Категория'] == cat, wine_data))
        wines_by_categories[cat] = drinks
    rendered_page = template.render(age=delta_years, drinks=wines_by_categories, on_sale=options.on_sale_phrase)
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
