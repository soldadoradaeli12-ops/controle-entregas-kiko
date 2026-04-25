import streamlit as st
import requests

st.set_page_config(page_title="Cadastro de Entregas", layout="centered")

DB_URL = "https://api.jsonbin.io/v3/b/67bdc657ad19ca34f8115598"
HEADERS = {"X-Master-Key": "$2b$10$f06u9Lp29R09/X.Y8K8R0.H9U3j8G7j6K5L4M3N2O1P0Q9R8S7T6", "Content-Type": "application/json"}

st.title("📝 Preparar Entregas do Dia")

st.info("Dica: Cole a lista de clientes abaixo, um por linha.")

# Caixa de texto para colar a lista
lista_bruta = st.text_area("Lista de Clientes/Locais:", height=200, placeholder="Exemplo:\nMercado Silva\nAuto Peças Norte\nPadaria Central")

if st.button("🚀 Gerar e Salvar Nova Lista"):
    if lista_bruta:
        linhas = [linha.strip() for linha in lista_bruta.split('\n') if linha.strip()]
        novas_entregas = []
        
        for i, cliente in enumerate(linhas):
            id_entrega = str(i + 1).zfill(2)
            novas_entregas.append({"id": id_entrega, "cliente": cliente, "status": "Pendente"})
        
        # Envia para o banco de dados
        response = requests.put(DB_URL, json={"entregas": novas_entregas}, headers=HEADERS)
        
        if response.status_code == 200:
            st.success(f"✅ Sucesso! {len(novas_entregas)} entregas cadastradas para hoje.")
            st.balloons()
        else:
            st.error("Erro ao salvar no banco de dados.")
    else:
        st.warning("A lista está vazia!")
