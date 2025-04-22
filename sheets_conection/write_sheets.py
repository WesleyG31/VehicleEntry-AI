#import os
#from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
# Calcula la ruta absoluta al .env que está en la raíz del proyecto
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#dotenv_path = os.path.join(BASE_DIR, ".env")
#load_dotenv(dotenv_path)


# Configurar acceso a Google Sheets
class GoogleSheet_write:
    def __init__(self, credentials_file, spreadsheet_name, worksheet_name):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        # Leer credenciales desde el archivo JSON
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
        client = gspread.authorize(creds)

        # Abrir la hoja de cálculo (CAMBIA EL NOMBRE A TU HOJA)
        self.spreadsheet = client.open(spreadsheet_name)
        self.worksheet = self.spreadsheet.worksheet(worksheet_name)

    def write_events(self, placa, propietario, autorizado,id_carro):
        # Convertir los datos en un DataFrame de Pandas
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')     
        self.worksheet.append_row([now, placa, propietario, "SI" if autorizado else "NO", id_carro])

