import streamlit as st
import services.database as db
import pandas as pd

def RecDF(rd):
    return pd.DataFrame.from_records(rd, columns=["Grupo", "Alunos"])

def ListaGrupos():
    qryGrupo = 'select "DS_Grupo", count("NM_Aluno") as qtdAluno from "Grupo_Aluno", "Grupo", "Aluno" where "Grupo"."IDGrupo" = "fk_Grupo_rGrupo" and "IDAluno" = "fk_Aluno_rAluno" and "Ativo" = true group by "DS_Grupo"'
    db.curssor.execute(qryGrupo)
    return RecDF(db.curssor.fetchall())