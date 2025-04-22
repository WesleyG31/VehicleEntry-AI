from datetime import datetime, timedelta

class RegistroTemporal:
    def __init__(self, intervalo_segundos=30):
        self.historial = {}
        self.intervalo = timedelta(seconds=intervalo_segundos)

    def puede_registrar(self, placa):
        ahora = datetime.now()

        if placa not in self.historial:
            self.historial[placa] = ahora
            return True

        ultima_vez = self.historial[placa]
        if ahora - ultima_vez > self.intervalo:
            self.historial[placa] = ahora
            return True

        return False
