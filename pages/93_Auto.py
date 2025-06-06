import cryptocode
import streamlit as st
import datetime as dt
import controllers.Presenca as controlPresenca
import controllers.Grupo as controlGrupo 
import controllers.Aluno as controlAluno
import pytz

if  'link' not in st.query_params:
    st.switch_page("1_🏠_Home.py")
    
fuso_horario = pytz.timezone('America/Sao_Paulo')
link = cryptocode.decrypt(st.query_params.link, st.secrets.Chave_Link)
if  link:
    link = link.split(";")
    with st.form(key="cad_grupo", border=True):
         retusr = controlGrupo.ListaGrupo(link[0])
         dti = dt.date(int(link[1].split("-")[0]), int(link[1].split("-")[1]), int(link[1].split("-")[2])).strftime("%d/%m/%Y")
         st.write(f"Grupo : :red[{retusr.DS_Grupo}]")
         st.write(f"Data : :red[{dti}]")
         st.write(f"Hora Inicial : :red[{link[2]}]")
         st.write(f"Hora Final : :red[{link[3]}]")
         cd_crc = st.text_input(label="Código do Aluno", value="")
         col1, col2 = st.columns(2)
         bSalvar = col1.form_submit_button(label="Presença", type="primary")
         if  bSalvar:
             Agora = dt.datetime.now(fuso_horario)
             dti = dt.datetime(int(link[1].split("-")[0]), int(link[1].split("-")[1]), int(link[1].split("-")[2]), int(link[2].split(":")[0]), int(link[2].split(":")[1]), 0).replace(tzinfo=fuso_horario)
             dtf = dt.datetime(int(link[1].split("-")[0]), int(link[1].split("-")[1]), int(link[1].split("-")[2]), int(link[3].split(":")[0]), int(link[3].split(":")[1]), 0).replace(tzinfo=fuso_horario)
             #st.write(f"Agora : :red[{Agora}]")
             #st.write(f"Intervalo : :red[{dti}] - :red[{dtf}]")
             if  (Agora >= dti) and (Agora <= dtf):
                 retusr = controlAluno.LocalizaAlunoCD_CRC(cd_crc.strip())
                 if  retusr:
                     st.write(f"Aluno : :red[{retusr.NM_Aluno}]")
                     controlPresenca.GerarListaPresencaAluno(link[1], link[0], retusr.IDAluno)
                     st.write("Presença gerada com sucesso.")
                 else:
                     st.write("Aluno nao cadastrado.")
             else:
                 st.write("Presença não gerada.")