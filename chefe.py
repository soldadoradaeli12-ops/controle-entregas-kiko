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

# --- TÍTULO E INFORMAÇÃO ---
st.title("📊 Monitoramento de Frota - Iveco VUC")
st.info("🔄 O painel atualiza automaticamente a cada 30 segundos.")

# --- CONFIGURAÇÃO DO BANCO ---
DB_URL = "https://api.jsonbin.io/v3/b/69ece496856a68218970575d"
HEADERS = {"X-Master-Key": "$2a$10$MUfpq2SfAKHcsLfMGJAigO.ieesITCNCewVMEfvXJf7B.S3a0ivaC"}

def buscar_dados():
    try:
        response = requests.get(DB_URL, headers=HEADERS)
        # O JSONBin retorna os dados dentro da chave 'record'
        return response.json().get("record", {}).get("entregas", [])
    except:
        return []

# --- CARREGAMENTO E EXIBIÇÃO ---
entregas = buscar_dados()

if entregas:
    # Conta apenas as entregas que contêm o emoji verde
    concluidas = [e for e in entregas if "🟢" in e.get("status", "")]
    
    total = len(entregas)
    quantidade_concluidas = len(concluidas)
    
    # Gráfico de progresso
    progresso = quantidade_concluidas / total
    st.write(f"### Progresso das Entregas: {quantidade_concluidas} / {total}")
    st.progress(progresso)
    
    # Tabela com os dados
    st.write("### Detalhes do Status")
    df = pd.DataFrame(entregas)
    # Remove a coluna de índice para ficar mais limpo
    st.table(df)
else:
    st.warning("⚠️ Aguardando início das entregas ou banco de dados vazio.")

if st.button("🔄 Atualizar Agora"):
    st.rerun()

# --- ATUALIZAÇÃO AUTOMÁTICA (FINAL DO CÓDIGO) ---
# Ele espera 30 segundos e reinicia a rodagem do script
time.sleep(30)
st.rerun()
