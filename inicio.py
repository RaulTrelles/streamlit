import streamlit as st
import pandas as pd
import plotly.express as px
# from funciones import cargar_datos
import datetime


today = datetime.date.today()
year = today.year

st.set_page_config(
    page_title="Paguina de ventas tiendas  -  Tech", 
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

st.header('Tablero de control de ventas - Tienda Tech')

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    productosAct= dfmesActual['Cantidad'].sum()
    productosAnt= dfmesAnterior['Cantidad'].sum()
    variacion = productosAnt - productosAct
    st.metric(f"Productos vendidos", f'{productosAct:,.0f} unidades', f'{variacion}')

with c2:
    ordenesAct= dfmesActual['orden'].count()
    ordenesAnt= dfmesAnterior['orden'].count()
    variacion = ordenesAct - ordenesAnt
    st.metric(f"Ventas Realizadas", f'{ordenesAct:,.0f}', f'{variacion:.1f}')
with c3:
    ventasAct= dfmesActual['Total'].sum()
    ventasAnt= dfmesAnterior['Total'].sum()
    variacion = ventasAct - ventasAnt
    st.metric(f"Ventas Realizadas", f'US$ {ventasAct:,.0f}', f'{variacion}')
with c4:
    utilidadAct= dfmesActual['utilidad'].sum()
    utilidadAnt= dfmesAnterior['utilidad'].sum()
    variacion = utilidadAct - utilidadAnt
    st.metric(f"Utilidades", f'US$ {utilidadAct:,.0f}', f'{variacion:,.0f}')
with c5:
    utilpercentAct= (utilidadAct/ventasAct)*100
    utilidadAnt= (utilidadAnt/ventasAnt)*100
    variacion = utilidadAnt - utilpercentAct
    st.metric(f"Utilidad porcentual", f'{utilpercentAct:,.2f} %', f'{variacion:,.0f} %')


# declaramos 2 columnas en una porcion de 60% y 40%
c1, c2 = st.columns([60, 40])
with c1:
    dfventasMes = dfdata.groupby('mes').agg({'Total':'sum'}).reset_index()
    fig = px.line(dfventasMes, x='mes', y='Total', title='Ventas por Mes')
    st.plotly_chart(fig, use_container_width=True)
with c2:
    dfventasPais = dfmesActual.groupby('pais').agg({'Total': 'sum'}).reset_index().sort_values(by='Total', ascending=False)
    fig = px.bar(dfventasPais, x='pais', y='Total', title=f'ventas por categoria Mes: {parMes}', color='pais', text_auto=',.0f')
    st.plotly_chart(fig, use_container_width=True)

# declaramos 2 columnas en una porcion de 60% y 40%
c1, c2 = st.columns([60, 40])
with c1:
    dfventasCategoria = dfdata.groupby(['mes', 'categoría']).agg({'Total':'sum'}).reset_index()
    fig = px.line(dfventasCategoria, x='mes', y='Total', title='Ventas por Mes y categoría', color='categoría')
    st.plotly_chart(fig, use_container_width=True)
with c2:
    dfventasCategoria = dfmesActual.groupby('categoría').agg({'Total': 'sum'}).reset_index().sort_values(by='Total', ascending=False)
    fig = px.bar(dfventasCategoria, x='categoría', y='Total', title=f'ventas por categoria Mes: {parMes}', color='categoría', text_auto=',.0f')
    fig.update_layout(showlegend=False) #determinacion si se muestra leyenda o no
    st.plotly_chart(fig, use_container_width=True)


dfventasPais = dfmesActual.groupby(['categoría', 'pais']).agg(cantidad=('orden', 'count')).reset_index()
fig = px.pie(dfventasPais, color='categoría', values='cantidad', facet_col='pais', facet_col_wrap=4, height=800, title='ventas por categoria')
st.plotly_chart(fig, use_container_width=True)

c1, c2 = st.columns(2)
dfproductosventas = dfmesActual.groupby(['categoría', 'producto']).agg({'Total': 'sum', 'orden': 'count'}).reset_index()
with c1:
    st.subheader('Top 10 productos más vendidos')
    st.table(dfproductosventas.sort_values(by='orden', ascending=False).head(10)[['categoría', 'producto', 'Total', 'orden']])
with c2:
    st.subheader('Top 10 productos menos vendidos')
    st.table(dfproductosventas.sort_values(by='orden').head(10)[['categoría', 'producto', 'Total', 'orden']])





