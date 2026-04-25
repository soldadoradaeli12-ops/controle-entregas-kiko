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

# Cria os botões para cada entrega da sua lista
for entrega in entregas:
    col_nome, col_btn = st.columns([3, 2])
    with col_nome:
        st.write(f"**Entrega #{entrega['id']}:** {entrega['cliente']}")
    
    with col_btn:
        # Se clicar, a gente atualiza o status no banco
        if st.button(f"Confirmar #{entrega['id']}", key=f"btn_{entrega['id']}"):
            # Aqui você pode adicionar a lógica para mudar para 'Entregue'
            st.success(f"Entrega {entrega['id']} confirmada!")
            st.balloons()
