import streamlit as st
import base64
import pandas as pd
from datetime import datetime, timedelta

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Lista para armazenar as obrigações
obrigações = []
obrigacao_selecionada = None
ordenar_por = None
direcao_ordem = "asc"

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
            nova_obrigacao = {
                "Parte Devedora": parte_devedora,
                "Documento": documento_operacao,
                "Seção/Cláusula": secao_clausula,
                "Resumo": resumo_obrigacao,
                "Prazo": prazo,
                "Periodicidade": tipo_periodicidade,
                "Status": "Pendente"
            }
            obrigações.append(nova_obrigacao)
            st.success("Obrigação Cadastrada com Sucesso!")

    # Exibe a tabela de obrigações
    st.subheader("Obrigações Cadastradas")
    if obrigações:
        df_obrigações = pd.DataFrame(obrigações)
        df_obrigações["Detalhes"] = [f"Ver Detalhes {i}" for i in range(len(df_obrigações))]
        st.dataframe(df_obrigações, hide_index=True)

        global obrigacao_selecionada
        for i, obrigacao in enumerate(obrigações):
            if st.button(f"Ver Detalhes {i}"):
                obrigacao_selecionada = obrigacao
    else:
        st.info("Nenhuma obrigação cadastrada ainda.")

def controle():
    st.title("Controle de Obrigações")

    global obrigacao_selecionada, ordenar_por, direcao_ordem

    termo_busca = st.text_input("Buscar Obrigações", "")
    status_selecionado = st.selectbox("Filtrar por Status", ["Todos", "Pendente", "Em Andamento", "Concluída", "Atrasada"])

    obrigações_filtradas = []
    hoje = datetime.now().date()
    for obrigacao in obrigações:
        if termo_busca.lower() in " ".join(str(v) for v in obrigacao.values()).lower():
            if status_selecionado == "Todos" or obrigacao["Status"] == status_selecionado:
                obrigações_filtradas.append(obrigacao)

    if obrigações_filtradas:
        df_obrigações = pd.DataFrame(obrigações_filtradas)

        # Alertas Visuais
        def aplicar_estilo(valor, coluna):
            if coluna == "Prazo":
                prazo = datetime.strptime(str(valor), '%Y-%m-%d').date()
                if prazo < hoje:
                    return 'color: red'
                elif (prazo - hoje).days <= 7:
                    return 'color: orange'
            return ''

        df_estilo = df_obrigações.style.applymap(aplicar_estilo)
        st.dataframe(df_estilo, hide_index=True)

        # Ordenação
        def ao_clicar_no_cabecalho(coluna):
            global ordenar_por, direcao_ordem
            if ordenar_por == coluna:
                direcao_ordem = "desc" if direcao_ordem == "asc" else "asc"
            else:
                ordenar_por = coluna
                direcao_ordem = "asc"

        colunas_ordenaveis = ["Parte Devedora", "Documento", "Resumo", "Prazo", "Status"]
        colunas = st.columns(len(colunas_ordenaveis))
        for i, coluna in enumerate(colunas_ordenaveis):
            with colunas[i]:
                if st.button(coluna):
                    ao_clicar_no_cabecalho(coluna)

        if ordenar_por:
            df_obrigações = df_obrigações.sort_values(by=ordenar_por, ascending=(direcao_ordem == "asc"))
    else:
        st.info("Nenhuma obrigação encontrada com os critérios selecionados.")

    # Detalhes da Obrigação
    if obrigacao_selecionada:
        st.subheader("Detalhes da Obrigação")
        st.write(f"Parte Devedora: {obrigacao_selecionada['Parte Devedora']}")
        st.write(f"Documento: {obrigacao_selecionada['Documento']}")
        st.write(f"Seção/Cláusula: {obrigacao_selecionada['Seção/Cláusula']}")
        st.write(f"Resumo: {obrigacao_selecionada['Resumo']}")
        st.write(f"Prazo: {obrigacao_selecionada['Prazo']}")
        st.write(f"Periodicidade: {obrigacao_selecionada['Periodicidade']}")

        novo_status = st.selectbox("Status", ["Pendente", "Em Andamento", "Concluída", "Atrasada"])
        if st.button("Salvar Status"):
            for obrigacao in obrigações:
                if obrigacao["Documento"] == obrigacao_selecionada["Documento"] and obrigacao["Resumo"] == obrigacao_selecionada["Resumo"]:
                    obrigacao["Status"] = novo_status
                    break
            st.success("Status Atualizado!")
            obrigacao_selecionada = None
    else:
        st.info("Selecione uma obrigação para ver os detalhes.")

# Régua de Cobrança
regua_cobranca = {
    "Lembrete": {"dias": -30, "acao": "Enviar Lembrete"},
    "Primeira Cobrança": {"dias": 2, "acao": "Cobrança por E-mail + Reporte"},
    "Notificação Jurídica": {"dias": 2 + 7, "acao": "Notificação Jurídica"},
    "Ação Judicial": {"dias": 2 + 7 + 15, "acao": "Ação Judicial"}
}

# Funções para calcular as datas de cobrança
def calcular_data_cobranca(data_vencimento, dias):
    return data_vencimento + timedelta(days=dias)

def cobranca():
    st.title("Cobrança")
    st.header("Régua de Cobrança")

    hoje = datetime.now().date()

    for etapa, detalhes in regua_cobranca.items():
        with st.expander(etapa):
            st.write(f"**{etapa}:** {detalhes['acao']}")
            st.write(f"**Dias após o vencimento:** {detalhes['dias']} dias")

            obrigações_etapa = []
            for obrigacao in obrigações:
                data_vencimento = datetime.strptime(str(obrigacao["Prazo"]), '%Y-%m-%d').date()
                data_cobranca = calcular_data_cobranca(data_vencimento, detalhes["dias"])
                obrigacao["Data " + etapa] = data_cobranca  # Adiciona a data à obrigação

                if (detalhes["dias"] < 0 and data_cobranca <= hoje) or \
                   (detalhes["dias"] > 0 and data_cobranca <= hoje and obrigacao["Status"] == "Atrasada") or \
                   (detalhes["dias"] == 2 and data_cobranca <= hoje and obrigacao["Status"] == "Em Andamento"):
                    obrigações_etapa.append(obrigacao)

            if obrigações_etapa:
                df_etapa = pd.DataFrame(obrigações_etapa)
                st.dataframe(df_etapa, hide_index=True)
            else:
                st.info(f"Nenhuma obrigação nesta etapa.")


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
