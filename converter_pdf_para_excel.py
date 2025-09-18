import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO
import requests

def pdf_para_excel_bytes(pdf_file):
    # pdf_file pode ser caminho, BytesIO, ou arquivo enviado pelo usuário
    output = BytesIO()
    with pdfplumber.open(pdf_file) as pdf:
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            for i, page in enumerate(pdf.pages):
                tabelas = page.extract_tables()
                for j, tabela in enumerate(tabelas):
                    if tabela:
                        df = pd.DataFrame(tabela[1:], columns=tabela[0])  # usa primeira linha como header
                        df.to_excel(writer, sheet_name=f'Pg{i+1}_Tab{j+1}', index=False)
    return output.getvalue()

st.title("Conversor PDF para Excel")

url_input = st.text_input("Cole a URL do arquivo PDF aqui:")

if url_input:
    try:
        resposta = requests.get(url_input)
        if resposta.status_code == 200:
            arquivo_pdf = BytesIO(resposta.content)
            excel_bytes = pdf_para_excel_bytes(arquivo_pdf)
            st.download_button(
                label="Baixar Excel convertido da URL",
                data=excel_bytes,
                file_name="tabelas_convertidas.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error("Erro ao baixar o PDF da URL.")
    except Exception as e:
        st.error(f"Erro: {e}")

st.write("---")

uploaded_file = st.file_uploader("Ou envie um arquivo PDF local", type=['pdf'])

if uploaded_file is not None:
    try:
        excel_bytes = pdf_para_excel_bytes(uploaded_file)
        st.download_button(
            label="Baixar Excel convertido",
            data=excel_bytes,
            file_name="tabelas_convertidas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")


