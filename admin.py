import streamlit as st
import requests

st.set_page_config(page_title="Cadastro de Entregas", layout="centered")

# Verifique se esse ID (67bd...) é o mesmo que aparece no seu JSONBin
DB_URL = "https://api.jsonbin.io/v3/b/67bdc657ad19ca34f8115598"
HEADERS = {
    "X-Master-Key": "$2b$10$f06u9Lp29R09/X.Y8K8R0.H9U3j8G7j6K5L4M3N2O1P0Q9R8S7T6",
    "Content-Type": "application/json"
}

st.title("📝 Preparar Entregas do Dia")

lista_bruta = st.text_area("Lista de Clientes/Locais:", height=200)

if st.button("🚀 Gerar e Salvar Nova Lista"):
    if lista_bruta:
        linhas = [linha.strip() for linha in lista_bruta.split('\n') if linha.strip()]
        novas_entregas = [{"id": str(i+1).zfill(2), "cliente": c, "status": "Pendente"} for i, c in enumerate(linhas)]
        
        # Tentativa de salvamento
        try:
            response = requests.put(DB_URL, json={"entregas": novas_entregas}, headers=HEADERS)
            if response.status_code == 200:
                st.success("✅ Lista atualizada com sucesso!")
                st.balloons()
            else:
                # Isso vai nos mostrar o erro real do site
                st.error(f"Erro do Banco: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Erro de conexão: {e}")
