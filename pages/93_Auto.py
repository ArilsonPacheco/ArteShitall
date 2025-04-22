import cryptocode
import streamlit as st
import datetime as dt
import controllers.Presenca as controlPresenca
import controllers.Grupo as controlGrupo 
import controllers.Aluno as controlAluno

link = cryptocode.decrypt(st.query_params.link, st.secrets.Chave_Link)
if  link:
    link = link.split(";")
    with st.form(key="cad_grupo", border=True):
         retusr = controlGrupo.ListaGrupo(link[0])
         st.write(f"Grupo : :red[{retusr.DS_Grupo}]")
         st.write(f"Data : :red[{link[1]}]")
         st.write(f"Hora Inicial : :red[{link[2]}]")
         st.write(f"Hora Final : :red[{link[3]}]")
         cd_crc = st.text_input(label="Código do Aluno", value="")
         col1, col2 = st.columns(2)
         bSalvar = col1.form_submit_button(label="Presença", type="primary")
         if  bSalvar:
             dti = dt.datetime(int(link[1].split("-")[0]), int(link[1].split("-")[1]), int(link[1].split("-")[2]), int(link[2].split(":")[0]), int(link[2].split(":")[1]), 0)
             dtf = dt.datetime(int(link[1].split("-")[0]), int(link[1].split("-")[1]), int(link[1].split("-")[2]), int(link[3].split(":")[0]), int(link[3].split(":")[1]), 0)
             if  (dt.datetime.now() >= dti) and (dt.datetime.now() <= dtf):
                 retusr = controlAluno.LocalizaAlunoCD_CRC(cd_crc.strip())
                 if  retusr:
                     st.write(f"Aluno : :red[{retusr.NM_Aluno}]")
                     controlPresenca.GerarListaPresencaAluno(link[1], link[0], retusr.IDAluno)
                     st.write("Presença gerada com sucesso.")
                 else:
                     st.write("Aluno nao cadastrado.")
             else:
                 st.write("Presença não gerada.")