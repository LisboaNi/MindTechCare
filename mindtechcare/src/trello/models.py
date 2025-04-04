from django.db import models
from employees.models import Employee
from utils.models import TimestampMixin

class BoardTrello(models.Model):
    nome_board = models.CharField(max_length=255)
    trello_board_id = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.nome_board

class CardTrello(TimestampMixin):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='cards_trello')
    board = models.ForeignKey(BoardTrello, on_delete=models.CASCADE, related_name='cards')
    nome_card = models.CharField(max_length=255)
    data_criacao = models.DateTimeField()
    trello_card_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.nome_card} ({self.board.nome_board})"
    
    def save(self, *args, **kwargs):
        super(CardTrello, self).save(*args, **kwargs)
        
        if self.employee is None:
            self.employee = Employee.objects.get(user=self.user)
            self.save()

        if self.employee:
            self.employee.save()

class AtividadeTrello(TimestampMixin):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    nome_card = models.CharField(max_length=255)
    data_atividade = models.DateTimeField()

    def __str__(self):
        return f"{self.employee.name} - {self.nome_card}"
