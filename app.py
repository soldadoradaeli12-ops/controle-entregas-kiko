import streamlit as st
import requests

st.set_page_config(page_title="App Motorista - VUC", page_icon="🚚")

DB_URL = "https://api.jsonbin.io/v3/b/69ed0a51856a68218970e577"
# Adicionei o Content-Type para permitir que você salve a confirmação
HEADERS = {
    "X-Master-Key": "$2a$10$BGSSpcMjRoTr4mY4HBAK8.3UVE05u4mo.yp7BPz8CUE8dfT.nlILK",
    "Content-Type": "application/json",
    "X-Bin-Meta": "false"
}

st.title("🚚 Minhas Entregas")

try:
    response = requests.get(DB_URL, headers=HEADERS)
    if response.status_code == 200:
        entregas = response.json().get("entregas", [])
    else:
        st.error("Erro ao carregar entregas.")
        entregas = []
except:
    st.error("Erro de conexão.")
    entregas = []

if not entregas:
    st.warning("Nenhuma entrega cadastrada para hoje.")

def confirmar_no_banco(lista_atualizada):
    requests.put(DB_URL, json={"entregas": lista_atualizada}, headers=HEADERS)

for i, entrega in enumerate(entregas):
    col_nome, col_btn = st.columns([3, 2])
    status_atual = entrega.get('status', 'Pendente')
    
    with col_nome:
        st.write(f"**Entrega #{entrega['id']}:** {entrega['cliente']} ({status_atual})")
    
    with col_btn:
            # Só mostra o botão se ainda não foi entregue
            # Alteramos para reconhecer o emoji que vem do admin.py
            if status_atual == "🔴 Pendente": 
                if st.button(f"Confirmar #{entrega['id']}", key=f"btn_{i}"):
                    # Aqui salvamos com o emoji verde para o chefe conseguir contar
                    entregas[i]['status'] = "🟢 Entregue" 
                    confirmar_no_banco(entregas)
                    st.success("Enviado ao painel!")
                    st.rerun()
