import streamlit as st
import controllers.Grupos as controlGrupos
from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm

st.subheader(":bar_chart: Gráfico de Grupos e Alunos", divider="rainbow")

init_streamlit_comm()

df = controlGrupos.ListaGrupos()

render = StreamlitRenderer(df, debug=False)

render.render_explore(scrolling=True)