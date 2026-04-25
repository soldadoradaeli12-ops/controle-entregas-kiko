import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Painel Chefe", layout="wide")

# --- SISTEMA DE SENHA ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    senha = st.text_input("Digite a senha para acessar o painel:", type="password")
    if st.button("Entrar"):
        if senha == st.secrets["senha_chefe"]:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Senha incorreta!")
    st.stop()
# ------------------------

st.title("📊 Monitoramento de Frota - Iveco VUC")

# URL do seu banco de dados (o mesmo do app.py)
DB_URL = "https://api.jsonbin.io/v3/b/69ece496856a68218970575d"
HEADERS = {"X-Master-Key": "$2a$10$MUfpq2SfAKHcSLfMGJAigO.ieesITCNCewVMEfvXJf7B.S3a0ivaC"}

def buscar_dados():
    response = requests.get(DB_URL, headers=HEADERS)
    return response.json()["record"]["entregas"]

def salvar_dados(entregas):
    requests.put(DB_URL, json={"entregas": entregas}, headers=HEADERS)

try:
    entregas = buscar_dados()
    concluidas = [e for e in entregas if e["status"] == "Entregue"]
    
    st.write(f"### Progresso das Entregas")
    progresso = len(concluidas) / len(entregas)
    st.progress(progresso)
    st.subheader(f"{len(concluidas)} / {len(entregas)}")

    st.write("### Tabela de Status")
    df = pd.DataFrame(concluidas)
    if not df.empty:
        st.table(df[["id", "cliente", "status"]])
    else:
        st.info("Nenhuma entrega concluída ainda.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Atualizar Dados"):
            st.rerun()
    with col2:
        if st.button("🗑️ LIMPAR DIA (Zerar Tudo)"):
            for e in entregas: e["status"] = "Pendente"
            salvar_dados(entregas)
            st.success("Dados resetados!")
            st.rerun()

except:
    st.info("Aguardando início das entregas... (Banco Vazio)")
