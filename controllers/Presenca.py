import streamlit as st
import services.database as db
import models.Presenca as Presenca
import pandas as pd

whr = ' and "IDPresenca" = %s'
whr1= ' where "IDPresenca" = %s'

def RecDF(rd):
    return pd.DataFrame.from_records(rd, columns=["Presente", "Justificado", "Data", "Aluno", "Grupo", "id", "id Aluno", "id Grupo", "created_at"])

def ListaPresenca(id, data, idgrupo):
    qryPresenca = 'select "Presente", "Justificado", "Data"::Date, "NM_Aluno", "DS_Grupo", "IDPresenca", "fk_Aluno_rpAluno", "fk_Grupo_rpGrupo", p.created_at from "Presenca" p, "Grupo", "Aluno" where "IDGrupo" = "fk_Grupo_rpGrupo" and "IDAluno" = "fk_Aluno_rpAluno"'
    if  id:
        retusr = []
        db.curssor.execute(qryPresenca + whr, (id,))
        df = RecDF(db.curssor.fetchall())
        for row in df.itertuples():
            retusr.append(Presenca.Presenca(row.id, row.created_at, row.Presente, row.Justificado, row.Data, row[8], row[7], row.Grupo, row.Aluno))
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

def GerarListaPresencaAluno(data, idgrupo, idaluno):
    gerPresenca = 'select "GerarPresencaAluno"(%s, %s, %s)'
    params = (data, idgrupo, idaluno,)
    db.curssor.execute(gerPresenca, params)

def ExcluirListaPresenca(data, idgrupo):
    excPresenca = 'select "ExcluirPresenca"(%s, %s)'
    params = (data, idgrupo,)
    db.curssor.execute(excPresenca, params)
    
def ConsultaPresenca(DataI, DataF, IDGrupo):
    qry = """
          select "DS_Grupo" as grupo, "NM_Aluno" as aluno, tot_encontro as encontros, tot_faltas as faltas, tot_just as justificadas, round((1-(tot_faltas/tot_encontro))*100,2) as porcentagem from (
          select "fk_Grupo_rpGrupo", "fk_Aluno_rpAluno", sum(tot_encontro) as tot_encontro, sum(tot_Faltas) as tot_Faltas, sum(tot_Just) as tot_Just from (
          select "fk_Grupo_rpGrupo", "fk_Aluno_rpAluno", count(*) as tot_encontro, 0 as tot_Faltas, 0 as tot_Just from "Presenca" where "fk_Grupo_rpGrupo" = %s and "Data" between %s and %s group by "fk_Grupo_rpGrupo", "fk_Aluno_rpAluno"
          union all
          select "fk_Grupo_rpGrupo", "fk_Aluno_rpAluno", 0 as tot_encontro, count(*) as tot_Faltas, 0 as tot_Just from "Presenca" where "fk_Grupo_rpGrupo" = %s and "Data" between %s and %s and "Presente" = false group by "fk_Grupo_rpGrupo", "fk_Aluno_rpAluno"
          union all
          select "fk_Grupo_rpGrupo", "fk_Aluno_rpAluno", 0 as tot_encontro, 0 as tot_Faltas, count(*) as tot_Just from "Presenca" where "fk_Grupo_rpGrupo" = %s and "Data" between %s and %s and "Presente" = false and "Justificado" = true group by "fk_Grupo_rpGrupo", "fk_Aluno_rpAluno"
          ) tot1
          group by "fk_Grupo_rpGrupo", "fk_Aluno_rpAluno"
          ) tot2, "Grupo", "Aluno" where "IDGrupo" = "fk_Grupo_rpGrupo" and "IDAluno" = "fk_Aluno_rpAluno" 
      """
    params = (IDGrupo, DataI, DataF, IDGrupo, DataI, DataF, IDGrupo, DataI, DataF,)
    db.curssor.execute(qry, params)
    return pd.DataFrame.from_records(db.curssor.fetchall(), columns=["Grupo", "Aluno", "Encontros", "Faltas", "Justificadas", "% Presença"])
