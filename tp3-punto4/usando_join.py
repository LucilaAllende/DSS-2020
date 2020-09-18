import csv
import pandas as pd

if __name__ == "__main__":
    ruta_provincias = 'datos/pop_provs.csv'
    ruta_covid = 'datos/transformacion.csv'

    datos_provincia = pd.read_csv(ruta_provincias)
    df_p = pd.DataFrame(datos_provincia)

    datos_covid = pd.read_csv(ruta_covid)
    df_c = pd.DataFrame(datos_covid)

    merged_inner = pd.merge(left=df_p, right=df_c,
                            left_on='name', right_on='provincia')

    merged_inner.to_csv('datos/innerjoins.csv', index=False)
