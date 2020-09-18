import csv
import pandas as pd

if __name__ == "__main__":
    ruta_provincias = 'datos/pop_provs.csv'
    ruta_covid = 'datos/transformacion.csv'

    datos_provincia = pd.read_csv(ruta_provincias)
    df_p = pd.DataFrame(datos_provincia)

    datos_covid = pd.read_csv(ruta_covid)
    df_c = pd.DataFrame(datos_covid)

    df_concatenado = pd.concat([df_p, df_c], ignore_index=True)

    df_concatenado.to_csv('datos/concatenados.csv', index=False)
