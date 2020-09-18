import json
import csv
import pandas as pd


def transformar_archivo(ruta):
    with open(ruta) as contenido:
        provincias = json.load(contenido)
    with open("datos/pop_provs.csv", "w") as archivo:
        csv_file = csv.writer(archivo)
        csv_file.writerow(["code", "name", "pop_dens",
                           "total_pop", "country_percentage"])
        for provincia in provincias:
            csv_file.writerow([provincia['code'], provincia['name'], provincia['pop_dens'],
                               provincia['total_pop'], provincia['country_percentage']])


if __name__ == "__main__":
    ruta_json = 'datos/pop_provs.json'
    transformar_archivo(ruta_json)
