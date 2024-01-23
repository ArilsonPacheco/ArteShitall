
import streamlit as st
from st_aggrid import AgGrid
import st_aggrid as agg
import df_grid as grid
import controllers.Grupo as controlGrupo
import models.Grupo as Grupo

st.subheader("Cadastrado de grupo", divider="rainbow")
if  ('Nivel' not in st.session_state) or (st.session_state.Nivel == 0) or (st.session_state.Nivel > 1):
    st.switch_page("Home.py")
    
if  'sel_grupo' not in st.session_state:
     st.session_state['sel_grupo'] = 0

def btnNovoClick():
    st.session_state.sel_grupo = -1
    
if  st.session_state.sel_grupo == 0:
    df = grid.filter_dataframe(controlGrupo.ListaGrupo(None))
    builder = agg.GridOptionsBuilder.from_dataframe(df)
    #builder.configure_pagination(enabled=True)
    builder.configure_selection(selection_mode='single', use_checkbox=False)
    builder.configure_column('id', editable=False)
    grid_options = builder.build()

    return_value = AgGrid(df, gridOptions=grid_options, columns_auto_size_mode=agg.ColumnsAutoSizeMode.FIT_CONTENTS)
    
    st.button(label="Novo Grupo", type="primary", on_click=btnNovoClick)
    
    if return_value['selected_rows']:
        st.session_state.sel_grupo = return_value['selected_rows'][0]['id']
        st.rerun()
        
if  st.session_state.sel_grupo > 0:
    bVoltar = st.button(label="Voltar", type="primary")
    if  bVoltar:
        st.session_state.sel_grupo = 0
        st.rerun()
    with st.form(key="cad_grupo", border=True):
        retusr = controlGrupo.ListaGrupo(st.session_state.sel_grupo)
        igrupo = st.text_input(label="Grupo", value=retusr.DS_Grupo)
        col1, col2 = st.columns(2)
        bSalvar = col1.form_submit_button(label="Salvar", type="primary")
        bExcluir = col2.form_submit_button(label="Excluir", type="primary")
        
        if  bSalvar:
            controlGrupo.AtualizaGrupo(Grupo.Grupo(st.session_state.sel_grupo, 0, igrupo))
            st.session_state.sel_grupo = 0
            st.rerun()
            
        if  bExcluir:
            controlGrupo.ApagaGrupo(st.session_state.sel_grupo)
            st.session_state.sel_grupo = 0
            st.rerun()

if  st.session_state.sel_grupo == -1:
    bVoltar = st.button(label="Voltar", type="primary")
    if  bVoltar:
        st.session_state.sel_grupo = 0
        st.rerun()
    with st.form(key="cad_grupo", border=True):
        igrupo = st.text_input(label="Grupo", value="")
        col1, col2 = st.columns(2)
        bSalvar = col1.form_submit_button(label="Salvar", type="primary")
        
        if  bSalvar:
            controlGrupo.InsereGrupo(Grupo.Grupo(0, 0, igrupo))
            st.session_state.sel_grupo = 0
            st.rerun()
    