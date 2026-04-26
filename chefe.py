import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Painel Chefe", layout="wide")

# --- SISTEMA DE SENHA ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    senha = st.text_input("Senha:", type="password")
    if st.button("Entrar"):
        if senha == st.secrets["senha_chefe"]:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Erro!")
    st.stop()

# --- BANCO DE DADOS ---
DB_URL = "https://api.jsonbin.io/v3/b/69ed0a51856a68218970e577"
HEADERS = {"X-Master-Key": "$2a$10$MUfpq2SfAKHcsLfMGJAigO.ieesITCNCewVMEfvXJf7B.S3a0ivaC", "X-Bin-Meta": "false"}

def buscar_dados():
    try:
        response = requests.get(DB_URL, headers=HEADERS, timeout=10)
        return response.json().get("entregas", [])
    except:
        return []

st.title("📊 Painel Iveco VUC")

if st.button("🔄 Atualizar"):
    st.rerun()

entregas = buscar_dados()

# Trecho principal do chefe.py para contar as entregas
if entregas:
    # Ele verifica se o emoji verde existe em qualquer parte do status
    concluidas = [e for e in entregas if "🟢" in str(e.get("status", ""))]
    total = len(entregas)
    
    st.metric("Progresso Total", f"{len(concluidas)} / {total}")
    st.progress(len(concluidas) / total if total > 0 else 0)
    
    # Tabela com os dados reais
    st.table(pd.DataFrame(entregas))
else:
    st.warning("Aguardando dados...")
