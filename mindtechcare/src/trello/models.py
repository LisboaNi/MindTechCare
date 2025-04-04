from django.db import models
from employees.models import Employee
from utils.models import TimestampMixin

class BoardTrello(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name='boards_trello')
    nome_board = models.CharField(max_length=255)
    trello_board_id = models.CharField(max_length=255, unique=True)
    trello_token = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.nome_board

class CardTrello(TimestampMixin):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name='card_trello')
    board = models.ForeignKey(BoardTrello, on_delete=models.CASCADE, null=True, blank=True, related_name='cards')
    nome_card = models.CharField(max_length=255)
    data_criacao = models.DateTimeField()
    trello_card_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.nome_card} ({self.board.nome_board})"
