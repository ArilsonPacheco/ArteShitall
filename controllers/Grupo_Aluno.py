import streamlit as st
import services.database as db
import models.Grupo_Aluno as Grupo_Aluno
import pandas as pd

whr = ' and "IDGrupo_Aluno" = %s'
whr1= ' where "IDGrupo_Aluno" = %s'
def RecDF(rd):
    return pd.DataFrame.from_records(rd, columns=["Grupo", "Aluno", "id", "id Grgupo", "id Aluno", "created_at"])

def ListaGrupo_Aluno(id):
    qryGrupo_Aluno = 'select "DS_Grupo", "NM_Aluno", "IDGrupo_Aluno", "fk_Grupo_rGrupo", "fk_Aluno_rAluno", ga.created_at from "Grupo_Aluno" ga, "Aluno", "Grupo" where "IDAluno" = "fk_Aluno_rAluno" and "IDGrupo" = "fk_Grupo_rGrupo"'
    if  id:
        retusr = []
        db.curssor.execute(qryGrupo_Aluno + whr, (id,))
        df = RecDF(db.curssor.fetchall())
        for row in df.itertuples():
            retusr.append(Grupo_Aluno.Grupo_Aluno(row.id, row.created_at, row[4], row[5], row.Aluno, row.Grupo))
        return retusr[0]
    else:
        db.curssor.execute(qryGrupo_Aluno)
        return RecDF(db.curssor.fetchall())

def InsereGrupo_Aluno(Grupo_Aluno):
    insGrupo_Aluno = 'select "InsereGrupoAluno"(%s, %s)'
    params = (Grupo_Aluno.fk_Grupo_rGrupo, Grupo_Aluno.fk_Aluno_rAluno, )
    db.curssor.execute(insGrupo_Aluno, params)

def AtualizaGrupo_Aluno(Grupo_Aluno):
    altGrupo_Aluno = 'update "Grupo_Aluno" set "fk_Grupo_rGrupo" = %s, "fk_Aluno_rAluno" = %s ' + whr1
    params = (Grupo_Aluno.fk_Grupo_rGrupo, Grupo_Aluno.fk_Aluno_rAluno, Grupo_Aluno.IDGrupo_Aluno,)
    db.curssor.execute(altGrupo_Aluno, params)

def ApagaGrupo_Aluno(id):
    delGrupo_Aluno = 'delete from "Grupo_Aluno" ' + whr1
    db.curssor.execute(delGrupo_Aluno, (id,))
