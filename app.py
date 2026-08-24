#%%
import config
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px


st.title("ONS - Dados Abertos")


def formata_valor(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

@st.cache_resource
def get_connection():
    return sqlite3.connect(config.DATABASE_PATH, check_same_thread=False)


@st.cache_data
def carregar_dados(nome_arquivo_sql: str):
    caminho = config.QUERIES_DIR / nome_arquivo_sql

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



df_carga_media = carregar_dados(config.QUERY_CARGA_MEDIA)
df_carga_maxima = carregar_dados(config.QUERY_CARGA_MAXIMA)
df_util_fim_semana = carregar_dados(config.QUERY_UTIL_FIM_SEMANA)
df_media_mensal = carregar_dados(config.QUERY_MEDIA_MENSAL)
df_percent_media_fonte = carregar_dados(config.QUERY_PERCENT_MEDIA)
df_maior_menor_percent = carregar_dados(config.QUERY_PERCENT_MAIOR_E_MENOR)
df_balanco_carga = carregar_dados(config.QUERY_BALANCO_CARGA)
df_ena_ear = carregar_dados(config.QUERY_ENA_EAR)
df_intercambio = carregar_dados(config.QUERY_INTERCAMBIO)
df_cmo_ear = carregar_dados(config.QUERY_CMO)


tab1, tab2, tab3, tab4 = st.tabs(["Consumo", "Geração", "ENA VS EAR", "CMO"])

with tab1:
    st.subheader("Comparativo da Carga Média por Subsistema")
    # query da carga média
    st.bar_chart(
        df_carga_media, 
        x="subsistema",
        y="media_de_carga",
        x_label="Subsistema",
        y_label="Média de Carga (MWmed)"
    )
    st.caption("**Figura 1:** Carga Média de Energia por Subsistema (ONS).")

    st.markdown(
            f"O gráfico revela uma assimetria estrutural na demanda de energia entre as regiões do Sistema Interligado Nacional (SIN). O subsistema Sudeste/Centro-Oeste concentra, isoladamente, quase metade da carga média do país (~43.000 MW) — reflexo direto da densidade populacional e industrial de estados como São Paulo, Minas Gerais e Rio de Janeiro. Sul e Nordeste aparecem em um patamar intermediário e semelhante entre si (~13.000–14.000 MW), enquanto o Norte apresenta a menor carga de todas (~8.000 MW)."

    )
    st.markdown(
            "Esse último dado é o mais revelador: o Norte, apesar da baixa demanda local, abriga algumas das maiores usinas hidrelétricas do país (Belo Monte, Tucuruí), tornando-se um exportador estrutural de energia. Esse descompasso entre geração abundante e consumo local reduzido é o que sustenta os fluxos de intercâmbio predominantemente positivos observados no subsistema — e, por consequência, explica por que o Custo Marginal de Operação (CMO) do Norte tende a permanecer em zero na maior parte do tempo, mesmo diante de variações no nível de reservatórios: o preço local reflete menos a escassez hídrica e mais a capacidade de escoamento da energia excedente para os centros de consumo."
        )

    

    # query da carga máxima
    st.subheader("Comparativo da Carga Máxima diária por Subsistema")
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

    st.caption("**Figura 2:** Carga Máxima diária por Subsistema (ONS).")


    st.markdown(
                f"Enquanto a carga média revela o padrão de consumo típico de cada região, a carga máxima diária expõe os picos de demanda — momentos críticos para o dimensionamento do sistema elétrico. O Sudeste/Centro-Oeste lidera com folga também aqui, atingindo 55.584,90 MWmed em seu pico (18/02/2025), mais que o triplo do Sul (19.246,63 MWmed) e quase seis vezes o Norte (9.500,11 MWmed). A hierarquia entre subsistemas se mantém a mesma da carga média, mas a distância entre o Sudeste/Centro-Oeste e os demais se acentua no pico — sinal de uma demanda mais concentrada e volátil na região que concentra o maior parque industrial e a maior população do país."
    )

    st.markdown(
                "O dado mais revelador aqui, no entanto, é a data de ocorrência de cada pico. Sudeste/Centro-Oeste e Sul atingiram seu máximo em fevereiro de 2025 — pleno verão, período de maior uso de climatização e ar-condicionado nessas regiões mais urbanizadas. Já Nordeste e Norte registraram seus picos em outubro e novembro, respectivamente — período tipicamente mais seco e quente nessas regiões, associado a maior demanda por refrigeração e irrigação. Essa defasagem sazonal entre subsistemas é um indicativo de que a demanda de pico no Brasil não é um fenômeno nacional único e simultâneo, mas sim regionalizado por clima — um fator relevante para o planejamento de capacidade e para entender por que o intercâmbio entre subsistemas ajuda a suavizar picos que não coincidem no tempo."
    )


    # query de comparação de carga entre dia útil versus fim de semana
    st.subheader("Comparativo de carga entre dia útil e fim de semana")
    st.bar_chart(df_util_fim_semana, x="subsistema", y=["dia_util", "fim_de_semana"], x_label="Dia Útil", y_label="Fim de Semana", stack=False)
    st.caption("**Figura 3:** Dia Útil x Fim de Semana (ONS).")

    st.markdown("O gráfico compara a carga média em dias úteis (azul claro) e fins de semana (azul escuro) para cada subsistema, e o padrão é consistente em todas as regiões: a demanda cai nos finais de semana, refletindo a redução da atividade industrial e comercial nesses dias. O Sudeste/Centro-Oeste apresenta a maior queda em termos absolutos (de ~45.000 para ~40.000 MW), o que é esperado dado seu parque industrial concentrado — quanto maior a base de consumo atrelada à produção, maior o efeito de calendário sobre a carga.")

    # query da carga média mensal
    st.subheader("Carga Média Mensal")
    st.line_chart(
        df_media_mensal,
        x="mes",
        y="media_mensal",
        x_label="Mês",
        y_label="Média Mensal",
        color="subsistema"
    )

    st.caption("**Figura 4:** Carga Média Mensal (ONS).")
    
    st.markdown("A série temporal mensal (2023–2025) evidencia que o Sudeste/Centro-Oeste não só mantém a maior carga do sistema como também apresenta a maior variabilidade sazonal, com um pico visível em torno de janeiro/fevereiro de 2025 (~50.000 MW) e uma tendência de crescimento ao longo dos anos. Os demais subsistemas (Sul, Nordeste, Norte) permanecem relativamente estáveis e próximos entre si, sem oscilações tão pronunciadas — reforçando que o Sudeste/Centro-Oeste é o principal motor de variação de demanda do SIN como um todo.")

with tab2:

    # query do percentual médio de cada fonte por dia
    st.subheader("Percentual médio diário de participação de cada fonte")
    st.bar_chart(
        df_percent_media_fonte,
        x="subsistema",
        y=[
            "percent_hidraulica",
            "percent_terminca",
            "percent_eolica",
            "percent_solar"
        ],
        x_label="Subsistema",
        color="subsistema",
        stack=True
    )

    st.caption("**Figura 5:** Percentual médio diário de participação de cada fonte (ONS).")
    st.markdown("Esse gráfico revela a diversidade da matriz energética brasileira por região: enquanto Norte, Sudeste/Centro-Oeste e Sul têm a geração hidráulica (azul escuro) como fonte amplamente dominante, o Nordeste se destaca por uma matriz muito mais diversificada, com participação expressiva de eólica (mais de 50%) e solar — um reflexo direto do potencial de vento e irradiação da região. Essa diferença estrutural é o motivo pelo qual o Nordeste tende a ter uma dinâmica de geração menos dependente do regime de chuvas do que os demais subsistemas.")



with tab3:
    # ena x ear
    subsistema_sel = st.selectbox(
        "Selecione o Subsistema",
        options=df_ena_ear["subsistema"].unique()
    )

    df_filtrado = df_ena_ear[df_ena_ear["subsistema"] == subsistema_sel]

    st.subheader("Comparativo entre ENA e EAR")
    fig = px.line(
        df_filtrado,
        x="dia",
        y=["ena_percentual", "ear_percentual"],
        title=f"Evolução Temporal ENA vs EAR - {subsistema_sel}",
        labels={"value": "Percentual (%)", "variable": "Métrica"},
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("**Figura 6:** Comparativo entre ENA e EAR (ONS).")
    st.markdown("O gráfico sobrepõe duas séries temporais diárias — ENA (percentual de afluência, energia que chega aos reservatórios via chuva) e EAR (percentual de energia armazenada, o estoque acumulado) — no mesmo eixo, permitindo visualizar a relação entre fluxo de entrada e nível de reservatório ao longo do tempo. Como a ENA reage de forma mais rápida e volátil às chuvas, enquanto a EAR se move de forma suavizada, acumulando o efeito da ENA ao longo de semanas, o gráfico deixa evidente o padrão de defasagem entre as duas grandezas: picos sustentados de ENA precedem e sustentam as fases de recuperação da EAR, e períodos prolongados de ENA baixa antecedem o esvaziamento gradual dos reservatórios.")



    # intercâmbio de energia
    st.subheader("Intercâmbio de energia: Exportador vs Importador")
    df_intercambio["rota"] = df_intercambio["exportador"] + " ➔ " + df_intercambio["importador"]

    fig = px.bar(
        df_intercambio,
        x="ano",
        y="valor",
        color="rota",
        barmode="group",
        title="Evolução do Intercâmbio de Energia por Rota (2023-2025)",
        labels={"valor": "Energia (MWmed)", "ano": "Ano", "rota": "Fluxo"},
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("**Figura 7:** Intercâmbio de energia: Exportador vs Importador (ONS).")
    st.markdown("O gráfico de rotas de intercâmbio por ano confirma numericamente o que a análise anterior já sugeria: Norte→Sudeste e Nordeste→Sudeste são, de longe, os maiores fluxos do sistema, consolidando essas duas regiões como exportadoras estruturais de energia para o centro de consumo do país. Vale destacar a queda expressiva da rota Sudeste→Sul ao longo dos três anos (de ~27M para ~8M MWmed) e o crescimento simultâneo de Nordeste→Norte — mudanças que sinalizam uma reconfiguração dos fluxos regionais de energia ao longo do período analisado, possivelmente ligada a variações na geração eólica/solar do Nordeste e à expansão de capacidade de transmissão.")

with tab4:
    st.subheader("EAR x CMO")

    df_cmo_ear["posicao"] = df_cmo_ear["saldo_intercambio_semana"].apply(
        lambda x: "Exportador" if x > 0 else "Importador"
    )

    fig = px.scatter(
        df_cmo_ear,
        x="ear_media_semana",
        y="val_cmomediasemanal",
        color="posicao", 
        hover_data=["din_instante", "ena_media_semana", "saldo_intercambio_semana"],
        labels={"ear_media_semana": "EAR (%)", "val_cmomediasemanal": "CMO médio (R$/MWh)"}
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("**Figura 8:** Relação entre EAR e CMO (ONS).")
    st.markdown("Esse mostra que o CMO se distribui em faixas bem definidas (próximo de zero, ~100, ~250–320 e acima de 550 R$/MWh) em vez de crescer de forma contínua conforme a EAR cai — um comportamento típico de um sistema com preços em degrau, influenciado por patamares de carga e custos de acionamento de térmicas específicas. A mistura de pontos exportador/importador em praticamente todas as faixas de EAR confirma que, mesmo numa visão mais ampla do sistema, a energia armazenada sozinha não explica o CMO — reforçando a necessidade das variáveis complementares (intercâmbio, ENA, fonte).")


