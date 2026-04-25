import streamlit as st
import requests
import pandas as pd
import time

# Faz o painel recarregar sozinho a cada 30 segundos
st.empty() 
if st.sidebar.checkbox("Ativar Atualização Automática", value=True):
    time.sleep(30)
    st.rerun()

st.set_page_config(page_title="Painel Chefe", layout="wide")

# Sistema de Senha (conforme sua imagem)
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

st.title("📊 Monitoramento de Frota - Iveco VUC")

DB_URL = "https://api.jsonbin.io/v3/b/69ed0a51856a68218970e577"
HEADERS = {"X-Master-Key": "$2a$10$BGSSpcMjRoTr4mY4HBAK8.3UVE05u4mo.yp7BPz8CUE8dfT.nlILK", "X-Bin-Meta": "false"}

def buscar_dados():
    response = requests.get(DB_URL, headers=HEADERS)
    return response.json().get("entregas", [])

try:
    entregas = buscar_dados()
    if entregas:
        concluidas = [e for e in entregas if e["status"] == "Entregue"]
        
        # Gráfico de Progresso
        progresso = len(concluidas) / len(entregas)
        st.write(f"### Progresso: {len(concluidas)} / {len(entregas)}")
        st.progress(progresso)
        
        # Tabela Geral
        st.write("### Tabela de Status")
        df = pd.DataFrame(entregas)
        st.table(df)
    else:
        st.info("Nenhuma entrega no banco.")
except:
    st.error("Erro ao carregar dados.")

if st.button("🔄 Atualizar Dados"):
    st.rerun()
