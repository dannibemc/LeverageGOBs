import streamlit as st
import base64
import pandas as pd
from datetime import datetime, timedelta
import time  # Importa a biblioteca time

# --- Configurações de Cores (Brandbook) ---
cor_primaria = "#343E83"
cor_secundaria = "#32BECB"
cor_accent = "#9E36EF"
cor_fundo_claro = "#FFFFFF"
cor_texto_claro = "#000000"
cor_fundo_escuro = "#1E1E1E"
cor_texto_escuro = "#FFFFFF"
cor_alerta = "#FF4B4B"
cor_sucesso = "#4CAF50"

# --- Configurações de Tipografia (Brandbook) ---
fonte_titulo = "Comfortaa"
fonte_texto = "Montserrat"
fonte_html = "Verdana"

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Lista para armazenar as obrigações (simulação de banco de dados)
if 'obrigações' not in st.session_state:
    st.session_state['obrigações'] = []
obrigações = st.session_state['obrigações']

obrigacao_selecionada_index = st.session_state.get('obrigacao_selecionada_index', None)
ordenar_por = st.session_state.get('ordenar_por', None)
direcao_ordem = st.session_state.get('direcao_ordem', "asc")

def aplicar_tema():
    st.markdown(f"""
        <style>
            :root {{
                --cor-primaria: {cor_primaria};
                --cor-secundaria: {cor_secundaria};
                --cor-accent: {cor_accent};
                --cor-fundo-claro: {cor_fundo_claro};
                --cor-texto-claro: {cor_texto_claro};
                --cor-fundo-escuro: {cor_fundo_escuro};
                --cor-texto-escuro: {cor_texto_escuro};
                --cor-alerta: {cor_alerta};
                --cor-sucesso: {cor_sucesso};
                --fonte-titulo: {fonte_titulo}, sans-serif;
                --fonte-texto: {fonte_texto}, sans-serif;
                --fonte-html: {fonte_html}, sans-serif;
            }}
            body {{
                font-family: var(--fonte-texto);
                color: var(--cor-texto-claro);
                background-color: var(--cor-fundo-claro);
            }}
            h1, h2, h3, h4, h5, h6 {{
                font-family: var(--fonte-titulo);
                color: var(--cor-primaria);
            }}
            .stButton>button {{
                background-color: var(--cor-secundaria);
                color: var(--cor-texto-claro);
                border-radius: 0.3rem;
                border: none;
                padding: 0.5rem 1rem;
                font-size: 1rem;
                cursor: pointer;
            }}
            .stButton>button:hover {{
                background-color: var(--cor-accent);
            }}
            .stTextInput>label, .stTextArea>label, .stDateInput>label, .stSelectbox>label, .stRadio>label, .stCheckbox>label {{
                color: var(--cor-primaria);
            }}
            .stDataFrame {{
                border: 1px solid var(--cor-primaria);
                border-radius: 0.3rem;
            }}
            .stDataFrame th {{
                background-color: var(--cor-primaria);
                color: var(--cor-texto-claro);
            }}
            .stDataFrame td {{
                border-bottom: 1px solid var(--cor-primaria);
            }}
            .streamlit-expanderHeader {{
                font-family: var(--fonte-titulo);
                color: var(--cor-primaria);
            }}
            .streamlit-expanderContent {{
                color: var(--cor-texto-claro);
            }}
            .stSuccess {{
                color: var(--cor-sucesso);
                background-color: #e6ffe6;
                padding: 0.8rem;
                border-radius: 0.3rem;
            }}
            .stInfo {{
                color: #17a2b8;
                background-color: #e0f7fa;
                padding: 0.8rem;
                border-radius: 0.3rem;
            }}
            .stWarning {{
                color: #ffc107;
                background-color: #fff3cd;
                padding: 0.8rem;
                border-radius: 0.3rem;
            }}
        </style>
    """, unsafe_allow_html=True)

def dashboard():
    st.title("Dashboard")
    st.write("Conteúdo do Dashboard")

def mapeamento():
    st.title("Mapeamento de Obrigações")

    with st.form("cadastro_obrigacao"):
        st.subheader("Cadastrar Nova Obrigação")

        col1, col2 = st.columns(2)  # Layout em colunas

        with col1:
            parte_devedora = st.text_input("Parte Devedora da Obrigação")
            documento_operacao = st.text_input("Documento da Operação")
            secao_clausula = st.text_input("Seção/Cláusula/Subcláusula/Item")

        with col2:
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
            st.session_state['obrigações'] = obrigações # Atualiza a session state
            st.success("Obrigação Cadastrada com Sucesso!")

    # Exibe a tabela de obrigações
    st.subheader("Obrigações Cadastradas")
    if obrigações:
        df_obrigações = pd.DataFrame(obrigações)
        df_obrigações["Detalhes"] = [f"Ver Detalhes {i}" for i in range(len(df_obrigações))]
        st.dataframe(df_obrigações, hide_index=True)

        for i, obrigacao in enumerate(obrigações):
            if st.button(f"Ver Detalhes {i}"):
                st.session_state['obrigacao_selecionada_index'] = i
    else:
        st.info("Nenhuma obrigação cadastrada ainda.")

