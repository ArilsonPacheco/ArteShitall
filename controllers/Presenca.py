import streamlit as st
import services.database as db
import models.Presenca as Presenca
import pandas as pd

whr = ' and "IDPresenca" = %s'
whr1= ' where "IDPresenca" = %s'

def RecDF(rd):
    return pd.DataFrame.from_records(rd, columns=["id", "Presente", "Justificado", "Data", "id Aluno", "Aluno", "id Grupo", "Grupo", "created_at"])

def ListaPresenca(id, data, idgrupo):
    qryPresenca = 'select "IDPresenca", "Presente", "Justificado", "Data"::Date, "fk_Aluno_rpAluno", "NM_Aluno", "fk_Grupo_rpGrupo", "DS_Grupo", p.created_at from "Presenca" p, "Grupo", "Aluno" where "IDGrupo" = "fk_Grupo_rpGrupo" and "IDAluno" = "fk_Aluno_rpAluno"'
    if  id:
        retusr = []
        db.curssor.execute(qryPresenca + whr, (id,))
        df = RecDF(db.curssor.fetchall())
        for row in df.itertuples():
            retusr.append(Presenca.Presenca(row.id, row.created_at, row.Presente, row.Justificado, row.Data, row[7], row[5], row.Grupo, row.Aluno))
        return retusr[0]
    else:
        whr3 = ' and "Data" = %s and "fk_Grupo_rpGrupo" = %s'
        params = (data, idgrupo,)
        db.curssor.execute(qryPresenca + whr3, params)
        return RecDF(db.curssor.fetchall())

def InserePresenca(Presenca):
    insPresenca = 'insert into "Presenca" ("Presente", "Justificado", "Data", "fk_Grupo_rpGrupo", "fk_Aluno_rpAluno") values (%s, %s, %s, %s, %s)'
    params = (Presenca.Presente, Presenca.Justificado, Presenca.Data, Presenca.fk_Grupo_rpGrupo, Presenca.fk_Aluno_rpAluno, )
    db.curssor.execute(insPresenca, params)

def AtualizaPresenca(Presenca):
    altPresenca = 'update "Presenca" set "Presente" = %s, "Justificado" = %s, "Data" = %s, "fk_Grupo_rpGrupo" = %s, "fk_Aluno_rpAluno" = %s ' + whr1
    params = (Presenca.Presente, Presenca.Justificado, Presenca.Data, Presenca.fk_Grupo_rpGrupo, Presenca.fk_Aluno_rpAluno, Presenca.IDPresenca,)
    db.curssor.execute(altPresenca, params)

def ApagaPresenca(id):
    delPresenca = 'delete from "Presenca" ' + whr1
    db.curssor.execute(delPresenca, (id,))

def GerarListaPresenca(data, idgrupo):
    gerPresenca = 'select "GerarPresenca"(%s, %s)'
    params = (data, idgrupo,)
    db.curssor.execute(gerPresenca, params)