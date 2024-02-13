
import streamlit as st
import df_grid as grid
import controllers.Grupo_Aluno as controlGrupo_Aluno
import controllers.Grupo as controlGrupo
import controllers.Aluno as controlAluno
import models.Grupo_Aluno as Grupo_Aluno

st.set_page_config(page_title="ArteShitall - Grupo Aluno", page_icon=st.secrets.Logo1, initial_sidebar_state="expanded")

st.subheader(":busts_in_silhouette: Cadastro de grupo aluno", divider="rainbow")
if  ('Nivel' not in st.session_state) or (st.session_state.Nivel == 0) or (st.session_state.Nivel not in st.secrets.Nivel_y):
    st.switch_page("1_🏠_Home.py")
    
if  'sel_Grupo_Aluno' not in st.session_state:
     st.session_state['sel_Grupo_Aluno'] = 0

def btnNovoClick():
    st.session_state.sel_Grupo_Aluno = -1
    
if  st.session_state.sel_Grupo_Aluno == 0:
    df = grid.filter_dataframe(controlGrupo_Aluno.ListaGrupo_Aluno(None))
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
        st.session_state.sel_Grupo_Aluno = fld.id
        st.rerun()
        
    st.button(label="Novo Grupo Aluno", type="primary", on_click=btnNovoClick)
        
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
            
    