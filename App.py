import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="📊",
    layout="wide",
) 

df = pd.read_csv('dados-pokemon-filtrados.csv')

# Traduzir valores da coluna 'Lendário'
df['Lendário'] = df['Lendário'].map({0.0: 'Comum', 1.0: 'Lendário'})

st.sidebar.header("🔍 Filtros")

lista_nomes = sorted(df['Name'].drop_duplicates())
nome_pokemon_select = st.sidebar.selectbox("Selecione um Pokémon:", options=["(Todos)"] + lista_nomes)

if nome_pokemon_select != "(Todos)":
    nome_pokemon = nome_pokemon_select
else:
    nome_pokemon = ""



tipo1 = sorted(df['Tipo 1'].unique())
tipo1_selecionado = st.sidebar.multiselect("Filtro da primeira tipagem 1:", tipo1, default=tipo1)

tipo2 = sorted(df['Tipo 2'].dropna().unique())
tipo2_opcoes = list(tipo2) + ['[Sem Tipo 2]']
tipo2_selecionado = st.sidebar.multiselect("Filtro da segunda tipagem 2:", tipo2_opcoes, default=tipo2_opcoes)



geracao = sorted(df['Geração'].unique())
geracao_selecionada = st.sidebar.multiselect("Filtro da Geração:", geracao, default=geracao)

lendario = sorted(df['Lendário'].dropna().unique())
lendario_selecionado = st.sidebar.multiselect("Filtro de Raridade:", lendario, default=lendario)

#mega = sorted(df['Mega'].unique())
#mega_selecionado = st.sidebar.multiselect("Filtro de Mega Evolução:", mega, default=mega)


if nome_pokemon:
    df_filtrado = df[
        (df['Tipo 1'].isin(tipo1_selecionado)) &
        (
            (df['Tipo 2'].isin([t for t in tipo2_selecionado if t != '[Sem Tipo 2]'])) |
            ((df['Tipo 2'].isna()) & ('[Sem Tipo 2]' in tipo2_selecionado))
        ) &
        (df['Geração'].isin(geracao_selecionada)) &
        (df['Lendário'].isin(lendario_selecionado)) &
        (df['Name'] == nome_pokemon)
    ]
else:
    df_filtrado = df[
        (df['Tipo 1'].isin(tipo1_selecionado)) &
        (
            (df['Tipo 2'].isin([t for t in tipo2_selecionado if t != '[Sem Tipo 2]'])) |
            ((df['Tipo 2'].isna()) & ('[Sem Tipo 2]' in tipo2_selecionado))
        ) &
        (df['Geração'].isin(geracao_selecionada)) &
        (df['Lendário'].isin(lendario_selecionado))
    ]


st.title("📊 Dashboard de Pokémon")
st.markdown("Explore os dados dos Pokémon filtrando por tipo, geração, raridade, mega evolução e nome.")

st.subheader("Gráficos")

st.subheader("Quantidade de Pokémon pela tipagem 1")
if not df_filtrado.empty:
    pokemons_contagem = df_filtrado['Tipo 1'].value_counts().reset_index()
    pokemons_contagem.columns = ['Tipo 1', 'Contagem']
    pokemons_contagem = pokemons_contagem.iloc[::-1].reset_index(drop=True)
    fig1 = px.bar(pokemons_contagem, x='Tipo 1', y='Contagem', title='Contagem de Pokémon por Tipo 1', color='Tipo 1', text='Contagem')
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("Nenhum Pokémon encontrado com os filtros selecionados.")

st.subheader("Quantidade de Pokémon pela tipagem 2")
if not df_filtrado.empty:
    pokemons_contagem = df_filtrado['Tipo 2'].value_counts().reset_index()
    pokemons_contagem.columns = ['Tipo 2', 'Contagem']
    pokemons_contagem = pokemons_contagem.iloc[::-1].reset_index(drop=True)
    fig1 = px.bar(pokemons_contagem, x='Tipo 2', y='Contagem', title='Contagem de Pokémon por Tipo 2', color='Tipo 2', text='Contagem')
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("Nenhum Pokémon encontrado com os filtros selecionados.")

if not df_filtrado.empty:
    pokemons_geracao = df_filtrado['Geração'].value_counts().reset_index()
    pokemons_geracao.columns = ['Geração', 'Contagem']
    grafico_geracao = px.bar(pokemons_geracao, x='Geração', y='Contagem', color='Geração')
    configuração_geracao = {"title": {"text": "Quantidade de pokemons por geração"}, }
    # Esse comando
    grafico_geracao.update_layout(configuração_geracao)
    st.plotly_chart(grafico_geracao, use_container_width=True)
else:
    st.warning("Nenhum Pokémon encontrado com os filtros selecionados.")

st.subheader("Informações Detalhadas de Cada Pokémon")

st.subheader("Gráfico de Raridade dos Pokémon")
if not df_filtrado.empty:
    porcentagem_raridades = df_filtrado['Lendário'].value_counts().reset_index()
    porcentagem_raridades.columns = ['Lendário', 'count']
    porcentagem_raridades['Lendário'] = porcentagem_raridades['Lendário'].replace({0.0: 'Comum', 100.0: 'Lendário'})

    grafico_lendario = px.pie(porcentagem_raridades, values='count' , names='Lendário', hole=0.5)
    configuração = {
        "title": {"text": "Porcentagem de pokemons lendários e comuns"},
        "showlegend": True,
        "legend": {"title": {"text": "Raridade"}}
    }
    # Esse comando carregará as configurações feitas
    grafico_lendario.update_layout(configuração)
    st.plotly_chart(grafico_lendario, use_container_width=True)
else:
    st.warning("Nenhum Pokémon encontrado com os filtros selecionados.")


st.subheader("Teia de Status do Pokémon")

if nome_pokemon_select == "(Todos)":
    st.warning("Nenhum Pokémon encontrado com os filtros selecionados.")
elif not df_filtrado.empty:
    linha = df_filtrado.iloc[0]
    gráfico_teia = pd.DataFrame(dict(
        r=[linha['HP'], 
           linha['Att'], 
           linha['Def'], 
           linha['Spa'], 
           linha['Spd'], 
           linha['Spe']],
        theta=['HP', 'Att', 'Def', 'Spa', 'Spd', 'Spe']
    ))

    fig = px.line_polar(gráfico_teia, r='r', theta='theta', line_close=True)
    configuração = {
        "title": {"text": nome_pokemon_select},
        "polar": {
            "radialaxis": {
                "visible": True,
                "range": [0, 150]
            }
        }
    }
    fig.update_layout(configuração)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Nenhum Pokémon encontrado com os filtros selecionados.")

if not df_filtrado.empty:
    st.subheader("Tabela de Pokémon")
    st.dataframe(df_filtrado.reset_index(drop=True))
else:
    st.warning("Nenhum Pokémon encontrado com os filtros selecionados.")