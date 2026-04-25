import streamlit as st
import requests
import pandas as pd

URL_BASE = "https://entregas---motorista-kiko-default-rtdb.firebaseio.com/"

st.set_page_config(page_title="Painel Chefe", page_icon="📊", layout="wide")
st.title("📊 Monitoramento de Frota - Iveco VUC")

# --- FUNÇÃO PARA LIMPAR O BANCO ---
def limpar_entregas():
    requests.delete(f"{URL_BASE}/entregas.json")
    st.success("O dia foi zerado com sucesso!")

# Busca dados
response = requests.get(f"{URL_BASE}/entregas.json")
dados_fb = response.json()

if dados_fb:
    lista = [{"ID": k, "Cliente": v['cliente'], "Status": v['status']} for k, v in dados_fb.items()]
    df = pd.DataFrame(lista).sort_values("ID")
    
    total = 10 
    concluidas = len(df[df["Status"] == "✅ Entregue"])
    
    st.metric("Progresso das Entregas", f"{concluidas} / {total}")
    st.progress(concluidas / total)
    
    st.write("### Tabela de Status")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Aguardando início das entregas... (Banco Vazio)")

# --- BOTÕES DE CONTROLE ---
st.divider() # Cria uma linha divisória
col_att, col_limpar = st.columns(2)

with col_att:
    if st.button("🔄 Atualizar Dados"):
        st.rerun()

with col_limpar:
    if st.button("🗑️ LIMPAR DIA (Zerar Tudo)"):
        limpar_entregas()
        st.rerun()