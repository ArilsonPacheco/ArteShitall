
import streamlit as st
from st_aggrid import AgGrid
import st_aggrid as agg
import df_grid as grid
import controllers.categoria as controlCategoria
import models.Categoria as Ctg

st.subheader("Cadastrado de categoria", divider="rainbow")
if  ('Nivel' not in st.session_state) or (st.session_state.Nivel == 0) or (st.session_state.Nivel > 1):
    st.switch_page("Home.py")
    
if  'sel_categoria' not in st.session_state:
     st.session_state['sel_categoria'] = 0

if  'f7_categoria' not in st.session_state:
    st.session_state.f7_categoria = 0
    
def btnNovoClick():
    st.session_state.sel_categoria = -1
    
if  st.session_state.sel_categoria == 0:
    df = grid.filter_dataframe(controlCategoria.ListaCategoria(None))
    builder = agg.GridOptionsBuilder.from_dataframe(df)
    #builder.configure_pagination(enabled=True)
    builder.configure_selection(selection_mode='single', use_checkbox=False)
    builder.configure_column('id', editable=False)
    grid_options = builder.build()

    return_value = AgGrid(df, gridOptions=grid_options, columns_auto_size_mode=agg.ColumnsAutoSizeMode.FIT_CONTENTS)
    
    st.button(label="Nova Categoria", type="primary", on_click=btnNovoClick)
    
    if return_value['selected_rows']:
        st.session_state.sel_categoria = return_value['selected_rows'][0]['id']
        st.rerun()
        
if  st.session_state.sel_categoria > 0:
    bVoltar = st.button(label="Voltar", type="primary")
    if  bVoltar:
        st.session_state.sel_categoria = 0
        st.rerun()
    with st.form(key="cad_categoria", border=True):
        retusr = controlCategoria.ListaCategoria(st.session_state.sel_categoria)
        icategoria = st.text_input(label="Categoria", value=retusr.DS_Categoria)
        col1, col2 = st.columns(2)
        bSalvar = col1.form_submit_button(label="Salvar", type="primary")
        bExcluir = col2.form_submit_button(label="Excluir", type="primary")
        
        if  bSalvar:
            controlCategoria.AtualizaCategoria(Ctg.Categoria(st.session_state.sel_categoria, 0, icategoria))
            st.session_state.sel_categoria = 0
            st.rerun()
            
        if  bExcluir:
            controlCategoria.ApagaCategoria(st.session_state.sel_categoria)
            st.session_state.sel_categoria = 0
            st.rerun()

if  st.session_state.sel_categoria == -1:
    bVoltar = st.button(label="Voltar", type="primary")
    if  bVoltar:
        st.session_state.sel_categoria = 0
        st.rerun()
    with st.form(key="cad_usuario", border=True):
        icategoria = st.text_input(label="Categoria", value="")
        col1, col2 = st.columns(2)
        bSalvar = col1.form_submit_button(label="Salvar", type="primary")
        
        if  bSalvar:
            controlCategoria.InsereCategoria(Ctg.Categoria(0, 0, icategoria))
            st.session_state.sel_categoria = 0
            st.rerun()
    