import streamlit as st
import services.database as db
import models.Aluno as Aluno
import pandas as pd

whr = ' where "IDAluno" = %s'
whr1= ' and "IDAluno" = %s'

def RecDF(rd):
    return pd.DataFrame.from_records(rd, columns=["id", "Aluno", "Categoria", "Data Nasc.", "Data Cadastro", "Ativo", "id categoria", "created_at"])

def ListaAluno(id):
    qryAluno = 'select "IDAluno", "NM_Aluno", "DS_Categoria", "DT_Nasc"::Date, "DT_Cadastro"::Date, "Ativo", "fk_Categoria_rCategoria", a."created_at" from "Aluno" a, "Categoria" c where c."IDCategoria" = a."fk_Categoria_rCategoria"'
    if  id:
        retusr = []
        db.curssor.execute(qryAluno + whr1, (id,))
        df = RecDF(db.curssor.fetchall())
        for row in df.itertuples():
            retusr.append(Aluno.Aluno(row.id, row.created_at, row.Aluno, row[4], row[5], row.Ativo, row[7], row.Categoria))
        return retusr[0]
    else:
        db.curssor.execute(qryAluno)
        return RecDF(db.curssor.fetchall())

def ListaAlunoF7():
    qryAluno = 'select "IDAluno", "NM_Aluno" from "Aluno"'
    db.curssor.execute(qryAluno)
    return pd.DataFrame.from_records(db.curssor.fetchall(), columns=["id", "Aluno"])
    
def InsereAluno(Aluno):
    insAluno = 'insert into "Aluno" ("NM_Aluno", "DT_Nasc", "DT_Cadastro", "Ativo", "fk_Categoria_rCategoria") values (%s, %s, %s, %s, %s)'
    params = (Aluno.NM_Aluno, Aluno.DT_Nasc, Aluno.DT_Cadastro, Aluno.Ativo, Aluno.fk_Categoria_rCategoria, )
    db.curssor.execute(insAluno, params)

def AtualizaAluno(Aluno):
    altAluno = 'update "Aluno" set "NM_Aluno" = %s, "DT_Nasc" = %s, "DT_Cadastro" = %s, "Ativo" = %s, "fk_Categoria_rCategoria" = %s ' + whr
    params = (Aluno.NM_Aluno, Aluno.DT_Nasc, Aluno.DT_Cadastro, Aluno.Ativo, Aluno.fk_Categoria_rCategoria, Aluno.IDAluno,)
    db.curssor.execute(altAluno, params)

def ApagaAluno(id):
    delAluno = 'delete from "Aluno" ' + whr
    db.curssor.execute(delAluno, (id,))
