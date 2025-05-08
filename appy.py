import streamlit as st
import base64  # Importe a biblioteca base64

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def dashboard():
    st.title("Dashboard")
    st.write("Conteúdo do Dashboard")

def mapeamento():
    st.title("Mapeamento de Obrigações")
    st.write("Formulário de Cadastro e Tabela de Obrigações")

def controle():
    st.title("Controle de Obrigações")
    st.write("Tabela Detalhada e Painel de Controle")

def cobranca():
    st.title("Cobrança")
    st.write("Régua de Cobrança")

def reporte():
    st.title("Reporte")
    st.write("Relatórios e Dashboards")

def configuracoes():
    st.title("Configurações")
    st.write("Gerenciamento de Usuários e Configurações Gerais")

def main():
    local_css("style.css")  # Carrega o CSS
    st.sidebar.title("Navegação")
    menu = ["Dashboard", "Mapeamento de Obrigações", "Controle de Obrigações", "Cobrança", "Reporte", "Configurações"]
    choice = st.sidebar.selectbox("Selecione a página", menu)

    if choice == "Dashboard":
        dashboard()
    elif choice == "Mapeamento de Obrigações":
        mapeamento()
    elif choice == "Controle de Obrigações":
        controle()
    elif choice == "Cobrança":
        cobranca()
    elif choice == "Reporte":
        reporte()
    elif choice == "Configurações":
        configuracoes()

if __name__ == "__main__":
    main()
