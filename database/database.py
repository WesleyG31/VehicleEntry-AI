import pandas as pd

class VehicleData:
    def __init__(self, file_path):
        self.file_path= file_path
        self.load_data()

    def load_data(self):

        self.df= pd.read_excel(self.file_path)
        # Asegura que las placas estén en mayúscula sin espacios
        self.df['PLACA'] = self.df['PLACA'].astype(str).str.strip().str.upper()

    def get_info(self,placa):
        placa= placa.strip().upper()

        result= self.df[self.df['PLACA']==placa]

        if not result.empty:
            registro= result.iloc[0]
            return {"autorizado": True,
                  "placa": registro["PLACA"],
                  "propietario": registro["PROPIETARIO"]}
        else:
            return {"autorizado": False,
                    "placa": placa,
                  "propietario": "Desconocido"}