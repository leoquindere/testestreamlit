import streamlit as st
import pandas as pd

# Título
st.set_page_config(page_title="Dashboard Financeiro", layout="wide")
st.title("📊 Dashboard Financeiro - SEMEC")

# Upload de arquivo
uploaded = st.file_uploader("Carregar arquivo Excel", type=["xlsx"])
if uploaded:
    df = pd.read_excel(uploaded, engine="openpyxl")

    # Convertendo colunas numéricas
    for col in df.columns:
        if df[col].dtype == "object":
            try:
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace(".", "", regex=False)
                    .str.replace(",", ".", regex=False)
                    .astype(float)
                )
            except:
                pass

    # 🔹 Filtro por Unidade Gestora
    if "Unidade Gestora" in df.columns:
        unidade = st.selectbox("Selecione a Unidade Gestora", df["Unidade Gestora"].unique())
        df = df[df["Unidade Gestora"] == unidade]

    # 🔹 Somatório das colunas numéricas
    totais = df.select_dtypes(include="number").sum().round(2)

    st.subheader("📌 Totais da Unidade Selecionada")
    st.dataframe(totais)

    # 🔹 Botão para download do arquivo filtrado
    st.subheader("⬇️ Baixar arquivo filtrado")
    csv = df.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")
    st.download_button(
        label="📥 Baixar CSV",
        data=csv,
        file_name=f"dados_filtrados_{unidade}.csv",
        mime="text/csv",
    )
else:
    st.info("Faça upload de um arquivo Excel para começar.")
from io import BytesIO

# Função para exportar Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Filtrado")
    processed_data = output.getvalue()
    return processed_data

# Botão para download do Excel filtrado
excel_file = to_excel(df)
st.download_button(
    label="📥 Baixar Excel filtrado",
    data=excel_file,
    file_name="dados_filtrados.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
