import streamlit as st
import requests
import json

URL_BASE = "https://entregas---motorista-kiko-default-rtdb.firebaseio.com/"

st.set_page_config(page_title="App Motorista - VUC", page_icon="🚚")
st.title("🚚 Minhas Entregas")

# Lista das 10 entregas (Você pode mudar os nomes aqui)
entregas_do_dia = [
    "Mercado Silva", "Auto Peças Norte", "Loja do Centro", 
    "Transportadora ABC", "Deposito Sul", "Oficina do Kiko",
    "Material de Construção", "Supermercado 24h", "Galpão 07", "Entrega Final"
]

def atualizar_status(id_e, cliente, status):
    dados = {"cliente": cliente, "status": status}
    requests.put(f"{URL_BASE}/entregas/{id_e:02d}.json", data=json.dumps(dados))

# Criando 10 botões organizados
for i, cliente in enumerate(entregas_do_dia, start=1):
    col_nome, col_btn = st.columns([3, 2])
    with col_nome:
        st.write(f"**Entrega #{i:02d}:** {cliente}")
    with col_btn:
        if st.button(f"Confirmar #{i:02d}", key=f"btn_{i}"):
            atualizar_status(i, cliente, "✅ Entregue")
            st.toast(f"Entrega {i} enviada!") # Um aviso rapidinho na tela