from django.db import models
from employees.models import Employee

class RepositorioGitHub(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='repositorios')
    nome_repositorio = models.CharField(max_length=255)
    github_username = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.github_username}/{self.nome_repositorio}"
    
class AtividadeGitHub(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    commit_mensagem = models.TextField()
    data_commit = models.DateTimeField()

    def __str__(self):
        return f"{self.employee.name} - {self.commit_mensagem[:50]}..."
