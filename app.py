import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard de Valores", layout="wide")

st.title("📊 Dashboard de Valores por Unidade Gestora e Classificação")

# Upload do arquivo
uploaded = st.file_uploader(r"C:\Users\03362306217\Desktop\teste.xlsx", type=["xlsx"])

if uploaded:
    # ✅ Leitura já tratando número brasileiro
    df = pd.read_excel(uploaded, decimal=",", thousands=".")

    # Colunas numéricas (pega valores financeiros e saldos)
    valor_cols = [col for col in df.columns if "Vlr" in col or "Sld" in col]

    # 🔹 Sidebar para filtros
    st.sidebar.header("Filtros")

    # 🔹 Filtro de unidade gestora
    if "Unidade Gestora" in df.columns:
        unidades = df["Unidade Gestora"].dropna().unique().tolist()
        unidade_sel = st.sidebar.multiselect(
            "Selecione a(s) Unidade(s) Gestora(s):",
            sorted(unidades),
            default=unidades
        )
        df = df[df["Unidade Gestora"].isin(unidade_sel)]

    # 🔹 Filtro de classificação
    opcoes = ["Continuada", "Fixo/Outro", "Valores Totais"]
    filtros = st.sidebar.multiselect("Selecione as Classificações:", opcoes, default=opcoes)

    # Aplica o filtro de classificação
    if "Valores Totais" not in filtros:
        if "Classificação" in df.columns:
            df = df[df["Classificação"].isin(filtros)]

    # 🔹 Cálculo dos totais
    totais = df[valor_cols].sum(numeric_only=True).round(2)

    # Função para formatar em padrão brasileiro
    def br_fmt(v: float) -> str:
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # 🔹 Exibir os totais em cards
    st.subheader("📌 Totais por Coluna (após filtros aplicados)")
    cols = st.columns(3)
    for i, (col, val) in enumerate(totais.items()):
        with cols[i % 3]:
            st.metric(label=col, value=br_fmt(val))

