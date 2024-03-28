
import streamlit as st
import controllers.Presenca as controlPresenca
import controllers.Grupo as controlGrupo
import controllers.Aluno as controlAluno
import models.Presenca as Presenca

st.set_page_config(page_title="ArteShitall - Presença", page_icon=st.secrets.Logo1, initial_sidebar_state="expanded")

st.subheader(":ballot_box_with_check: Lista de presença", divider="rainbow")
if  ('Nivel' not in st.session_state) or (st.session_state.Nivel == 0) or (st.session_state.Nivel not in st.secrets.Nivel_z):
    st.switch_page("1_🏠_Home.py")
    
if  'sel_Presenca' not in st.session_state:
     st.session_state['sel_Presenca'] = -2

if  'sel_fltData' not in st.session_state:
     st.session_state['sel_fltData'] = 0

if  'sel_fltGrp' not in st.session_state:
     st.session_state['sel_fltGrp'] = 0

if  'sel_DesGrp' not in st.session_state:
     st.session_state['sel_DesGrp'] = ""
     
if  st.session_state.sel_Presenca == -2:
    with st.form(key="pre_filtro", border=True):
        st.write("* Filtra data e grupo da presença")
        st.write("* Cria lista de presença")
        st.write("---")
        dfgrp = controlGrupo.ListaGrupo(None)
        selgrp = st.selectbox(label="Grupo", options=dfgrp.Grupo.unique(), index=0)
        idata = st.date_input(label="Data", value="today", format="DD/MM/YYYY")
        col1, col2, col3 = st.columns(3)
        bFiltrar = col1.form_submit_button(label="Fitrar", type="primary")
        bCriarLista = col2.form_submit_button(label="Cria Listar", type="primary")
        bExcluirLista = col3.form_submit_button(label="Excluir Listar", type="primary")
        
        if  bFiltrar or bCriarLista or bExcluirLista:
            for v in dfgrp.loc[dfgrp.Grupo == selgrp, 'id']:
                idselgrp = v
            st.session_state.sel_fltGrp = idselgrp
            st.session_state.sel_fltData = idata
            st.session_state.sel_DesGrp = selgrp
            st.session_state.sel_Presenca = 0
            if  bCriarLista:
                st.session_state.sel_Presenca = -3
            if  bExcluirLista:
                st.session_state.sel_Presenca = -4
            st.rerun()

if  (st.session_state.sel_Presenca == -3) or (st.session_state.sel_Presenca == -4):
    if  st.session_state.sel_Presenca == -3:
        txt = "Inserir"
    else:
        txt = "Excluir"
    data = st.session_state.sel_fltData.strftime("%d/%m/%Y")
    st.write(f"Grupo : :red[{st.session_state.sel_DesGrp}]")
    st.write(f"Data : :red[{data}]")
    st.write("----")
    st.write(f"Deseja mesmo :red[{txt}] presença para o grupo e a data informada?")
    col1, col2, col3 = st.columns(3)
    bVoltar = col1.button(label="Voltar", type="primary")
    bContinua = col2.button(label=txt, type="primary")
    if  bContinua:
        if  st.session_state.sel_Presenca == -3:
            controlPresenca.GerarListaPresenca(st.session_state.sel_fltData, st.session_state.sel_fltGrp)
        else:
            controlPresenca.ExcluirListaPresenca(st.session_state.sel_fltData, st.session_state.sel_fltGrp)
        st.session_state.sel_Presenca = 0
        st.rerun()
    if  bVoltar:
        st.session_state.sel_Presenca = -2
        st.rerun()    
        
def btnNovoClick():
    st.session_state.sel_Presenca = -1
    
def btnNovoFiltroClick():
    st.session_state.sel_Presenca = -2
    
