import streamlit as st
import openpyxl
import io

st.title("Processador de Arquivo TXT com Excel")

# Excel fixo embutido
ARQUIVO_EXCEL = "valores.xlsx"

# Upload apenas do TXT
arquivo_txt = st.file_uploader("Selecione o arquivo TXT", type=["txt"])

if arquivo_txt:
    # Carrega o Excel fixo
    wb = openpyxl.load_workbook(ARQUIVO_EXCEL)
    ws = wb.active

    # Cria dicionário com os valores do Excel
    mapa = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is not None and row[1] is not None:
            chave = str(row[1]).strip()
            valor = str(row[0]).strip()
            mapa[chave] = valor

    # Lê todas as linhas do TXT
    conteudo_txt = arquivo_txt.read().decode("utf-8")
    linhas = [linha.rstrip("\n") for linha in conteudo_txt.splitlines()]

    linhas_saida = []
    for i, linha in enumerate(linhas):
        # Se for a primeira ou última linha -> não altera
        if i == 0 or i == len(linhas) - 1:
            linhas_saida.append(linha)
            continue

        # Pega o trecho a substituir
        trecho = linha[23:34]  # colunas 24 a 34 (11 posições)

        if trecho in mapa:
            novo_valor = mapa[trecho].zfill(11)
            linha = linha[:23] + novo_valor + linha[34:]

        # Agora altera a "coluna anterior"
        if linha[22] == "0":  # posição anterior ao trecho (coluna 23)
            linha = linha[:22] + "8" + linha[23:]

        linhas_saida.append(linha)

    # Junta o resultado final
    resultado = "\n".join(linhas_saida)

    # Botão para baixar
    st.download_button(
        "Baixar arquivo processado",
        resultado,
        file_name="Rep_Ref2.txt",
        mime="text/plain"
    )
