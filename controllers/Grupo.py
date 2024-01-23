import streamlit as st
import services.database as db
import models.Grupo as Grupo
import pandas as pd

whr = ' where "IDGrupo" = %s'

def RecDF(rd):
    return pd.DataFrame.from_records(rd, columns=["id", "created_at", "Grupo"])

def ListaGrupo(id):
    qryGrupo = 'select "IDGrupo", "created_at", "DS_Grupo" from "Grupo"'
    if  id:
        retusr = []
        db.curssor.execute(qryGrupo + whr, (id,))
        df = RecDF(db.curssor.fetchall())
        for row in df.itertuples():
            retusr.append(Grupo.Grupo(row.id, row.created_at, row.Grupo))
        return retusr[0]
    else:
        db.curssor.execute(qryGrupo)
        return RecDF(db.curssor.fetchall())

def InsereGrupo(Grupo):
    insGrupo = 'insert into "Grupo" ("DS_Grupo") values (%s)'
    params = (Grupo.DS_Grupo, )
    db.curssor.execute(insGrupo, params)

def AtualizaGrupo(Grupo):
    altGrupo = 'update "Grupo" set "DS_Grupo" = %s ' + whr
    params = (Grupo.DS_Grupo, Grupo.IDGrupo,)
    db.curssor.execute(altGrupo, params)

def ApagaGrupo(id):
    delGrupo = 'delete from "Grupo" ' + whr
    db.curssor.execute(delGrupo, (id,))
