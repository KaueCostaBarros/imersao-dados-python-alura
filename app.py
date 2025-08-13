import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="📊",
    layout="wide",
)

# --- Carregamento dos dados ---
df = pd.read_csv(
    "https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv"
)

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")
anos_disponiveis = sorted(df['ano'].unique())
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)
senioridades_disponiveis = sorted(df['senioridade'].unique())
senioridades_selecionadas = st.sidebar.multiselect("Senioridade", senioridades_disponiveis, default=senioridades_disponiveis)
contratos_disponiveis = sorted(df['contrato'].unique())
contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis)
tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)

# --- Controles interativos ---
st.sidebar.header("⚙️ Configurações de Gráficos")
top_n_cargos = st.sidebar.slider("Número de Top cargos", min_value=5, max_value=20, value=10, step=1)
hist_bins = st.sidebar.slider("Número de bins do histograma", min_value=10, max_value=50, value=30, step=1)

# --- Filtragem do DataFrame ---
df_filtrado = df.query(
    "ano in @anos_selecionados and senioridade in @senioridades_selecionadas "
    "and contrato in @contratos_selecionados and tamanho_empresa in @tamanhos_selecionados"
)

# --- Função utilitária para padronizar layout dos gráficos ---
def padronizar_layout(fig, altura=400, titulo_x=0.05):
    fig.update_layout(
        margin=dict(l=50, r=50, t=50, b=50),
        title_x=titulo_x,
        height=altura,
        font=dict(family="Arial, sans-serif", size=14),
        transition=dict(duration=1000, easing='cubic-in-out')
    )
    return fig

# --- Conteúdo Principal ---
st.title("🎲 Dashboard de Análise de Salários na Área de Dados")
st.markdown(
    "Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise."
)

# --- Métricas gerais ---
st.subheader("Métricas gerais (Salário anual em USD)")
if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_maximo = df_filtrado['usd'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado['cargo'].value_counts().idxmax()
else:
    salario_medio, salario_maximo, total_registros, cargo_mais_frequente = 0, 0, 0, ""

cols = st.columns(4)
cols[0].metric("Salário médio", f"${salario_medio:,.0f}")
cols[1].metric("Salário máximo", f"${salario_maximo:,.0f}")
cols[2].metric("Total de registros", f"{total_registros:,}")
cols[3].metric("Cargo mais frequente", cargo_mais_frequente)

st.markdown("---")

# --- Gráficos gerais ---
if not df_filtrado.empty:
    # Top cargos
    salario_cargo = df_filtrado.groupby('cargo')['usd'].mean().reset_index()
    top_cargos = salario_cargo.nlargest(top_n_cargos, 'usd').sort_values('usd', ascending=True)
    fig_top = px.bar(
        top_cargos,
        x='usd',
        y='cargo',
        orientation='h',
        title=f"Top {top_n_cargos} cargos por salário médio",
        labels={'usd': 'Média salarial anual (USD)', 'cargo': ''}
    )
    fig_top.update_traces(marker_color='steelblue', hovertemplate='%{y}: %{x:$,.0f}<extra></extra>')
    st.subheader("Top cargos")
    st.plotly_chart(padronizar_layout(fig_top, altura=400), use_container_width=True)
    st.markdown("---")

    # Distribuição de salários
    fig_hist = px.histogram(
        df_filtrado,
        x='usd',
        nbins=hist_bins,
        title="Distribuição de salários anuais",
        labels={'usd': 'Faixa salarial (USD)', 'count': ''}
    )
    fig_hist.update_traces(marker_color='steelblue', hovertemplate='Salário: %{x:$,.0f}<br>Contagem: %{y}<extra></extra>')
    st.subheader("Distribuição de salários")
    st.plotly_chart(padronizar_layout(fig_hist, altura=400), use_container_width=True)
    st.markdown("---")

    # Proporção de tipos de trabalho
    remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
    remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
    fig_remoto = px.pie(
        remoto_contagem,
        names='tipo_trabalho',
        values='quantidade',
        title='Proporção dos tipos de trabalho',
        hole=0.5
    )
    fig_remoto.update_traces(textinfo='percent+label', hovertemplate='%{label}: %{value}<extra></extra>')
    st.plotly_chart(padronizar_layout(fig_remoto, altura=400), use_container_width=True)

# --- Seção Cientistas de Dados ---
if not df_filtrado.empty:
    df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
    st.subheader("Cientistas de Dados")

    if not df_ds.empty:
        # Agrupa por ano e país
        df_anim = df_ds.groupby(['ano', 'residencia_iso3'], as_index=False)['usd'].mean()
        df_anim = df_anim.sort_values('usd', ascending=False)

        # Mapeia nome completo e ISO2
        def obter_pais_info(code):
            country = pycountry.countries.get(alpha_3=code)
            if country:
                return pd.Series([country.name, country.alpha_2])
            return pd.Series([code, code[:2]])

        df_anim[['pais_full', 'pais_abrev']] = df_anim['residencia_iso3'].apply(obter_pais_info)

        # Média global por ano para cores divergentes
        media_global = df_ds.groupby('ano')['usd'].mean().to_dict()
        df_anim['cor'] = df_anim.apply(lambda row: row['usd'] - media_global[row['ano']], axis=1)

        # --- Gráfico de barras animado ---
        fig_bar_anim = px.bar(
            df_anim,
            x='pais_abrev',
            y='usd',
            text='pais_abrev',
            color='cor',
            color_continuous_scale='RdYlGn',
            animation_frame='ano',
            hover_data={'pais_full': True, 'usd': ':.0f'},
            labels={'pais_abrev': '', 'usd': 'Salário médio (USD)'}
        )
        fig_bar_anim.update_traces(textposition='outside', marker_line_color='black', marker_line_width=1.2,
                                   hovertemplate='%{customdata[0]}: %{y:$,.0f}<extra></extra>')
        fig_bar_anim.update_layout(
            title=dict(text='📊 Média salarial por país (Animado por Ano)', font=dict(size=22, family='Arial, sans-serif'), x=0.05),
            xaxis=dict(showticklabels=False),
            bargap=0.15,
            bargroupgap=0.02,
            margin=dict(l=50, r=50, t=80, b=50),
            height=520,
            coloraxis_colorbar=dict(title="Diferença da Média"),
            transition=dict(duration=1000, easing='cubic-in-out')
        )
        st.plotly_chart(fig_bar_anim, use_container_width=True)

# --- Tabela de dados detalhados ---
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado.head(1000), height=400)
