''' Create a simple stocks correlation dashboard.

Choose stocks to compare in the drop down widgets, and make selections
on the plots to update the summary and histograms accordingly.

.. note::
    Running this example requires downloading sample data. See
    the included `README`_ for more information.

Use the ``bokeh serve`` command to run the example by executing:

    bokeh serve stocks

at your command prompt. Then navigate to the URL

    http://localhost:5006/stocks

.. _README: https://github.com/bokeh/bokeh/blob/master/examples/app/stocks/README.md

'''
from datetime import datetime
from functools import lru_cache
from os.path import dirname, join

import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, PreText, Select
from bokeh.plotting import figure

DATA_DIR = join(dirname(__file__))

# Esta lista representa los codigos de provincia que tenemos en el csv
DEFAULT_PROVS = ['AR-B', 'AR-V', 'AR-C', 'AR-A','AR-X','AR-R', 'AR-U', 'AR-Z', 'AR-K', 'AR-S', 'AR-G', 'AR-M', 'AR-H', 'AR-Q', 'AR-F', 'AR-E', 'AR-T', 'AR-V']

def nix(val, lst):
    return [x for x in lst if x != val]

# este metodo lee los datos del .csv y devuelve un dataframe
def load_prov(prov_code):
    # path del archivo
    fname = join(DATA_DIR, 'innerjoins.csv')

    # leemos el .csv
    mydateparser = lambda x: datetime.strptime(x, "%d/%m/%Y")
    df = pd.read_csv(fname, parse_dates=['fecha'], date_parser=mydateparser)

    # nos quedamos con la provincia indicada por parámetros
    df = df[df['code'] == prov_code]

    # renombramos 'fecha' a 'date' para que lo tome bien el gráfico
    df.rename(columns={'fecha':'date'}, inplace=True)

    # la fecha tiene que ser el índice
    df = df.set_index('date')

    # por algún motivo había fechas duplicadas así que las quitamos
    df = df[~df.index.duplicated(keep='first')]

    # devolvemos el DF con el formato esperado
    return pd.DataFrame({prov_code: df.nue_casosconf, prov_code + '_returns': df.nue_casosconf.diff()})


def get_data(p1, p2):
    df1 = load_prov(p1)
    df2 = load_prov(p2)
    df1 = fill_missing_dates(df1)
    df2 = fill_missing_dates(df2)
    data = pd.concat([df1, df2], axis=1)
    data = data.dropna()
    data['p1'] = data[p1]
    data['p2'] = data[p2]
    return data


def fill_missing_dates(df):
    """ Completa con datos para las fechas que faltan """

    # usamos datos de fila 0 para completar fechas previas a la fila 0
    filler = df.iloc[0]
    # iteramos el rango completo de fechas buscando las que faltan en el DF y la insertamos con datos
    for date in pd.date_range('2020-03-05', '2020-07-10', freq='d'):
        if not date in df.index:
            df.loc[date] = filler
        else:
            filler = df.loc[date]
    return df.sort_index()

# set up widgets

stats = PreText(text='', width=500)
provincia1 = Select(value='AR-V', options=nix('AR-V', DEFAULT_PROVS))
provincia2 = Select(value='AR-B', options=nix('AR-B', DEFAULT_PROVS))

# set up plots

source = ColumnDataSource(data=dict(date=[], p1=[], p2=[]))
source_static = ColumnDataSource(data=dict(date=[], p1=[], p2=[]))
tools = 'pan,wheel_zoom,xbox_select,reset'

ts1 = figure(plot_width=900, plot_height=200, tools=tools, x_axis_type='datetime', active_drag="xbox_select")
ts1.line('date', 'p1', source=source_static)
ts1.circle('date', 'p1', size=1, source=source, color=None, selection_color="orange")

ts2 = figure(plot_width=900, plot_height=200, tools=tools, x_axis_type='datetime', active_drag="xbox_select")
ts2.x_range = ts1.x_range
ts2.line('date', 'p2', source=source_static)
ts2.circle('date', 'p2', size=1, source=source, color=None, selection_color="orange")


# set up callbacks

def prov1_change(attrname, old, new):
    provincia2.options = nix(new, DEFAULT_PROVS)
    update()


def prov2_change(attrname, old, new):
    provincia1.options = nix(new, DEFAULT_PROVS)
    update()


def update(selected=None):
    p1, p2 = provincia1.value, provincia2.value

    df = get_data(p1, p2)
    data = df[['p1', 'p2']]
    source.data = data
    source_static.data = data

    update_stats(df, p1, p2)

    ts1.title.text, ts2.title.text = p1, p2


def update_stats(data, p1, p2):
    stats.text = str(data[[p1, p2]].describe())


provincia1.on_change('value', prov1_change)
provincia2.on_change('value', prov2_change)


def selection_change(attrname, old, new):
    p1, p2 = provincia1.value, provincia2.value
    data = get_data(p1, p2)
    selected = source.selected.indices
    if selected:
        data = data.iloc[selected, :]
    update_stats(data, p1, p2)


source.selected.on_change('indices', selection_change)

# set up layout
widgets = column(provincia1, provincia2, stats)
main_row = row( widgets)

## Las siguientes lineas son para cambiar los ejes x e y por otras variables (no funciona)
fname = join(DATA_DIR, 'innerjoins.csv')
dataframe = pd.DataFrame()
mydateparser = lambda x: datetime.strptime(x, "%d/%m/%Y")
dataframe = pd.read_csv(fname, parse_dates=['fecha'], date_parser=mydateparser)
columns = sorted(dataframe.columns)
x = Select(title='X-Axis', value='date', options=columns)
#x.on_change('value', update)

y = Select(title='Y-Axis', value='nue_casosconf', options=columns)
#y.on_change('value', update)

series = column(ts1, ts2)
#series = column(x, y,ts1, ts2)
layout = column(main_row, series)


# initialize
update()

curdoc().add_root(layout)
curdoc().title = "Covid"
