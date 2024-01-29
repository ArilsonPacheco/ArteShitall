
import streamlit as st
import df_grid as grid
import controllers.usuario as controlUsuario
import models.Usuario as Usr

st.set_page_config(page_title="ArteShitall - Usuário", page_icon=st.secrets.Logo1, initial_sidebar_state="expanded")

st.subheader(":lock: Cadastrado de usuário", divider="rainbow")
if  ('Nivel' not in st.session_state) or (st.session_state.Nivel == 0) or (st.session_state.Nivel not in st.secrets.Nivel_x):
    st.switch_page("1_🏠_Home.py")
    
if  'sel_usuario' not in st.session_state:
     st.session_state['sel_usuario'] = 0

def btnNovoClick():
    st.session_state.sel_usuario = -1
    
if  st.session_state.sel_usuario == 0:
    df = grid.filter_dataframe(controlUsuario.ListaUsuario(None))
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)
                       },
        disabled=df.columns,
    )
    selected_rows = df[edited_df.Select]
    
    for fld in selected_rows.itertuples():
        st.session_state.sel_usuario = fld.id
        st.rerun()
        
    st.button(label="Novo Usuário", type="primary", on_click=btnNovoClick)
    
if  st.session_state.sel_usuario > 0:
    bVoltar = st.button(label="Voltar", type="primary")
    if  bVoltar:
        st.session_state.sel_usuario = 0
        st.rerun()
        
    with st.form(key="cad_usuario", border=True):
        retusr = controlUsuario.ListaUsuario(st.session_state.sel_usuario)
        inome = st.text_input(label="Usuário", value=retusr.NM_Usuario)
        ipass = st.text_input(label="Pass", value=retusr.DS_Pass)
        inivel = st.number_input(label="Nível", value=retusr.Nivel, format="%d", step=1)
        col1, col2 = st.columns(2)
        bSalvar = col1.form_submit_button(label="Salvar", type="primary")
        bExcluir = col2.form_submit_button(label="Excluir", type="primary")
        
        if  bSalvar:
            controlUsuario.AtualizaUsuario(Usr.Usuario(st.session_state['sel_usuario'], 0, inome, ipass, inivel))
            st.session_state.sel_usuario = 0
            st.rerun()
            
        if  bExcluir:
            controlUsuario.ApagaUsuario(st.session_state.sel_usuario)
            st.session_state.sel_usuario = 0
            st.rerun()

if  st.session_state.sel_usuario == -1:
    bVoltar = st.button(label="Voltar", type="primary")
    if  bVoltar:
        st.session_state.sel_usuario = 0
        st.rerun()
    with st.form(key="cad_usuario", border=True):
        inome = st.text_input(label="Usuário", value="")
        ipass = st.text_input(label="Pass", value="")
        inivel = st.number_input(label="Nível", value=0, format="%d", step=1)
        col1, col2 = st.columns(2)
        bSalvar = col1.form_submit_button(label="Salvar", type="primary")
        
        if  bSalvar:
            controlUsuario.InsereUsuario(Usr.Usuario(0, 0, inome, ipass, inivel))
            st.session_state.sel_usuario = 0
            st.rerun()
    