import json
import pandas as pd


def transformar_datos(dataframe):
    dataframe.drop(['osm_admin_level_2', 'nue_fallecidos_diff', 'tot_recuperados', 'tot_terapia',
                    'test_RT-PCR_negativos', 'test_RT-PCR_total', 'informe_link', 'observacion', 'covid19argentina_admin_level_4'], axis='columns', inplace=True)
    # dataframe[['dia_cuarentena_dnu260']].astype(int)
    dataframe.rename(columns={'dia_cuarentena_dnu260': 'dia_cuarentena',
                              'osm_admin_level_4': 'provincia',
                              'osm_admin_level_8': 'ciudad',
                              'nue_casosconf_diff': 'nue_casosconf'}, inplace=True)

    # los datos iniciales fueron antes de comenzar la cuarentena y no tienen un dia asociado
    dataframe['dia_cuarentena'] = dataframe['dia_cuarentena'].fillna(0)

    # Son pocas ciuaddes las que estan identificadas, pero es un dato importante
    dataframe['ciudad'] = dataframe['ciudad'].fillna('C_Indeterminado')

    # despues de cierto tiempo, el virus se extendio y se presupone que el contagio siempre es por transmision comunitaria
    dataframe['transmision_tipo'] = dataframe['transmision_tipo'].fillna(
        'transmision comunitaria')

    # despues de cierto tiempo estos datos se obtuvieron de informes pronviciales
    dataframe['informe_tipo'] = dataframe['informe_tipo'].fillna(
        'informe provincial')

    # es necesario pasar esta columna a enteros, por algun motivo la transformacion anterior lo deja como flotante y ese tipo de dato no es representatitvo
    dataframe['dia_cuarentena'] = dataframe['dia_cuarentena'].astype('int64')

    print(dataframe.head(5))
    dataframe.to_csv('datos/transformacion.csv', index=False)


def cargar_datos_json(ruta):
    with open(ruta) as contenido:
        provincias = json.load(contenido)
        for provincia in provincias:
            print(provincia.get('name'))


def cargar_datos_csv(ruta):
    datos = pd.read_csv(ruta)
    df = pd.DataFrame(datos)
    primeros = df.head(5)
    print(primeros)
    transformar_datos(df)


if __name__ == "__main__":
    ruta_json = 'datos/pop_provs.json'
    ruta_csv = 'datos/export.csv'
    cargar_datos_json(ruta_json)
    cargar_datos_csv(ruta_csv)
