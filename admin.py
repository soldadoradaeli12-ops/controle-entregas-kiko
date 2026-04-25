import streamlit as st
import requests

st.set_page_config(page_title="Cadastro de Entregas", layout="centered")

DB_URL = "https://api.jsonbin.io/v3/b/69ed0a51856a68218970e577"
HEADERS = {
    "X-Master-Key": "$2a$10$BGSSpcMjRoTr4mY4HBAK8.3UVE05u4mo.yp7BPz8CUE8dfT.nlILK",
    "Content-Type": "application/json"
}

st.title("📝 Preparar Entregas do Dia")

lista_bruta = st.text_area("Lista de Clientes/Locais:", height=200)

if st.button("🚀 Gerar e Salvar Nova Lista"):
    if lista_bruta:
        linhas = [linha.strip() for linha in lista_bruta.split('\n') if linha.strip()]
        novas_entregas = [{"id": str(i+1).zfill(2), "cliente": c, "status": "Pendente"} for i, c in enumerate(linhas)]
        
        try:
            response = requests.put(DB_URL, json={"entregas": novas_entregas}, headers=HEADERS)
            if response.status_code == 200:
                st.success("✅ Lista atualizada com sucesso!")
                st.balloons()
            else:
                st.error(f"Erro do Banco: {response.status_code}")
        except Exception as e:
            st.error(f"Erro de conexão: {e}")
