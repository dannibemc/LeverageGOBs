# App de Gestão de Obrigações e Garantias (Streamlit)

Este pacote contém:
- `streamlit_obrigacoes_app.py`: Código principal da aplicação
- `usuarios_logs.db`: Banco de dados com usuários e histórico de ações
- `README.txt`: Este arquivo de instruções

## Como executar

1. Instale os requisitos (idealmente num ambiente virtual):
   pip install streamlit pandas matplotlib seaborn python-docx fpdf

2. Execute o app com:
   streamlit run streamlit_obrigacoes_app.py

3. Login padrão:
   - Usuário: admin
   - Senha: 1234

A aplicação gerencia obrigações e garantias, gera relatórios em PDF/Excel e permite controle de usuários com autenticação e logs.