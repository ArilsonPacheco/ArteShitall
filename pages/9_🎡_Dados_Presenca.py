import streamlit as st
import controllers.Grupo as controlGrupo
import controllers.Presenca as controlPresenca
import datetime as dt

st.set_page_config(page_title="ArteShitall - Dados Presença", page_icon=st.secrets.Logo1, initial_sidebar_state="expanded")

st.subheader(":ferris_wheel: Dados de presença", divider="rainbow")
if  ('Nivel' not in st.session_state) or (st.session_state.Nivel == 0) or (st.session_state.Nivel not in st.secrets.Nivel_z):
    st.switch_page("1_🏠_Home.py")

with st.form(key="Consulta", border=True):
    dti = st.date_input(label="Data Inicial", format="DD/MM/YYYY", value=dt.date(year=2024, month=1, day=1))
    dtf = st.date_input(label="Data Final", format="DD/MM/YYYY")
    dfgrp = controlGrupo.ListaGrupo(None)
    selgrp = st.selectbox(label="Grupo", options=dfgrp.Grupo.unique(), index=0)

    col1, col2 = st.columns([0.4, 0.6])
    bConsultar = col2.form_submit_button(label="Consultar", type="primary")
    
    if  bConsultar:
        for v in dfgrp.loc[dfgrp.Grupo == selgrp, 'id']:
            idselgrp = v
        df = controlPresenca.ConsultaPresenca(dti, dtf, idselgrp)
        st.dataframe(df)
