
import requests
import pandas as pd
import pdfplumber
from io import BytesIO

def escolher_pdf():
    path = filedialog.askopenfilename(filetypes=[("PDF files","*.pdf")])
    if path:
        pdf_entry.delete(0, tk.END)
        pdf_entry.insert(0, path)

def baixar_pdf_url():
    url = pdf_entry.get()
    if not url.startswith("http"):
        messagebox.showerror("Erro", "Insira uma URL válida.")
        return None
    try:
        r = requests.get(url)
        r.raise_for_status()
        return BytesIO(r.content)
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        return None

def converter_pdf():
    btn_converter.config(state="disabled")
    pdf_path = pdf_entry.get()
    if pdf_path.startswith("http"):
        pdf_stream = baixar_pdf_url()
        if not pdf_stream: 
            btn_converter.config(state="normal")
            return
        input_pdf = pdf_stream
    else:
        if not pdf_path:
            messagebox.showerror("Erro", "Selecione um PDF ou informe a URL.")
            btn_converter.config(state="normal")
            return
        input_pdf = pdf_path

    try:
        # Extrai tabelas usando pdfplumber
        dfs = []
        with pdfplumber.open(input_pdf) as pdf:
            for page in pdf.pages:
                extracted_tables = page.extract_tables()
                for table in extracted_tables:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    dfs.append(df)

        if not dfs:
            messagebox.showerror("Erro", "Nenhuma tabela encontrada no PDF.")
            btn_converter.config(state="normal")
            return

        global resultado_excel
        resultado_excel = BytesIO()
        with pd.ExcelWriter(resultado_excel, engine='openpyxl') as writer:
            for idx, df in enumerate(dfs):
                df.to_excel(writer, sheet_name=f'Tabela{idx+1}', index=False)

        btn_baixar.config(state="normal")
        messagebox.showinfo("Sucesso", "PDF convertido. Clique em BAIXAR para salvar o Excel.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))
    finally:
        btn_converter.config(state="normal")

def baixar_excel():
    if resultado_excel:
        export_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if export_path:
            with open(export_path, "wb") as f:
                f.write(resultado_excel.getvalue())
            messagebox.showinfo("Salvo", "Arquivo Excel baixado com sucesso.")