def controle():
    st.title("Controle de Obrigações")

    global obrigacao_selecionada_index, ordenar_por, direcao_ordem

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
                    return 'color: var(--cor-alerta)'
                elif (prazo - hoje).days <= 7:
                    return 'color: orange'
            return ''

        df_estilo = df_obrigações.style.applymap(aplicar_estilo)
        st.dataframe(df_estilo, hide_index=True)

        # Ordenação
        def ao_clicar_no_cabecalho(coluna):
            if st.session_state.get('ordenar_por') == coluna:
                st.session_state['direcao_ordem'] = "desc" if st.session_state['direcao_ordem'] == "asc" else "asc"
            else:
                st.session_state['ordenar_por'] = coluna
                st.session_state['direcao_ordem'] = "asc"
            st.rerun()

        colunas_ordenaveis = ["Parte Devedora", "Documento", "Resumo", "Prazo", "Status"]
        colunas = st.columns(len(colunas_ordenaveis))
        for i, coluna in enumerate(colunas_ordenaveis):
            with colunas[i]:
                if st.button(coluna):
                    ao_clicar_no_cabecalho(coluna)

        if st.session_state.get('ordenar_por'):
            df_obrigações = df_obrigações.sort_values(by=st.session_state['ordenar_por'], ascending=(st.session_state['direcao_ordem'] == "asc"))
            st.dataframe(df_obrigações, hide_index=True) # Exibe a tabela ordenada novamente
    else:
        st.info("Nenhuma obrigação encontrada com os critérios selecionados.")

    # Detalhes da Obrigação
    if obrigacao_selecionada_index is not None and 0 <= obrigacao_selecionada_index < len(obrigações):
        obrigacao_selecionada = obrigações[obrigacao_selecionada_index]
        st.subheader("Detalhes da Obrigação")
        st.write(f"**Parte Devedora:** {obrigacao_selecionada['Parte Devedora']}")
        st.write(f"**Documento:** {obrigacao_selecionada['Documento']}")
        st.write(f"**Seção/Cláusula:** {obrigacao_selecionada['Seção/Cláusula']}")
        st.write(f"**Resumo:** {obrigacao_selecionada['Resumo']}")
        st.write(f"**Prazo:** {obrigacao_selecionada['Prazo']}")
        st.write(f"**Periodicidade:** {obrigacao_selecionada['Periodicidade']}")

        novo_status = st.selectbox("Status", ["Pendente", "Em Andamento", "Concluída", "Atrasada"], index=["Pendente", "Em Andamento", "Concluída", "Atrasada"].index(obrigacao_selecionada['Status']))
        if st.button("Salvar Status"):
            obrigações[obrigacao_selecionada_index]['Status'] = novo_status
            st.session_state['obrigações'] = obrigações # Atualiza a session state
            st.success("Status Atualizado!")
            st.session_state['obrigacao_selecionada_index'] = None # Limpa a seleção
            st.rerun()
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
            for i, obrigacao in enumerate(obrigações):
                data_vencimento = datetime.strptime(str(obrigacao["Prazo"]), '%Y-%m-%d').date()
                data_cobranca = calcular_data_cobranca(data_vencimento, detalhes["dias"])
                obrigacao_com_data = obrigacao.copy()
                obrigacao_com_data["Data " + etapa] = data_cobranca  # Adiciona a data à cópia da obrigação

                if (detalhes["dias"] < 0 and data_cobranca <= hoje) or \
                   (detalhes["dias"] > 0 and data_cobranca <= hoje and obrigacao["Status"] == "Atrasada") or \
                   (detalhes["dias"] == 2 and data_cobranca <= hoje and obrigacao["Status"] == "Em Andamento"):
                    obrigações_etapa.append(obrigacao_com_data)

            if obrigações_etapa:
                df_etapa = pd.DataFrame(obrigações_etapa)
                st.dataframe(df_etapa, hide_index=True)
            else:
                st.info(f"Nenhuma obrigação nesta etapa.")

# Funções para gerar relatórios
def gerar_relatorio_por_devedor(devedor):
    relatorio = [obrigacao for obrigacao in obrigações if obrigacao["Parte Devedora"] == devedor]
    return pd.DataFrame(relatorio)

def gerar_relatorio_por_status(status):
    relatorio = [obrigacao for obrigacao in obrigações if obrigacao["Status"] == status]
    return pd.DataFrame(relatorio)

def gerar_relatorio_por_periodo(data_inicio, data_fim):
    relatorio = [obrigacao for obrigacao in obrigações if data_inicio <= datetime.strptime(str(obrigacao["Prazo"]), '%Y-%m-%d').date() <= data_fim]
    return pd.DataFrame(relatorio)

def reporte():
    st.title("Reporte")
    st.header("Gerar Relatórios")

    tipo_relatorio = st.selectbox("Selecione o tipo de relatório", ["Por Devedor", "Por Status", "Por Período"])

    if tipo_relatorio == "Por Devedor":
        devedor = st.text_input("Devedor")
        if st.button("Gerar Relatório"):
            with st.spinner("Gerando Relatório..."): # Adiciona o spinner
                time.sleep(1) # Simula o tempo de geração
                relatorio = gerar_relatorio_por_devedor(devedor)
            st.dataframe(relatorio)
            if not relatorio.empty:
                nome_arquivo = f"relatorio_devedor_{devedor}.csv"
                st.download_button(label="Baixar CSV", data=relatorio.to_csv(index=False).encode('utf-8'), file_name=nome_arquivo, mime='text/csv')
            else:
                st.info("Nenhuma obrigação encontrada para este devedor.")

    elif tipo_relatorio == "Por Status":
        status = st.selectbox("Status", ["Pendente", "Em Andamento", "Concluída", "Atrasada"])
        if st.button("Gerar Relatório"):
            with st.spinner("Gerando Relatório..."): # Adiciona o spinner
                time.sleep(1) # Simula o tempo de geração
                relatorio = gerar_relatorio_por_status(status)
            st.dataframe(relatorio)
            if not relatorio.empty:
                nome_arquivo = f"relatorio_status_{status}.csv"
                st.download_button(label="Baixar CSV",
