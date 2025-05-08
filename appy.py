import streamlit as st
import base64
import pandas as pd  # Importe a biblioteca pandas

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Lista para armazenar as obrigações
obrigações = []

def dashboard():
    st.title("Dashboard")
    st.write("Conteúdo do Dashboard")

def mapeamento():
    st.title("Mapeamento de Obrigações")

    with st.form("cadastro_obrigacao"):
        st.subheader("Cadastrar Nova Obrigação")

        parte_devedora = st.text_input("Parte Devedora da Obrigação")
        documento_operacao = st.text_input("Documento da Operação")
        secao_clausula = st.text_input("Seção/Cláusula/Subcláusula/Item")
        resumo_obrigacao = st.text_area("Resumo da Obrigação")
        prazo = st.date_input("Prazo")
        tipo_periodicidade = st.selectbox("Tipo de Periodicidade", ["Única", "Diária", "Semanal", "Mensal", "Anual"])

        submit_button = st.form_submit_button("Cadastrar")

        if submit_button:
            # Adiciona a obrigação à lista
            nova_obrigacao = {
                "Parte Devedora": parte_devedora,
                "Documento": documento_operacao,
                "Seção/Cláusula": secao_clausula,
                "Resumo": resumo_obrigacao,
                "Prazo": prazo,
                "Periodicidade": tipo_periodicidade
            }
            obrigações.append(nova_obrigacao)
            st.success("Obrigação Cadastrada com Sucesso!")

    # Exibe a tabela de obrigações
    st.subheader("Obrigações Cadastradas")
    if obrigações:
        df_obrigações = pd.DataFrame(obrigações)
        st.dataframe(df_obrigações)
    else:
        st.info("Nenhuma obrigação cadastrada ainda.")


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
    local_css("style.css")
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
