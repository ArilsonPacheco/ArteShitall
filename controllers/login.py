import streamlit as st
import services.database as db
import models.Usuario as Usuario

def Logar(Usuario):
    db.curssor.execute('select "Usuario"."Nivel" from "Usuario" where "Usuario"."NM_Usuario" = %s and "Usuario"."DS_Pass" = %s',
                        (Usuario.NM_Usuario, Usuario.DS_Pass,))
    df = db.curssor.fetchall()
    
    for ret in df:
        return ret[0]
