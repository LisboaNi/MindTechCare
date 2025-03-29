from django.db import models
from employees.models import Employee
from utils.models import TimestampMixin

class RepositorioGitHub(TimestampMixin):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='repositorios')
    nome_repositorio = models.CharField(max_length=255)
    github_username = models.CharField(max_length=255)
    git_token = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.github_username}/{self.nome_repositorio}"
    
    def save(self, *args, **kwargs):
        super(RepositorioGitHub, self).save(*args, **kwargs)

        if self.employee is None:
            self.employee = Employee.objects.get(user=self.user)
            self.save()
        
        if self.employee:
            self.employee.save()
    
class AtividadeGitHub(TimestampMixin):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    commit_mensagem = models.TextField()
    data_commit = models.DateTimeField()

    def __str__(self):
        return f"{self.employee.name} - {self.commit_mensagem[:50]}..."
