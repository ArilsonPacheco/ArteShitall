
import streamlit as st
import services.database as db
import models.Categoria as Ctg
import pandas as pd

whr = ' where "IDCategoria" = %s'

def RecDF(rd):
    return pd.DataFrame.from_records(rd, columns=["id", "created_at", "categoria"])

def ListaCategoria(id):
    qryCategoria = 'select "IDCategoria", created_at, "DS_Categoria" from "Categoria"'
    if  id:
        retusr = []
        db.curssor.execute(qryCategoria + whr, (id,))
        df = RecDF(db.curssor.fetchall())
        for row in df.itertuples():
            retusr.append(Ctg.Categoria(row.id, row.created_at, row.categoria))
        return retusr[0]
    else:
        db.curssor.execute(qryCategoria)
        return RecDF(db.curssor.fetchall())

def InsereCategoria(Categoria):
    insCategoria = 'insert into "Categoria" ("DS_Categoria") values (%s)' 
    db.curssor.execute(insCategoria, (Categoria.DS_Categoria,))

def AtualizaCategoria(Categoria):
    altCategoria = 'update "Categoria" set "DS_Categoria" = %s' + whr
    params = (Categoria.DS_Categoria, Categoria.IDCategoria,)
    db.curssor.execute(altCategoria, params)
    
def ApagaCategoria(id):
    delCategoria = 'delete from "Categoria"' + whr
    db.curssor.execute(delCategoria, (id,))
    