#%%
from config import QUERIES_DIR, DATABASE_PATH, QUERY_CARGA_MEDIA, QUERY_CARGA_MAXIMA, QUERY_UTIL_FIM_SEMANA, QUERY_MEDIA_MENSAL, QUERY_PERCENT_MEDIA, QUERY_PERCENT_MAIOR_E_MENOR, QUERY_BALANCO_CARGA
import streamlit as st
import pandas as pd
import sqlite3


st.title("ONS - Dados Abertos")


def formata_valor(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

@st.cache_resource
def get_connection():
    return sqlite3.connect(DATABASE_PATH, check_same_thread=False)


@st.cache_data
def carregar_dados(nome_arquivo_sql: str):
    caminho = QUERIES_DIR / nome_arquivo_sql

    try:
        with open(caminho, encoding="utf-8") as f:
            query = f.read()
    except FileNotFoundError:
        st.error(f"Arquivo de query não encontrado: `{caminho}`")
        st.stop()    

    try:
        conn = get_connection()
        return pd.read_sql_query(query, conn)
    except (sqlite3.OperationalError, pd.errors.DatabaseError) as e:
        st.error(f"Erro ao executar a query `{nome_arquivo_sql}`: {e}")
        st.stop()



df_carga_media = carregar_dados(QUERY_CARGA_MEDIA)
df_carga_maxima = carregar_dados(QUERY_CARGA_MAXIMA)
df_util_fim_semana = carregar_dados(QUERY_UTIL_FIM_SEMANA)
df_media_mensal = carregar_dados(QUERY_MEDIA_MENSAL)
df_percent_media_fonte = carregar_dados(QUERY_PERCENT_MEDIA)
df_maior_menor_percent = carregar_dados(QUERY_PERCENT_MAIOR_E_MENOR)


tab1, tab2, tab3, = st.tabs(["Consumo", "Geração", "Qualidade do Dado"])

with tab1:
    # query da carga média
    st.subheader("Carga Média por Subsistema")
    st.bar_chart(df_carga_media, x="subsistema", y="media_de_carga")

    # query da carga máxima
    st.subheader("Carga Máxima diária por Subsistema")
    rows = [df_carga_maxima.iloc[i:i+2] for i in range(0, len(df_carga_maxima), 2)]
    for row_df_carga_maxima in rows:
        cols = st.columns(2)
        for col, (_, row) in zip(cols, row_df_carga_maxima.iterrows()):
            with col:
                st.metric(
                    label=row["subsistema"],
                    value=f'{formata_valor(row["maximo_carga"])} MWmed'
                )
                st.markdown(f"📅 **{row['data']}**")

    # query de comparação de carga entre dia útil versus fim de semana
    st.subheader("Dia útil x Fim de semana")
    st.bar_chart(df_util_fim_semana, x="subsistema", y=["dia_util", "fim_de_semana"], stack=False)

    # query da carga média mensal
    st.subheader("Carga Média Mensal")
    st.line_chart(
        df_media_mensal,
        x="mes",
        y="media_mensal",
        color="subsistema"
    )

with tab2:

    # query do percentual médio de cada fonte por dia
    st.subheader("PERCENTUAL MÉDIO DIÁRIO DE PARTICIPAÇÃO DE CADA FONTE")
    st.bar_chart(
        df_percent_media_fonte,
        x="subsistema",
        y=[
            "percent_hidraulica",
            "percent_terminca",
            "percent_eolica",
            "percent_solar"
        ],
        color="subsistema",
        stack=True
    )

    # query do maior/menor percentual médio da energia eólica
    st.subheader("Participação da geração eólica: maior e menor")
    