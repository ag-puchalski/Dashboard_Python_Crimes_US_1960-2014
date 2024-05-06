
import streamlit as st
from graficos import *

st.set_page_config(layout='wide')
st.title("Dashboard de Crimes nos Estados Unidos 1960 - 2014  :gun: :mag:")


st.sidebar.title('Filtro 10 anos mais Criminosos :bar_chart: ')
filtro_top10_total = st.sidebar.checkbox('Mostrar apenas os 10 maiores valores de Total')

if filtro_top10_total:
    df = df.nlargest(10, 'Total')
    
st.sidebar.title('Filtro de Violência :knife:')
filtro_violencia = st.sidebar.checkbox('Violência acima de 1.000.000')

if filtro_violencia:
    df = df[df['Violento'] > 1000000]



aba1, aba2, aba3, aba4, aba5, aba6, aba7 = st.tabs(['Dataset', 'Crimes por Ano','Porcentagem de Crimes por Década', 'Crimes Violentos por Década', 'Propriedade X Violência', 'População X Crimes','Década mais perigosa'])


colunas_para_exibir = ['Ano', 'Populacao', 'Total', 'Violento', 'Propriedade', 'Homicidio', 'Estupro', 'Roubo_Residencia', 'Assalto_Agravante', 
                       'Furto_Residencia', 'Furto_Roubo_Geral', 'Roubo_Veiculo']

def gerar_graficos_pizza1(df_decadas):
    for decada, dados_decada in df_decadas.iterrows():
        labels = ['Homicidio', 'Estupro', 'Roubo_Residencia', 
                  'Assalto_Agravante', 'Furto_Residencia', 'Furto_Roubo_Geral', 'Roubo_Veiculo']
        sizes = dados_decada[[col + '_Porcentagem' for col in labels]].tolist()
        fig = px.pie(names=labels, values=sizes)
        fig.update_traces(textinfo='percent+label')
        fig.update_layout(title=f'Porcentagem dos Crimes na Década de {decada.left.year}s', height=700, width=1100)
        st.plotly_chart(fig)

def gerar_grafico_pizza2(df):
    total_propriedade = df['Propriedade'].sum()
    total_violento = df['Violento'].sum()
    total_crimes = total_propriedade + total_violento

    labels = ['Propriedade', 'Violento']
    sizes = [total_propriedade / total_crimes * 100, total_violento / total_crimes * 100]

    fig = px.pie(names=labels, values=sizes)
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(title='Porcentagem de Crimes Propriedade e Violentos (Total)', height=700, width=1100)
    st.plotly_chart(fig)

def gerar_graficos_pizza_violentos(df_decadas_violentos):
    for decada, dados_decada in df_decadas_violentos.iterrows():
        labels = ['Homicidio', 'Estupro', 'Roubo_Residencia', 'Assalto_Agravante']
        sizes = dados_decada.tolist()
        fig = px.pie(names=labels, values=sizes)
        fig.update_traces(textinfo='percent+label')
        fig.update_layout(title=f'Porcentagem dos Crimes Violentos na Década de {decada.left.year}s', height=700, width=1100)
        st.plotly_chart(fig) 

with aba1:
  st.markdown("### Algumas informações sobre determinadas colunas específicas:")
  st.markdown("- **Violento**: Total de Crimes violentos naquele Ano (Soma de Homicídio, Estupro, Roubo_Residência e Assalto_Agravante)")
  st.markdown("- **Propriedade**: Total de Crimes à Propriedade (Soma de Furto_Residencial, Furto_Roubo_Geral, Roubo_Veículo)")
  st.markdown("- **Total**:  Total de Crimes no Geral naquele Ano (Soma de Violento e Propriedade)")
  st.markdown("- **Link Base de Dados**:  [US_Crime_Rates_1960_2014](https://www.kaggle.com/datasets/mahmoudshogaa/us-crime-rates-1960-2014/data)")

  anos_unicos = df['Ano'].dt.year.unique()
  ano_minimo = int(min(anos_unicos))
  ano_maximo = int(max(anos_unicos))
  ano_inicio, ano_fim = st.slider('Selecione um intervalo de anos', ano_minimo, ano_maximo, (ano_minimo, ano_maximo))
  df_filtrado = df[(df['Ano'].dt.year >= ano_inicio) & (df['Ano'].dt.year <= ano_fim)]
  st.dataframe(df_filtrado[colunas_para_exibir])

with aba2:
  # Filtro de multiselect para selecionar os anos
  anos_selecionados = st.multiselect('Selecione o(s) ano(s):', df['Ano'].dt.year.unique())

    # Filtrando o DataFrame com base nos anos selecionados
  df_filtrado = df[df['Ano'].dt.year.isin(anos_selecionados)]

  
  coluna1, coluna2, coluna3 = st.columns(3)

  with coluna1:
        st.metric('Crimes violentos no(s) ano(s) selecionado(s)', format_number(df_filtrado['Violento'].sum()))
        df_crimes_violentos_por_ano

  with coluna2:
        st.metric('Crimes de Propriedade no(s) ano(s) selecionado(s)', format_number(df_filtrado['Propriedade'].sum()))
        df_crimes_propriedade_por_ano
        
  with coluna3:
        st.metric('Total de Crimes no(s) ano(s) selecionado(s)', format_number(df_filtrado['Total'].sum()))
        df_crimes_por_ano 

with aba3:
  gerar_graficos_pizza1(df_decadas)

with aba4:
  gerar_graficos_pizza_violentos(df_decadas_violentos)

with aba5:
 gerar_grafico_pizza2(df)
    
with aba6:
  st.plotly_chart(grafico_crimes_populacao, use_container_width=True)

with aba7:
  st.plotly_chart(grafico_crimes_por_decada, use_container_width=True)



