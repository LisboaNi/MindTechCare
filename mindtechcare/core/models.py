from django.db import models
from django.contrib.auth.models import User

class Empresa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True, db_index=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    senha = models.CharField(max_length=255, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome}"
    
    def save(self, *args, **kwargs):
        if not self.id:
            user = User.objects.create_user(username=self.email, email=self.email, password=self.senha)
            self.user = user
        super(Empresa, self).save(*args, **kwargs)

class Profissional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True)
    nome = models.CharField(max_length=255)
    cargo = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)
    senha = models.CharField(max_length=255, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome}"

    def save(self, *args, **kwargs):
        # Se o profissional não tiver um usuário ainda
        if not self.id:
            user = User.objects.create_user(username=self.email, email=self.email, password=self.senha)
            self.user = user
        super(Profissional, self).save(*args, **kwargs)

class RepositorioGitHub(models.Model):
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, related_name='repositorios')
    nome_repositorio = models.CharField(max_length=255)
    github_username = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.github_username}/{self.nome_repositorio}"
    
class AtividadeGitHub(models.Model):
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    commit_mensagem = models.TextField()
    data_commit = models.DateTimeField()

    def __str__(self):
        return f"{self.profissional.nome} - {self.commit_mensagem[:50]}..."

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

