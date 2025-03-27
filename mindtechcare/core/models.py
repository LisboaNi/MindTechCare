from django.db import models

class Empresa(models.Model):
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True, db_index=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Profissional(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True)
    cargo = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cargo}"

class AtividadeGitHub(models.Model):
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    commit_mensagem = models.TextField()
    data_commit = models.DateTimeField()

    def __str__(self):
        return f"{self.profissional.usuario.username} - {self.commit_mensagem[:50]}..."

class TarefaJira(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_progresso', 'Em Progresso'),
        ('concluido', 'Concluído'),
    ]

    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        return f"{self.titulo} - {self.status}"

