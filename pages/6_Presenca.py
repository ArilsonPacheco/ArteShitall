
import streamlit as st
from st_aggrid import AgGrid
import st_aggrid as agg
import df_grid as grid
import controllers.Presenca as controlPresenca
import controllers.Grupo as controlGrupo
import controllers.Aluno as controlAluno
import models.Presenca as Presenca

st.subheader("Lista de presença", divider="rainbow")
if  ('Nivel' not in st.session_state) or (st.session_state.Nivel == 0) or (st.session_state.Nivel > 1):
    st.switch_page("Home.py")
    
if  'sel_Presenca' not in st.session_state:
     st.session_state['sel_Presenca'] = -2

if  'sel_fltData' not in st.session_state:
     st.session_state['sel_fltData'] = 0

if  'sel_fltGrp' not in st.session_state:
     st.session_state['sel_fltGrp'] = 0

if  st.session_state.sel_Presenca == -2:
    with st.form(key="pre_filtro", border=True):
        st.write("* Filtra data e grupo da presença")
        st.write("* Cria lista de presença")
        st.write("---")
        dfgrp = controlGrupo.ListaGrupo(None)
        selgrp = st.selectbox(label="Grupo", options=dfgrp.Grupo.unique(), index=0)
        idata = st.date_input(label="Data", value="today", format="DD/MM/YYYY")
        col1, col2 = st.columns(2)
        bFiltrar = col1.form_submit_button(label="Fitrar", type="primary")
        bCriarLista = col2.form_submit_button(label="Cria Listar", type="primary")
        
        if  bFiltrar or bCriarLista:
            for v in dfgrp.loc[dfgrp.Grupo == selgrp, 'id']:
                idselgrp = v
            st.session_state.sel_fltGrp = idselgrp
            st.session_state.sel_fltData = idata
            st.session_state.sel_Presenca = 0
            if  bCriarLista:
                controlPresenca.GerarListaPresenca(idata, idselgrp)
            st.rerun()

def btnNovoClick():
    st.session_state.sel_Presenca = -1
    
def btnNovoFiltroClick():
    st.session_state.sel_Presenca = -2
    
if  st.session_state.sel_Presenca == 0:
    st.button(label="Novo Filtro", type="primary", on_click=btnNovoFiltroClick)
            
    checkbox_renderer = agg.JsCode(
            """
            class CheckboxRenderer{
            init(params) {
                this.params = params;
                this.eGui = document.createElement('input');
                this.eGui.type = 'checkbox';
                this.eGui.checked = params.value;
                this.checkedHandler = this.checkedHandler.bind(this);
                this.eGui.addEventListener('click', this.checkedHandler);
            }
            checkedHandler(e) {
                let checked = e.target.checked;
                let colId = this.params.column.colId;
                this.params.node.setDataValue(colId, checked);
            }
            getGui(params) {
                return this.eGui;
            }
            destroy(params) {
            this.eGui.removeEventListener('click', this.checkedHandler);
            }
            }//end class
        """
        )
    rowStyle_renderer = agg.JsCode(
        """
        function(params) {
            if (params.data.Selected) {
                return {
                    'color': 'black',
                    'backgroundColor': 'pink'
                }
            }
            else {
                return {
                    'color': 'black',
                    'backgroundColor': 'white'
                }
            }
        }; 
        """   
    ) 

    df = controlPresenca.ListaPresenca(None, st.session_state.sel_fltData, st.session_state.sel_fltGrp)
    builder = agg.GridOptionsBuilder.from_dataframe(df)
    builder.configure_pagination(enabled=True)
    builder.configure_selection(selection_mode='single', use_checkbox=False)
    builder.configure_column('id', editable=False)
    builder.configure_column("Data", type=["customDateTimeFormat"], custom_format_string='dd/MM/yyyy')
    builder.configure_column("Presente", cellRenderer=checkbox_renderer)
    builder.configure_column("Justificado", cellRenderer=checkbox_renderer)
    
    grid_options = builder.build()

    return_value = AgGrid(df, gridOptions=grid_options, columns_auto_size_mode=agg.ColumnsAutoSizeMode.FIT_CONTENTS, allow_unsafe_jscode=True)
    
    st.button(label="Nova Preseça", type="primary", on_click=btnNovoClick)
    
    if return_value['selected_rows']:
        st.session_state.sel_Presenca = return_value['selected_rows'][0]['id']
        st.rerun()
        
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
            
    