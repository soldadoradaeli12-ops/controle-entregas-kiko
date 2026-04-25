import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Painel Chefe", layout="wide")

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
DB_URL = "https://api.jsonbin.io/v3/b/69ed0a51856a68218970e577"
HEADERS = {"X-Master-Key": "$2a$10$MUfpq2SfAKHcsLfMGJAigO.ieesITCNCewVMEfvXJf7B.S3a0ivaC", "X-Bin-Meta": "false"}

def buscar_dados():
    try:
        response = requests.get(DB_URL, headers=HEADERS)
        if response.status_code == 200:
            # Puxa direto a lista de entregas
            return response.json().get("entregas", [])
        return []
    except:
        return []

st.title("📊 Monitoramento de Frota - Iveco VUC")

# --- BOTÃO MANUAL (COMO ESTAVA ANTES) ---
if st.button("🔄 Atualizar Dados Agora"):
    st.rerun()

# --- CARREGAMENTO E EXIBIÇÃO ---
entregas = buscar_dados()

if entregas:
    # CORREÇÃO DO FILTRO: Procura o emoji 🟢 que você colocou no app.py
    concluidas = [e for e in entregas if "🟢" in str(e.get("status", ""))]
    
    total = len(entregas)
    qtd_concluidas = len(concluidas)
    
    st.write(f"### Progresso: {qtd_concluidas} / {total}")
    st.progress(qtd_concluidas / total)
    
    st.write("### Tabela de Status")
    df = pd.DataFrame(entregas)
    st.table(df)
else:
    st.warning("⚠️ Aguardando dados do banco...")
