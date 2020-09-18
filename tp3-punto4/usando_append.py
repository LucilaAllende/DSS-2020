import csv
import pandas as pd

if __name__ == "__main__":
    ruta_provincias = 'datos/pop_provs.csv'
    ruta_covid = 'datos/transformacion.csv'

    datos_provincia = pd.read_csv(ruta_provincias)
    df_p = pd.DataFrame(datos_provincia)

    datos_covid = pd.read_csv(ruta_covid)
    df_c = pd.DataFrame(datos_covid)

    merged_append = df_p.append(df_c, ignore_index=True)

    merged_append.to_csv('datos/append.csv', index=False)
