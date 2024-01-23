
import streamlit as st
from st_aggrid import AgGrid
import st_aggrid as agg
import df_grid as grid
import controllers.Grupo_Aluno as controlGrupo_Aluno
import controllers.Grupo as controlGrupo
import controllers.Aluno as controlAluno
import models.Grupo_Aluno as Grupo_Aluno

st.subheader("Cadastrado de grupo aluno", divider="rainbow")
if  ('Nivel' not in st.session_state) or (st.session_state.Nivel == 0) or (st.session_state.Nivel > 1):
    st.switch_page("Home.py")
    
if  'sel_Grupo_Aluno' not in st.session_state:
     st.session_state['sel_Grupo_Aluno'] = 0

def btnNovoClick():
    st.session_state.sel_Grupo_Aluno = -1
    
if  st.session_state.sel_Grupo_Aluno == 0:
    df = grid.filter_dataframe(controlGrupo_Aluno.ListaGrupo_Aluno(None))
    builder = agg.GridOptionsBuilder.from_dataframe(df)
    #builder.configure_pagination(enabled=True)
    builder.configure_selection(selection_mode='single', use_checkbox=False)
    builder.configure_column('id', editable=False)
    grid_options = builder.build()

    return_value = AgGrid(df, gridOptions=grid_options, columns_auto_size_mode=agg.ColumnsAutoSizeMode.FIT_CONTENTS)
    
    st.button(label="Novo Grupo Aluno", type="primary", on_click=btnNovoClick)
    
    if return_value['selected_rows']:
        st.session_state.sel_Grupo_Aluno = return_value['selected_rows'][0]['id']
        st.rerun()
        
if  st.session_state.sel_Grupo_Aluno > 0:
    bVoltar = st.button(label="Voltar", type="primary")
    if  bVoltar:
        st.session_state.sel_Grupo_Aluno = 0
        st.rerun()

    with st.form(key="cad_Grupo_Aluno", border=True):
        dfalu = controlAluno.ListaAlunoF7()
        dfgrp = controlGrupo.ListaGrupo(None)
        retusr = controlGrupo_Aluno.ListaGrupo_Aluno(st.session_state.sel_Grupo_Aluno)
        
        idselalu = int(dfalu.loc[dfalu['Aluno'] == retusr.Aluno].index[0])
        selalu = st.selectbox(label="Aluno", options=dfalu.Aluno.unique(), index=idselalu)
        
        idselgrp = int(dfgrp.loc[dfgrp['Grupo'] == retusr.Grupo].index[0])
        selgrp = st.selectbox(label="Grupo", options=dfgrp.Grupo.unique(), index=idselgrp)
        
        col1, col2 = st.columns(2)
        bSalvar = col1.form_submit_button(label="Salvar", type="primary")
        bExcluir = col2.form_submit_button(label="Excluir", type="primary")
        
        if  bSalvar:
            for v in dfalu.loc[dfalu.Aluno == selalu, 'id']:
                idselalu = v
            for v in dfgrp.loc[dfgrp.Grupo == selgrp, 'id']:
                idselgrp = v
            controlGrupo_Aluno.AtualizaGrupo_Aluno(Grupo_Aluno.Grupo_Aluno(st.session_state.sel_Grupo_Aluno, 0, idselgrp, idselalu, None, None))
            st.session_state.sel_Grupo_Aluno = 0
            st.rerun()
            
        if  bExcluir:
            controlGrupo_Aluno.ApagaGrupo_Aluno(st.session_state.sel_Grupo_Aluno)
            st.session_state.sel_Grupo_Aluno = 0
            st.rerun()
        
if  st.session_state.sel_Grupo_Aluno == -1:
    bVoltar = st.button(label="Voltar", type="primary")
    if  bVoltar:
        st.session_state.sel_Grupo_Aluno = 0
        st.rerun()
    with st.form(key="cad_Grupo_Aluno", border=True):
        dfalu = controlAluno.ListaAlunoF7()
        dfgrp = controlGrupo.ListaGrupo(None)

        selalu = st.selectbox(label="Aluno", options=dfalu.Aluno.unique(), index=0)

        selgrp = st.selectbox(label="Grupo", options=dfgrp.Grupo.unique(), index=0)
        
        col1, col2 = st.columns(2)
        bSalvar = col1.form_submit_button(label="Salvar", type="primary")
        
        if  bSalvar:
            for v in dfalu.loc[dfalu.Aluno == selalu, 'id']:
                idselalu = v
            for v in dfgrp.loc[dfgrp.Grupo == selgrp, 'id']:
                idselgrp = v
            controlGrupo_Aluno.InsereGrupo_Aluno(Grupo_Aluno.Grupo_Aluno(0, 0, idselgrp, idselalu, None, None))
            st.session_state.sel_Grupo_Aluno = 0
            st.rerun()
            
    