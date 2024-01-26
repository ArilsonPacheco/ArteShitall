
import streamlit as st
import df_grid as grid
import controllers.Grupo as controlGrupo
import models.Grupo as Grupo

st.set_page_config(page_title="ArteShitall - Grupo", page_icon=st.secrets.Logo1, initial_sidebar_state="expanded")

st.subheader("Cadastrado de grupo", divider="rainbow")
if  ('Nivel' not in st.session_state) or (st.session_state.Nivel == 0) or (st.session_state.Nivel not in st.secrets.Nivel_y):
    st.switch_page("Home.py")
    
if  'sel_grupo' not in st.session_state:
     st.session_state['sel_grupo'] = 0

def btnNovoClick():
    st.session_state.sel_grupo = -1
    
if  st.session_state.sel_grupo == 0:
    df = grid.filter_dataframe(controlGrupo.ListaGrupo(None))
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
        st.session_state.sel_grupo = fld.id
        st.rerun()
    
    st.button(label="Novo Grupo", type="primary", on_click=btnNovoClick)
            
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
    