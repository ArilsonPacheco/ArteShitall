
import streamlit as st
import df_grid as grid
import controllers.Aluno as controlAluno
import controllers.categoria as controlCategoria
import models.Aluno as Aluno

st.set_page_config(page_title="ArteShitall - Aluno", page_icon=st.secrets.Logo1, initial_sidebar_state="expanded")

st.subheader(":scientist: Cadastrado de aluno", divider="rainbow")
if  ('Nivel' not in st.session_state) or (st.session_state.Nivel == 0) or (st.session_state.Nivel not in st.secrets.Nivel_y):
    st.switch_page("1_🏠_Home.py")
    
if  'sel_Aluno' not in st.session_state:
     st.session_state['sel_Aluno'] = 0

def btnNovoClick():
    st.session_state.sel_Aluno = -1
    
if  st.session_state.sel_Aluno == 0:
    df = grid.filter_dataframe(controlAluno.ListaAluno(None))
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True),
                       "Data Nasc.": st.column_config.DateColumn(format="DD/MM/YYYY"),
                       "Data Cadastro": st.column_config.DateColumn(format="DD/MM/YYYY")
                       },
        disabled=df.columns,
    )
    selected_rows = df[edited_df.Select]
    
    for fld in selected_rows.itertuples():
        st.session_state.sel_Aluno = fld.id
        st.rerun()
    
    st.button(label="Novo Aluno", type="primary", on_click=btnNovoClick)
        
if  st.session_state.sel_Aluno > 0:
    bVoltar = st.button(label="Voltar", type="primary")
    if  bVoltar:
        st.session_state.sel_Aluno = 0
        st.rerun()

    with st.form(key="cad_Aluno", border=True):
        dfcat = controlCategoria.ListaCategoria(None)
        retusr = controlAluno.ListaAluno(st.session_state.sel_Aluno)
        iAluno = st.text_input(label="Aluno", value=retusr.NM_Aluno)
        idatanc = st.date_input(label="Data Nascimento", value=retusr.DT_Nasc, format="DD/MM/YYYY")
        idatacad = st.date_input(label="Data Cadastro", value=retusr.DT_Cadastro, format="DD/MM/YYYY")
        iativo = st.checkbox(label="Ativo", value=retusr.Ativo)
        idsel = int(dfcat.loc[dfcat['categoria'] == retusr.Categoria].index[0])
        selcat = st.selectbox(label="Categoria", options=dfcat.categoria.unique(), index=idsel)
        
        col1, col2 = st.columns(2)
        bSalvar = col1.form_submit_button(label="Salvar", type="primary")
        bExcluir = col2.form_submit_button(label="Excluir", type="primary")
        
        if  bSalvar:
            for v in dfcat.loc[dfcat.categoria == selcat, 'id']:
                idsel = v
            controlAluno.AtualizaAluno(Aluno.Aluno(st.session_state.sel_Aluno, 0, iAluno, idatanc, idatacad, iativo, idsel, None))
            st.session_state.sel_Aluno = 0
            st.rerun()
            
        if  bExcluir:
            controlAluno.ApagaAluno(st.session_state.sel_Aluno)
            st.session_state.sel_Aluno = 0
            st.rerun()
        
if  st.session_state.sel_Aluno == -1:
    bVoltar = st.button(label="Voltar", type="primary")
    if  bVoltar:
        st.session_state.sel_Aluno = 0
        st.rerun()
    with st.form(key="cad_Aluno", border=True):
        iAluno = st.text_input(label="Aluno", value="")
        idatanc = st.date_input(label="Data Nascimento", format="DD/MM/YYYY")
        idatacad = st.date_input(label="Data Cadastro", value="today", format="DD/MM/YYYY")
        iativo = st.checkbox(label="Ativo", value=True)
        dfcat = controlCategoria.ListaCategoria(None)
        selcat = st.selectbox(label="Categoria", options=dfcat.categoria.unique(), index=0)
        
        col1, col2 = st.columns(2)
        bSalvar = col1.form_submit_button(label="Salvar", type="primary")
        
        if  bSalvar:
            for v in dfcat.loc[dfcat.categoria == selcat, 'id']:
                idsel = v
            controlAluno.InsereAluno(Aluno.Aluno(0, 0, iAluno, idatanc, idatacad, iativo, idsel, None))
            st.session_state.sel_Aluno = 0
            st.rerun()
    