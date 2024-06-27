
import streamlit as st
import services.database as db
import controllers.login as controlLogin
import models.Usuario as Usuario

st.set_page_config(page_title="ArteShitall", page_icon=st.secrets.Logo1, initial_sidebar_state="expanded")

if 'Nivel' not in st.session_state:
    st.session_state['Nivel'] = 0

with st.sidebar:
    col1, col2 = st.columns([0.4, 0.6])
    col2.image(st.secrets.Logo1, width=50)
#st.logo(st.secrets.Logo1)

if  st.session_state.Nivel == 0:    
    login_form = st.form(key="login", border=True)
    login_form.image(st.secrets.Logo2)
    login_form.write(':earth_americas: www.arteshitall.com.br')
    lsuser = login_form.text_input(label="Usuário")
    lspass = login_form.text_input(label="Senha", type="password")
    col1, col2 = login_form.columns([0.4, 0.6])
    bEntrar = col2.form_submit_button(label="Entrar", type="primary")

    if  bEntrar:
        Nivel = controlLogin.Logar(Usuario.Usuario(0,0, lsuser, lspass, 0))
        if  Nivel:
            st.session_state.Nivel = Nivel
            st.rerun()
        else:
            st.error("Login incorreto!")

if  st.session_state.Nivel > 0:
    st.image(st.secrets.Logo2)
    st.write(':earth_americas: www.arteshitall.com.br')
    st.subheader(f":house: Você está logado com nível : {st.session_state.Nivel}", divider="rainbow")
    bLogin = st.button(label="Novo Login", type="primary")
    if  bLogin:
        st.session_state.Nivel = 0
        st.rerun()

          