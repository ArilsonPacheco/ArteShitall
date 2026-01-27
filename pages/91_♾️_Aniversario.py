import streamlit as st
import df_grid as grid
import controllers.Aluno as controlAluno
import datetime as dt


st.set_page_config(page_title="ArteShitall - Aniverssário", page_icon=st.secrets.Logo1, initial_sidebar_state="expanded")

st.subheader(":infinity: Lista de Aniversário", divider="rainbow")
if  ('Nivel' not in st.session_state) or (st.session_state.Nivel == 0) or (st.session_state.Nivel not in st.secrets.Nivel_y):
    st.switch_page("1_🏠_Home.py")

with st.form(key="cad_Aluno", border=True):
    hoje = int(dt.datetime.now().strftime("%m"))
    desc_mes = dt.datetime.now().strftime("%d/%m/%Y")
    mes = st.number_input(f"Mês do Aniverssário? [ hoje é {desc_mes} ]", min_value=1, max_value=12, value=hoje)
    col1, col2 = st.columns([0.4, 0.6])
    bConsulta = col2.form_submit_button(label="Consultar", type="primary")
    if  bConsulta:
        df = controlAluno.ListaAniverssario(mes)
        st.data_editor(df,column_config={"Data Nasc.": st.column_config.DateColumn(format="DD/MM/YYYY"),
                    "Data Cadastro": st.column_config.DateColumn(format="DD/MM/YYYY")
                    }, hide_index=True, width='stretch',
                    disabled=df.columns)
