import streamlit as st
import pandas as pd
import requests as req

urlmulheres = 'https://dadosabertos.camara.leg.br/api/v2/deputados?siglaSexo=F&ordem=ASC&ordenarPor=nome'
resposta = req.get(urlmulheres)
dados = resposta.json()
dfmulheres = pd.DataFrame(dados['dados'])
dfmulheres['sexo'] = 'F'

urlhomens = 'https://dadosabertos.camara.leg.br/api/v2/deputados?siglaSexo=M&ordem=ASC&ordenarPor=nome'
resposta = req.get(urlhomens)
dados = resposta.json()
dfhomens = pd.DataFrame(dados['dados'])
dfhomens['sexo'] = 'M'

df = pd.concat([dfmulheres, dfhomens])

opcao = st.selectbox(
    'Qual o sexo?',
     df['sexo'].unique())
dfFiltrado = df[df['sexo'] == opcao]
st.title('Deputados do sexo ' + opcao)

ocorrencias = dfFiltrado['siglaUf'].value_counts()
dfEstados = pd.DataFrame({
    'siglaUf': ocorrencias.index,
    'quantidade': ocorrencias.values}
    )

#total de homens
totalhomens = dfhomens['id'].count()
st.metric('Total de Homens', totalhomens)
#total de mulheres
totalmulheres = dfmulheres['id'].count()
st.metric('Total de Mulheres', totalmulheres)
st.write('Total de deputadas do sexo ' + opcao)
st.bar_chart(dfEstados,
             x = 'siglaUf',
             y = 'quantidade',
             x_label='Siglas dos estados',
             y_label='Quantidade de deputados')
st.dataframe(dfFiltrado)
