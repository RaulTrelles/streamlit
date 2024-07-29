import streamlit as st
import pandas as pd
import plotly.express as px
from matplotlib import colormaps
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
# from funciones import cargar_datos
import datetime

# calculamos en gradiente
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))

def plot_color_gradients(cmap_list):
    nrows=len(cmap_list)
    figh= 0.35 + 0.15 + (nrows + (nrows - 1 ) * 0.1 ) * 0.22

    fig, axs = plt.subplots(nrows = nrows + 1 , figsize = (6.4, figh))
    fig.subplots_adjust(top= 1 - 0.35 / figh, bottom=0.15 / figh, 
                        left=0.2, right=0.99 )
    axs[0].set_title('Colormaps', fontsize=10)

    for ax, name in zip(axs, cmap_list):
        ax.imshow(gradient, aspect='auto', cmap=mpl.colormaps[name])
        ax.text(-0.01, 0.5, name, va = 'center', ha='right', fontsize=10, 
                transform=ax.transAxes)
    for ax in axs:
        ax.set_axis_off()

    return fig
   


today = datetime.date.today()
year = today.year

st.set_page_config(
    page_title="Paguina de Tablas - tiendas Tech", 
    layout="wide", 
    page_icon="🦈",
    initial_sidebar_state="expanded"
)

# cargamos el dataframe
dfdata = pd.read_csv('data/datosTiendaTecnologiaLatam.csv')

# st.dataframe(dfdata)

# declaramos los parametros para la barra lateral

with st.sidebar:
    parAno=st.selectbox('Año', options=dfdata['anio'].unique(), index=0)
    parMes=st.selectbox('Mes', options=dfdata['mes'].unique(), index=0)
    parPais=st.multiselect('Pais',options=dfdata['pais'].unique() )

# si hay continente seleccionado aplicamos filtro.
if parAno:
    dfdata=dfdata[dfdata['anio']==parAno]
if parMes:
    dfdata=dfdata[dfdata['mes']<=parMes]
# obtenemos los datos de los meses seleccioanados
if len(parPais)>0:
    dfdata=dfdata[dfdata['pais'].isin(parPais)]

# obtener los datos del mes seleccioando
dfmesActual = dfdata[dfdata['mes']==parMes]

# obtenemos los datos del año anterior
if parMes:
    if parMes>1:
        dfmesAnterior = dfdata[dfdata['mes']==parMes-1]
    else:
        dfmesAnterior = dfdata[dfdata['mes']==parMes]

st.header('Tablas sin formato - Tienda Tech')

dfproductosventas = dfdata.groupby(['categoría']).agg({'Total': 'sum', 'orden': 'count'}).reset_index()
dfproductosventas['Porcentaje_ventas']= (dfproductosventas['Total'] / dfproductosventas['Total'].sum())

st.header('Tabla sin formato')
c1, c2, c3 = st.columns(3)
with c1:
    st.caption('st.table')
    st.table(dfproductosventas)
with c2:
    st.caption('st.dataframe')
    st.dataframe(dfproductosventas, use_container_width=True, hide_index=True)
with c3:
    st.caption('st.dataeditor')
    st.data_editor(dfproductosventas, use_container_width=True, hide_index=True, disabled=False, key='de0')

dfformato = dfproductosventas.style.format({"Total":"$ {:,.2f}", "orden":"{:.2f} órdenes", 'Porcentaje_ventas':"{:.2%}"})

st.subheader('Formato de número y Porcentale')
c1, c2, c3 = st.columns(3)
with c1:
    st.caption('st.table')
    st.table(dfformato)
with c2:
    st.caption('st.dataframe')
    st.dataframe(dfformato, use_container_width=True, hide_index=True)
with c3:
    st.caption('st.dataeditor')
    st.data_editor(dfformato, use_container_width=True, hide_index=True, disabled=True, key='de1')

parColorMap = st.selectbox('Matplotlib ColorMaps', options=list(colormaps))
colormapsCant=len(list(colormaps))
st.write(f'Cantidad de Paletas de colores : {colormapsCant}')

with st.expander('colormaps'):
    fig = plot_color_gradients(list(colormaps))
    st.write(fig)
dfformato = dfproductosventas.style.background_gradient(cmap=parColorMap, subset=['Total', 'Porcentaje_ventas']).format({"Total":"$ {:,.2f}", "orden": "{:.2f} órdenes", "Porcentaje_ventas":"{:.2%}"})

# dfformato = dfproductosventas.style.background_gradient(cmap=parColorMap).format({"Total":"$ {:,.2f}", "orden": "{:.2f} órdenes", # "Porcentaje_ventas":"{:.2%}"})


st.subheader("formato headmap combinado con formato de número")
c1, c2, c3 = st.columns(3)
with c1:
    st.caption('st.table')
    st.table(dfformato)
with c2:
    st.caption('st.dataframe')
    st.dataframe(dfformato, use_container_width=True, hide_index=True)
with c3:
    st.caption('st.dataeditor')
    st.data_editor(dfformato, use_container_width=True, hide_index=True, disabled=True, key='de2')


#  resaltar valores

parResaltar= st.radio('Resaltar Valores', options=['Máximos', 'Mínimos'], horizontal=True )

if parResaltar=='Máximos':
    dfformato=dfproductosventas.style.highlight_max(subset=['Total', 'Porcentaje_ventas'], color='green')
else:
     dfformato=dfproductosventas.style.highlight_min(subset=['Total', 'Porcentaje_ventas'], color='red')

st.subheader(f"Formato resaltar valores {parResaltar}" )
c1, c2, c3 = st.columns(3)
with c1:
    st.caption('st.table')
    st.table(dfformato)
with c2:
    st.caption('st.dataframe')
    st.dataframe(dfformato, use_container_width=True, hide_index=True)
with c3:
    st.caption('st.dataeditor')
    st.data_editor(dfformato, use_container_width=True, hide_index=True, disabled=True, key='de3')



dfformato = dfproductosventas.style.bar(color='lightgrey', height=90)
st.subheader("Formato Barras Celdas")

c1, c2, c3 = st.columns(3)
with c1:
    st.caption('st.table')
    st.table(dfformato)
with c2:
    st.caption('st.dataframe')
    st.dataframe(dfformato, use_container_width=True, hide_index=True)
with c3:
    st.caption('st.dataeditor')
    st.data_editor(dfformato, use_container_width=True, hide_index=True, disabled=True, key='de4')

    


