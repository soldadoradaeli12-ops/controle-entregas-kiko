import streamlit as st
import requests
import pandas as pd
import time

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

# --- CONFIGURAÇÃO DO BANCO ---
DB_URL = "https://api.jsonbin.io/v3/b/69ece496856a68218970575d"
HEADERS = {"X-Master-Key": "$2a$10$MUfpq2SfAKHcsLfMGJAigO.ieesITCNCewVMEfvXJf7B.S3a0ivaC"}

def buscar_dados():
    try:
        # O segredo: buscar sem cache para vir dado novo na hora
        response = requests.get(DB_URL, headers=HEADERS)
        return response.json().get("record", {}).get("entregas", [])
    except:
        return []

st.title("📊 Monitoramento de Frota - Iveco VUC")

# --- BOTÃO MANUAL (AGORA FUNCIONA NA HORA) ---
if st.button("🔄 Atualizar Dados Agora"):
    st.rerun()

# --- BUSCA DOS DADOS ---
entregas = buscar_dados()

if entregas:
    # CORREÇÃO AQUI: Agora ele procura o emoji verde 🟢
    concluidas = [e for e in entregas if "🟢" in str(e.get("status", ""))]
    
    total = len(entregas)
    qtd_concluidas = len(concluidas)
    
    st.write(f"### Progresso: {qtd_concluidas} / {total}")
    st.progress(qtd_concluidas / total)
    
    st.write("### Tabela de Status")
    df = pd.DataFrame(entregas)
    st.table(df) # table é mais rápido que dataframe comum
else:
    st.warning("⚠️ Banco de dados vazio ou erro de conexão.")

# --- ATUALIZAÇÃO AUTOMÁTICA (NO FINAL PARA NÃO TRAVAR) ---
st.info("⌛ O painel atualizará sozinho em 30 segundos...")
time.sleep(30)
st.rerun()
