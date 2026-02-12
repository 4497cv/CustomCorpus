
import workspace
import os
import sys
from datetime import date
import json
import requests
import json
import requests
import pandas as pd


class Guardian():
    # base url for the search
    API_ENDPOINT = "http://content.guardianapis.com/search"

    # parameter dictionary for the search
    api_params = {}

    key_api = ""

    def __init__(self):
        # retrieve the guardian key string
        self.key_api = self.read_guardian_api_key()

        # initialize dictionary for parameter search
        self.api_params = {
            'from-date':"",
            'to-date':"",
            'order-by':"newest",
            'show-fields': "bodyText",
            'page-size': 200,
            'api-key': self.key_api
        }

        start_date = date(2026,1,1)
        end_date = date(2026,2,11)


    def fetch_articles(self, start_date, end_date, debug = 1):
        resultados = []
        # string date conversion
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        # article file name
        filename = os.path.join(workspace.get_articles_path(), start_date_str + '.json')
                
        if(not os.path.exists(filename)):
            if(debug): print("\nDownloading pages for %s\n" % filename)
            
            self.api_params['from-date'] = start_date_str
            self.api_params['to-date'] = end_date_str

            current_page = 1
            # estamos tomando páginas de 200 artículos

            while current_page <= total_pages:
                print("...page", current_page)
                self.api_params['page'] = current_page
                resp = requests.get(self.API_ENDPOINT, self.api_params)
                data = resp.json()
                resultados.extend(data['response']['results'])
                # if there is more than one page
                current_page += 1
                total_pages = data['response']['pages']

            # store the result in a json file
            with open(filename, 'w') as f:
                print("\nWriting to", filename)
                # hacemos un dump para que se imprima bonito
                f.write(json.dumps(resultados, indent=2))
                
            self.process_json_pages(filename)
        else:
            if(debug): print("\nFile %s already exists\n" %filename)

            with open(filename, 'r') as f:
                lines = f.readlines()
                
                if("[]" in lines or (len(lines) == 0)):
                    if(debug): print("\n> File %s is empty..., re-fetching files\n" %filename)
                    f.close()
                    os.remove(filename)
                    self.fetch_articles(start_date, end_date, total_pages, debug)
                else:
                    self.process_json_pages(filename)

    def process_json_pages(self, file_name, debug = 1):
        titulos = []
        articulos = []
        csv_struct = []

        with open(file_name, "r") as f:
            contenido = json.load(f)
            i = 0
            for page in contenido:
                titulo = page["webTitle"]
                titulos.append(page["webTitle"])
                
                articulo = page["fields"]["bodyText"]
                articulos.append(articulo)
                
                csv_struct.append([i, titulo, articulo])
                columnas = ["id", "Web Title", "Body Text"]
                df = pd.DataFrame(csv_struct, columns=columnas)

                page_csv_path = os.path.join(workspace.get_texts_path(), ".csv")
                df.to_csv(page_csv_path, index=False, encoding="utf-8-sig")
                
                print("%i. %s" % (i, titulo))
                i = i + 1



    def read_guardian_api_key(self, debug = 0):
        api_key_path = workspace.get_guardian_key_path()

        with open(api_key_path,'r') as f:
            MY_API_KEY = f.read().strip()

            if(len(MY_API_KEY) == 0):
                print("ERROR: API key is empty - %s" % MY_API_KEY)
                sys.exit()

        if(debug): print("API KEY: %s" % MY_API_KEY)
        return MY_API_KEY
