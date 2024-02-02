
import streamlit as st
import controllers.Grupos as controlGrupos
import df_grid as grid
import altair as alt

st.set_page_config(page_title="ArteShitall - Grupos", page_icon=st.secrets.Logo1, initial_sidebar_state="expanded")

if 'Grupos' not in st.session_state:
    st.session_state['Grupos'] = 0
    st.session_state['dfGrupos'] = 0
    
st.subheader(":bar_chart: Gráfico de Grupos e Alunos", divider="rainbow")
if  ('Nivel' not in st.session_state) or (st.session_state.Nivel == 0) or (st.session_state.Nivel not in st.secrets.Nivel_y):
    st.switch_page("1_🏠_Home.py")

if  st.button(label="Carrega dados", type="primary"):
    st.session_state.Grupos = 0

if  st.session_state.Grupos == 0:
    df = grid.filter_dataframe(controlGrupos.ListaGrupos())
    st.session_state.Grupos = 1
    st.session_state.dfGrupos = df
else:
    df = grid.filter_dataframe(st.session_state.dfGrupos)
    
st.dataframe(df)

base = alt.Chart(df).encode(
        theta=alt.Theta("Alunos:Q", stack=True), color=alt.Color("Grupo:N", legend=None)
    )

pie = base.mark_arc(outerRadius=120)
text = base.mark_text(radius=140, size=12).encode(text="Grupo:N")

chart = pie + text
    
st.altair_chart(chart, theme="streamlit")