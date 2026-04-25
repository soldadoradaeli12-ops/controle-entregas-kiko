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

# --- TÍTULO E CONFIGURAÇÃO ---
st.title("📊 Monitoramento de Frota - Iveco VUC")

# URL e Headers do seu JSONBin
DB_URL = "https://api.jsonbin.io/v3/b/69ece496856a68218970575d"
HEADERS = {"X-Master-Key": "$2a$10$MUfpq2SfAKHcsLfMGJAigO.ieesITCNCewVMEfvXJf7B.S3a0ivaC"}

def buscar_dados():
    try:
        # Forçamos o request sem cache para garantir dados novos
        response = requests.get(DB_URL, headers=HEADERS)
        return response.json().get("record", {}).get("entregas", [])
    except:
        return []

# --- BOTÃO DE ATUALIZAÇÃO MANUAL ---
# Colocamos o botão ANTES de buscar os dados. O rerun fará o script recomeçar e buscar os dados novos.
if st.button("🔄 Atualizar Agora"):
    st.rerun()

# --- CARREGAMENTO DOS DADOS ---
entregas = buscar_dados()

if entregas:
    # Filtro corrigido para os novos status com emojis
    concluidas = [e for e in entregas if "🟢" in str(e.get("status", ""))]
    
    total = len(entregas)
    quantidade_concluidas = len(concluidas)
    
    progresso = quantidade_concluidas / total
    st.write(f"### Progresso das Entregas: {quantidade_concluidas} / {total}")
    st.progress(progresso)
    
    st.write("### Detalhes do Status")
    df = pd.DataFrame(entregas)
    st.table(df)
else:
    st.warning("⚠️ Aguardando início das entregas ou banco de dados vazio.")

# --- ATUALIZAÇÃO AUTOMÁTICA (JEITO CORRETO) ---
# Colocamos a espera no final para não travar a visualização inicial
st.info("⌛ Próxima atualização automática em 30 segundos...")
time.sleep(30)
st.rerun()
