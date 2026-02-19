
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

    start_date = date
    end_date = date

    def __init__(self, start_date:date, end_date:date):
        # retrieve the guardian key string
        self.key_api = self.read_guardian_api_key()
        self.start_date = start_date
        self.end_date = end_date
        # initialize dictionary for parameter search
        self.api_params = {
            'from-date':"",
            'to-date':"",
            'order-by':"newest",
            'show-fields': "bodyText",
            'page-size': 200,
            'api-key': self.key_api
        }


    def fetch_articles(self, debug = 1):
        resultados = []
        # string date conversion
        start_date_str = self.start_date.strftime("%Y-%m-%d")
        end_date_str = self.end_date.strftime("%Y-%m-%d")
        # article file name
        filename = os.path.join(workspace.get_articles_path(), start_date_str + '.json')
        total_pages = 200
                
        if(not os.path.exists(filename)):
            if(debug): print("\nDownloading pages for %s\n" % filename)
            print(start_date_str)
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
                print(current_page)

            # store the result in a json file
            with open(filename, 'w') as f:
                print("\nWriting to", filename)
                # hacemos un dump para que se imprima bonito
                f.write(json.dumps(resultados, indent=2))
                
            self.process_json_pages(filename, start_date_str)
        else:
            if(debug): print("\nFile %s already exists\n" %filename)

            with open(filename, 'r') as f:
                lines = f.readlines()
                
                if("[]" in lines or (len(lines) == 0)):
                    if(debug): print("\n> File %s is empty..., re-fetching files\n" %filename)
                    f.close()
                    os.remove(filename)
                    self.fetch_articles(self.start_date, self.end_date, total_pages, debug)
                else:
                    print(filename)
                    self.process_json_pages(filename, start_date_str)
                    self.process_articles_to_text_csv()
                    

    def process_json_pages(self, file_name, start_date_str, debug = 1):
        titulos = []
        articulos = []
        csv_struct = []
        section_id = []

        with open(file_name, "r") as f:
            contenido = json.load(f)
            i = 0
            for page in contenido:
                titulo = page["webTitle"]
                titulos.append(page["webTitle"])
                
                articulo = page["fields"]["bodyText"]
                articulos.append(articulo)

                section = page["sectionId"]
                section_id.append(section)
                
                csv_struct.append([i, titulo, articulo, section])
                columnas = ["id", "Web Title", "Body Text", "SecId"]
                df = pd.DataFrame(csv_struct, columns=columnas)
                csv_file_name = "articulos-" + start_date_str
                page_csv_path = os.path.join(workspace.get_texts_path(), (csv_file_name+ ".csv"))
                df.to_csv(page_csv_path, index=False, encoding="utf-8-sig")
                
                if(debug): print("%i. %s" % (i, titulo))
                i = i + 1
    
    def process_articles_to_text_csv(self, debug=1):

        base_path = workspace.get_texts_path()

        files = os.listdir(base_path)

        for f in files:
            # Only process CSV files
            if f.endswith(".csv"):
                csv_full_path = os.path.join(base_path, f)

                df = pd.read_csv(csv_full_path)

                for index, row in df.iterrows():
                    article_id = row["id"]
                    body_text = row["Body Text"]
                    section = row["SecId"]

                    if("nan" in str(body_text)):
                        output_path = os.path.join(base_path, section)
                        
                        if(not os.path.exists(output_path)):
                            os.makedirs(output_path, exist_ok=True)
                            
                        filename = f"article{article_id}.txt"
                        filepath = os.path.join(output_path, filename)

                        with open(filepath, "w", encoding="utf-8") as file:
                            file.write(str(body_text))

                        if debug:
                            print(f"Saved {filename}")

        if debug:
            print("All articles saved successfully.")



    def read_guardian_api_key(self, debug = 0):
        api_key_path = workspace.get_guardian_key_path()

        with open(api_key_path,'r') as f:
            MY_API_KEY = f.read().strip()

            if(len(MY_API_KEY) == 0):
                if(debug): print("ERROR: API key is empty - %s" % MY_API_KEY)
                sys.exit()

        if(debug): print("API KEY: %s" % MY_API_KEY)
        return MY_API_KEY
