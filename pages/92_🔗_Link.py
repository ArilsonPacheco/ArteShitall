import cryptocode
import streamlit as st
import urllib.parse as xurl
import controllers.Grupo as controlGrupo

st.set_page_config(page_title="ArteShitall - Link", page_icon=st.secrets.Logo1, initial_sidebar_state="expanded")

st.subheader(":link: Link", divider="rainbow")
if  ('Nivel' not in st.session_state) or (st.session_state.Nivel == 0) or (st.session_state.Nivel not in st.secrets.Nivel_y):
    st.switch_page("1_🏠_Home.py")
     
with st.form(key="pLink", border=True):
    dfgrp = controlGrupo.ListaGrupo(None)
    selgrp = st.selectbox(label="Grupo", options=dfgrp.Grupo.unique(), index=0)
    data = st.date_input(label="Data", format="DD/MM/YYYY")
    hora_i = st.time_input(label="Hora Inicial")
    hora_f = st.time_input(label="Hora Final")  

    col1, col2 = st.columns(2)
    
    bSalvar = col1.form_submit_button(label="Gerar Link", type="primary")
    if bSalvar:
       for v in dfgrp.loc[dfgrp.Grupo == selgrp, 'id']:
                idselgrp = v 
       link = f"{idselgrp};{data};{hora_i};{hora_f}"
       crp = cryptocode.encrypt(link, st.secrets.Chave_Link)
       #st.write(f"Link criptografado : :green[{crp}]")     
       #st.write(f"Link descriptografado : :green[{cryptocode.decrypt(crp, st.secrets.Chave_Link)}]")
      
       surl = xurl.urlencode({"link" : crp})
       link = f"https://dbarte.streamlit.app/Auto?{surl}" 
       st.write(f"Link : :green[{link}]")