if  st.session_state.sel_Presenca == 0:
    st.button(label="Novo Filtro", type="primary", on_click=btnNovoFiltroClick)
            
    df = controlPresenca.ListaPresenca(None, st.session_state.sel_fltData, st.session_state.sel_fltGrp)
    
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True),
                       "Data": st.column_config.DateColumn(format="DD/MM/YYYY")
                       },
        disabled=df.columns,
    )
    #selected_indices = list(np.where(edited_df.Select)[0])
    selected_rows = df[edited_df.Select]
    
    for fld in selected_rows.itertuples():
        st.session_state.sel_Presenca = fld.id
        st.rerun()
    
    st.button(label="Nova Preseça", type="primary", on_click=btnNovoClick)
    
if  st.session_state.sel_Presenca > 0:
    bVoltar = st.button(label="Voltar", type="primary")
    if  bVoltar:
        st.session_state.sel_Presenca = 0
        st.rerun()

    with st.form(key="cad_Presenca", border=True):
        dfalu = controlAluno.ListaAlunoF7()
        dfgrp = controlGrupo.ListaGrupo(None)
        retusr = controlPresenca.ListaPresenca(st.session_state.sel_Presenca, None, None)
        
        idselalu = int(dfalu.loc[dfalu['Aluno'] == retusr.Aluno].index[0])
        selalu = st.selectbox(label="Aluno", options=dfalu.Aluno.unique(), index=idselalu)
        
        idselgrp = int(dfgrp.loc[dfgrp['Grupo'] == retusr.Grupo].index[0])
        selgrp = st.selectbox(label="Grupo", options=dfgrp.Grupo.unique(), index=idselgrp)
        
        idata = st.date_input(label="Data", value=retusr.Data, format="DD/MM/YYYY")
        ipresente = st.checkbox(label="Presente", value=retusr.Presente)
        ijustificado = st.checkbox(label="Justificado", value=retusr.Justificado)
        col1, col2 = st.columns(2)
        bSalvar = col1.form_submit_button(label="Salvar", type="primary")
        bExcluir = col2.form_submit_button(label="Excluir", type="primary")
        
        if  bSalvar:
            for v in dfalu.loc[dfalu.Aluno == selalu, 'id']:
                idselalu = v
            for v in dfgrp.loc[dfgrp.Grupo == selgrp, 'id']:
                idselgrp = v
            controlPresenca.AtualizaPresenca(Presenca.Presenca(st.session_state.sel_Presenca, 0, ipresente, ijustificado, idata, idselgrp, idselalu, None, None))
            st.session_state.sel_Presenca = 0
            st.rerun()
            
        if  bExcluir:
            controlPresenca.ApagaPresenca(st.session_state.sel_Presenca)
            st.session_state.sel_Presenca = 0
            st.rerun()
        
if  st.session_state.sel_Presenca == -1:
    bVoltar = st.button(label="Voltar", type="primary")
    if  bVoltar:
        st.session_state.sel_Presenca = 0
        st.rerun()
    with st.form(key="cad_Presenca", border=True):
        dfalu = controlAluno.ListaAlunoF7()
        dfgrp = controlGrupo.ListaGrupo(None)

        selalu = st.selectbox(label="Aluno", options=dfalu.Aluno.unique(), index=0)

        selgrp = st.selectbox(label="Grupo", options=dfgrp.Grupo.unique(), index=0)
        
        idata = st.date_input(label="Data", value="today", format="DD/MM/YYYY")
        ipresente = st.checkbox(label="Presente", value=True)
        ijustificado = st.checkbox(label="Justificado", value=False)
        
        col1, col2 = st.columns(2)
        bSalvar = col1.form_submit_button(label="Salvar", type="primary")
        
        if  bSalvar:
            for v in dfalu.loc[dfalu.Aluno == selalu, 'id']:
                idselalu = v
            for v in dfgrp.loc[dfgrp.Grupo == selgrp, 'id']:
                idselgrp = v
            controlPresenca.InserePresenca(Presenca.Presenca(0, 0, ipresente, ijustificado, idata, idselgrp, idselalu, None, None))
            st.session_state.sel_Presenca = 0
            st.rerun()
            
    