
import streamlit as st
import services.database as db
import models.Usuario as Usr
import controllers.login as login
import pandas as pd

whr = ' where "Usuario"."IDUsuario" = %s'

def RecDF(rd):
    return pd.DataFrame.from_records(rd, columns=["id", "usuario", "passw", "Nivel", "created_at"])

def ListaUsuario(id):
    qryUsuario = 'select "IDUsuario", "NM_Usuario", "DS_Pass", "Nivel", created_at from "Usuario"'
    if  id:
        retusr = []
        db.curssor.execute(qryUsuario + whr, (id,))
        df = RecDF(db.curssor.fetchall())
        for row in df.itertuples():
            retusr.append(Usr.Usuario(row.id, row.created_at, row.usuario, row.passw, row.Nivel))
        return retusr[0]
    else:
        db.curssor.execute(qryUsuario)
        return RecDF(db.curssor.fetchall())

def InsereUsuario(Usuario):
    if  not login.Logar(Usuario):
        insUsuario = 'insert into "Usuario" ("NM_Usuario", "DS_Pass", "Nivel") values (%s, %s, %s)' 
        params = (Usuario.NM_Usuario, Usuario.DS_Pass, Usuario.Nivel,)
        db.curssor.execute(insUsuario, params)

def AtualizaUsuario(Usuario):
    altUsuario = 'update "Usuario" set "NM_Usuario" = %s, "DS_Pass" = %s, "Nivel" = %s ' + whr
    params = (Usuario.NM_Usuario, Usuario.DS_Pass, Usuario.Nivel, Usuario.IDUsuario,)
    db.curssor.execute(altUsuario, params)
    
def ApagaUsuario(id):
    delUsuario = 'delete from "Usuario" ' + whr
    db.curssor.execute(delUsuario, (id,))
    