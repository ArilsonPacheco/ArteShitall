
import streamlit as st
from st_aggrid import AgGrid
import st_aggrid as agg
import df_grid as grid
import controllers.Aluno as controlAluno
import controllers.categoria as controlCategoria
import models.Aluno as Aluno
import datetime as dt

st.subheader("Cadastrado de aluno", divider="rainbow")
if  ('Nivel' not in st.session_state) or (st.session_state.Nivel == 0) or (st.session_state.Nivel > 1):
    st.switch_page("Home.py")
    
if  'sel_Aluno' not in st.session_state:
     st.session_state['sel_Aluno'] = 0

def btnNovoClick():
    st.session_state.sel_Aluno = -1
    
if  st.session_state.sel_Aluno == 0:
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

    df = grid.filter_dataframe(controlAluno.ListaAluno(None))
    builder = agg.GridOptionsBuilder.from_dataframe(df)
    builder.configure_pagination(enabled=True)
    builder.configure_selection(selection_mode='single', use_checkbox=False)
    builder.configure_column('id', editable=False)
    builder.configure_column("Data Nasc.", type=["customDateTimeFormat"], custom_format_string='dd/MM/yyyy')
    builder.configure_column("Data Cadastro", type=["customDateTimeFormat"], custom_format_string='dd/MM/yyyy')
    builder.configure_column("Ativo", cellRenderer=checkbox_renderer)
    grid_options = builder.build()

    return_value = AgGrid(df, gridOptions=grid_options, columns_auto_size_mode=agg.ColumnsAutoSizeMode.FIT_CONTENTS, allow_unsafe_jscode=True)
    
    st.button(label="Novo Aluno", type="primary", on_click=btnNovoClick)
    
    if return_value['selected_rows']:
        st.session_state.sel_Aluno = return_value['selected_rows'][0]['id']
        st.rerun()
        
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
    