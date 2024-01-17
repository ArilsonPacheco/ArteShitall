
import streamlit as st
from st_aggrid import AgGrid
import st_aggrid as agg
import df_grid as grid
import controllers.usuario as controlUsuario
import models.Usuario as Usr

if  ('Nivel' not in st.session_state) or (st.session_state.Nivel == 0) or (st.session_state.Nivel > 1):
    st.switch_page("Home.py")
    
if  'sel_usuario' not in st.session_state:
     st.session_state['sel_usuario'] = 0

def btnNovoClick():
    st.session_state['sel_usuario'] = -1
    
if  st.session_state['sel_usuario'] == 0:
    df = grid.filter_dataframe(controlUsuario.ListaUsuario(None))
    builder = agg.GridOptionsBuilder.from_dataframe(df)
    #builder.configure_pagination(enabled=True)
    builder.configure_selection(selection_mode='single', use_checkbox=False)
    builder.configure_column('id', editable=False)
    grid_options = builder.build()

    return_value = AgGrid(df, gridOptions=grid_options, columns_auto_size_mode=agg.ColumnsAutoSizeMode.FIT_CONTENTS)
    
    st.button(label="Novo Usuário", type="primary", on_click=btnNovoClick)
    
    if return_value['selected_rows']:
        st.session_state['sel_usuario'] = return_value['selected_rows'][0]['id']
        st.rerun()
        
if  st.session_state['sel_usuario'] > 0:
    with st.form(key="cad_usuario", border=True):
        retusr = controlUsuario.ListaUsuario(st.session_state['sel_usuario'])
        inome = st.text_input(label="Usuário", value=retusr.NM_Usuario)
        ipass = st.text_input(label="Pass", value=retusr.DS_Pass)
        inivel = st.number_input(label="Nível", value=retusr.Nivel, format="%d", step=1)
        col1, col2 = st.columns(2)
        bSalvar = col1.form_submit_button(label="Salvar", type="primary")
        bExcluir = col2.form_submit_button(label="Excluir", type="primary")
        
        if  bSalvar:
            controlUsuario.AtualizaUsuario(Usr.Usuario(st.session_state['sel_usuario'], 0, inome, ipass, inivel))
            st.session_state['sel_usuario'] = 0
            st.rerun()
            
        if  bExcluir:
            controlUsuario.ApagaUsuario(st.session_state.sel_usuario)
            st.session_state.sel_usuario = 0;
            st.rerun()

if  st.session_state['sel_usuario'] == -1:
    with st.form(key="cad_usuario", border=True):
        inome = st.text_input(label="Usuário", value="")
        ipass = st.text_input(label="Pass", value="")
        inivel = st.number_input(label="Nível", value=0, format="%d", step=1)
        col1, col2 = st.columns(2)
        bSalvar = col1.form_submit_button(label="Salvar", type="primary")
        
        if  bSalvar:
            controlUsuario.InsereUsuario(Usr.Usuario(0, 0, inome, ipass, inivel))
            st.session_state['sel_usuario'] = 0
            st.rerun()
    