import streamlit as st
import requests

st.set_page_config(page_title="App Motorista - VUC", page_icon="🚚")

# Use EXATAMENTE o mesmo ID e Chave que deu certo no seu Admin
DB_URL = "https://api.jsonbin.io/v3/b/69ece496856a68218970575d"
HEADERS = {
    "X-Master-Key": "$2a$10$MUfpq2SfAKHcSLfMGJAigO.ieesITCNCewVMEfvXJf7B.S3a0ivaC",
    "X-Bin-Meta": "false"
}

st.title("🚚 Minhas Entregas")

# Busca as entregas que você cadastrou no Admin
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

# ... (mantenha o início igual ao da image_e0aa35.png)

# 1. Função para enviar a atualização para o banco
def confirmar_no_banco(lista_atualizada):
    requests.put(DB_URL, json={"entregas": lista_atualizada}, headers=HEADERS)

# 2. Lógica dos botões
for i, entrega in enumerate(entregas):
    col_nome, col_btn = st.columns([3, 2])
    with col_nome:
        status_atual = entrega.get('status', 'Pendente')
        st.write(f"**Entrega #{entrega['id']}:** {entrega['cliente']} ({status_atual})")
    
    with col_btn:
        # Só mostra o botão se ainda não foi entregue
        if status_atual == "Pendente":
            if st.button(f"Confirmar #{entrega['id']}", key=f"btn_{i}"):
                entregas[i]['status'] = "Entregue"  # Muda o status na lista
                confirmar_no_banco(entregas)        # Salva no JSONBin
                st.success("Enviado ao painel!")
                st.rerun()
            st.balloons()
