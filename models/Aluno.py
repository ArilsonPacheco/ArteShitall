
class Aluno:
    def __init__(self, IDAluno, created_at, NM_Aluno, DT_Nasc, DT_Cadastro, Ativo, fk_Categoria_rCategoria, Categoria):
        self.IDAluno = IDAluno
        self.created_at = created_at
        self.NM_Aluno = NM_Aluno
        self.DT_Nasc = DT_Nasc
        self.DT_Cadastro = DT_Cadastro
        self.Ativo = Ativo
        self.fk_Categoria_rCategoria = fk_Categoria_rCategoria
        self.Categoria = Categoria
