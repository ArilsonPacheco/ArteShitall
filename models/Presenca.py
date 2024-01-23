
class Presenca:
    def __init__(self, IDPresenca, created_at, Presente, Justificado, Data, fk_Grupo_rpGrupo, fk_Aluno_rpAluno, Grupo, Aluno):
        self.IDPresenca = IDPresenca
        self.created_at = created_at
        self.Presente = Presente
        self.Justificado = Justificado
        self.Data = Data
        self.fk_Grupo_rpGrupo = fk_Grupo_rpGrupo
        self.fk_Aluno_rpAluno = fk_Aluno_rpAluno
        self.Grupo = Grupo
        self.Aluno = Aluno
