import streamlit as st
import df_grid as grid
import controllers.Presenca as controlPresenca
import datetime as dt

st.set_page_config(page_title="ArteShitall - Dados Presença", page_icon=st.secrets.Logo1, initial_sidebar_state="expanded")

st.subheader(":ferris_wheel: Dados de presença", divider="rainbow")
if  ('Nivel' not in st.session_state) or (st.session_state.Nivel == 0) or (st.session_state.Nivel not in st.secrets.Nivel_z):
    st.switch_page("1_🏠_Home.py")

with st.form(key="Consulta", border=True):
    dti = st.date_input(label="Data Inicial", format="DD/MM/YYYY", value=dt.date(year=2024, month=1, day=1))
    dtf = st.date_input(label="Data Final", format="DD/MM/YYYY")
    col1, col2 = st.columns([0.4, 0.6])
    bConsultar = col2.form_submit_button(label="Consultar", type="primary")
    
    if  bConsultar:
        df = grid.filter_dataframe(controlPresenca.ConsultaPresenca(dti, dtf))
        st.dataframe(df)
