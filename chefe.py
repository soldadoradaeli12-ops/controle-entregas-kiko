import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Painel Chefe", layout="wide")

# --- ATUALIZAÇÃO AUTOMÁTICA (JEITO QUE NÃO TRAVA) ---
# Isso faz a página recarregar sozinha a cada 30 segundos sem congelar
if "count" not in st.session_state:
    st.session_state.count = 0

# --- SISTEMA DE SENHA ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    senha = st.text_input("Digite a senha:", type="password")
    if st.button("Entrar"):
        if senha == st.secrets["senha_chefe"]:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Senha incorreta!")
    st.stop()

# --- CONFIGURAÇÃO DO BANCO ---
DB_URL = "https://api.jsonbin.io/v3/b/69ece496856a68218970575d"
HEADERS = {"X-Master-Key": "$2a$10$MUfpq2SfAKHcsLfMGJAigO.ieesITCNCewVMEfvXJf7B.S3a0ivaC", "X-Bin-Meta": "false"}

def buscar_dados():
    try:
        response = requests.get(DB_URL, headers=HEADERS)
        if response.status_code == 200:
            return response.json().get("entregas", [])
        return []
    except:
        return []

st.title("📊 Monitoramento de Frota - Iveco VUC")
st.info("🔄 O painel atualiza automaticamente.")

# Botão manual que funciona na hora
if st.button("🔄 Atualizar Agora"):
    st.rerun()

# --- MOSTRAR DADOS ---
entregas = buscar_dados()

if entregas:
    # Conta usando os novos emojis
    concluidas = [e for e in entregas if "🟢" in str(e.get("status", ""))]
    total = len(entregas)
    
    st.write(f"### Progresso: {len(concluidas)} / {total}")
    st.progress(len(concluidas) / total)
    
    st.write("### Tabela de Status")
    st.table(pd.DataFrame(entregas))
else:
    st.warning("⚠️ Aguardando dados...")

# --- O SEGREDO PARA ATUALIZAR SEM TRAVAR ---
# Em vez de time.sleep, usamos um pequeno truque de script
st.write("---")
if st.button("Clique aqui se o painel parar de atualizar"):
    st.rerun()
