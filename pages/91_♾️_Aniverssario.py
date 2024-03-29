import streamlit as st
import df_grid as grid
import controllers.Aluno as controlAluno


st.set_page_config(page_title="ArteShitall - Aniverssário", page_icon=st.secrets.Logo1, initial_sidebar_state="expanded")

st.subheader(":infinity: Lista de Aniverssário", divider="rainbow")
if  ('Nivel' not in st.session_state) or (st.session_state.Nivel == 0) or (st.session_state.Nivel not in st.secrets.Nivel_y):
    st.switch_page("1_🏠_Home.py")

with st.form(key="cad_Aluno", border=True):
    mes = st.number_input("Mês do Aniverssário", min_value=1, max_value=12, value=1)
    col1, col2 = st.columns([0.4, 0.6])
    bConsulta = col2.form_submit_button(label="Consultar", type="primary")
    if  bConsulta:
        df = controlAluno.ListaAniverssario(mes)
        st.data_editor(df,column_config={"Data Nasc.": st.column_config.DateColumn(format="DD/MM/YYYY"),
                    "Data Cadastro": st.column_config.DateColumn(format="DD/MM/YYYY")
                    }, hide_index=True, use_container_width=True,
                    disabled=df.columns)
