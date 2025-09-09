import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Dashboard Financeiro", layout="wide")
st.title("📊 Dashboard Financeiro - SEMEC")

# Upload de arquivo
uploaded = st.file_uploader("Carregar arquivo Excel", type=["xlsx"])
if uploaded:
    df = pd.read_excel(uploaded, engine="openpyxl")

    # ✅ Conversão de colunas numéricas (padrão brasileiro)
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
        unidades = df["Unidade Gestora"].dropna().unique().tolist()
        unidade_sel = st.sidebar.multiselect(
            "Selecione a(s) Unidade(s) Gestora(s):",
            sorted(unidades),
            default=unidades
        )
        df = df[df["Unidade Gestora"].isin(unidade_sel)]

    # 🔹 Filtro por Classificação
    opcoes = ["Continuada", "Fixo/Outro", "Valores Totais"]
    filtros = st.sidebar.multiselect("Selecione as Classificações:", opcoes, default=opcoes)

    if "Valores Totais" not in filtros:
        if "Classificação" in df.columns:
            df = df[df["Classificação"].isin(filtros)]

    # 🔹 Identificar colunas numéricas para somar
    valor_cols = [col for col in df.columns if "Vlr" in col or "Sld" in col]

    # 🔹 Cálculo dos totais
    totais = df[valor_cols].sum(numeric_only=True).round(2)

    # Função para formatar em BRL
    def br_fmt(v: float) -> str:
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # 🔹 Exibir cards de totais
    st.subheader("📌 Totais por Coluna (após filtros aplicados)")
    cols = st.columns(3)
    for i, (col, val) in enumerate(totais.items()):
        with cols[i % 3]:
            st.metric(label=col, value=br_fmt(val))

    # 🔹 Função para exportar Excel
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Filtrado")
        processed_data = output.getvalue()
        return processed_data

    # 🔹 Botão para download
    excel_file = to_excel(df)
    nome_arquivo = "dados_filtrados.xlsx"
    if len(unidade_sel) == 1:  # se só uma unidade foi selecionada, personaliza o nome
        nome_arquivo = f"dados_{unidade_sel[0]}.xlsx"

    st.subheader("⬇️ Baixar arquivo filtrado")
    st.download_button(
        label="📥 Baixar Excel filtrado",
        data=excel_file,
        file_name=nome_arquivo,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

else:
    st.info("Faça upload de um arquivo Excel para começar.")
