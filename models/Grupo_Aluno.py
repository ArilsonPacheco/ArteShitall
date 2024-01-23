
class Grupo_Aluno:
    def __init__(self, IDGrupo_Aluno, created_at, fk_Grupo_rGrupo, fk_Aluno_rAluno, Aluno, Grupo):
        self.IDGrupo_Aluno = IDGrupo_Aluno
        self.created_at = created_at
        self.fk_Grupo_rGrupo = fk_Grupo_rGrupo
        self.fk_Aluno_rAluno = fk_Aluno_rAluno
        self.Aluno = Aluno
        self.Grupo = Grupo
